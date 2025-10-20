# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file, Response
from io import BytesIO, StringIO
import csv
import os
import time
import  openai
import random

from database import init_db, db, User, ChatHistory
from chatbot_model import process_message

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_secret_key")
init_db(app)

# openai.OPENROUTER_API_KEY = os.getenv("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")

# ---------------- USER ROUTES ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    """Login page"""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Please enter username and password", "warning")
            return redirect(url_for("index"))

        # Admin shortcut
        if username == "admin":
            return redirect(url_for("admin_login"))

        user = User.get_by_username(username)
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("chat_page"))
        flash("Invalid username or password", "danger")
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration"""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not password:
            flash("Please enter username and password", "warning")
            return redirect(url_for("register"))
        if User.get_by_username(username):
            flash("Username already exists", "danger")
            return redirect(url_for("register"))
        User.create(username, password)
        flash("Registered successfully — please login", "success")
        return redirect(url_for("index"))
    return render_template("register.html")


# @app.route("/chat", methods=["GET", "POST"])
# def chat():
#     if "user_id" not in session:
#         return redirect(url_for("index"))

#     if request.method == "POST":
#         user_input = request.form.get("message", "").strip()
#         if not user_input:
#             return jsonify({"response": "Please enter a message."})

#         user_id = session.get("user_id")
        
#         def generate_and_store():
#             response_collector = []
#             for token in process_message(user_input):
#                 response_collector.append(token)
#                 yield token
#                 time.sleep(random.uniform(0.02, 0.04))
#             # after streaming completes
#             full_response = "".join(response_collector).strip()
#             if user_id:  # avoid using session directly here
#                 with app.app_context():
#                     ChatHistory.create(user_id, user_input, full_response)
#             yield "\n"
#         return Response(generate_and_store(), content_type="text/plain; charset=UTF-8")
    
    
# 🟩 For showing the chat page (GET)
@app.route("/chat", methods=["GET"])
def chat_page():
    if "user_id" not in session:
        return redirect(url_for("index"))
    chats = ChatHistory.query.filter_by(
        user_id=session["user_id"]
    ).order_by(ChatHistory.timestamp.asc()).all()
    return render_template(
        "chat.html",
        username=session.get("username"),
        chats=chats
    )


# 🟦 For handling streamed chat replies (POST)
@app.route("/chat", methods=["POST"])
def chat_stream():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 403

    user_input = request.form.get("message", "").strip()
    if not user_input:
        return jsonify({"response": "Please enter a message."})

    user_id = session.get("user_id")

    def generate():
        response_collector = []
        for token in process_message(user_input):
            yield token
            response_collector.append(token)
            time.sleep(0.02)

        # Save full response after streaming ends
        full_response = "".join(response_collector).replace("[OFFLINE]", "").strip()
        with app.app_context():
            ChatHistory.create(user_id, user_input, full_response)
        yield "\n"

    return Response(generate(), content_type="text/plain; charset=utf-8")


# 🟥 Optional: Catch accidental GETs to /chat POST route
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method Not Allowed. Use POST for chat."}), 405

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for("index"))


# ---------------- ADMIN ROUTES ----------------
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    """Simple admin login (username=admin / password=admin123 by default)"""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        flash("Invalid admin credentials", "danger")
    return render_template("admin_login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    q = request.args.get("q", "").strip()
    if q:
        # join with users so we can search username + message + response
        chats = (ChatHistory.query
                 .join(User, ChatHistory.user_id == User.id)
                 .filter(
                     (User.username.ilike(f"%{q}%")) |
                     (ChatHistory.message.ilike(f"%{q}%")) |
                     (ChatHistory.response.ilike(f"%{q}%"))
                 )
                 .order_by(ChatHistory.timestamp.desc())
                 .all())
    else:
        chats = ChatHistory.query.order_by(ChatHistory.timestamp.desc()).all()

    return render_template("admin_dashboard.html", chats=chats, query=q)


@app.route("/admin/download")
def admin_download():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    chats = ChatHistory.query.join(User, ChatHistory.user_id == User.id).order_by(ChatHistory.timestamp.desc()).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "User ID", "Username", "Message", "Response", "Timestamp"])
    for c in chats:
        writer.writerow([c.id, c.user_id, c.user.username if c.user else "Unknown", c.message, c.response, c.timestamp])

    mem = BytesIO()
    mem.write(output.getvalue().encode("utf-8"))
    mem.seek(0)
    output.close()
    return send_file(mem, mimetype="text/csv", as_attachment=True, download_name="chat_history.csv")


@app.route("/admin/clear_history", methods=["POST"])
def clear_history():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    ChatHistory.query.delete()
    db.session.commit()
    flash("Chat history cleared", "success")
    return redirect(url_for("admin_dashboard"))


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)

/* script.js — Hybrid GPT-Agro Fusion
   Full rebuild: streaming, shimmer, leaves, typing sound, waveform,
   copy/edit/regenerate, swipe-to-reply, animated gradient bubbles.
   Keeps backend endpoints unchanged: /api/chat, /api/analyze-image
*/

/* ---------------- THEME HANDLING (unchanged behaviour) ---------------- */
(function () {
  const THEME_KEY = 'agrobot_theme';
  function applyTheme(theme) {
    if (theme === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
    else document.documentElement.removeAttribute('data-theme');
  }
  function saveTheme(theme) { try { localStorage.setItem(THEME_KEY, theme); } catch (e) {} }
  function initTheme() {
    let stored = null;
    try { stored = localStorage.getItem(THEME_KEY); } catch (e) { stored = null; }
    if (!stored) {
      const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
      stored = prefersDark ? 'dark' : 'light';
    }
    applyTheme(stored);
  }
  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next); saveTheme(next);
  }
  window.toggleAgrobotTheme = toggleTheme;
  document.addEventListener('DOMContentLoaded', initTheme);
})();

/* ----------------- MAIN UI & CHAT LOGIC ----------------- */
document.addEventListener('DOMContentLoaded', () => {
  console.log('AI-AgroBot UI booting — Hybrid GPT-Agro Fusion');

  // ---------------- resources
  const typingSound = new Audio('/static/typing.mp3'); // keep file in /static/
  typingSound.volume = 0.24;
  function playTypingSound() { typingSound.currentTime = 0; typingSound.play().catch(()=>{}); }

  // ---------------- elements (existing IDs used)
  const messages = document.getElementById('messages');
  const input = document.getElementById('msg');
  const sendBtn = document.getElementById('sendBtn');
  const voiceBtn = document.getElementById('voiceBtn');
  const imageInput = document.getElementById('imageInput');

  // small state stores
  const userMessageHistory = []; // stores last user messages (for regenerate)
  let pendingStreamAbort = null;  // for controlling streaming if regen/stop
  let thinkingActive = false;

  // ---------------- Voice recognition + waveform toggles ----------------
  let recognition = null;
  let isListening = false;
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.interimResults = false;
    recognition.continuous = false;
    recognition.lang = 'en-IN';

    recognition.onresult = (e) => {
      const t = e.results[0][0].transcript || '';
      input.value = t;
      updateVoiceUI(false);
      setMicActive(false);
      input.focus();
    };

    recognition.onerror = (e) => {
      console.warn('speech error', e);
      updateVoiceUI(false);
      setMicActive(false);
      addSystemMessage('Voice input error: ' + (e.error || 'unknown'));
    };

    recognition.onend = () => {
      updateVoiceUI(false);
      setMicActive(false);
    };
  } else {
    if (voiceBtn) voiceBtn.style.display = 'none';
  }

  function updateVoiceUI(listening) {
    isListening = !!listening;
    if (!voiceBtn) return;
    voiceBtn.classList.toggle('listening', listening);
    voiceBtn.setAttribute('aria-pressed', listening ? 'true' : 'false');
    voiceBtn.title = listening ? 'Listening — click to stop' : 'Voice input';
    voiceBtn.innerText = listening ? '🎙️ Listening...' : '🎤';
  }

  function toggleVoiceInput() {
    if (!recognition) { addSystemMessage('Voice not supported in this browser'); return; }
    if (isListening) {
      recognition.stop(); updateVoiceUI(false); setMicActive(false);
    } else {
      try { recognition.start(); updateVoiceUI(true); setMicActive(true); }
      catch (e) { console.error(e); addSystemMessage('Could not start voice'); }
    }
  }

  // ---------------- helpers: scroll, format, create controls ----------------
  function scrollToBottom(smooth = true) {
    if (!messages) return;
    messages.scrollTo({ top: messages.scrollHeight, behavior: smooth ? 'smooth' : 'auto' });
  }

  function escapeHtml(s) {
    return String(s || '')
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  // create actions toolbar for each message (copy, edit, regen)
  function createMsgActions(isUser, payload) {
    const actions = document.createElement('div');
    actions.className = 'msg-actions';
    // copy
    const copy = document.createElement('button');
    copy.className = 'action-btn copy';
    copy.title = 'Copy';
    copy.innerText = 'Copy';
    copy.onclick = () => {
      navigator.clipboard?.writeText(payload.text || '').then(()=> {
        flashTiny('Copied');
      }).catch(()=> { flashTiny('Copy failed'); });
    };
    actions.appendChild(copy);

    // edit (only for user)
    if (isUser) {
      const edit = document.createElement('button');
      edit.className = 'action-btn edit';
      edit.title = 'Edit message';
      edit.innerText = 'Edit';
      edit.onclick = () => {
        input.value = payload.text || '';
        input.focus();
        // mark last edited so next send replaces earlier message? We keep simple: new send creates new message
        flashTiny('Edit in input — press Send');
      };
      actions.appendChild(edit);
    } else {
      // regenerate (for bot) — re-query the backend using the matching original user prompt if available
      const regen = document.createElement('button');
      regen.className = 'action-btn regen';
      regen.title = 'Regenerate';
      regen.innerText = 'Regenerate';
      regen.onclick = async () => {
        if (!payload.orig_user) {
          flashTiny('No original user message found');
          return;
        }
        // abort any running stream, hide thinking bubbles
        abortPendingStream();
        showThinking();
        await delay(180);
        doChatRequest(payload.orig_user, { regenFrom: payload.message_id });
      };
      actions.appendChild(regen);
    }
    return actions;
  }

  function flashTiny(msg) {
    const flash = document.createElement('div');
    flash.className = 'tiny-flash';
    flash.innerText = msg;
    document.body.appendChild(flash);
    setTimeout(()=> flash.classList.add('visible'), 20);
    setTimeout(()=> flash.classList.remove('visible'), 1400);
    setTimeout(()=> flash.remove(), 1700);
  }

  function delay(ms){ return new Promise(r=>setTimeout(r, ms)); }

  // ---------------- system message helper ----------------
  function addSystemMessage(msg) {
    const el = document.createElement('div');
    el.className = 'message system';
    el.innerHTML = `<div class="bubble"><div class="message-text">${escapeHtml(msg)}</div></div>`;
    messages.appendChild(el);
    scrollToBottom();
  }

  // ---------------- create user/bot messages ----------------
  function appendUserMessage(text) {
    const el = document.createElement('div');
    el.className = 'message user';
    el.dataset.role = 'user';

    const bubble = document.createElement('div');
    bubble.className = 'bubble user-bubble';

    const content = document.createElement('div');
    content.className = 'message-text';
    content.innerHTML = escapeHtml(text);

    bubble.appendChild(content);
    bubble.appendChild(createMsgActions(true, { text }));
    el.appendChild(bubble);

    // attach swipe-to-reply on user bubbles
    attachSwipeReply(el, text);

    messages.appendChild(el);
    scrollToBottom();
    // store in history
    userMessageHistory.push(text);
    return el;
  }

  function appendBotMessageStreamPlaceholder(origUser, opts = {}) {
    // returns an element to stream into
    const wrapper = document.createElement('div');
    wrapper.className = 'message bot';
    wrapper.dataset.role = 'bot';

    const bubble = document.createElement('div');
    bubble.className = 'bubble bot-bubble streaming';
    // gradient container — content will be appended word-by-word
    bubble.innerHTML = `<div class="message-text"></div>`;
    wrapper.appendChild(bubble);
    // store metadata for regen action
    wrapper._meta = {
      orig_user: origUser,
      message_id: opts.message_id || Date.now().toString()
    };
    messages.appendChild(wrapper);
    scrollToBottom();
    return wrapper;
  }

  function appendBotMessageFinal(text, origUser, message_id) {
    const wrapper = document.createElement('div');
    wrapper.className = 'message bot';
    wrapper.dataset.role = 'bot';

    const bubble = document.createElement('div');
    bubble.className = 'bubble bot-bubble';
    bubble.innerHTML = `<div class="message-text">${escapeHtml(text)}</div>`;
    bubble.appendChild(createMsgActions(false, { text, orig_user: origUser, message_id }));
    wrapper.appendChild(bubble);

    messages.appendChild(wrapper);
    scrollToBottom();
    return wrapper;
  }

  // ---------------- Thinking shimmer + leaves ----------------
  function spawnLeaves() {
    removeLeaves();
    const container = document.createElement('div');
    container.className = 'leaf-container';
    container.id = 'leafFX';
    for (let i=0;i<8;i++){
      const leaf = document.createElement('div');
      leaf.className = 'leaf';
      leaf.style.left = (Math.random() * 85) + '%';
      leaf.style.top = (Math.random() * 60) + '%';
      leaf.style.animationDelay = (Math.random()*1.8) + 's';
      leaf.style.transform = `rotate(${Math.random()*360}deg)`;
      container.appendChild(leaf);
    }
    const panel = document.querySelector('.chat-panel') || document.body;
    panel.appendChild(container);
  }
  function removeLeaves() { const fx = document.getElementById('leafFX'); if (fx) fx.remove(); }

  let thinkingEl = null;
  function showThinking() {
    if (thinkingActive) return;
    thinkingActive = true;
    spawnLeaves();
    thinkingEl = document.createElement('div');
    thinkingEl.id = 'thinkingBubble';
    thinkingEl.className = 'message bot';
    thinkingEl.innerHTML = `
      <div class="bubble bot-bubble thinking">
        <div class="skeleton-bubble"></div>
        <div class="think-dots">
          <span class="think-dot"></span>
          <span class="think-dot"></span>
          <span class="think-dot"></span>
        </div>
      </div>`;
    messages.appendChild(thinkingEl);
    scrollToBottom();
    // subtle typing sound loop while thinking (non-blocking)
    playTypingSound();
  }
  function hideThinking() {
    thinkingActive = false;
    if (thinkingEl) thinkingEl.remove();
    thinkingEl = null;
    removeLeaves();
  }

  // ---------------- abort stream helper ----------------
  function abortPendingStream() {
    if (pendingStreamAbort) {
      pendingStreamAbort.abort();
      pendingStreamAbort = null;
    }
  }

  // ---------------- streaming (word-by-word) ----------------
  async function streamBotMessage(fullText, origUser, message_id) {
    hideThinking();
    abortPendingStream();
    const wrapper = appendBotMessageStreamPlaceholder(origUser, { message_id });
    const bubbleText = wrapper.querySelector('.message-text');
    bubbleText.innerHTML = ''; // start empty

    // create an AbortController so we can cancel mid-stream
    const ac = new AbortController();
    pendingStreamAbort = ac;

    const words = String(fullText || '').split(/\s+/);
    for (let i = 0; i < words.length; i++) {
      if (ac.signal.aborted) { // stopped
        pendingStreamAbort = null;
        return;
      }
      bubbleText.innerHTML += escapeHtml(words[i]) + ' ';
      playTypingSound();
      scrollToBottom();
      // speed tweak: faster early, slower later
      await delay(42 + Math.min(120, Math.floor(Math.random()*40)));
    }

    // finalize bubble: replace streaming wrapper with a final one that has actions
    wrapper.remove();
    appendBotMessageFinal(fullText, origUser, message_id);
    pendingStreamAbort = null;
  }

  // ---------------- api chat request wrapper ----------------
  async function doChatRequest(userMessage, opts = {}) {
    try {
      // call chat endpoint
      const init = { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: userMessage }) };
      const res = await fetch('/api/chat', init);
      if (!res.ok) {
        const txt = await res.text();
        throw new Error(txt || 'Server error');
      }
      const data = await res.json();
      const answer = data.response || data.answer || 'No response';
      // stream
      await streamBotMessage(answer, userMessage, opts.message_id || Date.now().toString());
    } catch (err) {
      hideThinking();
      addSystemMessage('Error: ' + (err.message || 'unknown'));
    }
  }

  // ---------------- image analyze flow (keeps your existing endpoint) ----------------
  function handleImageUpload(file) {
    return new Promise((resolve, reject) => {
      if (!file || !file.type || !file.type.startsWith('image/')) return reject(new Error('Invalid image'));
      if (file.size > 5*1024*1024) return reject(new Error('Image too large (>5MB)'));
      const r = new FileReader();
      r.onload = (e) => resolve(e.target.result);
      r.onerror = ()=> reject(new Error('Read failed'));
      r.readAsDataURL(file);
    });
  }
  async function analyzeImage(imageFile, textMessage='') {
    const f = new FormData();
    f.append('image', imageFile);
    if (textMessage) f.append('message', textMessage);
    const res = await fetch('/api/analyze-image', { method: 'POST', body: f });
    if (!res.ok) throw new Error('Image analysis failed');
    const text = await res.json();
    return text;
  }

  // ---------------- SEND MESSAGE (wired to sendBtn) ----------------
  async function sendMessage(e) {
    if (e) e.preventDefault();
    const msg = (input.value || '').trim();
    const imageFile = imageInput?.files?.[0] || null;
    if (!msg && !imageFile) return;
    sendBtn.disabled = true;
    abortPendingStream(); // stop any previous
    try {
      if (imageFile) {
        // show user image message
        const dataUrl = await handleImageUpload(imageFile);
        appendUserMessage(msg || 'Image uploaded');
        // call analyze endpoint
        showThinking();
        const analysis = await analyzeImage(imageFile, msg);
        // if analysis.response present, stream it
        const responseText = (analysis && (analysis.response || analysis.summary)) || 'Analysis complete';
        await streamBotMessage(responseText, msg, Date.now().toString());
        imageInput.value = '';
      } else {
        appendUserMessage(msg);
        // store and call
        showThinking();
        // small delay so shimmer is visible
        await delay(220);
        await doChatRequest(msg);
      }
    } catch (err) {
      hideThinking();
      addSystemMessage('Error: ' + (err.message || 'unknown'));
    } finally {
      sendBtn.disabled = false;
      input.value = '';
      input.focus();
    }
  }

  // ---------------- swipe-to-reply (touch support) ----------------
  function attachSwipeReply(node, messageText) {
    let startX = 0, startY = 0, moved = false;
    node.addEventListener('touchstart', (ev) => {
      const t = ev.touches[0];
      startX = t.clientX; startY = t.clientY; moved = false;
    }, { passive: true });
    node.addEventListener('touchmove', (ev) => {
      const t = ev.touches[0];
      const dx = t.clientX - startX, dy = t.clientY - startY;
      if (Math.abs(dx) > 30 && Math.abs(dy) < 30) {
        moved = true;
        node.classList.add('swipe-preview');
      }
    }, { passive: true });
    node.addEventListener('touchend', (ev) => {
      node.classList.remove('swipe-preview');
      if (moved) {
        input.value = messageText;
        input.focus();
        flashTiny('Replied in input');
      }
    });
    // also enable mouse double-click to reply quickly
    node.addEventListener('dblclick', () => {
      input.value = messageText; input.focus(); flashTiny('Replied in input');
    });
  }

  // ---------------- small helpers wired to UI ----------------
  function setMicActive(on) {
    const mic = document.getElementById('voiceBtn');
    if (!mic) return;
    mic.classList.toggle('listening', !!on);
  }
  window.setMicActive = setMicActive; // keep compatibility

  // ---------------- events ----------------
  sendBtn?.addEventListener('click', sendMessage);
  voiceBtn?.addEventListener('click', toggleVoiceInput);

  input?.addEventListener('keydown', (ev) => {
    if (ev.key === 'Enter' && !ev.shiftKey) {
      ev.preventDefault(); sendMessage();
    }
  });

  imageInput?.addEventListener('change', (ev) => {
    if (ev.target.files && ev.target.files.length) sendMessage();
  });

  // small UX helpers
  function makeQuickControls() {
    // regenerate last button (global)
    const ctrl = document.createElement('div');
    ctrl.className = 'quick-controls';
    ctrl.innerHTML = `<button id="regenLast" class="btn small ghost">Regenerate</button>`;
    document.querySelector('.chat-panel')?.prepend(ctrl);
    document.getElementById('regenLast')?.addEventListener('click', async () => {
      const last = userMessageHistory.slice(-1)[0];
      if (!last) { flashTiny('No message to regenerate'); return; }
      abortPendingStream();
      showThinking();
      await delay(180);
      doChatRequest(last);
    });
  }
  makeQuickControls();

  // final focus
  input?.focus();
}); // DOMContentLoaded end

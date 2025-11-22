/* script.js
   -> Merged chat logic (from your original script) + theme toggle + small UI helpers
   -> Keep backend endpoints unchanged (/api/chat, /api/analyze-image)
   -> Theme saved in localStorage as "agrobot_theme"
*/

/* ------------------- THEME HANDLING ------------------- */
(function () {
  const THEME_KEY = 'agrobot_theme';

  function applyTheme(theme) {
    if (theme === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
    else document.documentElement.removeAttribute('data-theme');
  }

  function saveTheme(theme) {
    try { localStorage.setItem(THEME_KEY, theme); } catch (e) {}
  }

  function initTheme() {
    let stored = null;
    try { stored = localStorage.getItem(THEME_KEY); } catch (e) { stored = null; }
    if (!stored) {
      // prefer dark if user OS prefers dark
      const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
      stored = prefersDark ? 'dark' : 'light';
    }
    applyTheme(stored);
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    saveTheme(next);
  }

  // Expose toggle for the button
  window.toggleAgrobotTheme = toggleTheme;

  // Init on load
  document.addEventListener('DOMContentLoaded', initTheme);
})();

/* ------------------- UI & CHAT LOGIC ------------------- */
document.addEventListener('DOMContentLoaded', () => {
  console.log('script loaded — UI + Chat ready');

  // Theme toggle wiring
  const themeBtn = document.getElementById('themeToggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      window.toggleAgrobotTheme();
      // small pressed animation
      themeBtn.animate([{ transform: 'scale(1)' }, { transform: 'scale(.96)' }, { transform: 'scale(1)' }], { duration: 160 });
    });
  }

  // --- Existing elements (kept names so backend works) ---
  const messages = document.getElementById('messages');
  const input = document.getElementById('msg');
  const sendBtn = document.getElementById('sendBtn');
  const imageInput = document.getElementById('imageInput');
  const voiceBtn = document.getElementById('voiceBtn');

  // Voice recognition variables
  let recognition = null;
  let isListening = false;

  // Initialize voice recognition if available
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-IN';

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      input.value = transcript;
      updateVoiceButton(false);
      setMicActive(false);     // <<< animate mic off
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      updateVoiceButton(false);
      setMicActive(false);     // <<< animate mic off
      addMessage('system', `Voice input error: ${event.error}`);
    };

    recognition.onend = () => {
      updateVoiceButton(false);
      setMicActive(false);    // <<< animate mic off
    };
  } else {
    console.warn('Speech recognition not supported in this browser');
    if (voiceBtn) voiceBtn.style.display = 'none';
  }

  function updateVoiceButton(listening) {
    isListening = listening;
    if (voiceBtn) {
      voiceBtn.textContent = listening ? '🎙️ Listening...' : '🎤 Voice';
      if (listening) voiceBtn.classList.add('listening');
      else voiceBtn.classList.remove('listening');
    }
  }

  function toggleVoiceInput() {
  if (!recognition) {
    addMessage('system', 'Voice input is not supported in your browser');
    return;
  }

  if (isListening) {
    recognition.stop();
    updateVoiceButton(false);
    setMicActive(false);     // <<< animate mic off
  } else {
    try {
      recognition.start();
      updateVoiceButton(true);
      setMicActive(true);    // <<< animate mic ON 🔥
    } catch (error) {
      console.error('Error starting voice recognition:', error);
    }
  }
}


  function addMessage(who, text, imageData = null) {
    const el = document.createElement('div');
    el.className = 'message ' + who;

    const bubble = document.createElement('div');
    bubble.className = 'bubble';

    // Add image if provided
    if (imageData) {
      const imgContainer = document.createElement('div');
      imgContainer.className = 'image-container';

      const img = document.createElement('img');
      img.src = imageData;
      img.alt = 'Uploaded image';
      img.className = 'chat-image';
      img.style.maxWidth = '240px';
      img.style.borderRadius = '8px';
      img.style.display = 'block';

      imgContainer.appendChild(img);
      bubble.appendChild(imgContainer);

      if (text) {
        const textSpacer = document.createElement('div');
        textSpacer.style.marginTop = '10px';
        bubble.appendChild(textSpacer);
      }
    }

    if (text) {
      const textElement = document.createElement('div');
      textElement.className = 'message-text';

      const formattedText = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');

      textElement.innerHTML = formattedText;
      bubble.appendChild(textElement);
    }

    el.appendChild(bubble);
    messages.appendChild(el);
    // messages.scrollTop = messages.scrollHeight;
    scrollToBottom();}

  function handleImageUpload(file) {
    return new Promise((resolve, reject) => {
      if (!file.type.startsWith('image/')) {
        reject(new Error('Please select an image file'));
        return;
      }
      if (file.size > 5 * 1024 * 1024) {
        reject(new Error('Image size should be less than 5MB'));
        return;
      }
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target.result);
      reader.onerror = () => reject(new Error('Failed to read image file'));
      reader.readAsDataURL(file);
    });
  }

  async function analyzeImage(imageFile, textMessage = '') {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);
      if (textMessage) formData.append('message', textMessage);

      const res = await fetch('/api/analyze-image', { method: 'POST', body: formData });
      const responseText = await res.text();

      if (responseText.trim().startsWith('<!DOCTYPE') || responseText.includes('<html') || responseText.includes('login')) {
        throw new Error('Authentication required. Please log in to use image analysis.');
      }

      if (!res.ok) {
        let errorData;
        try {
          errorData = JSON.parse(responseText);
          throw new Error(errorData.error || `Server error: ${res.status}`);
        } catch (e) {
          throw new Error(`Server error: ${res.status}. Please try again.`);
        }
      }

      const data = JSON.parse(responseText);
      return data;
    } catch (error) {
      console.error('Image analysis error:', error);
      throw error;
    }
  }

  async function sendMessage() {
    const msg = input.value.trim();
    const imageFile = imageInput?.files[0];
    if (!msg && !imageFile) return;
    sendBtn.disabled = true;

    try {
      // IMAGE FLOW
      if (imageFile) {
        addMessage('user', msg || `I uploaded this image for analysis`, await handleImageUpload(imageFile));
        try {
          const analysisResult = await analyzeImage(imageFile, msg);
          if (analysisResult.success) {
            // analysisResult.response is a text summary
            addMessage('bot', analysisResult.response);
          } else {
            addMessage('bot', `Analysis completed with issues: ${analysisResult.error || 'unknown'}`);
          }
        } catch (analysisError) {
          if (analysisError.message.includes('Authentication required') || analysisError.message.includes('login')) {
            addMessage('bot', '🔒 Please log in to use the image analysis feature. You can still chat without images.');
          } else {
            addMessage('bot', `Image analysis failed: ${analysisError.message}`);
          }
        }
        imageInput.value = '';
      }

      // TEXT ONLY FLOW
      else if (msg) {
        addMessage('user', msg);

        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: msg })
        });

        if (!res.ok) {
          // try parse JSON for error
          let errText = 'Network response not ok';
          try {
            const j = await res.json();
            errText = j.response || j.error || errText;
          } catch (e) {}
          throw new Error(errText);
        }
        const data = await res.json();
        addMessage('bot', data.response || 'No response');
      }
    } catch (err) {
      console.error('Send message error:', err);
      addMessage('bot', `Error: ${err.message}`);
    } finally {
      sendBtn.disabled = false;
      input.value = '';
      input.focus();
    }
  }

  // EVENTS
  sendBtn && sendBtn.addEventListener('click', sendMessage);
  voiceBtn && voiceBtn.addEventListener('click', toggleVoiceInput);

  input && input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // auto-send when image selected
  imageInput && imageInput.addEventListener('change', (e) => {
    if (e.target.files.length === 0) return;
    const file = e.target.files[0];
    if (!file.type.startsWith('image/')) {
      addMessage('system', 'Please select a valid image file (JPEG, PNG, GIF, WebP)');
      imageInput.value = '';
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      addMessage('system', 'Image size must be less than 5MB');
      imageInput.value = '';
      return;
    }
    sendMessage();
  });

  // small accessibility: focus message input on load
  if (input) input.focus();
});


function scrollToBottom() {
  const messages = document.getElementById("messages");
  messages.scrollTo({
    top: messages.scrollHeight,
    behavior: "smooth"
  });
}


function showTyping() {
  const el = document.createElement("div");
  el.id = "typingIndicator";
  el.className = "message bot";
  el.innerHTML = `<div class="bubble">Typing<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span></div>`;
  messages.appendChild(el);
  scrollToBottom();
}

function hideTyping() {
  const t = document.getElementById("typingIndicator");
  if (t) t.remove();
}


// Toggle mic animation state
function setMicActive(state) {
  const mic = document.getElementById("voiceBtn");
  if (state) mic.classList.add("listening");
  else mic.classList.remove("listening");
}


/* END OF script.js */
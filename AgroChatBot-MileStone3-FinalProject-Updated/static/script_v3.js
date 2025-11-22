/* script.js
   -> Fully upgraded with typing sound, shimmer, floating leaves FX,
      GPT-style streaming, but keeps ALL your original logic intact.
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

  window.toggleAgrobotTheme = toggleTheme;
  document.addEventListener('DOMContentLoaded', initTheme);
})();

/* ------------------- UI & CHAT LOGIC ------------------- */
document.addEventListener('DOMContentLoaded', () => {
  console.log('script loaded — UI + Chat ready');

  /* ------------------- TYPING SOUND ------------------- */
  const typingSound = new Audio("/static/typing.mp3");
  typingSound.volume = 0.25;

  function playTypingSound() {
    typingSound.currentTime = 0;
    typingSound.play().catch(()=>{});
  }

  /* ------------------- ELEMENTS ------------------- */
  const themeBtn = document.getElementById('themeToggle');
  const messages = document.getElementById('messages');
  const input = document.getElementById('msg');
  const sendBtn = document.getElementById('sendBtn');
  const imageInput = document.getElementById('imageInput');
  const voiceBtn = document.getElementById('voiceBtn');

  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      window.toggleAgrobotTheme();
      themeBtn.animate([{ transform: 'scale(1)' }, { transform: 'scale(.96)' }, { transform: 'scale(1)' }], { duration: 160 });
    });
  }

  /* ------------------- VOICE RECOGNITION ------------------- */
  let recognition = null;
  let isListening = false;

  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-IN';

    recognition.onresult = (event) => {
      input.value = event.results[0][0].transcript;
      updateVoiceButton(false);
      setMicActive(false);
    };

    recognition.onerror = (event) => {
      console.error('Speech error:', event.error);
      updateVoiceButton(false);
      setMicActive(false);
      addMessage('system', `Voice error: ${event.error}`);
    };

    recognition.onend = () => {
      updateVoiceButton(false);
      setMicActive(false);
    };
  } else {
    if (voiceBtn) voiceBtn.style.display = 'none';
  }

  function updateVoiceButton(v) {
    isListening = v;
    voiceBtn.textContent = v ? '🎙️ Listening...' : '🎤 Voice';
    voiceBtn.classList.toggle('listening', v);
  }

  function toggleVoiceInput() {
    if (!recognition) {
      addMessage('system', 'Voice not supported');
      return;
    }
    if (isListening) {
      recognition.stop();
      updateVoiceButton(false);
      setMicActive(false);
    } else {
      try {
        recognition.start();
        updateVoiceButton(true);
        setMicActive(true);
      } catch (e) { console.error(e); }
    }
  }

  /* ------------------- ORIGINAL addMessage() ------------------- */
  function addMessage(who, text, imageData = null) {
    const el = document.createElement('div');
    el.className = 'message ' + who;

    const bubble = document.createElement('div');
    bubble.className = 'bubble';

    if (imageData) {
      const img = document.createElement('img');
      img.src = imageData;
      img.className = 'chat-image';
      img.style.maxWidth = '240px';
      img.style.borderRadius = '8px';
      bubble.appendChild(img);
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
    scrollToBottom();
  }

  /* ------------------- IMAGE HANDLING ------------------- */
  function handleImageUpload(file) {
    return new Promise((resolve, reject) => {
      if (!file.type.startsWith('image/')) return reject(new Error('Invalid image'));
      if (file.size > 5 * 1024 * 1024) return reject(new Error('Image too large'));

      const reader = new FileReader();
      reader.onload = e => resolve(e.target.result);
      reader.onerror = () => reject(new Error('Read error'));
      reader.readAsDataURL(file);
    });
  }

  /* ------------------- AI THINKING SHIMMER + LEAVES ------------------- */
  let thinkingActive = false;

  function showThinking() {
    if (thinkingActive) return;
    thinkingActive = true;

    spawnLeaves();

    const el = document.createElement("div");
    el.id = "thinkingBubble";
    el.className = "message bot";

    el.innerHTML = `
      <div class="bubble">
        <div class="skeleton-bubble"></div>
        <div class="think-dots">
          <span class="think-dot"></span>
          <span class="think-dot"></span>
          <span class="think-dot"></span>
        </div>
      </div>
    `;

    messages.appendChild(el);
    scrollToBottom();
  }

  function hideThinking() {
    thinkingActive = false;
    const t = document.getElementById("thinkingBubble");
    if (t) t.remove();
    removeLeaves();
  }

  function spawnLeaves() {
    const container = document.createElement("div");
    container.className = "leaf-container";
    container.id = "leafFX";

    for (let i = 0; i < 6; i++) {
      const leaf = document.createElement("div");
      leaf.className = "leaf";
      leaf.style.left = (Math.random() * 60 + 10) + "%";
      leaf.style.top = (Math.random() * 40 + 10) + "%";
      leaf.style.animationDelay = (Math.random() * 2) + "s";
      container.appendChild(leaf);
    }

    document.querySelector(".chat-panel").appendChild(container);
  }

  function removeLeaves() {
    const fx = document.getElementById("leafFX");
    if (fx) fx.remove();
  }

  /* ------------------- GPT-STYLE STREAMING TEXT ------------------- */
  function streamBotMessage(fullText) {
    hideThinking();

    const wrapper = document.createElement("div");
    wrapper.className = "message bot";
    wrapper.innerHTML = `<div class="bubble"></div>`;
    messages.appendChild(wrapper);

    const bubble = wrapper.querySelector(".bubble");
    const words = fullText.split(" ");
    let index = 0;

    function showNext() {
      if (index < words.length) {
        bubble.innerHTML += words[index] + " ";
        index++;
        playTypingSound();
        scrollToBottom();
        setTimeout(showNext, 55);
      }
    }

    showNext();
  }

  /* ------------------- ANALYZE IMAGE ------------------- */
  async function analyzeImage(imageFile, textMessage = '') {
    const formData = new FormData();
    formData.append('image', imageFile);
    if (textMessage) formData.append('message', textMessage);

    const res = await fetch('/api/analyze-image', { method: 'POST', body: formData });
    const text = await res.text();

    if (!res.ok) throw new Error("Image analysis failed");

    return JSON.parse(text);
  }

  /* ------------------- SEND MESSAGE ------------------- */
  async function sendMessage() {
    const msg = input.value.trim();
    const imageFile = imageInput?.files[0];

    if (!msg && !imageFile) return;
    sendBtn.disabled = true;

    try {
      if (imageFile) {
        addMessage('user', msg || 'I uploaded this image', await handleImageUpload(imageFile));
        const result = await analyzeImage(imageFile, msg);
        streamBotMessage(result.response);
        imageInput.value = '';
      } else {
        addMessage('user', msg);

        showThinking();

        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: msg })
        });

        const data = await res.json();

        setTimeout(() => {
          streamBotMessage(data.response || "No response");
        }, 600);
      }
    } catch (e) {
      addMessage('bot', `Error: ${e.message}`);
    } finally {
      sendBtn.disabled = false;
      input.value = '';
      input.focus();
    }
  }

  /* ------------------- EVENTS ------------------- */
  sendBtn.addEventListener('click', sendMessage);
  voiceBtn.addEventListener('click', toggleVoiceInput);

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  imageInput.addEventListener('change', (e) => {
    if (e.target.files.length) sendMessage();
  });

  input.focus();
});

/* ------------------- HELPERS ------------------- */
function scrollToBottom() {
  const messages = document.getElementById("messages");
  messages.scrollTo({ top: messages.scrollHeight, behavior: "smooth" });
}

function setMicActive(v) {
  const mic = document.getElementById("voiceBtn");
  mic.classList.toggle("listening", v);
}

/* END OF script.js */

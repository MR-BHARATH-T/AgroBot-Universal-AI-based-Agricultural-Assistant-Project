/* script.js — Hybrid GPT-Agro Fusion
   Full rebuild: streaming, shimmer, leaves, typing sound, waveform, copy/edit/regenerate, swipe-to-reply.
*/

/* ---------- THEME HANDLING ---------- */
(() => {
  const THEME_KEY = 'agrobot_theme';
  function applyTheme(theme){ if(theme==='dark') document.documentElement.setAttribute('data-theme','dark'); else document.documentElement.removeAttribute('data-theme'); }
  function saveTheme(theme){ try{ localStorage.setItem(THEME_KEY, theme);}catch(e){} }
  function initTheme(){
    let stored=null;
    try{ stored=localStorage.getItem(THEME_KEY);}catch(e){}
    if(!stored){ const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches; stored = prefersDark ? 'dark' : 'light'; }
    applyTheme(stored);
  }
  function toggleTheme(){ const cur=document.documentElement.getAttribute('data-theme')==='dark'?'dark':'light'; const next=cur==='dark'?'light':'dark'; applyTheme(next); saveTheme(next);}
  window.toggleAgrobotTheme = toggleTheme;
  document.addEventListener('DOMContentLoaded', initTheme);
})();

/* ---------- DOM READY / App ---------- */
document.addEventListener('DOMContentLoaded', () => {
  console.log('AI-AgroChat ready');

  /* ---------- Typing sound ---------- */
  const typingSound = new Audio('/static/typing.mp3');
  typingSound.volume = 0.25;
  function playTypingSound(){ try{ typingSound.currentTime = 0; typingSound.play().catch(()=>{}); }catch(e){} }

  /* ---------- elements ---------- */
  const messagesEl = document.getElementById('messages');
  const inputEl = document.getElementById('msg');
  const sendBtn = document.getElementById('sendBtn');
  const imageInput = document.getElementById('imageInput');
  const voiceBtn = document.getElementById('voiceBtn');
  const themeToggle = document.getElementById('themeToggle');

  /* ---------- state ---------- */
  let recognition = null;
  let isListening = false;
  let thinkingActive = false;
  let lastUserQuery = '';
  let lastBotResponse = '';
  let streamingAbort = { aborted: false };

  /* ---------- helpers ---------- */
  function tinyFlash(text, timeout=1800){
    let el = document.querySelector('.tiny-flash');
    if(!el){ el = document.createElement('div'); el.className='tiny-flash'; document.body.appendChild(el); }
    el.textContent = text; el.classList.add('visible');
    clearTimeout(el._t); el._t = setTimeout(()=> el.classList.remove('visible'), timeout);
  }

  function scrollToBottom(behavior='smooth'){
    try{ messagesEl.scrollTo({ top: messagesEl.scrollHeight, behavior }); }catch(e){ messagesEl.scrollTop = messagesEl.scrollHeight; }
  }

  /* ---------- voice recognition ---------- */
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SR();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-IN';

    recognition.onresult = (evt) => {
      const t = evt.results[0][0].transcript;
      inputEl.value = t;
      updateVoiceBtn(false);
      setMicActive(false);
      tinyFlash('Captured voice input');
    };
    recognition.onerror = (e) => { console.error('speecherr', e); updateVoiceBtn(false); setMicActive(false); tinyFlash('Voice error'); };
    recognition.onend = () => { updateVoiceBtn(false); setMicActive(false); };
  } else {
    if(voiceBtn) voiceBtn.style.display = 'none';
  }

  function updateVoiceBtn(v){
    isListening = v;
    if(!voiceBtn) return;
    voiceBtn.classList.toggle('listening', !!v);
    voiceBtn.innerText = v ? '🎙️ Listening...' : '🎤 Voice';
  }

  function toggleVoice(){
    if(!recognition){ tinyFlash('Voice not available in this browser'); return; }
    if(isListening){ recognition.stop(); updateVoiceBtn(false); setMicActive(false); }
    else { try{ recognition.start(); updateVoiceBtn(true); setMicActive(true); }catch(e){ console.error(e); } }
  }

  function setMicActive(state){ const mic = document.getElementById('voiceBtn'); if(!mic) return; mic.classList.toggle('listening', !!state); }

  /* ---------- message create utilities ---------- */
  function createMessageElement({who='bot', text='', image=null, meta=null, streaming=false, allowRegenerate=false}) {
  const wrap = document.createElement('div');
  wrap.className = 'message ' + who + (streaming ? ' streaming' : '');

  const bubble = document.createElement('div');
  bubble.className = 'bubble ' + (who === 'bot' ? 'bot-bubble' : 'user-bubble');

  // image first
  if (image) {
    const img = document.createElement('img');
    img.src = image;
    img.className = 'chat-image';
    img.style.maxWidth = '320px';
    img.style.borderRadius = '8px';
    bubble.appendChild(img);
  }

  // text container
  const textEl = document.createElement('div');
  textEl.className = 'message-text';
  textEl.innerHTML = text ? sanitizeAndFormat(text) : '';
  bubble.appendChild(textEl);

  // action row
  const actions = document.createElement('div');
  actions.className = 'msg-actions';

  if (who === 'bot') {
    /* COPY ICON */
    const copyBtn = document.createElement('button');
    copyBtn.className = 'action-btn copy';
    copyBtn.title = 'Copy reply';
    copyBtn.innerHTML = `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
        <rect x="9" y="9" width="13" height="13" rx="2"></rect>
        <rect x="3" y="3" width="13" height="13" rx="2"></rect>
      </svg>`;
    copyBtn.onclick = () => copyToClipboard(textEl.innerText || text);
    actions.appendChild(copyBtn);

    /* REGENERATE ICON (ONLY if allowRegenerate) */
    if (allowRegenerate && lastUserQuery) {
      const regenBtn = document.createElement('button');
      regenBtn.className = 'action-btn regen';
      regenBtn.title = 'Regenerate reply';
      regenBtn.innerHTML = `
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="23 4 23 10 17 10"></polyline>
          <polyline points="1 20 1 14 7 14"></polyline>
          <path d="M3.51 9a9 9 0 0114.13-3.36L23 10"></path>
          <path d="M20.49 15a9 9 0 01-14.13 3.36L1 14"></path>
        </svg>`;
      regenBtn.onclick = () => regenerate(lastUserQuery);
      actions.appendChild(regenBtn);
    }

    /* REPLY ICON */
    const replyBtn = document.createElement('button');
    replyBtn.className = 'action-btn reply';
    replyBtn.title = 'Reply to message';
    replyBtn.innerHTML = `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
        <path d="M10 19l-7-7 7-7"></path>
        <path d="M3 12h14a4 4 0 014 4v1"></path>
      </svg>`;
    replyBtn.onclick = () => {
      inputEl.value = (textEl.innerText || '').slice(0, 300);
      inputEl.focus();
      tinyFlash("Reply inserted");
    };
    actions.appendChild(replyBtn);

  } else {
    /* USER BUBBLE → EDIT ICON */
    const editBtn = document.createElement('button');
    editBtn.className = 'action-btn edit';
    editBtn.title = 'Edit message';
    editBtn.innerHTML = `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 20h9"></path>
        <path d="M16.5 3.5a2.1 2.1 0 013 3L7 19l-4 1 1-4 12.5-12.5z"></path>
      </svg>`;
    editBtn.onclick = () => {
      inputEl.value = textEl.innerText || text;
      inputEl.focus();
      tinyFlash("Edit your query");
    };
    actions.appendChild(editBtn);
  }

  wrap.appendChild(bubble);
  bubble.appendChild(actions);

  return { wrap, textEl, bubble };
}
    function sanitizeAndFormat(text){
        const div = document.createElement('div');
        div.textContent = text;
        let sanitized = div.innerHTML;
        sanitized = sanitized.replace(/\n/g, '<br>');
        return sanitized;
    }
    function copyToClipboard(text){
        navigator.clipboard.writeText(text).then(() => {
            tinyFlash('Copied to clipboard');
        }).catch(() => {
            tinyFlash('Copy failed');
        });
    }


  /* ---------- thinking shimmer + leaves ---------- */
  function spawnLeaves(){
    removeLeaves();
    const container = document.createElement('div');
    container.className = 'leaf-container';
    container.id = 'leafFX';
    for(let i=0;i<7;i++){
      const leaf = document.createElement('div');
      leaf.className = 'leaf';
      leaf.style.left = (Math.random()*70 + 5) + '%';
      leaf.style.top = (Math.random()*60 + 5) + '%';
      leaf.style.animationDelay = (Math.random()*1.8) + 's';
      leaf.style.opacity = (0.6 + Math.random()*0.4);
      container.appendChild(leaf);
    }
    const panel = document.querySelector('.chat-panel') || document.body;
    panel.appendChild(container);
  }
  function removeLeaves(){ const fx = document.getElementById('leafFX'); if(fx) fx.remove(); }

  function showThinking(){
    if(thinkingActive) return;
    thinkingActive = true;
    spawnLeaves();
    const t = document.createElement('div');
    t.id = 'thinkingBubble';
    t.className = 'message bot thinking';
    t.innerHTML = `<div class="bubble bot-bubble">
      <div class="skeleton-bubble"></div>
      <div class="think-dots"><span class="think-dot"></span><span class="think-dot"></span><span class="think-dot"></span></div>
      <div class="msg-actions" style="position:absolute;right:10px;bottom:8px"><button class="action-btn action-small" id="cancelStream">Cancel</button></div>
    </div>`;
    messagesEl.appendChild(t);
    scrollToBottom();
    const cancelBtn = document.getElementById('cancelStream');
    if(cancelBtn) cancelBtn.addEventListener('click', ()=>{
      streamingAbort.aborted = true;
      hideThinking();
      tinyFlash('Cancelled');
    });
  }
  function hideThinking(){
    thinkingActive = false;
    const t = document.getElementById('thinkingBubble'); if(t) t.remove();
    removeLeaves();
  }

  /* ---------- streaming text (word-by-word) ---------- */
  async function streamBotMessage(fullText) {
  streamingAbort.aborted = false;
  hideThinking();

  // create bubble with allowRegenerate only for latest
  const { wrap, textEl, bubble } = createMessageElement({
    who: 'bot',
    text: '',
    streaming: true,
    allowRegenerate: true
  });

  messagesEl.appendChild(wrap);
  markLatestBot(wrap);
  scrollToBottom();

  const words = String(fullText || '').split(/\s+/);
  let i = 0;

  function next() {
    if (streamingAbort.aborted) {
      textEl.innerText += " — [stopped]";
      return;
    }
    if (i >= words.length) {
      lastBotResponse = fullText;
      bubble.animate([{ transform: "translateY(4px)" }, { transform: "translateY(0)" }], { duration: 280 });
      return;
    }

    textEl.innerText += (i === 0 ? "" : " ") + words[i];
    i++;
    playTypingSound();
    scrollToBottom("auto");

    setTimeout(next, 35 + Math.random() * 35);
  }

  next();
}


function markLatestBot(wrapEl) {
  // remove previous flags
  const prev = messagesEl.querySelectorAll('.message.bot.latest-bot');
  prev.forEach(p => p.classList.remove('latest-bot'));

  wrapEl.classList.add('latest-bot');
}


  /* ---------- stream fallback: immediate add ---------- */
  function addBotMessageImmediate(text) {
  const { wrap } = createMessageElement({
    who: 'bot',
    text,
    allowRegenerate: true
  });

  messagesEl.appendChild(wrap);
  markLatestBot(wrap);
  lastBotResponse = text;
  scrollToBottom();
}

  /* ---------- create user message ---------- */
  function addUserMessage(text, imageData=null){
    const { wrap } = createMessageElement({who:'user', text, image: imageData});
    messagesEl.appendChild(wrap);
    lastUserQuery = text;
    scrollToBottom();
  }

  /* ---------- image helper ---------- */
  function handleImageUpload(file){
    return new Promise((resolve,reject)=>{
      if(!file || !file.type.startsWith('image/')) return reject(new Error('Invalid image'));
      if(file.size > 6*1024*1024) return reject(new Error('Image too large'));
      const r = new FileReader();
      r.onload = e => resolve(e.target.result);
      r.onerror = ()=> reject(new Error('Read error'));
      r.readAsDataURL(file);
    });
  }

  /* ---------- network helpers ---------- */
  async function analyzeImageOnServer(file, caption=''){
    const fd = new FormData(); fd.append('image', file); if(caption) fd.append('message', caption);
    const res = await fetch('/api/analyze-image', { method:'POST', body: fd });
    if(!res.ok) throw new Error('Image analysis failed');
    return res.json();
  }

  async function chatToServer(message){
    const res = await fetch('/api/chat', {
      method:'POST', headers:{ 'Content-Type':'application/json' },
      body: JSON.stringify({ message })
    });
    if(!res.ok) {
      let txt = await res.text().catch(()=>null);
      try{ const j = JSON.parse(txt); throw new Error(j.error || j.response || 'Server error'); }catch(e){ throw new Error('Server error'); }
    }
    return res.json();
  }

  /* ---------- regenerate (calls same API with lastUserQuery) ---------- */
  async function regenerate(query){
    if(!query) { tinyFlash('No previous query'); return; }
    showThinking();
    try{
      const data = await chatToServer(query);
      setTimeout(()=> streamBotMessage(data.response || 'No response'), 600);
    }catch(e){
      hideThinking(); addBotMessageImmediate('Error: ' + (e.message || 'unknown'));
    }
  }

  /* ---------- main send flow ---------- */
  async function sendMessage(){
    const raw = (inputEl.value || '').trim();
    const file = imageInput?.files?.[0];
    if(!raw && !file) return;

    sendBtn.disabled = true;
    try{
      if(file){
        // handle upload preview and server analyze
        const preview = await handleImageUpload(file);
        addUserMessage(raw || 'Uploaded image', preview);
        showThinking();
        try{
          const result = await analyzeImageOnServer(file, raw);
          setTimeout(()=> streamBotMessage(result.response || 'No response'), 600);
        }catch(err){
          hideThinking();
          addBotMessageImmediate('Image analysis failed: ' + (err.message||''));
        }
        imageInput.value = '';
      } else {
        addUserMessage(raw);
        inputEl.value = '';
        showThinking();
        try{
          const data = await chatToServer(raw);
          // slight delay so shimmer is visible
          setTimeout(()=> streamBotMessage(data.response || 'No response'), 600);
        }catch(err){
          hideThinking();
          addBotMessageImmediate('Error: ' + (err.message||'Network error'));
        }
      }
    }catch(e){
      tinyFlash('Send failed: ' + (e.message || ''));
    } finally {
      sendBtn.disabled = false;
      inputEl.focus();
    }
  }

  /* ---------- copy/edit handlers already wired into createMessageElement actions ---------- */

  /* ---------- event bindings ---------- */
  if(sendBtn) sendBtn.addEventListener('click', sendMessage);
  if(voiceBtn) voiceBtn.addEventListener('click', toggleVoice);
  if(themeToggle) themeToggle.addEventListener('click', ()=>{ window.toggleAgrobotTheme(); themeToggle.animate([{transform:'scale(1)'},{transform:'scale(.96)'},{transform:'scale(1)'}],{duration:140}); });

  inputEl?.addEventListener('keydown', (e) => {
    if(e.key === 'Enter' && !e.shiftKey){ e.preventDefault(); sendMessage(); }
  });

  imageInput?.addEventListener('change', (e) => {
    if(e.target.files && e.target.files.length) sendMessage();
  });

  /* ---------- swipe-to-reply (drag) --- minimal: longpress / hold on bot message to insert to input ---------- */
  let pressTimer = null;
  messagesEl.addEventListener('pointerdown', (ev) => {
    const msg = ev.target.closest('.message.bot, .message.user');
    if(!msg) return;
    pressTimer = setTimeout(()=>{
      // on long press: copy message text to input for quick reply / edit
      const t = msg.querySelector('.message-text')?.innerText || '';
      if(t){ inputEl.value = t; inputEl.focus(); tinyFlash('Quick reply inserted'); }
    }, 520);
  });
  messagesEl.addEventListener('pointerup', ()=>{
    if(pressTimer) clearTimeout(pressTimer);
    pressTimer = null;
  });
  messagesEl.addEventListener('pointermove', ()=>{
    if(pressTimer) { clearTimeout(pressTimer); pressTimer = null; }
  });

  /* ---------- initial focus ---------- */
  inputEl?.focus();

  /* ---------- expose for debugging ---------- */
  window.agrobot = {
    streamBotMessage, showThinking, hideThinking, spawnLeaves, removeLeaves, regenerate, tinyFlash
  };
});

// ===================================
// Sidebar Dynamic Toggle Controller
// ===================================
const appShell = document.querySelector(".app-shell");
const bodyEl = document.body;
const sidebarToggle = document.querySelector(".small-toggle");

if (sidebarToggle) {
  sidebarToggle.addEventListener("click", () => {
    appShell.classList.toggle("sidebar-collapsed");
    bodyEl.classList.toggle("sidebar-hidden");
  });
}

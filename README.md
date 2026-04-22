<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>AutoStream — AI Sales Agent</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap" rel="stylesheet"/>
<style>
:root{
  --bg:#050508;
  --s1:#0c0c12;
  --s2:#111118;
  --s3:#18181f;
  --border:#ffffff0d;
  --border2:#ffffff18;
  --border3:#ffffff28;
  --accent:#3b6eff;
  --accent2:#2952d9;
  --accent-glow:rgba(59,110,255,0.18);
  --green:#00d4a0;
  --green-dim:rgba(0,212,160,0.12);
  --amber:#f5a623;
  --purple:#a78bfa;
  --red:#ff4d6d;
  --text:#f0f0f8;
  --muted:#6b6b80;
  --muted2:#9898b0;
  --ff:'DM Sans',sans-serif;
  --fh:'Syne',sans-serif;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;overflow:hidden}
body{font-family:var(--ff);background:var(--bg);color:var(--text);display:flex;flex-direction:column}

/* Ambient background */
body::before{
  content:'';position:fixed;inset:0;
  background:
    radial-gradient(ellipse 700px 500px at 10% 0%,rgba(59,110,255,0.06) 0%,transparent 70%),
    radial-gradient(ellipse 500px 400px at 90% 100%,rgba(0,212,160,0.04) 0%,transparent 70%),
    radial-gradient(ellipse 300px 300px at 50% 50%,rgba(167,139,250,0.02) 0%,transparent 70%);
  pointer-events:none;z-index:0
}

/* Grid overlay */
body::after{
  content:'';position:fixed;inset:0;
  background-image:linear-gradient(rgba(255,255,255,0.012) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.012) 1px,transparent 1px);
  background-size:48px 48px;
  pointer-events:none;z-index:0
}

/* ── Header ─────────────────────────────────────────────────────────────── */
.header{
  position:relative;z-index:10;
  display:flex;align-items:center;justify-content:space-between;
  padding:0 28px;height:58px;
  background:rgba(5,5,8,0.85);
  backdrop-filter:blur(20px);
  border-bottom:1px solid var(--border2);
}
.logo{display:flex;align-items:center;gap:12px}
.logo-mark{
  width:34px;height:34px;border-radius:10px;
  background:linear-gradient(135deg,var(--accent),#6b8fff);
  display:flex;align-items:center;justify-content:center;
  font-size:16px;
  box-shadow:0 0 20px rgba(59,110,255,0.3);
}
.logo-name{font-family:var(--fh);font-size:15px;font-weight:700;letter-spacing:-0.01em}
.logo-tag{
  font-size:10px;color:var(--muted);
  font-family:var(--ff);font-weight:300;letter-spacing:0.12em;text-transform:uppercase;
  margin-top:1px;
}
.header-right{display:flex;align-items:center;gap:10px}
.model-pill{
  display:flex;align-items:center;gap:7px;
  padding:5px 12px;border-radius:999px;
  background:var(--s2);border:1px solid var(--border2);
  font-size:11px;font-family:var(--ff);font-weight:500;color:var(--muted2);
}
.model-dot{width:6px;height:6px;background:var(--green);border-radius:50%;animation:blink 2.5s ease-in-out infinite}
@keyframes blink{0%,100%{opacity:1;box-shadow:0 0 4px var(--green)}50%{opacity:0.4;box-shadow:none}}

/* ── Layout ──────────────────────────────────────────────────────────────── */
.main{display:flex;flex:1;overflow:hidden;position:relative;z-index:1}

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
.sidebar{
  width:252px;flex-shrink:0;
  background:var(--s1);
  border-right:1px solid var(--border2);
  display:flex;flex-direction:column;
  overflow-y:auto;overflow-x:hidden;
}
.sidebar::-webkit-scrollbar{width:3px}
.sidebar::-webkit-scrollbar-thumb{background:var(--border3);border-radius:3px}

.sb-block{padding:18px 16px;border-bottom:1px solid var(--border)}
.sb-label{
  font-size:9px;font-family:var(--fh);font-weight:700;
  color:var(--muted);letter-spacing:0.15em;text-transform:uppercase;
  margin-bottom:12px;
}

/* Intent */
.intent-wrap{display:flex;align-items:center;gap:8px}
.intent-icon{font-size:18px;line-height:1}
.intent-text{font-size:12px;font-weight:500;color:var(--muted2);font-family:var(--ff)}
.intent-chip{
  display:inline-flex;align-items:center;gap:6px;
  padding:6px 12px;border-radius:8px;
  border:1px solid var(--border2);
  background:var(--s2);
  transition:all 0.35s ease;
  font-size:11px;font-weight:500;font-family:var(--ff);
  color:var(--muted2);width:100%;
}
.intent-chip.greeting{color:var(--green);border-color:rgba(0,212,160,0.25);background:rgba(0,212,160,0.06)}
.intent-chip.inquiry{color:var(--amber);border-color:rgba(245,166,35,0.25);background:rgba(245,166,35,0.06)}
.intent-chip.high{color:var(--purple);border-color:rgba(167,139,250,0.3);background:rgba(167,139,250,0.06)}

/* Lead fields */
.lead-stack{display:flex;flex-direction:column;gap:7px}
.lf{
  display:flex;align-items:center;gap:9px;
  padding:9px 11px;border-radius:10px;
  background:var(--s2);border:1px solid var(--border);
  transition:all 0.4s ease;
}
.lf.done{border-color:rgba(0,212,160,0.22);background:rgba(0,212,160,0.04)}
.lf-ico{font-size:13px;flex-shrink:0;width:18px;text-align:center}
.lf-body{flex:1;min-width:0}
.lf-key{font-size:9px;font-weight:600;color:var(--muted);letter-spacing:0.1em;text-transform:uppercase;font-family:var(--fh)}
.lf-val{font-size:12px;color:var(--muted2);margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;transition:color 0.3s}
.lf-val.set{color:var(--green)}
.lf-tick{font-size:13px;color:var(--border3);transition:all 0.3s;flex-shrink:0}
.lf-tick.done{color:var(--green)}

/* Reset btn */
.reset-btn{
  width:100%;margin-top:10px;
  padding:8px;border-radius:8px;
  background:none;border:1px solid var(--border2);
  color:var(--muted);font-size:11px;font-family:var(--ff);font-weight:500;
  cursor:pointer;transition:all 0.2s;letter-spacing:0.03em;
}
.reset-btn:hover{border-color:var(--border3);color:var(--muted2);background:var(--s2)}

/* KB items */
.kb-list{display:flex;flex-direction:column;gap:7px}
.kb-card{
  padding:10px 12px;border-radius:10px;
  background:var(--s2);border:1px solid var(--border);
}
.kb-name{font-family:var(--fh);font-size:12px;font-weight:600;color:var(--text)}
.kb-price{font-size:11px;color:var(--accent);font-weight:500;margin-top:2px}
.kb-feats{font-size:10px;color:var(--muted);margin-top:4px;line-height:1.6}
.kb-policy{font-size:10px;color:var(--muted);line-height:1.6;font-style:italic}

/* Supabase badge */
.db-badge{
  display:flex;align-items:center;gap:8px;
  padding:9px 12px;border-radius:10px;
  background:var(--s2);border:1px solid var(--border);
}
.db-dot{width:7px;height:7px;border-radius:50%;background:var(--green);flex-shrink:0;animation:blink 2.5s ease-in-out infinite}
.db-text{font-size:11px;color:var(--muted2)}
.db-text strong{color:var(--green);font-weight:600}

/* ── Chat area ────────────────────────────────────────────────────────────── */
.chat-wrap{flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0}

.messages{
  flex:1;overflow-y:auto;overflow-x:hidden;
  padding:28px 32px;
  display:flex;flex-direction:column;
  gap:20px;scroll-behavior:smooth;
}
.messages::-webkit-scrollbar{width:4px}
.messages::-webkit-scrollbar-thumb{background:var(--border3);border-radius:4px}

/* Welcome state */
.welcome{
  display:flex;flex-direction:column;align-items:center;
  justify-content:center;flex:1;text-align:center;gap:20px;
  padding:40px 20px;
  animation:fadeUp 0.6s ease forwards;
}
@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
.welcome-orb{
  width:72px;height:72px;border-radius:22px;
  background:linear-gradient(135deg,var(--accent) 0%,#7b6fff 100%);
  display:flex;align-items:center;justify-content:center;font-size:30px;
  box-shadow:0 0 0 1px rgba(59,110,255,0.3),0 0 60px rgba(59,110,255,0.2);
  animation:float 4s ease-in-out infinite;
}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
.welcome h2{font-family:var(--fh);font-size:24px;font-weight:700;letter-spacing:-0.02em}
.welcome p{font-size:14px;color:var(--muted2);max-width:380px;line-height:1.7;font-weight:300}
.chips{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:4px}
.chip{
  font-size:12px;padding:8px 16px;border-radius:999px;
  border:1px solid var(--border2);color:var(--muted2);
  cursor:pointer;transition:all 0.2s;background:var(--s2);
  font-weight:400;
}
.chip:hover{border-color:var(--accent);color:var(--text);background:rgba(59,110,255,0.1);transform:translateY(-1px)}
.chip:active{transform:translateY(0)}

/* Message rows */
.row{display:flex;gap:10px;align-items:flex-end;animation:fadeUp 0.3s ease forwards}
.row.user{flex-direction:row-reverse}

.av{
  width:30px;height:30px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:13px;flex-shrink:0;
}
.av.agent{background:var(--s2);border:1px solid var(--border2)}
.av.user{background:var(--accent);box-shadow:0 0 12px rgba(59,110,255,0.3)}

.bubble{
  max-width:70%;padding:12px 16px;
  border-radius:18px;font-size:14px;line-height:1.65;
  word-break:break-word;
}
.bubble.agent{
  background:var(--s2);border:1px solid var(--border2);
  border-bottom-left-radius:4px;color:var(--text);
}
.bubble.user{
  background:var(--accent);
  border-bottom-right-radius:4px;color:#fff;
  box-shadow:0 4px 20px rgba(59,110,255,0.25);
}
.bubble strong{font-weight:600}
.bubble table{width:100%;border-collapse:collapse;margin:10px 0;font-size:12px}
.bubble th{padding:6px 10px;background:var(--s3);border:1px solid var(--border2);text-align:left;font-weight:600;font-size:11px;color:var(--muted2);font-family:var(--fh);letter-spacing:0.04em}
.bubble td{padding:6px 10px;border:1px solid var(--border);font-size:12px}

/* Lead capture card */
.lead-card{
  max-width:340px;border-radius:16px;
  background:var(--s2);
  border:1px solid rgba(0,212,160,0.3);
  overflow:hidden;
  animation:fadeUp 0.4s ease forwards;
  box-shadow:0 0 40px rgba(0,212,160,0.06);
}
.lc-header{
  padding:14px 18px;
  background:linear-gradient(135deg,rgba(0,212,160,0.1),rgba(0,212,160,0.04));
  border-bottom:1px solid rgba(0,212,160,0.15);
  display:flex;align-items:center;gap:10px;
}
.lc-icon{
  width:30px;height:30px;border-radius:8px;
  background:rgba(0,212,160,0.15);
  display:flex;align-items:center;justify-content:center;font-size:15px;
}
.lc-title{font-family:var(--fh);font-size:13px;font-weight:700;color:var(--green)}
.lc-sub{font-size:10px;color:var(--muted);margin-top:1px;font-family:'DM Sans',sans-serif;font-style:italic}
.lc-rows{padding:12px 14px;display:flex;flex-direction:column;gap:6px}
.lc-row{
  display:flex;justify-content:space-between;align-items:center;
  padding:7px 10px;border-radius:8px;
  background:rgba(0,212,160,0.04);
  border:1px solid rgba(0,212,160,0.1);
}
.lc-key{font-size:10px;color:var(--muted);font-family:var(--fh);font-weight:600;letter-spacing:0.08em;text-transform:uppercase}
.lc-val{font-size:12px;color:var(--green);font-weight:600}

/* Typing indicator */
.typing-row{display:flex;gap:10px;align-items:flex-end}
.typing{
  padding:12px 16px;border-radius:18px;border-bottom-left-radius:4px;
  background:var(--s2);border:1px solid var(--border2);
  display:flex;align-items:center;gap:5px;
}
.typing span{
  width:5px;height:5px;border-radius:50%;
  background:var(--muted);
  animation:dots 1.3s ease-in-out infinite;
}
.typing span:nth-child(2){animation-delay:0.15s}
.typing span:nth-child(3){animation-delay:0.3s}
@keyframes dots{0%,60%,100%{transform:translateY(0);opacity:0.3}30%{transform:translateY(-5px);opacity:1}}

/* ── Input bar ───────────────────────────────────────────────────────────── */
.input-bar{
  padding:16px 24px 20px;
  border-top:1px solid var(--border);
  background:rgba(5,5,8,0.9);
  backdrop-filter:blur(16px);
  flex-shrink:0;
}
.input-inner{
  display:flex;align-items:flex-end;gap:10px;
  background:var(--s2);
  border:1px solid var(--border2);
  border-radius:14px;padding:10px 10px 10px 18px;
  transition:border-color 0.2s;
}
.input-inner:focus-within{border-color:rgba(59,110,255,0.5);box-shadow:0 0 0 3px rgba(59,110,255,0.06)}
#user-input{
  flex:1;background:none;border:none;outline:none;
  color:var(--text);font-family:var(--ff);font-size:14px;font-weight:400;
  resize:none;max-height:120px;line-height:1.55;padding:2px 0;
}
#user-input::placeholder{color:var(--muted)}
.send-btn{
  width:36px;height:36px;border-radius:10px;
  background:var(--accent);border:none;color:#fff;
  cursor:pointer;display:flex;align-items:center;justify-content:center;
  transition:all 0.2s;flex-shrink:0;font-size:15px;
  box-shadow:0 2px 12px rgba(59,110,255,0.3);
}
.send-btn:hover:not(:disabled){background:var(--accent2);transform:scale(1.06);box-shadow:0 4px 18px rgba(59,110,255,0.4)}
.send-btn:disabled{background:var(--s3);box-shadow:none;cursor:not-allowed;transform:none}
.input-hint{font-size:11px;color:var(--muted);margin-top:8px;text-align:center;letter-spacing:0.02em}
</style>
</head>
<body>

<header class="header">
  <div class="logo">
    <div class="logo-mark">🎬</div>
    <div>
      <div class="logo-name">AutoStream</div>
      <div class="logo-tag">Inflx · ServiceHive</div>
    </div>
  </div>
  <div class="header-right">
    <div class="model-pill">
      <div class="model-dot"></div>
      Groq · LLaMA 3.3 70B
    </div>
  </div>
</header>

<div class="main">

  <!-- ── Sidebar ── -->
  <aside class="sidebar">

    <div class="sb-block">
      <div class="sb-label">Detected Intent</div>
      <div class="intent-chip" id="intent-chip">
        <span id="intent-icon">·</span>
        <span id="intent-text">Awaiting input</span>
      </div>
    </div>

    <div class="sb-block">
      <div class="sb-label">Lead Progress</div>
      <div class="lead-stack">
        <div class="lf" id="lf-name">
          <div class="lf-ico">👤</div>
          <div class="lf-body">
            <div class="lf-key">Name</div>
            <div class="lf-val" id="lv-name">Not collected</div>
          </div>
          <div class="lf-tick" id="lt-name">○</div>
        </div>
        <div class="lf" id="lf-email">
          <div class="lf-ico">✉️</div>
          <div class="lf-body">
            <div class="lf-key">Email</div>
            <div class="lf-val" id="lv-email">Not collected</div>
          </div>
          <div class="lf-tick" id="lt-email">○</div>
        </div>
        <div class="lf" id="lf-platform">
          <div class="lf-ico">📱</div>
          <div class="lf-body">
            <div class="lf-key">Platform</div>
            <div class="lf-val" id="lv-platform">Not collected</div>
          </div>
          <div class="lf-tick" id="lt-platform">○</div>
        </div>
      </div>
      <button class="reset-btn" onclick="resetSession()">↺ &nbsp;New Session</button>
    </div>

    <div class="sb-block">
      <div class="sb-label">Knowledge Base</div>
      <div class="kb-list">
        <div class="kb-card">
          <div class="kb-name">Basic Plan</div>
          <div class="kb-price">$29 / month</div>
          <div class="kb-feats">10 videos · 720p · Auto-cut · Email support</div>
        </div>
        <div class="kb-card">
          <div class="kb-name">Pro Plan</div>
          <div class="kb-price">$79 / month</div>
          <div class="kb-feats">Unlimited · 4K · AI captions · 24/7 support · Auto-publish</div>
        </div>
        <div class="kb-card">
          <div class="kb-name" style="color:var(--muted2);font-size:11px">Policies</div>
          <div class="kb-policy">No refunds after 7 days · 24/7 support on Pro only · Cancel anytime</div>
        </div>
      </div>
    </div>

    <div class="sb-block">
      <div class="sb-label">Database</div>
      <div class="db-badge">
        <div class="db-dot"></div>
        <div class="db-text">Supabase <strong>connected</strong></div>
      </div>
    </div>

  </aside>

  <!-- ── Chat ── -->
  <div class="chat-wrap">
    <div class="messages" id="messages">
      <div class="welcome" id="welcome">
        <div class="welcome-orb">🤖</div>
        <h2>AutoStream Sales Agent</h2>
        <p>Ask about pricing, features, or say you're ready to sign up — I'll guide you through the full onboarding flow.</p>
        <div class="chips">
          <div class="chip" onclick="sendChip(this)">Hi there! 👋</div>
          <div class="chip" onclick="sendChip(this)">How much is the Pro plan?</div>
          <div class="chip" onclick="sendChip(this)">Does Basic include AI captions?</div>
          <div class="chip" onclick="sendChip(this)">What's the refund policy?</div>
          <div class="chip" onclick="sendChip(this)">I want to sign up for YouTube</div>
        </div>
      </div>
    </div>

    <div class="input-bar">
      <div class="input-inner">
        <textarea id="user-input" rows="1" placeholder="Ask about pricing, features, or say you're ready to sign up..."></textarea>
        <button class="send-btn" id="send-btn" onclick="sendMessage()">➤</button>
      </div>
      <div class="input-hint">Powered by LangGraph · FAISS RAG · Groq LLaMA 3.3 70B · Supabase</div>
    </div>
  </div>

</div>

<script>
// ── Session ───────────────────────────────────────────────────────────────────
let SID = localStorage.getItem('as_sid') || crypto.randomUUID();
localStorage.setItem('as_sid', SID);

// ── DOM ───────────────────────────────────────────────────────────────────────
const msgEl   = document.getElementById('messages');
const inputEl = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

inputEl.addEventListener('input', () => {
  inputEl.style.height = 'auto';
  inputEl.style.height = Math.min(inputEl.scrollHeight, 120) + 'px';
});
inputEl.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
});
function sendChip(el) { inputEl.value = el.textContent.replace('👋','').trim(); sendMessage(); }

// ── Send ──────────────────────────────────────────────────────────────────────
async function sendMessage() {
  const text = inputEl.value.trim();
  if (!text || sendBtn.disabled) return;
  hideWelcome();
  addBubble('user', text);
  inputEl.value = ''; inputEl.style.height = 'auto';
  sendBtn.disabled = true;
  const tid = showTyping();
  try {
    const res  = await fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({message: text, session_id: SID})
    });
    const data = await res.json();
    removeTyping(tid);
    if (data.leadCard) { addLeadCard(data.leadCard); await sleep(150); }
    addBubble('agent', data.text || data.error || '...');
    updateSidebar(data);
  } catch(e) {
    removeTyping(tid);
    addBubble('agent', '⚠️ Could not reach the server. Is `python server.py` running?');
  }
  sendBtn.disabled = false;
  inputEl.focus();
}

// ── Sidebar ───────────────────────────────────────────────────────────────────
function updateSidebar(d) {
  const chip = document.getElementById('intent-chip');
  const icon = document.getElementById('intent-icon');
  const text = document.getElementById('intent-text');
  const map = {
    greeting:        ['👋','greeting','greeting'],
    product_inquiry: ['🔍','product inquiry','inquiry'],
    high_intent:     ['🔥','high intent','high'],
  };
  if (d.intent && map[d.intent]) {
    const [ic, tx, cls] = map[d.intent];
    chip.className = 'intent-chip ' + cls;
    icon.textContent = ic; text.textContent = tx;
  }
  if (d.name)     setField('name', d.name);
  if (d.email)    setField('email', d.email);
  if (d.platform) setField('platform', d.platform);
}

function setField(key, val) {
  document.getElementById('lf-'+key).classList.add('done');
  const v = document.getElementById('lv-'+key);
  v.textContent = val; v.classList.add('set');
  const t = document.getElementById('lt-'+key);
  t.textContent = '✓'; t.classList.add('done');
}

// ── Reset ─────────────────────────────────────────────────────────────────────
async function resetSession() {
  try { await fetch('/session/'+SID, {method:'DELETE'}); } catch(_) {}
  SID = crypto.randomUUID();
  localStorage.setItem('as_sid', SID);
  msgEl.innerHTML = '';
  showWelcome();
  ['name','email','platform'].forEach(k => {
    document.getElementById('lf-'+k).classList.remove('done');
    const v = document.getElementById('lv-'+k); v.textContent = 'Not collected'; v.classList.remove('set');
    const t = document.getElementById('lt-'+k); t.textContent = '○'; t.classList.remove('done');
  });
  const chip = document.getElementById('intent-chip');
  chip.className = 'intent-chip';
  document.getElementById('intent-icon').textContent = '·';
  document.getElementById('intent-text').textContent = 'Awaiting input';
  inputEl.focus();
}

// ── UI helpers ────────────────────────────────────────────────────────────────
function hideWelcome() { const w=document.getElementById('welcome'); if(w) w.remove(); }
function showWelcome() {
  const w = document.createElement('div');
  w.className='welcome'; w.id='welcome';
  w.innerHTML=`
    <div class="welcome-orb">🤖</div>
    <h2>AutoStream Sales Agent</h2>
    <p>Ask about pricing, features, or say you're ready to sign up — I'll guide you through the full onboarding flow.</p>
    <div class="chips">
      <div class="chip" onclick="sendChip(this)">Hi there! 👋</div>
      <div class="chip" onclick="sendChip(this)">How much is the Pro plan?</div>
      <div class="chip" onclick="sendChip(this)">Does Basic include AI captions?</div>
      <div class="chip" onclick="sendChip(this)">What's the refund policy?</div>
      <div class="chip" onclick="sendChip(this)">I want to sign up for YouTube</div>
    </div>`;
  msgEl.appendChild(w);
}

function addBubble(role, text) {
  const row = document.createElement('div');
  row.className = 'row' + (role==='user' ? ' user' : '');
  const av = document.createElement('div');
  av.className = 'av ' + (role==='user' ? 'user' : 'agent');
  av.textContent = role==='user' ? '👤' : '🤖';
  const bub = document.createElement('div');
  bub.className = 'bubble ' + role;
  bub.innerHTML = fmt(text);
  row.appendChild(av); row.appendChild(bub);
  msgEl.appendChild(row); scroll();
}

function addLeadCard(d) {
  const c = document.createElement('div');
  c.className = 'lead-card';
  c.innerHTML = `
    <div class="lc-header">
      <div class="lc-icon">✅</div>
      <div>
        <div class="lc-title">Lead Captured Successfully</div>
        <div class="lc-sub">mock_lead_capture() fired · saved to Supabase</div>
      </div>
    </div>
    <div class="lc-rows">
      <div class="lc-row"><span class="lc-key">name</span><span class="lc-val">${d.name}</span></div>
      <div class="lc-row"><span class="lc-key">email</span><span class="lc-val">${d.email}</span></div>
      <div class="lc-row"><span class="lc-key">platform</span><span class="lc-val">${d.platform}</span></div>
    </div>`;
  msgEl.appendChild(c); scroll();
}

function showTyping() {
  const id = 'typ-'+Date.now();
  const row = document.createElement('div');
  row.className='typing-row'; row.id=id;
  row.innerHTML='<div class="av agent">🤖</div><div class="typing"><span></span><span></span><span></span></div>';
  msgEl.appendChild(row); scroll(); return id;
}
function removeTyping(id) { document.getElementById(id)?.remove(); }
function scroll() { msgEl.scrollTop = msgEl.scrollHeight; }
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function fmt(t) {
  return t
    .replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>')
    .replace(/\n\|(.+)\|\n\|[-| :]+\|\n((?:\|.+\|\n?)+)/g,(_,h,rows)=>{
      const ths = h.split('|').filter(Boolean).map(c=>`<th>${c.trim()}</th>`).join('');
      const trs = rows.trim().split('\n').map(r=>{
        const tds = r.split('|').filter(Boolean).map(c=>`<td>${c.trim()}</td>`).join('');
        return `<tr>${tds}</tr>`;
      }).join('');
      return `<table><thead><tr>${ths}</tr></thead><tbody>${trs}</tbody></table>`;
    })
    .replace(/\n/g,'<br>');
}
</script>
</body>
</html>
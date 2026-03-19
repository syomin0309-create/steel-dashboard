"""
AegisCore — UI Theme Module  v2.0  Light Edition
Crisp Intelligence aesthetic — clean, professional, readable
"""
import streamlit as st

AEGIS_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=JetBrains+Mono:wght@300;400;500;600&display=swap');

:root {
  --bg-base:       #f0f4f8;
  --bg-panel:      #ffffff;
  --bg-card:       #ffffff;
  --bg-card-hover: #f8fafc;
  --bg-input:      #f8fafc;
  --border:        rgba(99,102,241,0.15);
  --border-soft:   #e2e8f0;
  --border-focus:  rgba(99,102,241,0.5);
  --indigo:        #6366f1;
  --indigo-dim:    rgba(99,102,241,0.08);
  --indigo-mid:    rgba(99,102,241,0.15);
  --indigo-glow:   rgba(99,102,241,0.2);
  --gold:          #d97706;
  --gold-dim:      rgba(217,119,6,0.08);
  --cyan:          #0891b2;
  --green:         #059669;
  --green-dim:     rgba(5,150,105,0.08);
  --red:           #dc2626;
  --red-dim:       rgba(220,38,38,0.08);
  --amber:         #d97706;
  --text-primary:  #0f172a;
  --text-secondary:#475569;
  --text-dim:      #94a3b8;
  --radius-sm:     8px;
  --radius-md:     12px;
  --radius-lg:     18px;
  --shadow-sm:     0 1px 3px rgba(15,23,42,0.06),0 1px 2px rgba(15,23,42,0.04);
  --shadow-card:   0 4px 16px rgba(15,23,42,0.08),0 1px 4px rgba(15,23,42,0.04);
  --shadow-hover:  0 8px 32px rgba(15,23,42,0.12),0 2px 8px rgba(15,23,42,0.06);
  --shadow-glow:   0 0 24px rgba(99,102,241,0.2);
}

html, body { background-color: var(--bg-base) !important; }

.stApp {
  background-color: var(--bg-base) !important;
  background-image:
    radial-gradient(ellipse 90% 50% at 10% -10%, rgba(99,102,241,0.06) 0%, transparent 55%),
    radial-gradient(ellipse 70% 40% at 90% 110%, rgba(217,119,6,0.04) 0%, transparent 50%);
  background-attachment: fixed;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 15px !important;
  color: var(--text-primary) !important;
}

.main .block-container {
  max-width: 1400px !important;
  padding: 2rem 2.5rem !important;
  animation: page_fadein 0.45s ease both !important;
}

@keyframes page_fadein {
  from { opacity:0; transform:translateY(12px); }
  to   { opacity:1; transform:translateY(0); }
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
  background: var(--bg-panel) !important;
  border-right: 1px solid var(--border-soft) !important;
  box-shadow: 4px 0 24px rgba(15,23,42,0.06) !important;
}
section[data-testid="stSidebar"]::before {
  content:''; position:absolute; top:0; left:0; right:0; height:3px;
  background: linear-gradient(90deg, var(--indigo), var(--gold), var(--cyan));
}
section[data-testid="stSidebar"] h1 {
  font-family:'Syne',sans-serif !important;
  font-size:1rem !important; font-weight:700 !important;
  letter-spacing:1.5px !important; text-transform:uppercase !important;
  color:var(--text-primary) !important; -webkit-text-fill-color:var(--text-primary) !important;
  border-bottom:1px solid var(--border-soft) !important;
  padding-bottom:8px !important; margin-bottom:14px !important;
}
section[data-testid="stSidebar"] h2 {
  font-family:'JetBrains Mono',monospace !important;
  font-size:0.68rem !important; letter-spacing:2px !important;
  text-transform:uppercase !important;
  color:var(--text-secondary) !important; -webkit-text-fill-color:var(--text-secondary) !important;
  font-weight:500 !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] .stMarkdown p {
  color:var(--text-secondary) !important; font-size:0.88rem !important;
}
section[data-testid="stSidebar"] hr { border-color:var(--border-soft) !important; }

/* TYPOGRAPHY */
p, li, .stMarkdown p {
  font-family:'DM Sans',sans-serif !important;
  font-size:0.95rem !important; color:var(--text-secondary) !important; line-height:1.7 !important;
}
.stMarkdown h1 {
  font-family:'Syne',sans-serif !important; font-size:2.2rem !important; font-weight:800 !important;
  color:var(--text-primary) !important; -webkit-text-fill-color:var(--text-primary) !important;
  background:none !important; letter-spacing:-0.5px !important;
}
.stMarkdown h2 {
  font-family:'Syne',sans-serif !important; font-size:1.4rem !important; font-weight:700 !important;
  color:var(--text-primary) !important; -webkit-text-fill-color:var(--text-primary) !important;
}
.stMarkdown h3 {
  font-family:'JetBrains Mono',monospace !important; font-size:0.7rem !important;
  font-weight:600 !important; text-transform:uppercase !important; letter-spacing:2.5px !important;
  color:var(--indigo) !important; -webkit-text-fill-color:var(--indigo) !important;
  background:none !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
  background:var(--bg-panel) !important; border:1.5px solid var(--border-soft) !important;
  border-radius:100px !important; padding:4px !important; gap:2px !important;
  width:fit-content !important; box-shadow:var(--shadow-sm) !important;
}
.stTabs [data-baseweb="tab"] {
  background:transparent !important; border-radius:100px !important; border:none !important;
  color:var(--text-secondary) !important; font-family:'DM Sans',sans-serif !important;
  font-weight:500 !important; font-size:0.9rem !important; padding:9px 22px !important;
  transition:all 0.2s ease !important;
}
.stTabs [data-baseweb="tab"]:hover {
  background:var(--indigo-dim) !important; color:var(--indigo) !important;
}
.stTabs [aria-selected="true"] {
  background:linear-gradient(135deg,var(--indigo) 0%,#818cf8 100%) !important;
  color:#fff !important; font-weight:600 !important;
  box-shadow:0 2px 12px rgba(99,102,241,0.35) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display:none !important; }

/* INPUTS */
[data-testid="stNumberInput"] label,
[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label {
  font-family:'JetBrains Mono',monospace !important; font-size:0.65rem !important;
  letter-spacing:2px !important; color:var(--text-secondary) !important;
  text-transform:uppercase !important; font-weight:500 !important; margin-bottom:4px !important;
}
[data-testid="stNumberInput"] > div {
  background:var(--bg-input) !important; border:1.5px solid var(--border-soft) !important;
  border-radius:var(--radius-sm) !important;
}
[data-testid="stNumberInput"]:focus-within > div {
  border-color:var(--indigo) !important; box-shadow:0 0 0 3px var(--indigo-glow) !important;
}
[data-testid="stNumberInput"] button { color:var(--text-secondary) !important; background:transparent !important; border:none !important; }
[data-testid="stNumberInput"] button:hover { color:var(--indigo) !important; background:var(--indigo-dim) !important; }
input[type="text"], input[type="number"], textarea {
  background:var(--bg-input) !important; border:1.5px solid var(--border-soft) !important;
  border-radius:var(--radius-sm) !important; color:var(--text-primary) !important;
  font-family:'JetBrains Mono',monospace !important; font-size:0.9rem !important;
}
input:focus, textarea:focus { border-color:var(--indigo) !important; box-shadow:0 0 0 3px var(--indigo-glow) !important; }

/* SELECT */
[data-baseweb="select"] > div:first-child {
  background:var(--bg-input) !important; border:1.5px solid var(--border-soft) !important;
  border-radius:var(--radius-sm) !important; color:var(--text-primary) !important;
  font-family:'DM Sans',sans-serif !important; font-size:0.9rem !important;
}
[data-baseweb="select"]:focus-within > div:first-child {
  border-color:var(--indigo) !important; box-shadow:0 0 0 3px var(--indigo-glow) !important;
}
[data-baseweb="menu"] {
  background:var(--bg-panel) !important; border:1px solid var(--border-soft) !important;
  border-radius:var(--radius-md) !important; box-shadow:var(--shadow-hover) !important;
}
[data-baseweb="option"] {
  background:transparent !important; color:var(--text-secondary) !important;
  font-family:'DM Sans',sans-serif !important; font-size:0.9rem !important;
}
[data-baseweb="option"]:hover { background:var(--indigo-dim) !important; color:var(--indigo) !important; }
[aria-selected="true"][data-baseweb="option"] { background:var(--indigo-mid) !important; color:var(--indigo) !important; }

/* BUTTONS */
.stButton > button {
  background:linear-gradient(135deg,var(--indigo) 0%,#818cf8 100%) !important;
  border:none !important; border-radius:var(--radius-sm) !important;
  color:#fff !important; font-family:'DM Sans',sans-serif !important;
  font-weight:600 !important; font-size:0.9rem !important;
  padding:10px 24px !important; transition:all 0.25s ease !important;
  box-shadow:0 2px 12px rgba(99,102,241,0.3) !important;
}
.stButton > button:hover { transform:translateY(-2px) !important; box-shadow:0 6px 20px rgba(99,102,241,0.4) !important; }
.stDownloadButton > button {
  background:var(--bg-panel) !important; border:1.5px solid var(--border-soft) !important;
  border-radius:var(--radius-sm) !important; color:var(--text-secondary) !important;
  font-family:'DM Sans',sans-serif !important; font-size:0.9rem !important;
  box-shadow:var(--shadow-sm) !important;
}
.stDownloadButton > button:hover {
  border-color:var(--indigo) !important; color:var(--indigo) !important;
  background:var(--indigo-dim) !important; transform:translateY(-1px) !important;
}

/* FILE UPLOADER */
[data-testid="stFileUploadDropzone"] {
  background:var(--bg-panel) !important; border:2px dashed var(--border-soft) !important;
  border-radius:var(--radius-md) !important; transition:all 0.25s ease !important;
  box-shadow:var(--shadow-sm) !important;
}
[data-testid="stFileUploadDropzone"]:hover {
  border-color:var(--indigo) !important; background:var(--indigo-dim) !important;
  box-shadow:var(--shadow-glow) !important;
}
[data-testid="stFileUploadDropzone"] p { color:var(--text-secondary) !important; font-size:0.9rem !important; }

/* MULTISELECT */
[data-baseweb="tag"] {
  background:var(--indigo-dim) !important; border:1px solid var(--indigo-mid) !important;
  border-radius:6px !important; color:var(--indigo) !important;
  font-family:'DM Sans',sans-serif !important; font-size:0.82rem !important;
}

/* TOGGLE */
[data-testid="stToggle"] > label > div { background:#e2e8f0 !important; border:1px solid #cbd5e1 !important; }
[data-testid="stToggle"] > label > div[aria-checked="true"] {
  background:var(--indigo) !important; border-color:var(--indigo) !important;
  box-shadow:0 0 8px rgba(99,102,241,0.3) !important;
}
[data-baseweb="radio"] [data-checked="true"] div { background:var(--indigo) !important; border-color:var(--indigo) !important; }

/* ALERTS */
.stSuccess {
  background:var(--green-dim) !important; border:1px solid rgba(5,150,105,0.25) !important;
  border-radius:var(--radius-sm) !important; color:var(--green) !important; font-size:0.9rem !important;
}
.stWarning {
  background:rgba(217,119,6,0.06) !important; border:1px solid rgba(217,119,6,0.25) !important;
  border-radius:var(--radius-sm) !important; color:var(--amber) !important; font-size:0.9rem !important;
}
[data-testid="stAlert"] { border-radius:var(--radius-sm) !important; font-family:'DM Sans',sans-serif !important; font-size:0.9rem !important; }

/* DATAFRAME */
[data-testid="stDataFrame"] > div {
  background:var(--bg-panel) !important; border:1px solid var(--border-soft) !important;
  border-radius:var(--radius-md) !important; box-shadow:var(--shadow-sm) !important;
}
.stDataFrame th {
  background:#f8fafc !important; color:var(--text-secondary) !important;
  font-family:'JetBrains Mono',monospace !important; font-size:0.72rem !important;
  letter-spacing:1.5px !important; text-transform:uppercase !important;
  border-bottom:1px solid var(--border-soft) !important;
}
.stDataFrame td {
  color:var(--text-primary) !important; font-family:'JetBrains Mono',monospace !important;
  font-size:0.85rem !important; border-bottom:1px solid #f1f5f9 !important;
}

/* EXPANDER */
[data-testid="stExpander"] {
  background:var(--bg-panel) !important; border:1px solid var(--border-soft) !important;
  border-radius:var(--radius-md) !important; box-shadow:var(--shadow-sm) !important;
}
[data-testid="stExpander"] summary {
  color:var(--text-secondary) !important; font-family:'DM Sans',sans-serif !important;
  font-weight:500 !important; font-size:0.9rem !important; padding:12px 16px !important;
}
[data-testid="stExpander"] summary:hover { color:var(--indigo) !important; background:var(--indigo-dim) !important; }

/* CAPTION */
.stCaption, [data-testid="stCaptionContainer"] p {
  color:var(--text-dim) !important; font-family:'JetBrains Mono',monospace !important;
  font-size:0.75rem !important; letter-spacing:0.5px !important;
}

/* SCROLLBAR */
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:var(--bg-base); }
::-webkit-scrollbar-thumb { background:#cbd5e1; border-radius:3px; }
::-webkit-scrollbar-thumb:hover { background:var(--indigo); }

/* HR */
hr { border:none !important; height:1px !important; background:var(--border-soft) !important; margin:16px 0 !important; }

/* PLOTLY */
[data-testid="stPlotlyChart"] {
  background:var(--bg-panel) !important; border:1px solid var(--border-soft) !important;
  border-radius:var(--radius-md) !important; overflow:hidden !important;
  box-shadow:var(--shadow-card) !important; transition:box-shadow 0.3s,transform 0.2s !important;
}
[data-testid="stPlotlyChart"]:hover { box-shadow:var(--shadow-hover) !important; transform:translateY(-1px) !important; }

/* metric-highlight */
.metric-highlight {
  background:var(--bg-panel) !important; border:1px solid var(--border-soft) !important;
  border-radius:var(--radius-md) !important; border-left:3px solid var(--indigo) !important;
  padding:16px !important; box-shadow:var(--shadow-sm) !important; transition:all 0.2s !important;
}
.metric-highlight:hover { box-shadow:var(--shadow-card) !important; transform:translateY(-1px) !important; }
.metric-highlight strong, .metric-highlight small {
  font-family:'DM Sans',sans-serif !important; color:var(--text-secondary) !important; font-size:0.9rem !important;
}
.metric-highlight h2 {
  font-family:'Syne',sans-serif !important; color:var(--text-primary) !important;
  -webkit-text-fill-color:var(--text-primary) !important; font-weight:700 !important;
  font-size:1.8rem !important; background:none !important; margin:4px 0 2px !important;
}

/* SPC COMPONENTS */
.spc-sec {
  font-family:'JetBrains Mono',monospace !important; font-size:0.62rem !important;
  letter-spacing:3px !important; color:var(--indigo) !important; text-transform:uppercase !important;
  display:flex !important; align-items:center !important; gap:10px !important;
  margin:22px 0 14px 0 !important; font-weight:600 !important;
}
.spc-sec::after { content:'' !important; flex:1 !important; height:1px !important; background:linear-gradient(90deg,var(--indigo-mid),transparent) !important; }

.spc-card {
  background:var(--bg-panel) !important; border:1px solid var(--border-soft) !important;
  border-radius:var(--radius-md) !important; padding:18px 20px !important;
  position:relative !important; overflow:hidden !important;
  box-shadow:var(--shadow-card) !important; transition:all 0.25s !important;
}
.spc-card:hover { box-shadow:var(--shadow-hover) !important; transform:translateY(-2px) !important; }
.spc-card::before {
  content:'' !important; position:absolute !important; top:0;left:0;right:0 !important;
  height:2px !important; background:var(--ct,var(--indigo)) !important; opacity:0.7 !important;
}
.spc-lbl { font-family:'JetBrains Mono',monospace !important; font-size:0.6rem !important; letter-spacing:2px !important; color:var(--text-secondary) !important; text-transform:uppercase !important; margin-bottom:4px !important; }
.spc-val { font-family:'Syne',sans-serif !important; font-size:2.1rem !important; font-weight:700 !important; line-height:1.1 !important; margin:4px 0 2px 0 !important; }
.spc-badge { font-family:'JetBrains Mono',monospace !important; font-size:0.7rem !important; font-weight:700 !important; padding:3px 10px !important; border-radius:6px !important; border:1.5px solid currentColor !important; letter-spacing:1px !important; }
.spc-hdr { display:flex !important; align-items:center !important; justify-content:space-between !important; margin-bottom:2px !important; }
.spc-sub { font-family:'DM Sans',sans-serif !important; font-size:0.78rem !important; color:var(--text-secondary) !important; margin-bottom:8px !important; }
.spc-gauge { height:3px !important; background:#e2e8f0 !important; border-radius:2px !important; overflow:hidden !important; margin-top:8px !important; }
.spc-fill { height:100% !important; border-radius:2px !important; transition:width 0.8s cubic-bezier(0.4,0,0.2,1) !important; }
.spc-statsbar {
  background:var(--bg-panel) !important; border:1px solid var(--border-soft) !important;
  border-radius:var(--radius-md) !important; display:grid !important;
  grid-template-columns:repeat(6,1fr) !important; overflow:hidden !important;
  box-shadow:var(--shadow-sm) !important;
}
.spc-cell { padding:14px 10px !important; text-align:center !important; border-right:1px solid var(--border-soft) !important; transition:background 0.2s !important; }
.spc-cell:hover { background:#f8fafc !important; }
.spc-cell:last-child { border-right:none !important; }
.diag-item { padding:12px 16px !important; border-radius:var(--radius-sm) !important; border-left:3px solid !important; margin-bottom:8px !important; background:#f8fafc !important; display:flex !important; align-items:flex-start !important; gap:10px !important; transition:background 0.2s !important; }
.diag-item:hover { background:#f1f5f9 !important; }
.diag-text { font-family:'DM Sans',sans-serif !important; font-size:0.88rem !important; line-height:1.6 !important; color:var(--text-primary) !important; }

/* MARQUEE */
.marquee-container { width:100%; overflow:hidden; padding:8px 0 20px; display:flex; flex-direction:column; gap:16px; mask-image:linear-gradient(90deg,transparent 0%,black 8%,black 92%,transparent 100%); -webkit-mask-image:linear-gradient(90deg,transparent 0%,black 8%,black 92%,transparent 100%); }
.marquee-track { display:flex; width:max-content; animation:marquee_scroll 38s linear infinite; }
.marquee-track.reverse { animation-direction:reverse; }
.marquee-track:hover { animation-play-state:paused; }
@keyframes marquee_scroll { 0%{transform:translateX(0)} 100%{transform:translateX(-50%)} }

.glass-card { width:300px; min-width:300px; margin-right:16px; padding:18px 20px; background:var(--bg-panel) !important; border:1px solid var(--border-soft) !important; border-radius:var(--radius-md) !important; color:var(--text-secondary) !important; font-family:'DM Sans',sans-serif !important; font-size:0.88rem !important; line-height:1.55 !important; box-shadow:var(--shadow-card) !important; transition:all 0.3s ease !important; position:relative; overflow:hidden; }
.glass-card::before { content:'"'; position:absolute; top:8px; left:14px; font-size:3rem; font-family:'Syne',sans-serif; color:var(--indigo); opacity:0.07; line-height:1; }
.glass-card:hover { transform:translateY(-4px) !important; box-shadow:var(--shadow-hover) !important; border-color:rgba(99,102,241,0.25) !important; color:var(--text-primary) !important; }
.card-user { color:var(--indigo) !important; font-weight:600 !important; margin-top:10px !important; font-size:0.8rem !important; }

</style>
"""

# ── Landing page (shown before file upload) ────────────────────
LANDING_HTML = """
<style>
.ap-wordmark { font-family:'Syne',sans-serif; font-size:clamp(3.5rem,8vw,5.5rem); font-weight:800; letter-spacing:-4px; line-height:1; background:linear-gradient(135deg,#0f172a 0%,#6366f1 45%,#d97706 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; background-size:200% auto; animation:word_shimmer 5s ease-in-out infinite alternate; margin-bottom:12px; text-align:center; }
@keyframes word_shimmer { 0%{background-position:0% 50%} 100%{background-position:100% 50%} }
.ap-tagline { font-family:'JetBrains Mono',monospace; font-size:0.72rem; letter-spacing:5px; color:#94a3b8; text-transform:uppercase; margin-bottom:36px; text-align:center; }
.ap-hero { text-align:center; padding:44px 20px 28px; }

.ap-stats { display:flex; justify-content:center; gap:0; margin:0 auto 44px; max-width:660px; background:#fff; border:1px solid #e2e8f0; border-radius:16px; overflow:hidden; box-shadow:0 4px 16px rgba(15,23,42,0.07); }
.ap-stat { flex:1; padding:20px 14px; text-align:center; border-right:1px solid #e2e8f0; transition:background 0.2s; }
.ap-stat:last-child { border-right:none; }
.ap-stat:hover { background:#f8fafc; }
.ap-stat-num { font-family:'Syne',sans-serif; font-size:1.7rem; font-weight:800; color:#6366f1; line-height:1; margin-bottom:4px; }
.ap-stat-lbl { font-family:'JetBrains Mono',monospace; font-size:0.58rem; letter-spacing:1.5px; color:#94a3b8; text-transform:uppercase; }

.ap-features { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; max-width:880px; margin:0 auto 44px; }
.ap-feat { background:#fff; border:1px solid #e2e8f0; border-radius:14px; padding:22px 18px; position:relative; overflow:hidden; transition:all 0.3s ease; box-shadow:0 2px 8px rgba(15,23,42,0.05); animation:feat_fadein 0.6s ease both; }
.ap-feat:nth-child(1){animation-delay:0.1s}.ap-feat:nth-child(2){animation-delay:0.2s}.ap-feat:nth-child(3){animation-delay:0.3s}.ap-feat:nth-child(4){animation-delay:0.4s}.ap-feat:nth-child(5){animation-delay:0.5s}.ap-feat:nth-child(6){animation-delay:0.6s}
@keyframes feat_fadein { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
.ap-feat::before { content:''; position:absolute; top:0;left:0;right:0; height:2px; background:var(--fc,#6366f1); transform:scaleX(0); transform-origin:left; transition:transform 0.35s ease; }
.ap-feat:hover::before { transform:scaleX(1); }
.ap-feat:hover { transform:translateY(-4px); box-shadow:0 12px 32px rgba(15,23,42,0.1); border-color:rgba(99,102,241,0.2); }
.ap-feat-icon { width:40px; height:40px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.2rem; margin-bottom:12px; background:var(--fb,rgba(99,102,241,0.08)); }
.ap-feat-title { font-family:'Syne',sans-serif; font-size:0.95rem; font-weight:700; color:#0f172a; margin-bottom:6px; }
.ap-feat-desc { font-family:'DM Sans',sans-serif; font-size:0.82rem; color:#64748b; line-height:1.55; margin:0; }

/* Seamless Integration */
.ap-integration { max-width:860px; margin:0 auto 44px; background:#fff; border:1px solid #e2e8f0; border-radius:20px; padding:28px 24px; box-shadow:0 4px 16px rgba(15,23,42,0.07); position:relative; overflow:hidden; animation:feat_fadein 0.7s ease 0.3s both; }
.ap-integration::after { content:''; position:absolute; top:-80px; right:-80px; width:220px; height:220px; border-radius:50%; background:radial-gradient(circle,rgba(99,102,241,0.07) 0%,transparent 70%); }
.ap-int-header { display:flex; align-items:center; gap:12px; margin-bottom:22px; }
.ap-int-badge { font-family:'JetBrains Mono',monospace; font-size:0.6rem; letter-spacing:2px; text-transform:uppercase; color:#6366f1; background:rgba(99,102,241,0.07); border:1px solid rgba(99,102,241,0.18); border-radius:100px; padding:3px 12px; white-space:nowrap; }
.ap-int-title { font-family:'Syne',sans-serif; font-size:1.15rem; font-weight:700; color:#0f172a; margin:0; }
.ap-nodes { display:flex; align-items:center; justify-content:center; gap:0; }
.ap-node { display:flex; flex-direction:column; align-items:center; gap:8px; flex:1; min-width:80px; position:relative; animation:node_rise 0.5s ease both; }
.ap-node:nth-child(1){animation-delay:0.5s}.ap-node:nth-child(2){animation-delay:0.65s}.ap-node:nth-child(3){animation-delay:0.8s}.ap-node:nth-child(4){animation-delay:0.95s}.ap-node:nth-child(5){animation-delay:1.1s}.ap-node:nth-child(6){animation-delay:1.25s}
@keyframes node_rise { from{opacity:0;transform:scale(0.7)} to{opacity:1;transform:scale(1)} }
.ap-node:not(:last-child)::after { content:''; position:absolute; top:21px; left:calc(50% + 22px); width:calc(100% - 44px); height:1px; background:linear-gradient(90deg,#e2e8f0,#c7d2fe,#e2e8f0); animation:line_pulse 2.2s ease-in-out infinite; }
@keyframes line_pulse { 0%,100%{opacity:0.4} 50%{opacity:1} }
.ap-node-icon { width:42px; height:42px; border-radius:12px; background:#f8fafc; border:1.5px solid #e2e8f0; display:flex; align-items:center; justify-content:center; font-size:1.2rem; transition:all 0.3s ease; position:relative; z-index:1; }
.ap-node:hover .ap-node-icon { border-color:#6366f1; background:rgba(99,102,241,0.06); transform:translateY(-3px); box-shadow:0 6px 16px rgba(99,102,241,0.15); }
.ap-node-lbl { font-family:'JetBrains Mono',monospace; font-size:0.58rem; letter-spacing:1px; color:#94a3b8; text-transform:uppercase; text-align:center; }

/* Real-time Collab row */
.ap-live { max-width:860px; margin:0 auto 12px; display:grid; grid-template-columns:1fr 1fr; gap:14px; animation:feat_fadein 0.7s ease 0.5s both; }
.ap-live-card { background:#fff; border:1px solid #e2e8f0; border-radius:14px; padding:22px 20px; box-shadow:0 2px 8px rgba(15,23,42,0.05); position:relative; overflow:hidden; transition:all 0.3s; }
.ap-live-card:hover { border-color:rgba(99,102,241,0.2); box-shadow:0 8px 24px rgba(15,23,42,0.1); transform:translateY(-2px); }
.ap-live-header { display:flex; align-items:center; gap:10px; margin-bottom:16px; }
.ap-pulse { width:8px; height:8px; border-radius:50%; background:#10b981; animation:pulse_green 2s ease-in-out infinite; flex-shrink:0; }
@keyframes pulse_green { 0%{box-shadow:0 0 0 0 rgba(16,185,129,0.4)} 60%{box-shadow:0 0 0 8px rgba(16,185,129,0)} 100%{box-shadow:0 0 0 0 rgba(16,185,129,0)} }
.ap-live-title { font-family:'Syne',sans-serif; font-size:0.92rem; font-weight:700; color:#0f172a; }
.ap-metric-row { display:flex; gap:10px; }
.ap-mini-metric { flex:1; background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:12px 8px; text-align:center; transition:all 0.2s; }
.ap-mini-metric:hover { border-color:rgba(99,102,241,0.25); background:rgba(99,102,241,0.04); }
.ap-mini-num { font-family:'Syne',sans-serif; font-size:1.35rem; font-weight:800; color:#6366f1; line-height:1; margin-bottom:3px; }
.ap-mini-lbl { font-family:'JetBrains Mono',monospace; font-size:0.55rem; letter-spacing:1.5px; color:#94a3b8; text-transform:uppercase; }
.ap-steps { display:flex; flex-direction:column; gap:9px; }
.ap-step { display:flex; align-items:center; gap:12px; padding:10px 12px; background:#f8fafc; border-radius:10px; border:1px solid #e2e8f0; transition:all 0.2s; }
.ap-step:hover { background:rgba(99,102,241,0.04); border-color:rgba(99,102,241,0.2); }
.ap-step-num { width:26px; height:26px; background:linear-gradient(135deg,#6366f1,#818cf8); border-radius:8px; display:flex; align-items:center; justify-content:center; font-family:'Syne',sans-serif; font-size:0.78rem; font-weight:700; color:white; flex-shrink:0; }
.ap-step-text { font-family:'DM Sans',sans-serif; font-size:0.86rem; color:#475569; }
</style>

<div class="ap-hero">
  <div class="ap-wordmark">AegisCore</div>
  <div class="ap-tagline">Unifying Steel Data · Empowering Decisions</div>

  <div class="ap-stats">
    <div class="ap-stat"><div class="ap-stat-num">Ca</div><div class="ap-stat-lbl">準確度分析</div></div>
    <div class="ap-stat"><div class="ap-stat-num">Cp</div><div class="ap-stat-lbl">精密度分析</div></div>
    <div class="ap-stat"><div class="ap-stat-num">Cpk</div><div class="ap-stat-lbl">製程能力指標</div></div>
    <div class="ap-stat"><div class="ap-stat-num" style="font-size:1.3rem">A+~D</div><div class="ap-stat-lbl">五級評鑑系統</div></div>
  </div>

  <div class="ap-features">
    <div class="ap-feat" style="--fc:#6366f1"><div class="ap-feat-icon" style="--fb:rgba(99,102,241,0.08)">📊</div><div class="ap-feat-title">智能 SPC 分析</div><p class="ap-feat-desc">自動計算 Ca / Cp / Cpk，五級 A+～D 評鑑，附製程診斷建議。</p></div>
    <div class="ap-feat" style="--fc:#0891b2"><div class="ap-feat-icon" style="--fb:rgba(8,145,178,0.08)">📈</div><div class="ap-feat-title">趨勢異常監控</div><p class="ap-feat-desc">生產順序管制圖，7B 異常鋼捲自動標記，跨月箱型圖對比。</p></div>
    <div class="ap-feat" style="--fc:#d97706"><div class="ap-feat-icon" style="--fb:rgba(217,119,6,0.08)">🔍</div><div class="ap-feat-title">瀑布流篩選器</div><p class="ap-feat-desc">年月 × 厚度 × 寬度 × 材質 × 規格，六層條件即時連動。</p></div>
    <div class="ap-feat" style="--fc:#059669"><div class="ap-feat-icon" style="--fb:rgba(5,150,105,0.08)">🏭</div><div class="ap-feat-title">鍍鋅產線專屬</div><p class="ap-feat-desc">自動識別鍍層欄位，雙面總鍍層量 AVG，對應鋼捲規格分類。</p></div>
    <div class="ap-feat" style="--fc:#7c3aed"><div class="ap-feat-icon" style="--fb:rgba(124,58,237,0.08)">📋</div><div class="ap-feat-title">製程診斷報告</div><p class="ap-feat-desc">自動判斷偏移根因，提供 Offset 調整方向，清楚說明問題所在。</p></div>
    <div class="ap-feat" style="--fc:#dc2626"><div class="ap-feat-icon" style="--fb:rgba(220,38,38,0.08)">⬇️</div><div class="ap-feat-title">一鍵匯出 CSV</div><p class="ap-feat-desc">篩選數據集直接下載，UTF-8 編碼支援繁體中文不亂碼。</p></div>
  </div>

  <div class="ap-integration">
    <div class="ap-int-header">
      <span class="ap-int-badge">Seamless Workflow</span>
      <span class="ap-int-title">三步驟完成分析，零學習成本</span>
    </div>
    <div class="ap-nodes">
      <div class="ap-node"><div class="ap-node-icon">📁</div><div class="ap-node-lbl">上傳 Excel</div></div>
      <div class="ap-node"><div class="ap-node-icon">⚙️</div><div class="ap-node-lbl">自動解析</div></div>
      <div class="ap-node"><div class="ap-node-icon">🎛️</div><div class="ap-node-lbl">條件篩選</div></div>
      <div class="ap-node"><div class="ap-node-icon">📐</div><div class="ap-node-lbl">輸入規格</div></div>
      <div class="ap-node"><div class="ap-node-icon">🔬</div><div class="ap-node-lbl">SPC 運算</div></div>
      <div class="ap-node"><div class="ap-node-icon">✅</div><div class="ap-node-lbl">報告輸出</div></div>
    </div>
  </div>

  <div class="ap-live">
    <div class="ap-live-card">
      <div class="ap-live-header">
        <div class="ap-pulse"></div>
        <span class="ap-live-title">即時製程能力評鑑標準</span>
      </div>
      <div class="ap-metric-row">
        <div class="ap-mini-metric"><div class="ap-mini-num">≥1.67</div><div class="ap-mini-lbl">A+ 極佳</div></div>
        <div class="ap-mini-metric"><div class="ap-mini-num">≥1.33</div><div class="ap-mini-lbl">A 良好</div></div>
        <div class="ap-mini-metric"><div class="ap-mini-num">≥1.00</div><div class="ap-mini-lbl">B 尚可</div></div>
      </div>
    </div>
    <div class="ap-live-card">
      <div class="ap-live-header">
        <div class="ap-pulse" style="background:#6366f1;animation-name:pulse_indigo"></div>
        <style>@keyframes pulse_indigo{0%{box-shadow:0 0 0 0 rgba(99,102,241,0.4)}60%{box-shadow:0 0 0 8px rgba(99,102,241,0)}100%{box-shadow:0 0 0 0 rgba(99,102,241,0)}}</style>
        <span class="ap-live-title">上傳後立即開始分析</span>
      </div>
      <div class="ap-steps">
        <div class="ap-step"><div class="ap-step-num">1</div><div class="ap-step-text">左側拖曳或點擊上傳 XLSX / CSV</div></div>
        <div class="ap-step"><div class="ap-step-num">2</div><div class="ap-step-text">左側篩選器選擇年月、厚度、規格</div></div>
        <div class="ap-step"><div class="ap-step-num">3</div><div class="ap-step-text">切換「製程能力分析」分頁查看結果</div></div>
      </div>
    </div>
  </div>
</div>
"""


def inject_theme():
    """Call once at top of app.py after set_page_config"""
    st.markdown(AEGIS_CSS, unsafe_allow_html=True)


def render_landing():
    """Call to render the landing page (before file upload)"""
    st.markdown(LANDING_HTML, unsafe_allow_html=True)

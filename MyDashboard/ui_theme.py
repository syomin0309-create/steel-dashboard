"""
AegisCore — UI Theme Module
Obsidian Intelligence aesthetic
Import this at the top of app.py and call inject_theme()
"""

import streamlit as st

AEGIS_CSS = """
<style>
/* ═══════════════════════════════════════════════════════
   FONTS
═══════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=JetBrains+Mono:wght@300;400;500;600&display=swap');

/* ═══════════════════════════════════════════════════════
   DESIGN TOKENS
═══════════════════════════════════════════════════════ */
:root {
  --bg-base:       #080b11;
  --bg-panel:      #0d1117;
  --bg-card:       #111720;
  --bg-card-hover: #151d28;
  --bg-input:      #0a0e16;

  --border:        rgba(99,102,241,0.12);
  --border-focus:  rgba(99,102,241,0.45);
  --border-gold:   rgba(232,184,75,0.25);

  --indigo:        #6366f1;
  --indigo-dim:    rgba(99,102,241,0.15);
  --indigo-glow:   rgba(99,102,241,0.3);
  --gold:          #e8b84b;
  --gold-dim:      rgba(232,184,75,0.12);
  --cyan:          #22d3ee;
  --cyan-dim:      rgba(34,211,238,0.12);
  --green:         #4ade80;
  --red:           #f87171;
  --amber:         #fbbf24;

  --text-primary:  #e2e8f0;
  --text-secondary:#64748b;
  --text-dim:      #2d3748;
  --text-gold:     #e8b84b;

  --radius-sm:     6px;
  --radius-md:     10px;
  --radius-lg:     16px;

  --shadow-card:   0 4px 24px rgba(0,0,0,0.4), 0 1px 4px rgba(0,0,0,0.3);
  --shadow-glow:   0 0 20px rgba(99,102,241,0.15);
}

/* ═══════════════════════════════════════════════════════
   BASE — APP BACKGROUND (Gradient Mesh + Grain)
═══════════════════════════════════════════════════════ */
html, body { background-color: var(--bg-base) !important; }

.stApp {
  background-color: var(--bg-base) !important;
  background-image:
    radial-gradient(ellipse 80% 50% at 20% 0%, rgba(99,102,241,0.07) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 100%, rgba(232,184,75,0.05) 0%, transparent 55%),
    radial-gradient(ellipse 40% 60% at 50% 50%, rgba(34,211,238,0.03) 0%, transparent 70%),
    url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.025'/%3E%3C/svg%3E");
  background-attachment: fixed;
  font-family: 'DM Sans', sans-serif !important;
}

/* ═══════════════════════════════════════════════════════
   SIDEBAR — Premium glass panel
═══════════════════════════════════════════════════════ */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0d1117 0%, #090d14 100%) !important;
  border-right: 1px solid var(--border) !important;
  box-shadow: 4px 0 24px rgba(0,0,0,0.4) !important;
  position: relative !important;
}

section[data-testid="stSidebar"]::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--indigo), var(--gold), var(--cyan));
  opacity: 0.7;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
  font-family: 'Syne', sans-serif !important;
  color: var(--text-primary) !important;
  letter-spacing: 0.5px !important;
}

section[data-testid="stSidebar"] .stMarkdown p {
  color: var(--text-secondary) !important;
  font-size: 0.82rem !important;
}

/* Sidebar divider */
section[data-testid="stSidebar"] hr {
  border-color: var(--border) !important;
  margin: 12px 0 !important;
}

/* ═══════════════════════════════════════════════════════
   TYPOGRAPHY
═══════════════════════════════════════════════════════ */
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
h1, h2, h3 {
  font-family: 'Syne', sans-serif !important;
  letter-spacing: -0.3px !important;
  color: var(--text-primary) !important;
}

/* Gradient on main H1/H2 */
.stMarkdown h1 {
  background: linear-gradient(135deg, var(--text-primary) 0%, var(--gold) 100%);
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  background-clip: text !important;
  font-weight: 800 !important;
  font-size: 2rem !important;
  letter-spacing: -1px !important;
}

.stMarkdown h2 {
  font-size: 1.3rem !important;
  font-weight: 700 !important;
  color: var(--text-primary) !important;
}

.stMarkdown h3 {
  font-size: 1rem !important;
  font-weight: 600 !important;
  color: var(--text-secondary) !important;
  text-transform: uppercase !important;
  letter-spacing: 2px !important;
  font-family: 'JetBrains Mono', monospace !important;
}

p, .stMarkdown p, label, .stMarkdown li {
  font-family: 'DM Sans', sans-serif !important;
  color: var(--text-secondary) !important;
  line-height: 1.65 !important;
}

/* ═══════════════════════════════════════════════════════
   TABS — Premium pill navigation
═══════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 100px !important;
  padding: 4px !important;
  gap: 2px !important;
  width: fit-content !important;
  box-shadow: var(--shadow-card) !important;
}

.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: 100px !important;
  border: none !important;
  color: var(--text-secondary) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
  font-size: 0.85rem !important;
  padding: 8px 20px !important;
  transition: all 0.25s ease !important;
  white-space: nowrap !important;
}

.stTabs [data-baseweb="tab"]:hover {
  background: var(--indigo-dim) !important;
  color: var(--text-primary) !important;
}

.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, var(--indigo) 0%, #818cf8 100%) !important;
  color: #fff !important;
  font-weight: 600 !important;
  box-shadow: 0 2px 12px rgba(99,102,241,0.4) !important;
}

/* Remove the bottom bar indicator */
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"]    { display: none !important; }

/* ═══════════════════════════════════════════════════════
   INPUTS — Refined dark fields
═══════════════════════════════════════════════════════ */
input[type="text"],
input[type="number"],
textarea,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
  background: var(--bg-input) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-primary) !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.85rem !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}

input:focus, textarea:focus,
[data-baseweb="input"]:focus-within,
[data-baseweb="textarea"]:focus-within {
  border-color: var(--border-focus) !important;
  box-shadow: 0 0 0 3px var(--indigo-glow) !important;
}

/* Number input wrapper */
[data-testid="stNumberInput"] > div {
  background: var(--bg-input) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
}

[data-testid="stNumberInput"]:focus-within > div {
  border-color: var(--border-focus) !important;
  box-shadow: 0 0 0 3px var(--indigo-glow) !important;
}

/* Number input +/- buttons */
[data-testid="stNumberInput"] button {
  color: var(--text-secondary) !important;
  background: transparent !important;
  border: none !important;
}

[data-testid="stNumberInput"] button:hover {
  color: var(--indigo) !important;
  background: var(--indigo-dim) !important;
}

/* Labels */
[data-testid="stNumberInput"] label,
[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.62rem !important;
  letter-spacing: 2px !important;
  color: var(--text-secondary) !important;
  text-transform: uppercase !important;
  font-weight: 500 !important;
}

/* ═══════════════════════════════════════════════════════
   SELECT / DROPDOWN
═══════════════════════════════════════════════════════ */
[data-baseweb="select"] > div:first-child {
  background: var(--bg-input) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-primary) !important;
  font-family: 'DM Sans', sans-serif !important;
}

[data-baseweb="select"]:focus-within > div:first-child {
  border-color: var(--border-focus) !important;
  box-shadow: 0 0 0 3px var(--indigo-glow) !important;
}

[data-baseweb="menu"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  box-shadow: var(--shadow-card) !important;
}

[data-baseweb="option"] {
  background: transparent !important;
  color: var(--text-secondary) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.85rem !important;
  transition: all 0.15s !important;
}

[data-baseweb="option"]:hover {
  background: var(--indigo-dim) !important;
  color: var(--text-primary) !important;
}

[aria-selected="true"][data-baseweb="option"] {
  background: var(--indigo-dim) !important;
  color: var(--indigo) !important;
}

/* ═══════════════════════════════════════════════════════
   BUTTONS
═══════════════════════════════════════════════════════ */
.stButton > button {
  background: linear-gradient(135deg, var(--indigo) 0%, #818cf8 100%) !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  color: #fff !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.85rem !important;
  letter-spacing: 0.5px !important;
  padding: 10px 24px !important;
  transition: all 0.25s ease !important;
  box-shadow: 0 2px 12px rgba(99,102,241,0.3) !important;
  position: relative !important;
  overflow: hidden !important;
}

.stButton > button::before {
  content: '';
  position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
  transition: left 0.4s ease;
}

.stButton > button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 20px rgba(99,102,241,0.5) !important;
}

.stButton > button:hover::before { left: 100%; }

.stButton > button:active { transform: translateY(0) !important; }

/* Download button variant */
.stDownloadButton > button {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-secondary) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
}

.stDownloadButton > button:hover {
  border-color: var(--indigo) !important;
  color: var(--indigo) !important;
  background: var(--indigo-dim) !important;
  transform: translateY(-1px) !important;
}

/* ═══════════════════════════════════════════════════════
   FILE UPLOADER
═══════════════════════════════════════════════════════ */
[data-testid="stFileUploadDropzone"] {
  background: var(--bg-card) !important;
  border: 1.5px dashed var(--border) !important;
  border-radius: var(--radius-md) !important;
  transition: all 0.25s ease !important;
}

[data-testid="stFileUploadDropzone"]:hover {
  border-color: var(--indigo) !important;
  background: var(--indigo-dim) !important;
  box-shadow: var(--shadow-glow) !important;
}

[data-testid="stFileUploadDropzone"] p {
  color: var(--text-secondary) !important;
  font-family: 'DM Sans', sans-serif !important;
}

/* ═══════════════════════════════════════════════════════
   MULTISELECT
═══════════════════════════════════════════════════════ */
[data-baseweb="tag"] {
  background: var(--indigo-dim) !important;
  border: 1px solid var(--border-focus) !important;
  border-radius: 4px !important;
  color: var(--indigo) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.78rem !important;
}

/* ═══════════════════════════════════════════════════════
   TOGGLE / RADIO / CHECKBOX
═══════════════════════════════════════════════════════ */
[data-baseweb="radio"] [data-checked="true"] div {
  background: var(--indigo) !important;
  border-color: var(--indigo) !important;
}

[data-testid="stToggle"] > label > div {
  background: var(--bg-input) !important;
  border: 1px solid var(--border) !important;
}

[data-testid="stToggle"] > label > div[aria-checked="true"] {
  background: var(--indigo) !important;
  border-color: var(--indigo) !important;
  box-shadow: 0 0 8px rgba(99,102,241,0.4) !important;
}

/* ═══════════════════════════════════════════════════════
   ALERTS & MESSAGES
═══════════════════════════════════════════════════════ */
[data-testid="stAlert"] {
  border-radius: var(--radius-md) !important;
  border: 1px solid !important;
  background: transparent !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.85rem !important;
}

[data-testid="stAlert"][data-type="info"] {
  background: rgba(34,211,238,0.05) !important;
  border-color: rgba(34,211,238,0.2) !important;
  color: var(--cyan) !important;
}

[data-testid="stAlert"][data-type="success"] {
  background: rgba(74,222,128,0.05) !important;
  border-color: rgba(74,222,128,0.2) !important;
  color: var(--green) !important;
}

[data-testid="stAlert"][data-type="warning"] {
  background: rgba(251,191,36,0.05) !important;
  border-color: rgba(251,191,36,0.2) !important;
  color: var(--amber) !important;
}

[data-testid="stAlert"][data-type="error"] {
  background: rgba(248,113,113,0.05) !important;
  border-color: rgba(248,113,113,0.2) !important;
  color: var(--red) !important;
}

/* st.success / st.warning / st.error  */
.stSuccess {
  background: rgba(74,222,128,0.05) !important;
  border: 1px solid rgba(74,222,128,0.25) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--green) !important;
}

.stWarning {
  background: rgba(251,191,36,0.05) !important;
  border: 1px solid rgba(251,191,36,0.25) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--amber) !important;
}

/* ═══════════════════════════════════════════════════════
   DATAFRAME / TABLE
═══════════════════════════════════════════════════════ */
[data-testid="stDataFrame"] > div {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  overflow: hidden !important;
}

.stDataFrame th {
  background: var(--bg-input) !important;
  color: var(--text-secondary) !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.7rem !important;
  letter-spacing: 1px !important;
  text-transform: uppercase !important;
  border-bottom: 1px solid var(--border) !important;
}

.stDataFrame td {
  color: var(--text-primary) !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.8rem !important;
  border-bottom: 1px solid rgba(99,102,241,0.06) !important;
}

/* ═══════════════════════════════════════════════════════
   EXPANDER
═══════════════════════════════════════════════════════ */
[data-testid="stExpander"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  overflow: hidden !important;
  transition: border-color 0.2s !important;
}

[data-testid="stExpander"]:hover {
  border-color: rgba(99,102,241,0.3) !important;
}

[data-testid="stExpander"] summary {
  color: var(--text-secondary) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
  font-size: 0.85rem !important;
  padding: 12px 16px !important;
  background: var(--bg-card) !important;
}

[data-testid="stExpander"] summary:hover {
  color: var(--text-primary) !important;
  background: var(--bg-card-hover) !important;
}

/* ═══════════════════════════════════════════════════════
   CAPTION
═══════════════════════════════════════════════════════ */
.stCaption, [data-testid="stCaptionContainer"] p {
  color: var(--text-dim) !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.5px !important;
}

/* ═══════════════════════════════════════════════════════
   SCROLLBAR
═══════════════════════════════════════════════════════ */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 3px;
  transition: background 0.2s;
}
::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.4); }

/* ═══════════════════════════════════════════════════════
   HORIZONTAL DIVIDER
═══════════════════════════════════════════════════════ */
hr {
  border: none !important;
  height: 1px !important;
  background: linear-gradient(90deg, transparent, var(--border), transparent) !important;
  margin: 16px 0 !important;
}

/* ═══════════════════════════════════════════════════════
   HERO SECTION (landing page)
═══════════════════════════════════════════════════════ */
.hero-title {
  font-family: 'Syne', sans-serif !important;
  font-size: 5rem !important;
  font-weight: 800 !important;
  letter-spacing: -4px !important;
  text-align: center !important;
  background: linear-gradient(135deg,
    #e2e8f0 0%,
    var(--gold) 35%,
    var(--indigo) 65%,
    #c7d2fe 100%
  ) !important;
  background-size: 300% auto !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  background-clip: text !important;
  animation: aegis_shimmer 6s linear infinite !important;
  line-height: 1 !important;
  padding-bottom: 8px !important;
}

@keyframes aegis_shimmer {
  0%   { background-position: 0% 50%; }
  100% { background-position: 300% 50%; }
}

.hero-subtitle {
  font-family: 'JetBrains Mono', monospace !important;
  text-align: center !important;
  color: var(--text-secondary) !important;
  font-size: 0.75rem !important;
  letter-spacing: 5px !important;
  margin-bottom: 24px !important;
  opacity: 0.7 !important;
}

/* ═══════════════════════════════════════════════════════
   GLASS CARD (marquee)
═══════════════════════════════════════════════════════ */
.glass-card {
  background: rgba(17,23,32,0.6) !important;
  backdrop-filter: blur(12px) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  color: var(--text-secondary) !important;
  transition: all 0.3s ease !important;
}

.glass-card:hover {
  transform: translateY(-3px) !important;
  border-color: rgba(99,102,241,0.3) !important;
  box-shadow: 0 8px 24px rgba(0,0,0,0.3), var(--shadow-glow) !important;
  color: var(--text-primary) !important;
}

.card-user { color: var(--indigo) !important; }

/* ═══════════════════════════════════════════════════════
   SPC SECTION TITLES (from Tab 2)
═══════════════════════════════════════════════════════ */
.spc-sec {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.6rem !important;
  letter-spacing: 3px !important;
  color: var(--text-secondary) !important;
  text-transform: uppercase !important;
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
  margin: 20px 0 12px 0 !important;
}

.spc-sec::after {
  content: '' !important;
  flex: 1 !important;
  height: 1px !important;
  background: linear-gradient(90deg, rgba(99,102,241,0.2), transparent) !important;
}

/* SPC Metric Cards */
.spc-card {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  padding: 16px 18px !important;
  position: relative !important;
  overflow: hidden !important;
  transition: border-color 0.3s, box-shadow 0.3s, transform 0.2s !important;
  box-shadow: var(--shadow-card) !important;
}

.spc-card:hover {
  border-color: rgba(99,102,241,0.25) !important;
  box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 16px rgba(99,102,241,0.08) !important;
  transform: translateY(-1px) !important;
}

.spc-card::before {
  content: '' !important;
  position: absolute !important;
  top: 0; left: 0; right: 0 !important;
  height: 1.5px !important;
  background: var(--ct, rgba(99,102,241,0.4)) !important;
}

.spc-lbl {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.58rem !important;
  letter-spacing: 2px !important;
  color: var(--text-secondary) !important;
  text-transform: uppercase !important;
  margin-bottom: 4px !important;
}

.spc-val {
  font-family: 'Syne', sans-serif !important;
  font-size: 2rem !important;
  font-weight: 700 !important;
  line-height: 1.1 !important;
  margin: 4px 0 2px 0 !important;
  letter-spacing: -0.5px !important;
}

.spc-badge {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.68rem !important;
  font-weight: 700 !important;
  padding: 2px 8px !important;
  border-radius: 4px !important;
  border: 1px solid currentColor !important;
  letter-spacing: 1px !important;
}

.spc-sub {
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.72rem !important;
  color: var(--text-secondary) !important;
  margin-bottom: 8px !important;
}

.spc-hdr {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  margin-bottom: 2px !important;
}

.spc-gauge {
  height: 2px !important;
  background: rgba(255,255,255,0.06) !important;
  border-radius: 2px !important;
  overflow: hidden !important;
  margin-top: 8px !important;
}

.spc-fill {
  height: 100% !important;
  border-radius: 2px !important;
  transition: width 0.8s cubic-bezier(0.4,0,0.2,1) !important;
}

/* Stats Bar */
.spc-statsbar {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  display: grid !important;
  grid-template-columns: repeat(6,1fr) !important;
  overflow: hidden !important;
  box-shadow: var(--shadow-card) !important;
}

.spc-cell {
  padding: 12px 10px !important;
  text-align: center !important;
  border-right: 1px solid var(--border) !important;
  transition: background 0.2s !important;
}

.spc-cell:hover { background: var(--bg-card-hover) !important; }
.spc-cell:last-child { border-right: none !important; }

/* Diagnosis items */
.diag-item {
  padding: 10px 14px !important;
  border-radius: var(--radius-sm) !important;
  border-left: 2.5px solid !important;
  margin-bottom: 8px !important;
  background: rgba(0,0,0,0.2) !important;
  display: flex !important;
  align-items: flex-start !important;
  gap: 10px !important;
  transition: background 0.2s !important;
}

.diag-item:hover { background: rgba(0,0,0,0.3) !important; }

.diag-text {
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.8rem !important;
  line-height: 1.6 !important;
  color: var(--text-primary) !important;
}

/* metric-highlight (Tab1 legacy) */
.metric-highlight {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  border-left: 3px solid var(--indigo) !important;
  padding: 16px !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
  box-shadow: var(--shadow-card) !important;
}

.metric-highlight:hover {
  border-left-color: var(--gold) !important;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
}

.metric-highlight strong, .metric-highlight small {
  font-family: 'DM Sans', sans-serif !important;
  color: var(--text-secondary) !important;
}

.metric-highlight h2 {
  font-family: 'Syne', sans-serif !important;
  color: var(--text-primary) !important;
  -webkit-text-fill-color: var(--text-primary) !important;
  font-weight: 700 !important;
  margin: 4px 0 2px !important;
}

/* ═══════════════════════════════════════════════════════
   PAGE FADE-IN ANIMATION
═══════════════════════════════════════════════════════ */
.main .block-container {
  animation: page_fadein 0.5s ease both !important;
}

@keyframes page_fadein {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Stagger children */
.main .block-container > *:nth-child(1) { animation-delay: 0.05s !important; }
.main .block-container > *:nth-child(2) { animation-delay: 0.10s !important; }
.main .block-container > *:nth-child(3) { animation-delay: 0.15s !important; }
.main .block-container > *:nth-child(4) { animation-delay: 0.20s !important; }
.main .block-container > *:nth-child(5) { animation-delay: 0.25s !important; }

/* ═══════════════════════════════════════════════════════
   PLOTLY CHART CONTAINERS
═══════════════════════════════════════════════════════ */
[data-testid="stPlotlyChart"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  overflow: hidden !important;
  box-shadow: var(--shadow-card) !important;
  transition: box-shadow 0.3s !important;
}

[data-testid="stPlotlyChart"]:hover {
  box-shadow: 0 8px 32px rgba(0,0,0,0.5), 0 0 20px rgba(99,102,241,0.08) !important;
}

/* ═══════════════════════════════════════════════════════
   SIDEBAR HEADER SPECIAL TREATMENT
═══════════════════════════════════════════════════════ */
section[data-testid="stSidebar"] h1 {
  font-family: 'Syne', sans-serif !important;
  font-size: 1rem !important;
  font-weight: 700 !important;
  letter-spacing: 1px !important;
  text-transform: uppercase !important;
  color: var(--text-primary) !important;
  -webkit-text-fill-color: var(--text-primary) !important;
  padding-bottom: 4px !important;
  border-bottom: 1px solid var(--border) !important;
  margin-bottom: 12px !important;
}

/* Subheader in sidebar */
section[data-testid="stSidebar"] h2 {
  font-size: 0.7rem !important;
  letter-spacing: 2px !important;
  color: var(--text-secondary) !important;
  -webkit-text-fill-color: var(--text-secondary) !important;
  text-transform: uppercase !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-weight: 500 !important;
}

/* ═══════════════════════════════════════════════════════
   LOTTIE CONTAINER
═══════════════════════════════════════════════════════ */
[data-testid="column"] iframe {
  border-radius: var(--radius-lg) !important;
}


/* ═══════════════════════════════════════════════════════
   MARQUEE CARD CAROUSEL
═══════════════════════════════════════════════════════ */
.marquee-container {
  width: 100%;
  overflow: hidden;
  padding: 16px 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
  mask-image: linear-gradient(90deg, transparent 0%, black 8%, black 92%, transparent 100%);
  -webkit-mask-image: linear-gradient(90deg, transparent 0%, black 8%, black 92%, transparent 100%);
}

.marquee-track {
  display: flex;
  width: max-content;
  animation: marquee_scroll 35s linear infinite;
}

.marquee-track.reverse {
  animation-direction: reverse;
}

.marquee-track:hover {
  animation-play-state: paused;
}

@keyframes marquee_scroll {
  0%   { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

.glass-card {
  width: 300px;
  min-width: 300px;
  margin-right: 18px;
  padding: 18px 20px;
  background: linear-gradient(135deg, rgba(17,23,32,0.8) 0%, rgba(13,17,27,0.6) 100%) !important;
  backdrop-filter: blur(16px) !important;
  border: 1px solid rgba(99,102,241,0.1) !important;
  border-radius: 12px !important;
  color: var(--text-secondary) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.82rem !important;
  line-height: 1.55 !important;
  transition: all 0.3s ease !important;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
  position: relative;
  overflow: hidden;
}

.glass-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(99,102,241,0.3), transparent);
}

.glass-card:hover {
  transform: translateY(-4px) !important;
  border-color: rgba(99,102,241,0.3) !important;
  box-shadow: 0 12px 32px rgba(0,0,0,0.4), 0 0 20px rgba(99,102,241,0.1) !important;
  color: var(--text-primary) !important;
  background: linear-gradient(135deg, rgba(17,23,32,0.95) 0%, rgba(13,17,27,0.8) 100%) !important;
}

.card-user {
  color: var(--indigo) !important;
  font-weight: 600 !important;
  margin-top: 12px !important;
  font-size: 0.75rem !important;
  letter-spacing: 0.5px !important;
}

</style>
"""

def inject_theme():
    """Call this once at the top of app.py after set_page_config"""
    st.markdown(AEGIS_CSS, unsafe_allow_html=True)

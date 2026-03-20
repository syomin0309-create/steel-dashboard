import streamlit as st

# ══════════════════════════════════════════════════════
#  AegisCore Theme — 奶茶色系
#  背景 #F5EDE3 · 主色 #876D5A · 文字 #2C1F14
# ══════════════════════════════════════════════════════

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600;700&display=swap');

/* ── CSS 變數（奶茶色系）───────────────────────────── */
:root {
    --bg-page:      #F5EDE3;
    --bg-card:      #FDFAF6;
    --bg-strip:     #EFE3D5;
    --border:       #DABEA7;
    --border-dark:  #A98B73;
    --primary:      #876D5A;
    --primary-dark: #6B5445;
    --primary-light:#CDA581;
    --accent:       #9D7553;
    --text-main:    #2C1F14;
    --text-sub:     #5C4033;
    --text-hint:    #876D5A;
    --red:          #9A3B2E;
    --green:        #3D6B4A;
    --yellow:       #8A6200;
    --blue:         #2B5084;
}

/* ── 全域 ────────────────────────────────────────── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="block-container"] {
    background-color: var(--bg-page) !important;
    color: var(--text-main) !important;
    font-family: 'Google Sans', 'Microsoft JhengHei', 'Noto Sans TC', sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
    font-size: 15px !important;
}

/* ── 側邊欄 ─────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: var(--bg-card) !important;
    border-right: 1.5px solid var(--border) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-main) !important;
    font-size: 14px !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--primary) !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: var(--text-main) !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}

/* ── 標題 ────────────────────────────────────────── */
h1 { color: var(--text-main) !important; font-weight: 700 !important; font-size: 26px !important; }
h2 { color: var(--text-main) !important; font-weight: 700 !important; font-size: 22px !important; }
h3 { color: var(--text-main) !important; font-weight: 600 !important; font-size: 18px !important; }
p, li, div, span { color: var(--text-main) !important; font-size: 15px !important; }

[data-testid="stCaptionContainer"] p,
[data-testid="stCaptionContainer"] span {
    color: var(--text-sub) !important;
    font-size: 13px !important;
}

/* ── 指標卡片 ─────────────────────────────────────*/
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    box-shadow: 0 1px 4px rgba(135,109,90,0.10) !important;
}
[data-testid="metric-container"] label {
    color: var(--text-sub) !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--text-main) !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] span {
    font-size: 13px !important;
}

/* ── 分頁 Tab ────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1.5px solid var(--border) !important;
}
[data-testid="stTabs"] button {
    color: var(--text-sub) !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 12px 24px !important;
    border-radius: 0 !important;
    background: transparent !important;
}
[data-testid="stTabs"] button:hover {
    color: var(--primary) !important;
    background: var(--bg-strip) !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--primary) !important;
    font-weight: 700 !important;
    border-bottom: 2.5px solid var(--primary) !important;
    background: transparent !important;
}
[data-testid="stTabs"] button p { color: inherit !important; font-size: inherit !important; }

/* ── 下拉選單 ────────────────────────────────────── */
div[data-baseweb="select"] > div {
    border: 1.5px solid var(--border-dark) !important;
    border-radius: 8px !important;
    background-color: var(--bg-card) !important;
    font-size: 15px !important;
}
div[data-baseweb="select"] > div:hover { border-color: var(--primary) !important; }
div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color: var(--text-main) !important;
    background-color: var(--bg-card) !important;
    font-size: 15px !important;
}
div[data-baseweb="popover"] {
    background-color: var(--bg-card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 20px rgba(135,109,90,0.18) !important;
}
div[data-baseweb="popover"] li {
    color: var(--text-main) !important;
    font-size: 15px !important;
}
div[data-baseweb="popover"] li:hover {
    background-color: var(--bg-strip) !important;
}
[data-baseweb="tag"] {
    background-color: var(--bg-strip) !important;
    border: 1px solid var(--border-dark) !important;
}
[data-baseweb="tag"] span { color: var(--text-main) !important; font-size: 13px !important; }

/* ── 輸入框 ─────────────────────────────────────── */
input[type="number"], input[type="text"], textarea {
    background-color: var(--bg-card) !important;
    color: var(--text-main) !important;
    border: 1.5px solid var(--border-dark) !important;
    border-radius: 8px !important;
    font-size: 15px !important;
}
input:focus, textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px rgba(135,109,90,0.18) !important;
}
[data-testid="stNumberInput"] label p,
[data-testid="stSelectbox"] label p,
[data-testid="stMultiSelect"] label p,
[data-testid="stToggle"] label p,
[data-testid="stCheckbox"] label p {
    color: var(--text-main) !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

/* ── 버튼 ────────────────────────────────────────── */
[data-testid="stDownloadButton"] button,
[data-testid="stButton"] button {
    background-color: var(--primary) !important;
    color: #FDFAF6 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 9px 22px !important;
}
[data-testid="stDownloadButton"] button:hover,
[data-testid="stButton"] button:hover {
    background-color: var(--primary-dark) !important;
}
[data-testid="stDownloadButton"] button p,
[data-testid="stButton"] button p { color: #FDFAF6 !important; }

[data-testid="stButton"] button[kind="secondary"] {
    background-color: var(--bg-card) !important;
    color: var(--primary) !important;
    border: 1.5px solid var(--primary) !important;
}
[data-testid="stButton"] button[kind="secondary"] p { color: var(--primary) !important; }

/* ── 訊息框 ──────────────────────────────────────── */
[data-testid="stAlert"] { border-radius: 10px !important; font-size: 14px !important; }
[data-testid="stAlert"] p { font-size: 14px !important; color: inherit !important; }

/* ── File Uploader ───────────────────────────────── */
[data-testid="stFileUploader"],
[data-testid="stFileUploader"] > div,
[data-testid="stFileUploader"] section {
    background: #FDFAF6 !important;
    background-color: #FDFAF6 !important;
    border: 2px dashed #A98B73 !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"]:hover { border-color: #876D5A !important; }
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] label {
    color: #5C4033 !important;
    font-size: 14px !important;
}
[data-testid="stFileUploader"] button {
    background-color: #876D5A !important;
    color: #FDFAF6 !important;
    border: none !important;
    border-radius: 6px !important;
}

/* ── Expander ────────────────────────────────────── */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary {
    color: var(--text-main) !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}
[data-testid="stExpander"] summary p {
    color: var(--text-main) !important;
    font-size: 15px !important;
}

/* ── Dataframe ───────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] th {
    background-color: var(--bg-strip) !important;
    color: var(--text-main) !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}
[data-testid="stDataFrame"] td {
    color: var(--text-main) !important;
    font-size: 14px !important;
}

/* ── 分隔線 ──────────────────────────────────────── */
hr { border-color: var(--border) !important; margin: 20px 0 !important; }

/* ── 自訂元件 ────────────────────────────────────── */
.spec-banner {
    background: linear-gradient(135deg, #876D5A, #9D7553) !important;
    color: #FDFAF6 !important;
    border-radius: 12px !important;
    padding: 18px 28px !important;
    margin-bottom: 20px !important;
    font-size: 15px !important;
    line-height: 2 !important;
    box-shadow: 0 4px 14px rgba(135,109,90,0.25) !important;
}
.spec-banner b  { color: #FDFAF6 !important; font-weight: 700 !important; }
.spec-banner span { color: #FDFAF6 !important; }

.section-title {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: var(--text-main) !important;
    border-left: 4px solid var(--primary) !important;
    padding-left: 12px !important;
    margin: 24px 0 12px 0 !important;
}

.signal-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.signal-table th {
    background: var(--primary);
    color: #FDFAF6;
    padding: 11px 14px;
    text-align: center;
    font-weight: 600;
    font-size: 14px;
}
.signal-table td {
    padding: 10px 14px;
    text-align: center;
    border-bottom: 1px solid var(--border);
    color: var(--text-main);
    background: var(--bg-card);
    font-size: 14px;
}
.signal-table tr:nth-child(even) td { background-color: var(--bg-strip); }
.sig-green  { color: #3D6B4A; font-weight: 700; }
.sig-yellow { color: #7A5500; font-weight: 700; }
.sig-red    { color: #9A3B2E; font-weight: 700; }
.sig-gray   { color: #876D5A; }


/* ── Expander 深色修正 ────────────────────────────── */
[data-testid="stExpander"] {
    background: #FDFAF6 !important;
    background-color: #FDFAF6 !important;
    border: 1.5px solid #DABEA7 !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] > div,
[data-testid="stExpander"] div[data-testid="stExpanderDetails"],
[data-testid="stExpander"] div[role="group"] {
    background: #FDFAF6 !important;
    background-color: #FDFAF6 !important;
}
[data-testid="stExpander"] summary {
    background: #EFE3D5 !important;
    background-color: #EFE3D5 !important;
    color: #2C1F14 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
}
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span {
    color: #2C1F14 !important;
    font-size: 14px !important;
}
[data-testid="stExpander"] summary svg {
    fill: #876D5A !important;
    color: #876D5A !important;
}

/* ── Dataframe 深色修正 ──────────────────────────── */
[data-testid="stDataFrame"],
[data-testid="stDataFrame"] > div,
[data-testid="stDataFrame"] iframe {
    background: #FDFAF6 !important;
    background-color: #FDFAF6 !important;
    border: 1.5px solid #DABEA7 !important;
    border-radius: 10px !important;
}
/* glide-data-grid 覆蓋 */
.dvn-scroller,
.dvn-underlay,
[class*="dvn"],
[class*="glide"] {
    background: #FDFAF6 !important;
    background-color: #FDFAF6 !important;
    color: #2C1F14 !important;
}

/* ── 所有 div/section 強制奶茶底色覆蓋 ─────────────── */
/* Plotly 圖表容器 */
.js-plotly-plot .plotly,
.js-plotly-plot .plotly .main-svg,
.js-plotly-plot .plotly .bg {
    fill: #FDFAF6 !important;
    background: #FDFAF6 !important;
}

/* ── SPC 診斷卡內部背景 ──────────────────────────── */
.diag-item {
    background: #EFE3D5 !important;
    border-radius: 0 6px 6px 0 !important;
}
.diag-text { color: #2C1F14 !important; }

/* ── SPC 統計摘要列 ──────────────────────────────── */
.spc-statsbar {
    background: #EFE3D5 !important;
    border: 1.5px solid #DABEA7 !important;
    border-radius: 8px !important;
}
.spc-cell { border-right-color: #DABEA7 !important; }
.spc-lbl  { color: #5C4033 !important; }
.spc-val  { color: #2C1F14 !important; }

/* ── SPC 指標卡片（深色 → 奶茶）────────────────────── */
.spc-card {
    background: #FDFAF6 !important;
    border: 1.5px solid #DABEA7 !important;
    border-radius: 10px !important;
}
.spc-card::before { opacity: 0.6; }
.spc-lbl   { color: #5C4033 !important; font-size: 11px !important; font-family: 'Google Sans','Microsoft JhengHei',sans-serif !important; }
.spc-badge { font-family: 'Google Sans','Microsoft JhengHei',sans-serif !important; }
.spc-val   { font-family: 'Google Sans','Microsoft JhengHei',sans-serif !important; color: #2C1F14 !important; }
.spc-sub   { color: #5C4033 !important; font-family: 'Google Sans','Microsoft JhengHei',sans-serif !important; }
.spc-gauge { background: #DABEA7 !important; }
.spc-sec   { color: #5C4033 !important; font-family: 'Google Sans','Microsoft JhengHei',sans-serif !important; letter-spacing: 1px !important; }
.spc-sec::after { background: linear-gradient(90deg, #DABEA7, transparent) !important; }

/* ── 月份高亮按鈕 ─────────────────────────────────── */
button[kind="primary"] {
    background-color: #876D5A !important;
    color: #FDFAF6 !important;
}
button[kind="secondary"] {
    background-color: #FDFAF6 !important;
    color: #876D5A !important;
    border: 1.5px solid #A98B73 !important;
}

/* ── Streamlit 系統 toast / notification ─────────── */
[data-testid="stToast"],
[data-baseweb="toast"] {
    background: #FDFAF6 !important;
    color: #2C1F14 !important;
}

/* ── Success / info / warning 訊息框文字 ──────────── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
}
[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
[data-testid="stAlert"] div {
    font-size: 14px !important;
}

/* ── Number input +/- 按鈕 ───────────────────────── */
[data-testid="stNumberInput"] button {
    background-color: #EFE3D5 !important;
    color: #2C1F14 !important;
    border: 1px solid #DABEA7 !important;
}
[data-testid="stNumberInput"] button:hover {
    background-color: #DABEA7 !important;
}

/* ── Toggle switch ───────────────────────────────── */
[data-testid="stToggle"] label div[data-checked="true"] {
    background-color: #876D5A !important;
}

/* ── Caption / 小字 ──────────────────────────────── */
small, .caption, [class*="caption"] {
    color: #5C4033 !important;
    font-size: 13px !important;
}

/* ── Sidebar section divider ─────────────────────── */
[data-testid="stSidebarContent"] hr {
    border-color: #DABEA7 !important;
}

/* ── 所有白色背景容器改奶茶 ──────────────────────── */
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"] {
    background: transparent !important;
}

footer { visibility: hidden !important; }
#MainMenu { visibility: hidden !important; }
</style>
"""


# ══════════════════════════════════════════════════════
#  Plotly 圖表共用樣式（奶茶色系）
#  在 app.py 裡的所有 fig.update_layout() 都帶入這個 dict
# ══════════════════════════════════════════════════════
CHART_THEME = dict(
    plot_bgcolor  = "#FDFAF6",
    paper_bgcolor = "#FDFAF6",
    font          = dict(color="#2C1F14", family="'Google Sans','Microsoft JhengHei',sans-serif"),
    xaxis = dict(
        gridcolor  = "#DABEA7",
        tickfont   = dict(color="#2C1F14", size=11),
        title      = dict(font=dict(color="#2C1F14", size=12)),
        linecolor  = "#A98B73",
        zerolinecolor = "#A98B73",
    ),
    yaxis = dict(
        gridcolor  = "#DABEA7",
        tickfont   = dict(color="#2C1F14", size=11),
        title      = dict(font=dict(color="#2C1F14", size=12)),
        linecolor  = "#A98B73",
        zerolinecolor = "#A98B73",
    ),
    legend = dict(
        bgcolor     = "#FDFAF6",
        bordercolor = "#DABEA7",
        borderwidth = 1,
        font        = dict(size=12, color="#2C1F14"),
    ),
    hoverlabel = dict(
        bgcolor   = "#FDFAF6",
        font_size = 13,
        font_color= "#2C1F14",
        bordercolor="#A98B73",
    ),
)


def render_landing():
    st.markdown("""
    <style>
    .landing-wrap {
        font-family: 'Google Sans','Microsoft JhengHei',sans-serif;
        background: #FDFAF6;
        border: 1.5px solid #DABEA7;
        border-radius: 14px;
        overflow: hidden;
        margin-bottom: 24px;
        box-shadow: 0 2px 12px rgba(135,109,90,0.10);
    }
    .lp-header {
        display:flex; align-items:center; justify-content:space-between;
        padding:15px 28px; border-bottom:1.5px solid #DABEA7; background:#FDFAF6;
    }
    .lp-logo { display:flex; align-items:center; gap:10px; }
    .lp-logo-icon {
        width:32px; height:32px; background:#876D5A;
        border-radius:7px; display:flex; align-items:center; justify-content:center;
    }
    .lp-logo-name { font-size:16px; font-weight:700; color:#2C1F14; }
    .lp-version   { font-size:12px; color:#876D5A; letter-spacing:1px; text-transform:uppercase; }

    .lp-hero { padding:56px 28px 44px 28px; text-align:center; background:#FDFAF6; }
    .lp-tag {
        display:inline-block; background:#EFE3D5; border:1px solid #DABEA7;
        border-radius:20px; padding:5px 16px;
        font-size:12px; color:#5C4033; letter-spacing:1.5px; text-transform:uppercase;
        margin-bottom:20px;
    }
    .lp-title { font-size:34px; font-weight:700; color:#2C1F14; margin:0 0 16px 0; line-height:1.25; }
    .lp-sub   { font-size:16px; color:#5C4033; max-width:420px; margin:0 auto 36px auto; line-height:1.8; }
    .lp-cta-row { display:flex; gap:12px; justify-content:center; align-items:center; }
    .lp-btn-primary {
        background:#876D5A; color:#FDFAF6; border-radius:8px;
        padding:11px 26px; font-size:15px; font-weight:600; cursor:default;
    }
    .lp-btn-secondary {
        border:1.5px solid #DABEA7; border-radius:8px; padding:11px 26px;
        font-size:15px; color:#5C4033; cursor:default; background:#FDFAF6;
    }
    .lp-strip {
        text-align:center; padding:13px 28px;
        background:#EFE3D5; border-top:1px solid #DABEA7; border-bottom:1px solid #DABEA7;
        font-size:13px; color:#5C4033; letter-spacing:0.5px;
    }
    .lp-cards { display:grid; grid-template-columns:repeat(3,1fr); gap:0; }
    .lp-card  { padding:30px 28px; background:#FDFAF6; border-right:1px solid #DABEA7; }
    .lp-card:last-child { border-right:none; }
    .lp-card-icon {
        width:42px; height:42px; border-radius:10px;
        display:flex; align-items:center; justify-content:center; margin-bottom:16px;
    }
    .lp-card-title { font-size:16px; font-weight:700; color:#2C1F14; margin-bottom:10px; }
    .lp-card-desc  { font-size:14px; color:#5C4033; line-height:1.7; }

    .lp-stats { display:grid; grid-template-columns:repeat(4,1fr); gap:0; border-top:1px solid #DABEA7; }
    .lp-stat  { padding:22px 16px; text-align:center; background:#EFE3D5; border-right:1px solid #DABEA7; }
    .lp-stat:last-child { border-right:none; }
    .lp-stat-num   { font-size:24px; font-weight:700; color:#2C1F14; margin-bottom:6px; }
    .lp-stat-label { font-size:13px; color:#5C4033; }
    </style>

    <div class="landing-wrap">
      <div class="lp-header">
        <div class="lp-logo">
          <div class="lp-logo-icon">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <circle cx="8" cy="8" r="5" stroke="#FDFAF6" stroke-width="1.5"/>
              <circle cx="8" cy="8" r="2" fill="#FDFAF6"/>
            </svg>
          </div>
          <span class="lp-logo-name">AegisCore</span>
        </div>
        <span class="lp-version">鋼捲品質監控平台 v2.0</span>
      </div>

      <div class="lp-hero">
        <div class="lp-tag">Enterprise Quality Intelligence</div>
        <div class="lp-title">智能品質監控平台</div>
        <p class="lp-sub">上傳產線 RAW DATA，即時呈現<br>趨勢分析、跨月比對與製程能力診斷</p>
        <div class="lp-cta-row">
          <div class="lp-btn-primary">← 從左側上傳 RAW DATA 開始</div>
          <div class="lp-btn-secondary">支援 XLSX · CSV</div>
        </div>
      </div>

      <div class="lp-strip">
        支援格式：XLSX · CSV &nbsp;｜&nbsp; 單檔上限 200MB &nbsp;｜&nbsp; 資料本地處理，不上傳雲端
      </div>

      <div class="lp-cards">
        <div class="lp-card">
          <div class="lp-card-icon" style="background:#EFE3D5;">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <polyline points="2,16 7,9 12,11 18,3" stroke="#876D5A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="lp-card-title">趨勢監控</div>
          <div class="lp-card-desc">生產順序異常管制圖，±3σ 即時標示，7B 異常批次自動高亮顯示。</div>
        </div>
        <div class="lp-card">
          <div class="lp-card-icon" style="background:#EFE3D5;">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <rect x="2"  y="11" width="4" height="7" rx="1" fill="#9D7553"/>
              <rect x="8"  y="7"  width="4" height="11" rx="1" fill="#9D7553"/>
              <rect x="14" y="3"  width="4" height="15" rx="1" fill="#9D7553"/>
            </svg>
          </div>
          <div class="lp-card-title">跨月比對</div>
          <div class="lp-card-desc">鎖定規格條件後選擇月份，燈號總表一眼看出哪個月份哪個參數出現異常。</div>
        </div>
        <div class="lp-card">
          <div class="lp-card-icon" style="background:#EFE3D5;">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <circle cx="10" cy="10" r="7.5" stroke="#9A6852" stroke-width="2"/>
              <line x1="10" y1="4"  x2="10" y2="7"  stroke="#9A6852" stroke-width="2" stroke-linecap="round"/>
              <line x1="10" y1="13" x2="10" y2="16" stroke="#9A6852" stroke-width="2" stroke-linecap="round"/>
              <line x1="13" y1="10" x2="16" y2="10" stroke="#9A6852" stroke-width="2" stroke-linecap="round"/>
              <line x1="4"  y1="10" x2="7"  y2="10" stroke="#9A6852" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <div class="lp-card-title">製程能力</div>
          <div class="lp-card-desc">自動計算 Cp、Ca、Cpk，直方圖常態分佈與規格符合率圓餅圖即時呈現。</div>
        </div>
      </div>

      <div class="lp-stats">
        <div class="lp-stat"><div class="lp-stat-num">27+</div><div class="lp-stat-label">可分析參數欄位</div></div>
        <div class="lp-stat"><div class="lp-stat-num">200MB</div><div class="lp-stat-label">單次上傳上限</div></div>
        <div class="lp-stat"><div class="lp-stat-num">5 級</div><div class="lp-stat-label">製程能力評等</div></div>
        <div class="lp-stat"><div class="lp-stat-num">即時</div><div class="lp-stat-label">無需等待批次運算</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

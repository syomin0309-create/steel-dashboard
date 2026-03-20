import streamlit as st

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600;700&display=swap');

/* ── 全域底色與文字 ─────────────────────────────── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="block-container"] {
    background-color: #f8f9fb !important;
    color: #1f1f1f !important;
    font-family: 'Google Sans', 'Microsoft JhengHei', 'Noto Sans TC', sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
    font-size: 15px !important;
}

/* ── 側邊欄 ─────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #dadce0 !important;
}
[data-testid="stSidebar"] * {
    color: #1f1f1f !important;
    font-size: 14px !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #1a73e8 !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}
[data-testid="stSidebar"] label {
    color: #1f1f1f !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #3c4043 !important;
    font-size: 14px !important;
}

/* ── 主標題 ─────────────────────────────────────── */
h1 { color: #1f1f1f !important; font-weight: 700 !important; font-size: 26px !important; }
h2 { color: #1f1f1f !important; font-weight: 700 !important; font-size: 22px !important; }
h3 { color: #1f1f1f !important; font-weight: 600 !important; font-size: 18px !important; }

/* ── 一般文字段落 ────────────────────────────────── */
p, li, span, div {
    color: #1f1f1f !important;
    font-size: 15px !important;
}

/* ── caption / 說明文字 ─────────────────────────── */
[data-testid="stCaptionContainer"] p,
[data-testid="stCaptionContainer"] span {
    color: #3c4043 !important;
    font-size: 13px !important;
}

/* ── 指標卡片 ─────────────────────────────────────*/
[data-testid="metric-container"] {
    background: #ffffff !important;
    border: 1px solid #dadce0 !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    box-shadow: 0 1px 4px rgba(60,64,67,0.08) !important;
}
[data-testid="metric-container"] label {
    color: #3c4043 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #1f1f1f !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] span {
    font-size: 13px !important;
}

/* ── 分頁 Tab ─────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1.5px solid #dadce0 !important;
}
[data-testid="stTabs"] button {
    color: #3c4043 !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 12px 24px !important;
    border-radius: 0 !important;
    background: transparent !important;
}
[data-testid="stTabs"] button:hover {
    color: #1a73e8 !important;
    background: #f1f8ff !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #1a73e8 !important;
    font-weight: 700 !important;
    border-bottom: 2.5px solid #1a73e8 !important;
    background: transparent !important;
}
[data-testid="stTabs"] button p {
    color: inherit !important;
    font-size: inherit !important;
}

/* ── 下拉選單 ────────────────────────────────────── */
div[data-baseweb="select"] > div {
    border: 1.5px solid #dadce0 !important;
    border-radius: 8px !important;
    background-color: #ffffff !important;
    font-size: 15px !important;
}
div[data-baseweb="select"] > div:hover {
    border-color: #1a73e8 !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color: #1f1f1f !important;
    background-color: #ffffff !important;
    font-size: 15px !important;
}
div[data-baseweb="popover"] {
    background-color: #ffffff !important;
    border: 1px solid #dadce0 !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 20px rgba(60,64,67,0.15) !important;
}
div[data-baseweb="popover"] li {
    color: #1f1f1f !important;
    font-size: 15px !important;
}
div[data-baseweb="popover"] li:hover {
    background-color: #e8f0fe !important;
}

/* ── 멀티셀렉트 태그 ─────────────────────────────── */
[data-baseweb="tag"] {
    background-color: #e8f0fe !important;
}
[data-baseweb="tag"] span {
    color: #1a3a6e !important;
    font-size: 13px !important;
}

/* ── 입력박스 ────────────────────────────────────── */
input[type="number"],
input[type="text"],
textarea {
    background-color: #ffffff !important;
    color: #1f1f1f !important;
    border: 1.5px solid #dadce0 !important;
    border-radius: 8px !important;
    font-size: 15px !important;
}
input:focus, textarea:focus {
    border-color: #1a73e8 !important;
    box-shadow: 0 0 0 2px rgba(26,115,232,0.15) !important;
}
/* number input 라벨 */
[data-testid="stNumberInput"] label p {
    color: #1f1f1f !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}
/* selectbox 라벨 */
[data-testid="stSelectbox"] label p {
    color: #1f1f1f !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}
/* multiselect 라벨 */
[data-testid="stMultiSelect"] label p {
    color: #1f1f1f !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}
/* toggle 라벨 */
[data-testid="stCheckbox"] label p,
[data-testid="stToggle"] label p {
    color: #1f1f1f !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}

/* ── 버튼 ────────────────────────────────────────── */
[data-testid="stDownloadButton"] button,
[data-testid="stButton"] button {
    background-color: #1a73e8 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 8px 20px !important;
}
[data-testid="stDownloadButton"] button:hover,
[data-testid="stButton"] button:hover {
    background-color: #1557b0 !important;
}
[data-testid="stDownloadButton"] button p,
[data-testid="stButton"] button p {
    color: #ffffff !important;
    font-size: 14px !important;
}
/* secondary 버튼 */
[data-testid="stButton"] button[kind="secondary"] {
    background-color: #ffffff !important;
    color: #1a73e8 !important;
    border: 1.5px solid #1a73e8 !important;
}
[data-testid="stButton"] button[kind="secondary"] p {
    color: #1a73e8 !important;
}

/* ── 訊息框 ──────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-size: 14px !important;
}
[data-testid="stAlert"] p {
    font-size: 14px !important;
    color: inherit !important;
}

/* ── File Uploader ───────────────────────────────── */
[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 2px dashed #dadce0 !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #1a73e8 !important;
}
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p {
    color: #3c4043 !important;
    font-size: 14px !important;
}

/* ── Expander ────────────────────────────────────── */
[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #dadce0 !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary {
    color: #1f1f1f !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}
[data-testid="stExpander"] summary p {
    color: #1f1f1f !important;
    font-size: 15px !important;
}

/* ── Dataframe ───────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid #dadce0 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] th {
    background-color: #f1f3f4 !important;
    color: #1f1f1f !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}
[data-testid="stDataFrame"] td {
    color: #1f1f1f !important;
    font-size: 14px !important;
}

/* ── 水平分隔線 ──────────────────────────────────── */
hr { border-color: #dadce0 !important; margin: 20px 0 !important; }

/* ── 自訂元件 ────────────────────────────────────── */
.spec-banner {
    background: linear-gradient(135deg, #1a73e8, #4285f4) !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    padding: 18px 28px !important;
    margin-bottom: 20px !important;
    font-size: 15px !important;
    line-height: 2 !important;
}
.spec-banner b { color: #fef08a !important; font-weight: 700 !important; }
.spec-banner span { color: #ffffff !important; }

.section-title {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #1f1f1f !important;
    border-left: 4px solid #1a73e8 !important;
    padding-left: 12px !important;
    margin: 24px 0 12px 0 !important;
}

.signal-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.signal-table th {
    background: #1a73e8;
    color: #ffffff;
    padding: 11px 14px;
    text-align: center;
    font-weight: 600;
    font-size: 14px;
}
.signal-table td {
    padding: 10px 14px;
    text-align: center;
    border-bottom: 1px solid #dadce0;
    color: #1f1f1f;
    background: #ffffff;
    font-size: 14px;
}
.signal-table tr:nth-child(even) td { background-color: #f8f9fb; }
.sig-green  { color: #0d6e2f; font-weight: 700; }
.sig-yellow { color: #8a5c00; font-weight: 700; }
.sig-red    { color: #b71c1c; font-weight: 700; }
.sig-gray   { color: #5f6368; }

/* ── 隱藏頁腳 ────────────────────────────────────── */
footer { visibility: hidden !important; }
#MainMenu { visibility: hidden !important; }
</style>
"""


def render_landing():
    st.markdown("""
    <style>
    .landing-wrap {
        font-family: 'Google Sans', 'Microsoft JhengHei', sans-serif;
        background: #ffffff;
        border: 1px solid #dadce0;
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 24px;
    }
    .lp-header {
        display: flex; align-items: center; justify-content: space-between;
        padding: 14px 28px; border-bottom: 1px solid #dadce0; background: #ffffff;
    }
    .lp-logo { display: flex; align-items: center; gap: 10px; }
    .lp-logo-icon {
        width: 32px; height: 32px; background: #1a73e8;
        border-radius: 6px; display: flex; align-items: center; justify-content: center;
    }
    .lp-logo-name { font-size: 16px; font-weight: 700; color: #1f1f1f; }
    .lp-version { font-size: 12px; color: #5f6368; letter-spacing: 1px; text-transform: uppercase; }
    .lp-hero { padding: 56px 28px 44px 28px; text-align: center; background: #ffffff; }
    .lp-tag {
        display: inline-block; background: #f1f3f4; border: 1px solid #dadce0;
        border-radius: 20px; padding: 5px 16px;
        font-size: 12px; color: #3c4043; letter-spacing: 1.5px;
        text-transform: uppercase; margin-bottom: 20px;
    }
    .lp-title { font-size: 34px; font-weight: 700; color: #1f1f1f; margin: 0 0 16px 0; line-height: 1.25; }
    .lp-sub { font-size: 16px; color: #3c4043; max-width: 420px; margin: 0 auto 36px auto; line-height: 1.8; }
    .lp-cta-row { display: flex; gap: 12px; justify-content: center; align-items: center; }
    .lp-btn-primary {
        background: #1a73e8; color: #ffffff; border-radius: 8px;
        padding: 11px 26px; font-size: 15px; font-weight: 600; cursor: default;
    }
    .lp-btn-secondary {
        border: 1.5px solid #dadce0; border-radius: 8px; padding: 11px 26px;
        font-size: 15px; color: #3c4043; cursor: default; background: #ffffff;
    }
    .lp-strip {
        text-align: center; padding: 13px 28px;
        background: #f8f9fb; border-top: 1px solid #dadce0; border-bottom: 1px solid #dadce0;
        font-size: 13px; color: #3c4043; letter-spacing: 0.5px;
    }
    .lp-cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0; }
    .lp-card { padding: 30px 28px; background: #ffffff; border-right: 1px solid #dadce0; }
    .lp-card:last-child { border-right: none; }
    .lp-card-icon {
        width: 40px; height: 40px; border-radius: 10px;
        display: flex; align-items: center; justify-content: center; margin-bottom: 16px;
    }
    .lp-card-title { font-size: 16px; font-weight: 700; color: #1f1f1f; margin-bottom: 10px; }
    .lp-card-desc { font-size: 14px; color: #3c4043; line-height: 1.7; }
    .lp-stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; border-top: 1px solid #dadce0; }
    .lp-stat { padding: 22px 16px; text-align: center; background: #f8f9fb; border-right: 1px solid #dadce0; }
    .lp-stat:last-child { border-right: none; }
    .lp-stat-num { font-size: 24px; font-weight: 700; color: #1f1f1f; margin-bottom: 6px; }
    .lp-stat-label { font-size: 13px; color: #3c4043; }
    </style>

    <div class="landing-wrap">
      <div class="lp-header">
        <div class="lp-logo">
          <div class="lp-logo-icon">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <circle cx="8" cy="8" r="5" stroke="white" stroke-width="1.5"/>
              <circle cx="8" cy="8" r="2" fill="white"/>
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
          <div class="lp-card-icon" style="background:#e8f0fe;">
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <polyline points="2,14 6,8 11,10 16,3" stroke="#1a73e8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="lp-card-title">趨勢監控</div>
          <div class="lp-card-desc">生產順序異常管制圖，±3σ 即時標示，7B 異常批次自動高亮顯示。</div>
        </div>
        <div class="lp-card">
          <div class="lp-card-icon" style="background:#e6f4ea;">
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <rect x="2" y="10" width="4" height="6" rx="1" fill="#1e8e3e"/>
              <rect x="7" y="7"  width="4" height="9" rx="1" fill="#1e8e3e"/>
              <rect x="12" y="3" width="4" height="13" rx="1" fill="#1e8e3e"/>
            </svg>
          </div>
          <div class="lp-card-title">跨月比對</div>
          <div class="lp-card-desc">鎖定規格條件後選擇月份，燈號總表一眼看出哪個月份哪個參數出現異常。</div>
        </div>
        <div class="lp-card">
          <div class="lp-card-icon" style="background:#fce8e6;">
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <circle cx="9" cy="9" r="6.5" stroke="#d93025" stroke-width="2"/>
              <line x1="9" y1="3.5" x2="9" y2="6.5" stroke="#d93025" stroke-width="2" stroke-linecap="round"/>
              <line x1="9" y1="11.5" x2="9" y2="14.5" stroke="#d93025" stroke-width="2" stroke-linecap="round"/>
              <line x1="11.5" y1="9" x2="14.5" y2="9" stroke="#d93025" stroke-width="2" stroke-linecap="round"/>
              <line x1="3.5" y1="9" x2="6.5" y2="9" stroke="#d93025" stroke-width="2" stroke-linecap="round"/>
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

"""
=======================================================
  AegisCore UI Theme — SkyAgent 風格
  使用方式：把 THEME_CSS 的內容貼進你的 st.markdown() 裡
=======================================================
"""

THEME_CSS = """
<style>
/* ── 全域底色與文字 ─────────────────────────────── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #f8fafc !important;
    color: #1e293b !important;
}

/* ── 字體 ───────────────────────────────────────── */
html, body, [class*="css"], button, input, select, textarea {
    font-family: 'Microsoft JhengHei', 'Noto Sans TC', 'Inter', 'Segoe UI', sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
}

/* ── 側邊欄 ─────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}
[data-testid="stSidebar"] * {
    color: #1e293b !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #0ea5e9 !important;
    font-weight: 700 !important;
}

/* ── 主標題 ─────────────────────────────────────── */
h1 { color: #0f172a !important; font-weight: 800 !important; letter-spacing: -0.5px; }
h2 { color: #1e293b !important; font-weight: 700 !important; }
h3 { color: #334155 !important; font-weight: 600 !important; }

/* ── 指標卡片 ─────────────────────────────────────*/
[data-testid="metric-container"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
}
[data-testid="metric-container"] label {
    color: #64748b !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #0f172a !important;
    font-size: 26px !important;
    font-weight: 700 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 13px !important;
}

/* ── 分頁 Tab ────────────────────────────────────── */
[data-testid="stTabs"] button {
    color: #64748b !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 8px 18px !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #0ea5e9 !important;
    border-bottom: 2px solid #0ea5e9 !important;
    background: #f0f9ff !important;
}

/* ── 下拉選單 ────────────────────────────────────── */
div[data-baseweb="select"] * {
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #1e293b !important;
    background-color: #ffffff !important;
}
div[data-baseweb="select"] > div {
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    background-color: #ffffff !important;
}
div[data-baseweb="popover"] {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important;
}
div[data-baseweb="popover"] li {
    color: #1e293b !important;
}
div[data-baseweb="popover"] li:hover {
    background-color: #f0f9ff !important;
}

/* ── 輸入框 ─────────────────────────────────────── */
input[type="number"], input[type="text"], textarea {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
}
input[type="number"]:focus, input[type="text"]:focus {
    border-color: #0ea5e9 !important;
    box-shadow: 0 0 0 3px rgba(14,165,233,0.15) !important;
}

/* ── 按鈕 ────────────────────────────────────────── */
[data-testid="stDownloadButton"] button,
[data-testid="stButton"] button {
    background-color: #0ea5e9 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 8px 20px !important;
    transition: background 0.2s !important;
}
[data-testid="stDownloadButton"] button:hover,
[data-testid="stButton"] button:hover {
    background-color: #0284c7 !important;
}

/* ── 提示訊息框 ─────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-weight: 500 !important;
}
/* success */
[data-testid="stAlert"][data-baseweb="notification"][kind="positive"] {
    background-color: #f0fdf4 !important;
    border-left: 4px solid #22c55e !important;
    color: #166534 !important;
}
/* info */
[data-testid="stAlert"][data-baseweb="notification"][kind="info"] {
    background-color: #f0f9ff !important;
    border-left: 4px solid #0ea5e9 !important;
    color: #0c4a6e !important;
}
/* warning */
[data-testid="stAlert"][data-baseweb="notification"][kind="warning"] {
    background-color: #fffbeb !important;
    border-left: 4px solid #f59e0b !important;
    color: #78350f !important;
}
/* error */
[data-testid="stAlert"][data-baseweb="notification"][kind="error"] {
    background-color: #fef2f2 !important;
    border-left: 4px solid #ef4444 !important;
    color: #7f1d1d !important;
}

/* ── File uploader ──────────────────────────────── */
[data-testid="stFileUploader"] {
    background: #f8fafc !important;
    border: 2px dashed #cbd5e1 !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #0ea5e9 !important;
}
[data-testid="stFileUploader"] * {
    color: #475569 !important;
}

/* ── Expander ───────────────────────────────────── */
[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
[data-testid="stExpander"] summary {
    color: #334155 !important;
    font-weight: 600 !important;
}

/* ── 水平分隔線 ─────────────────────────────────── */
hr {
    border-color: #e2e8f0 !important;
}

/* ── Dataframe ──────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ── 自訂元件類別 ────────────────────────────────── */
.spec-banner {
    background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    padding: 18px 28px !important;
    margin-bottom: 20px !important;
    font-size: 15px !important;
    line-height: 2.2 !important;
    box-shadow: 0 4px 14px rgba(14,165,233,0.25) !important;
}
.spec-banner b { color: #fef9c3 !important; font-size: 16px !important; }

.section-title {
    font-size: 17px !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    border-left: 4px solid #0ea5e9 !important;
    padding-left: 12px !important;
    margin: 24px 0 12px 0 !important;
}

.signal-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.signal-table th {
    background-color: #0ea5e9;
    color: #ffffff;
    padding: 10px 14px;
    text-align: center;
    font-weight: 600;
}
.signal-table td {
    padding: 9px 14px;
    text-align: center;
    border-bottom: 1px solid #e2e8f0;
    color: #1e293b;
}
.signal-table tr:nth-child(even) { background-color: #f8fafc; }
.sig-green  { color: #16a34a; font-weight: 700; }
.sig-yellow { color: #d97706; font-weight: 700; }
.sig-red    { color: #dc2626; font-weight: 700; }
.sig-gray   { color: #94a3b8; }

/* ── 隱藏 Streamlit 預設頁腳 ─────────────────────── */
footer { visibility: hidden !important; }
</style>
"""

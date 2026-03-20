import streamlit as st

# ── 主題 CSS（米白底色，SkyAgent 天藍色系）────────────────
THEME_CSS = """
<style>
/* ── 全域底色與文字 ─────────────────────────────── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="block-container"] {
    background-color: #f5f7fa !important;
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
h1 { color: #0f172a !important; font-weight: 800 !important; }
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

/* ── 分頁 Tab ────────────────────────────────────── */
[data-testid="stTabs"] button {
    color: #64748b !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border-radius: 8px 8px 0 0 !important;
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
    box-shadow: 0 4px 20px rgba(0,0,0,0.10) !important;
}
div[data-baseweb="popover"] li { color: #1e293b !important; }
div[data-baseweb="popover"] li:hover { background-color: #f0f9ff !important; }

/* ── 輸入框 ─────────────────────────────────────── */
input[type="number"], input[type="text"], textarea {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
}

/* ── 按鈕 ────────────────────────────────────────── */
[data-testid="stDownloadButton"] button,
[data-testid="stButton"] button {
    background-color: #0ea5e9 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
[data-testid="stDownloadButton"] button:hover,
[data-testid="stButton"] button:hover {
    background-color: #0284c7 !important;
}

/* ── 提示訊息框 ─────────────────────────────────── */
[data-testid="stAlert"] { border-radius: 10px !important; }

/* ── File uploader ──────────────────────────────── */
[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 2px dashed #cbd5e1 !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"] * { color: #475569 !important; }

/* ── Expander ───────────────────────────────────── */
[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary {
    color: #334155 !important;
    font-weight: 600 !important;
}

/* ── Dataframe ──────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ── 自訂元件 ────────────────────────────────────── */
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
.spec-banner b { color: #fef9c3 !important; }

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

/* ── 隱藏頁腳 ────────────────────────────────────── */
footer { visibility: hidden !important; }
</style>
"""


# ── 封面頁（Landing Page）────────────────────────────────
def render_landing():
    """上傳檔案前顯示的歡迎封面"""
    st.markdown("""
    <div style="text-align:center; padding: 60px 20px 40px 20px;">
        <div style="
            display: inline-block;
            background: linear-gradient(135deg, #0ea5e9, #0284c7);
            border-radius: 20px;
            padding: 20px 28px;
            margin-bottom: 28px;
            box-shadow: 0 8px 24px rgba(14,165,233,0.30);
        ">
            <span style="font-size: 48px;">👁</span>
        </div>
        <h1 style="
            font-size: 38px;
            font-weight: 800;
            color: #0f172a;
            margin: 0 0 12px 0;
            letter-spacing: -1px;
        ">AegisCore</h1>
        <p style="
            font-size: 16px;
            color: #64748b;
            max-width: 480px;
            margin: 0 auto 48px auto;
            line-height: 1.8;
        ">智能鋼捲品質監控平台<br>上傳產線 RAW DATA，即時呈現品質趨勢與製程能力分析</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    cards = [
        ("📊", "趨勢監控", "即時追蹤各參數生產走勢，±3σ 管制線一眼辨識異常點"),
        ("🚦", "跨月比對", "鎖定規格條件，對比不同月份品質表現與異常燈號"),
        ("📐", "製程能力", "自動計算 Cp、Ca、Cpk，評估製程穩定性與改善方向"),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3], cards):
        col.markdown(f"""
        <div style="
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 32px 24px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        ">
            <div style="font-size: 34px; margin-bottom: 14px;">{icon}</div>
            <div style="font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 10px;">{title}</div>
            <div style="font-size: 13px; color: #64748b; line-height: 1.7;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 請從左側邊欄上傳產線的 RAW DATA（支援 .xlsx / .csv），系統將自動判別格式並產生分析圖表。")

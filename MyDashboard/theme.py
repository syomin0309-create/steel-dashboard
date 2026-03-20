import streamlit as st

# ══════════════════════════════════════════════════════
#  AegisCore Theme — Gemini 風格
#  米白底色 · 藍紫漸層點綴 · 統一簡潔路線
# ══════════════════════════════════════════════════════

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600;700&display=swap');

/* ── 全域 ────────────────────────────────────────── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="block-container"] {
    background-color: #f8f9fb !important;
    color: #1f1f1f !important;
    font-family: 'Google Sans', 'Microsoft JhengHei', 'Noto Sans TC', sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
}

/* ── 側邊欄 ──────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e8eaed !important;
}
[data-testid="stSidebar"] * { color: #3c4043 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #1a73e8 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    letter-spacing: 0.3px;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    font-size: 13px !important;
    color: #5f6368 !important;
}

/* ── 標題 ────────────────────────────────────────── */
h1 {
    color: #1f1f1f !important;
    font-weight: 700 !important;
    font-size: 26px !important;
    letter-spacing: -0.3px;
}
h2 { color: #202124 !important; font-weight: 600 !important; font-size: 20px !important; }
h3 { color: #3c4043 !important; font-weight: 600 !important; font-size: 16px !important; }

/* ── 指標卡片 ────────────────────────────────────── */
[data-testid="metric-container"] {
    background: #ffffff !important;
    border: 1px solid #e8eaed !important;
    border-radius: 12px !important;
    padding: 18px 20px !important;
    box-shadow: 0 1px 3px rgba(60,64,67,0.08) !important;
}
[data-testid="metric-container"] label {
    color: #5f6368 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #1f1f1f !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 12px !important;
    color: #5f6368 !important;
}

/* ── 分頁 Tab ─────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid #e8eaed !important;
    gap: 0 !important;
}
[data-testid="stTabs"] button {
    color: #5f6368 !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 10px 20px !important;
    border-radius: 0 !important;
    background: transparent !important;
    border: none !important;
}
[data-testid="stTabs"] button:hover { color: #1a73e8 !important; background: #f1f8ff !important; }
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #1a73e8 !important;
    font-weight: 600 !important;
    border-bottom: 2px solid #1a73e8 !important;
    background: transparent !important;
}

/* ── 下拉選單 ────────────────────────────────────── */
div[data-baseweb="select"] > div {
    border: 1px solid #dadce0 !important;
    border-radius: 8px !important;
    background-color: #ffffff !important;
    font-size: 14px !important;
}
div[data-baseweb="select"] > div:hover { border-color: #1a73e8 !important; }
div[data-baseweb="select"] * { color: #3c4043 !important; background-color: #ffffff !important; }
div[data-baseweb="popover"] {
    background-color: #ffffff !important;
    border: 1px solid #e8eaed !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 16px rgba(60,64,67,0.12) !important;
}
div[data-baseweb="popover"] li { color: #3c4043 !important; font-size: 14px !important; }
div[data-baseweb="popover"] li:hover { background-color: #f1f8ff !important; }

/* ── 輸入框 ──────────────────────────────────────── */
input[type="number"], input[type="text"], textarea {
    background-color: #ffffff !important;
    color: #3c4043 !important;
    border: 1px solid #dadce0 !important;
    border-radius: 8px !important;
    font-size: 14px !important;
}
input:focus, textarea:focus {
    border-color: #1a73e8 !important;
    box-shadow: 0 0 0 2px rgba(26,115,232,0.15) !important;
    outline: none !important;
}

/* ── 按鈕 ────────────────────────────────────────── */
[data-testid="stDownloadButton"] button,
[data-testid="stButton"] button {
    background-color: #1a73e8 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 8px 20px !important;
    transition: background 0.2s ease !important;
    box-shadow: 0 1px 3px rgba(26,115,232,0.3) !important;
}
[data-testid="stDownloadButton"] button:hover,
[data-testid="stButton"] button:hover {
    background-color: #1557b0 !important;
    box-shadow: 0 2px 6px rgba(26,115,232,0.4) !important;
}

/* ── 訊息框 ──────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border: none !important;
    font-size: 14px !important;
}

/* ── File Uploader ───────────────────────────────── */
[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 1.5px dashed #dadce0 !important;
    border-radius: 12px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover { border-color: #1a73e8 !important; }
[data-testid="stFileUploader"] * { color: #5f6368 !important; font-size: 13px !important; }

/* ── Expander ────────────────────────────────────── */
[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #e8eaed !important;
    border-radius: 10px !important;
    box-shadow: 0 1px 3px rgba(60,64,67,0.06) !important;
}
[data-testid="stExpander"] summary {
    color: #3c4043 !important;
    font-weight: 500 !important;
    font-size: 14px !important;
}

/* ── Dataframe ───────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid #e8eaed !important;
    border-radius: 10px !important;
    overflow: hidden !important;
    background: #ffffff !important;
}

/* ── 水平分隔線 ──────────────────────────────────── */
hr { border-color: #e8eaed !important; margin: 20px 0 !important; }

/* ── 自訂元件 ────────────────────────────────────── */
.spec-banner {
    background: linear-gradient(135deg, #1a73e8 0%, #4285f4 60%, #8ab4f8 100%) !important;
    color: #ffffff !important;
    border-radius: 14px !important;
    padding: 20px 28px !important;
    margin-bottom: 20px !important;
    font-size: 14px !important;
    line-height: 2 !important;
    box-shadow: 0 4px 16px rgba(26,115,232,0.22) !important;
}
.spec-banner b { color: #fef08a !important; font-weight: 600 !important; }

.section-title {
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #202124 !important;
    border-left: 3px solid #1a73e8 !important;
    padding-left: 12px !important;
    margin: 24px 0 12px 0 !important;
    letter-spacing: 0.2px;
}

.signal-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.signal-table th {
    background: linear-gradient(90deg, #1a73e8, #4285f4);
    color: #ffffff;
    padding: 10px 14px;
    text-align: center;
    font-weight: 500;
    letter-spacing: 0.3px;
}
.signal-table td {
    padding: 9px 14px;
    text-align: center;
    border-bottom: 1px solid #e8eaed;
    color: #3c4043;
    background: #ffffff;
}
.signal-table tr:nth-child(even) td { background-color: #f8f9fb; }
.sig-green  { color: #1e8e3e; font-weight: 600; }
.sig-yellow { color: #f29900; font-weight: 600; }
.sig-red    { color: #d93025; font-weight: 600; }
.sig-gray   { color: #9aa0a6; }

/* ── 隱藏頁腳 ────────────────────────────────────── */
footer { visibility: hidden !important; }
#MainMenu { visibility: hidden !important; }
</style>
"""


# ══════════════════════════════════════════════════════
#  封面頁 — render_landing()
#  Gemini 風格：漸層標題 + 輪動評語卡
# ══════════════════════════════════════════════════════

def render_landing():
    st.markdown("""
    <style>
    /* ── 漸層標題動畫 ── */
    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .hero-title {
        font-size: 48px;
        font-weight: 800;
        background: linear-gradient(270deg, #1a73e8, #8ab4f8, #4285f4, #a8c7fa);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 5s ease infinite;
        letter-spacing: -1.5px;
        margin: 0 0 12px 0;
        line-height: 1.1;
    }
    .hero-sub {
        font-size: 16px;
        color: #5f6368;
        max-width: 480px;
        margin: 0 auto 48px auto;
        line-height: 1.8;
    }

    /* ── 輪動卡片 ── */
    @keyframes scrollX {
        0%   { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    .marquee-wrapper {
        overflow: hidden;
        width: 100%;
        margin: 32px 0 0 0;
    }
    .marquee-track {
        display: flex;
        width: max-content;
        animation: scrollX 28s linear infinite;
        gap: 16px;
    }
    .marquee-track:hover { animation-play-state: paused; }
    .review-card {
        background: #ffffff;
        border: 1px solid #e8eaed;
        border-radius: 14px;
        padding: 20px 24px;
        width: 280px;
        flex-shrink: 0;
        box-shadow: 0 1px 4px rgba(60,64,67,0.08);
    }
    .review-card .avatar {
        width: 36px; height: 36px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 16px;
        margin-bottom: 10px;
    }
    .review-card .name {
        font-size: 13px; font-weight: 600; color: #202124;
    }
    .review-card .role {
        font-size: 12px; color: #80868b; margin-bottom: 10px;
    }
    .review-card .text {
        font-size: 13px; color: #3c4043; line-height: 1.6;
    }
    </style>

    <div style="text-align:center; padding: 64px 20px 32px 20px;">

        <!-- Logo badge -->
        <div style="
            display:inline-flex; align-items:center; gap:10px;
            background:#ffffff; border:1px solid #e8eaed;
            border-radius:50px; padding:8px 20px;
            box-shadow:0 1px 4px rgba(60,64,67,0.10);
            margin-bottom:28px;
        ">
            <span style="font-size:20px;">👁</span>
            <span style="font-size:13px; font-weight:600; color:#5f6368; letter-spacing:0.5px;">AEGISCORE</span>
        </div>

        <!-- 漸層流線標題 -->
        <div class="hero-title">智能品質監控平台</div>
        <p class="hero-sub">
            上傳產線 RAW DATA<br>
            即時呈現趨勢分析、跨月比對與製程能力診斷
        </p>

    </div>
    """, unsafe_allow_html=True)

    # ── 功能卡片 ──────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    cards = [
        ("#e8f0fe", "#1a73e8", "📊", "趨勢監控",  "±3σ 管制線即時追蹤，異常點一眼辨識"),
        ("#e6f4ea", "#1e8e3e", "🚦", "跨月比對",  "鎖定規格，橫向對比各月品質表現"),
        ("#fce8e6", "#d93025", "📐", "製程能力",  "自動計算 Cp · Ca · Cpk，評估製程穩定性"),
    ]
    for col, (bg, accent, icon, title, desc) in zip([c1, c2, c3], cards):
        col.markdown(f"""
        <div style="
            background:#ffffff; border:1px solid #e8eaed;
            border-radius:16px; padding:28px 22px;
            text-align:center;
            box-shadow:0 1px 4px rgba(60,64,67,0.08);
            transition: box-shadow 0.2s;
        ">
            <div style="
                display:inline-flex; align-items:center; justify-content:center;
                background:{bg}; border-radius:12px;
                width:52px; height:52px; font-size:26px;
                margin-bottom:14px;
            ">{icon}</div>
            <div style="font-size:15px; font-weight:700; color:#202124; margin-bottom:8px;">{title}</div>
            <div style="font-size:13px; color:#5f6368; line-height:1.7;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── 輪動評語卡 ────────────────────────────────────
    reviews = [
        ("🔵", "#e8f0fe", "品保部門",  "生產線副理", "透過跨月燈號表，我們立刻發現了三月份的異常偏移，處理效率大幅提升。"),
        ("🟢", "#e6f4ea", "製程工程",  "製程工程師", "CPK 分析讓我不需要手動計算，上傳資料就能直接看到製程能力等級。"),
        ("🔴", "#fce8e6", "品質主管",  "品質主管",   "每月例行報告再也不需要花半天整理 Excel，這個平台幫我省了大量時間。"),
        ("🟡", "#fef7e0", "冷軋產線",  "線長",       "以前要靠經驗判斷品質穩不穩，現在有數據支撐，溝通客訴更有底氣。"),
        ("🔵", "#e8f0fe", "技術研發",  "研發工程師", "相關性熱力圖讓我快速找到影響抗拉強度的關鍵製程參數。"),
        ("🟢", "#e6f4ea", "鍍層產線",  "製程主任",   "鍍層量 CPK 趨勢一覽無遺，異常批次再也不會漏網。"),
    ]
    # 複製一份讓輪播無縫循環
    all_reviews = reviews + reviews

    cards_html = ""
    for emoji, bg, dept, role, text in all_reviews:
        cards_html += f"""
        <div class="review-card">
            <div class="avatar" style="background:{bg};">{emoji}</div>
            <div class="name">{dept}</div>
            <div class="role">{role}</div>
            <div class="text">{text}</div>
        </div>
        """

    st.markdown(f"""
    <div style="margin-top:16px;">
        <p style="text-align:center; font-size:13px; color:#80868b; margin-bottom:16px; letter-spacing:0.5px;">
            來自各部門的使用心得
        </p>
        <div class="marquee-wrapper">
            <div class="marquee-track">
                {cards_html}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 請從左側邊欄上傳產線的 RAW DATA（支援 .xlsx / .csv），系統將自動判別格式並產生分析圖表。")

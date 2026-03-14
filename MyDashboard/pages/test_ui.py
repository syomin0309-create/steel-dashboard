import streamlit as st

# 1. 設定頁面為暗色模式的基礎底色 (這部分保持不變)
st.set_page_config(page_title="OpenClaw 風格測試", layout="wide")

# 2. 🔮 進階版 CSS 魔法陣：質感與細節封頂！
custom_css = """
<style>
    /* =========================================
       🅰️ 字體大變身：引入現代科技感字體 (這點最關鍵！)
       我們引入 Google Fonts 的 "Geist Sans" (超有 tech 質感)
       ========================================= */
    @import url('https://fonts.googleapis.com/css2?family=Geist:wght@100..900&display=swap');

    /* =========================================
       🎛️ 全域樣式：精細化背景與文字
       ========================================= */
    .stApp {
        /* 1. 更深邃、更高級的黑藍色背景 */
        background-color: #0d1117;
        /* 2. 套用 Geist 字體 */
        font-family: 'Geist Sans', system-ui, -apple-system, sans-serif !important;
        color: #f0f6fc;
        /* 3. 增加一點行高，讓文字呼吸 */
        line-height: 1.6;
    }

    /* 隱藏 streamlit 預設標題以避免視覺混亂 */
    .stApp > header {
        background-color: transparent !important;
    }

    /* =========================================
       🚀 Hero 區塊：漸層字體與排版優化
       ========================================= */
    .hero-title {
        /* 1. 調整字重和大小，讓它更有氣勢 */
        font-size: 6.5rem;
        font-weight: 800;
        letter-spacing: -3px; /* 緊縮字距，更有張力 */
        text-align: center;
        margin-top: 80px;
        margin-bottom: 5px;
        
        /* 2. 更柔和、更專業的漸層色 (使用 #ef4444 和 #f97316) */
        background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        /* 增加一點微弱的文字發光特效 */
        text-shadow: 0 0 40px rgba(255, 107, 107, 0.2);
    }
    
    .hero-subtitle {
        text-align: center;
        /* 1. 調整字重和顏色，讓它變成低調的配角 */
        color: #8b949e;
        font-size: 1.4rem;
        font-weight: 300;
        letter-spacing: 3px; /* 拉大字距，增加透氣感 */
        margin-bottom: 80px;
    }

    /* =========================================
       🔥 核心動畫：更流暢的無限輪播
       ========================================= */
    .marquee-container {
        width: 100%;
        overflow: hidden;
        position: relative;
        padding: 40px 0; /* 增加上下間距 */
    }

    /* 定義滑動動畫：更長的時間(30s)，讓速度更舒緩高級 */
    .marquee-track {
        display: flex;
        /* 預設總卡片數是 8 張 (4張內容複製兩份) */
        animation: scroll 30s linear infinite;
        /* GPU 加速提示，讓動畫更流暢 */
        will-change: transform;
    }

    /* 當滑鼠移過去時，動畫平滑暫停 */
    .marquee-track:hover {
        animation-play-state: paused;
    }

    /* 定義滑動動畫關鍵影格 (這裡需要根據你的卡片數量和寬度手動微調) */
    @keyframes scroll {
        0% { transform: translateX(0); }
        /* 關鍵：要精準推到「第一組卡片末端」才能無縫循環 */
        /* 這裡假設一張卡片 320px * 4 = 1280px */
        100% { transform: translateX(-1280px); }
    }

    /* =========================================
       🔮 卡片設計：極致毛玻璃與細節發光
       ========================================= */
    .glass-card {
        width: 300px;
        min-width: 300px;
        margin-right: 20px;
        padding: 30px; /* 增加內部填充，更顯大氣 */
        
        /* 1. 極致毛玻璃：更低透明度背景 + 更強模糊 */
        background: rgba(255, 255, 255, 0.015); /* 極低透明度 */
        backdrop-filter: blur(16px); /* 增強模糊 */
        
        /* 2. 精細化邊框：微光單色線條 (不使用全白) */
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        
        color: #c9d1d9;
        font-weight: 300;
        font-size: 1.05rem;
        
        /* 3. 增加一個非常柔和的外陰影，讓它更有立體感 */
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        
        /* 4. 平滑過渡效果 */
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        
        /* GPU 加速提示 */
        will-change: transform, border-color, box-shadow;
    }

    /* 卡片浮起與發光特效 (質感提升關鍵！) */
    .glass-card:hover {
        /* 1. 溫和地浮起 */
        transform: translateY(-8px);
        
        /* 2. 精細化邊框亮起：使用科技感橘紅色 */
        border-color: rgba(255, 107, 107, 0.3);
        
        /* 3. 增強陰影與霓虹光暈 */
        box-shadow: 0 15px 40px -10px rgba(255, 107, 107, 0.15),
                    0 0 10px rgba(255, 107, 107, 0.05);
    }

    .card-user {
        color: #ff6b6b;
        font-weight: bold;
        margin-top: 25px;
        font-size: 0.95rem;
        font-family: 'Geist Sans', sans-serif !important;
        letter-spacing: 0.5px;
    }
    
    /* 增加一點間距給中間的內容區塊 */
    .stMarkdown div p {
        margin-left: 5% !important;
    }
</style>
"""

# 注入 CSS
st.markdown(custom_css, unsafe_allow_html=True)

# 3. 建立網頁內容
st.markdown('<div class="hero-title">SteelClaw</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">THE AI DASHBOARD THAT ACTUALLY WORKS.</div>', unsafe_allow_html=True)
st.markdown('<h3 style="color:#f0f6fc; margin-left:5%; font-weight: 500;">〉What People Say</h3>', unsafe_allow_html=True)

# 4. 建立輪播卡片的 HTML 結構 (內容保持不變，只對應 CSS 改動)
cards_html = """
<div class="marquee-container">
    <div class="marquee-track">
        <div class="glass-card">"這個儀表板真的太狂了！解決了我們產線數據重複的痛點，而且介面超級帥！"<div class="card-user">@廠長_老王</div></div>
        <div class="glass-card">"自從用了 SteelClaw，我每天看報表的心情都變好了，那個動畫真的百看不厭。"<div class="card-user">@品管_小美</div></div>
        <div class="glass-card">"Why is this dashboard so nuts? It's fast, accurate, and looks like a startup."<div class="card-user">@TechBro</div></div>
        <div class="glass-card">"伸長率跟鍍層量的分析一目了然，Lottie 動畫簡直是神來一筆！"<div class="card-user">@數據分析師</div></div>
        
        <div class="glass-card">"這個儀表板真的太狂了！解決了我們產線數據重複的痛點，而且介面超級帥！"<div class="card-user">@廠長_老王</div></div>
        <div class="glass-card">"自從用了 SteelClaw，我每天看報表的心情都變好了，那個動畫真的百看不厭。"<div class="card-user">@品管_小美</div></div>
        <div class="glass-card">"Why is this dashboard so nuts? It's fast, accurate, and looks like a startup."<div class="card-user">@TechBro</div></div>
        <div class="glass-card">"伸長率跟鍍層量的分析一目了然，Lottie 動畫簡直是神來一筆！"<div class="card-user">@數據分析師</div></div>
    </div>
</div>
"""

st.markdown(cards_html, unsafe_allow_html=True)

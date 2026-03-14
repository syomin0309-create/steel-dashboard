import streamlit as st

# 1. 設定頁面為暗色模式的基礎底色
st.set_page_config(page_title="OpenClaw 風格測試", layout="wide")

# 2. 撰寫超炫的 CSS 動畫與玻璃特效
custom_css = """
<style>
    /* 設定全域星空黑背景與字體 */
    .stApp {
        background-color: #0b0f19;
        color: white;
    }

    /* 頂部大標題特效：漸層發光字體 */
    .hero-title {
        font-size: 5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #ff6b6b, #ff8e53);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .hero-subtitle {
        text-align: center;
        color: #8892b0;
        font-size: 1.2rem;
        margin-bottom: 50px;
    }

    /* =========================================
       🔥 核心動畫：無限輪播軌道 (Marquee)
       ========================================= */
    .marquee-container {
        width: 100%;
        overflow: hidden;
        position: relative;
        padding: 20px 0;
    }

    /* 讓兩組卡片排成一列，並執行 scroll 動畫 */
    .marquee-track {
        display: flex;
        width: calc(300px * 8); /* 假設有 8 張卡片，每張 300px */
        animation: scroll 15s linear infinite;
    }

    /* 當滑鼠移過去時，動畫暫停！ */
    .marquee-track:hover {
        animation-play-state: paused;
    }

    /* 定義滑動動畫關鍵影格 */
    @keyframes scroll {
        0% { transform: translateX(0); }
        100% { transform: translateX(calc(-300px * 4)); /* 往左推 4 張卡片的距離 */ }
    }

    /* =========================================
       🔮 卡片設計：玻璃擬物化 (Glassmorphism)
       ========================================= */
    .glass-card {
        width: 280px;
        min-width: 280px;
        margin-right: 20px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.03); /* 極低透明度的白色 */
        border: 1px solid rgba(255, 255, 255, 0.08); /* 微光的邊框 */
        border-radius: 16px;
        backdrop-filter: blur(10px); /* 背景模糊特效 */
        color: #ccd6f6;
        transition: transform 0.3s ease, border 0.3s ease;
    }

    /* 卡片浮起發光特效 */
    .glass-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(255, 107, 107, 0.5); /* 滑過變紅色邊框 */
        box-shadow: 0 10px 30px -10px rgba(255, 107, 107, 0.2);
    }

    .card-user {
        color: #ff6b6b;
        font-weight: bold;
        margin-top: 15px;
        font-size: 0.9rem;
    }
</style>
"""

# 注入 CSS
st.markdown(custom_css, unsafe_allow_html=True)

# 3. 建立網頁內容
st.markdown('<div class="hero-title">SteelClaw</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">THE AI DASHBOARD THAT ACTUALLY WORKS.</div>', unsafe_allow_html=True)
st.markdown('<h3 style="color:white; margin-left:5%;">〉What People Say</h3>', unsafe_allow_html=True)

# 4. 建立輪播卡片的 HTML 結構
# 為了讓無限輪播看起來沒有斷層，我們需要把相同的卡片複製兩份接在一起 (1234 + 1234)
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

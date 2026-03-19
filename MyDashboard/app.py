import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title="AegisCore", layout="wide", page_icon="👁️", initial_sidebar_state="expanded")

# 🎨 專業級視覺優化
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Microsoft JhengHei', 'Segoe UI', sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
    }
    .metric-highlight {
        padding: 15px;
        border-radius: 8px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-left: 4px solid #667eea;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)
# === 🌟 1. 貼在你原本的 CSS 下方 ===
openclaw_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Geist:wght@100..900&display=swap');
    
    /* 針對 Streamlit 的主容器 .stApp 設置星際背景 */
    .stApp {
        background-color: #0a0e17; /* 1. 基礎深藍黑背景色 */
        
        /* 2. 生成多層星星背景 (使用多個 radial-gradient 重疊) */
        background-image:
            /* 層 1: 小星星 (移動最快) */
            radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
            /* 層 2: 中星星 (移動其次) */
            radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px),
            /* 層 3: 星雲 (一個大型的 radial-gradient) */
            radial-gradient(circle at 20% 80%, rgba(70, 130, 180, 0.2), transparent 40%),
            radial-gradient(circle at 80% 20%, rgba(138, 43, 226, 0.2), transparent 40%);

        /* 3. 設置星星的大小和位置 */
        background-size:
            550px 550px, /* 層 1 大小 */
            350px 350px, /* 層 2 大小 */
            250px 250px, /* 層 3 大小 */
            100% 100%,   /* 層 4 (星雲) 大小 */
            100% 100%;   /* 層 5 (星雲) 大小 */

        /* 4. 加入動畫魔法 */
        animation:
            twinkle 5s ease-in-out infinite, /* 閃爍動畫 */
            parallax 15s linear infinite;    /* 移動動畫 */
            
        will-change: background-position; /* 提示 GPU 加速 */
    }
    
    /* 🌋 閃爍動畫 (改變透明度) */
    @keyframes twinkle {
        0%, 100% { opacity: 0.8; }
        50% { opacity: 1; }
    }

    /* 🚀 移動動畫 (改變背景位置，營造視差效果) */
    @keyframes parallax {
        0% { background-position: 0 0, 0 0, 0 0, 0 0, 0 0; }
        100% { background-position: -550px 0, -350px 0, -250px 0, 0 0, 0 0; } /* 小星星移動最快，中星星其次，大星星最慢 */
    }

    /* 🌋 火燙燙的熔岩大標題 */
    .hero-title {
        font-family: 'Geist Sans', sans-serif;
        font-size: 4.5rem;
        font-weight: 800;
        letter-spacing: -2px;
        text-align: center;
        margin-top: 10px;
        background-image: linear-gradient(135deg, 
                            #ff4500 0%,   /* 鮮豔的橙紅色 (火) */
                            #ffd700 25%,  /* 金黃色 (燙) */
                            #ff8c00 50%,  /* 橙色 */
                            #ff4500 75%,  /* 再回到鮮豔的橙紅色 */
                            #d2691e 100%  /* 巧克力色 (冷卻的金屬) */
                        );
        background-size: 200% auto; 
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: lava_flow 5s linear infinite; 
    }
    
    @keyframes lava_flow {
        0% { background-position: 0% 50%; } 
        100% { background-position: 200% 50%; } 
    }

    /* 👇 副標題排版 (保持原樣) 👇 */
    .hero-subtitle {
        font-family: 'Geist Sans', sans-serif;
        text-align: center; 
        color: #8b949e; 
        font-size: 1.1rem;
        letter-spacing: 2px; 
        margin-bottom: 20px;
    }
    
    /* 🎠 雙排字卡輪播 (保持原樣，記得靠左對齊！) */
    .marquee-container { 
        width: 100%; 
        overflow: hidden; 
        padding: 20px 0; 
        display: flex; 
        flex-direction: column; 
        gap: 25px; 
    }
    .marquee-track { 
        display: flex; 
        width: max-content; 
        animation: scroll 30s linear infinite; 
    }
    .marquee-track.reverse { animation-direction: reverse; }
    .marquee-track:hover { animation-play-state: paused; }
    @keyframes scroll { 0% { transform: translateX(0); } 100% { transform: translateX(-1280px); } }
    
    .glass-card {
        width: 300px; min-width: 300px; margin-right: 20px; padding: 20px;
        background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; 
        color: #c9d1d9; transition: all 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px); border-color: rgba(255, 107, 107, 0.4);
        box-shadow: 0 10px 20px rgba(255, 107, 107, 0.1);
    }
    .card-user { color: #ff6b6b; font-weight: bold; margin-top: 15px; }
</style>
"""
st.markdown(openclaw_css, unsafe_allow_html=True)

# --- Lottie 動畫讀取函式 ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# 預先載入動畫 (高科技掃描)
lottie_scanning = load_lottieurl("https://lottie.host/7e0b5030-80a5-4bf7-a931-bd6b7de583bc/Y90g3VvWqI.json")
@st.cache_data
def load_and_clean_data(file_bytes: bytes, file_name: str):
    import io
    if file_name.endswith('.csv'):
        try:
            df = pd.read_csv(io.BytesIO(file_bytes), encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(io.BytesIO(file_bytes), encoding='big5')
    else:
        df = pd.read_excel(io.BytesIO(file_bytes))
        
    # 🌟 徹底清除欄位名稱中的所有「空白、換行、不可見字元」
    df.columns = df.columns.astype(str).str.replace(r'\s+', '', regex=True).str.upper()
    
    # 📖 欄位對應字典
    rename_mapping = [
        (['鋼捲號碼', 'COIL_NO'], '產出鋼捲號碼'),
        (['PRODUCTION_DATE'], '生產日期'),
        (['QUALITY_CLASS'], '試驗等級'), # 已移除投入等級，避免誤判
        (['BASE_METAL_THICK'], '訂單厚度'),
        (['REAL_WIDTH'], '訂單寬度')
    ]
    
    rename_dict = {}
    for source_cols, target_name in rename_mapping:
        for col in source_cols:
            if col in df.columns:
                rename_dict[col] = target_name
                break
    
    df.rename(columns=rename_dict, inplace=True)
    
    if df.columns.duplicated().any():
        duplicated_cols = df.columns[df.columns.duplicated(keep=False)].unique()
        for col in duplicated_cols:
            indices = [i for i, x in enumerate(df.columns) if x == col]
            for idx in indices[1:]:
                df = df.drop(df.columns[idx], axis=1)

    # 🚀 自動計算雙面總鍍層量 
    xray_sets = [
        ['XRAY_A_T_N', 'XRAY_A_T_C', 'XRAY_A_T_S', 'XRAY_A_B_N', 'XRAY_A_B_C', 'XRAY_A_B_S'],
        ['NORTH_TOP_COAT_WEIGHT', 'CENTER_TOP_COAT_WEIGHT', 'SOUTH_TOP_COAT_WEIGHT', 
         'NORTH_BACK_COAT_WEIGHT', 'CENTER_BACK_COAT_WEIGHT', 'SOUTH_BACK_COAT_WEIGHT'],
        ['北正面鍍層', '中正面鍍層', '南正面鍍層', '北背面鍍層', '中背面鍍層', '南背面鍍層']
    ]
    
    best_set = None
    max_valid = -1
    
    for cols in xray_sets:
        if all(col in df.columns for col in cols):
            valid_count = df[cols].apply(pd.to_numeric, errors='coerce').notna().sum().sum()
            if valid_count > max_valid:
                max_valid = valid_count
                best_set = cols
                
    if best_set and max_valid > 0:
        for col in best_set:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df['雙面總鍍層量(AVG)'] = (df[best_set[0]] + df[best_set[1]] + df[best_set[2]]) / 3 + \
                                (df[best_set[3]] + df[best_set[4]] + df[best_set[5]]) / 3

    def extract_year_month(date_val):
        try:
            dt = pd.to_datetime(date_val)
            return f"{dt.year}年{dt.month}月"
        except:
            return str(date_val)
            
    if '生產日期' in df.columns:        
        df['生產年月'] = df['生產日期'].apply(extract_year_month)
    else:
        df['生產年月'] = '全區間'
        
    return df

# ============ 主頁面開始 ============

import base64

# --- 1. 讀取本地圖片並轉成編碼的輔助函數 ---
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# --- 2. 你的圖片檔名 (請確認與你資料夾內的名稱完全一致) ---
# 如果你換了名字，請把 "my_logo.png" 改掉
logo_filename = "MyDashboard/logo_zheng.png" 

try:
    img_base64 = get_image_base64(logo_filename)
    
    # --- 3. 定義 CSS 發光特效 ---
    # --- 重新定義 CSS：加上懸浮在右下角的魔法 ---
    glow_css = f"""
    <style>
    .glowing-logo {{
        position: fixed;      /* 絕對定位，讓它懸浮 */
        bottom: 80px;         /* 距離底部 30px */
        right: 30px;          /* 距離右邊 30px */
        width: 80px;          /* 稍微縮小一點，更精緻 */
        z-index: 9999;        /* 確保它永遠在最上層，不會被圖表擋住 */
        opacity: 0.6;         /* 預設稍微半透明，低調不突兀 */
        filter: drop-shadow(0px 0px 8px rgba(255, 50, 50, 0.6)); 
        transition: all 0.4s ease-in-out;
        cursor: pointer;
    }}
    /* 滑鼠移過去時的驚喜特效：變亮、發光增強、微微放大 */
    .glowing-logo:hover {{
        opacity: 1;           /* 恢復 100% 亮度 */
        filter: drop-shadow(0px 0px 20px rgba(255, 50, 50, 1));
        transform: scale(1.15) translateY(-5px); /* 微微放大並往上浮 */
    }}
    </style>
    """
    
    # 將 CSS 注入到網頁中
    st.markdown(glow_css, unsafe_allow_html=True)
    
    # 🌟 直接印出圖片 (完全不需要 col_logo 那些排版了)，CSS 會自動把它吸到右下角！
    st.markdown(f'<img src="data:image/png;base64,{img_base64}" class="glowing-logo">', unsafe_allow_html=True)
    
 
except FileNotFoundError:
    st.error(f"找不到圖片 {logo_filename}，請確認檔名和位置是否正確！")

with st.sidebar:
    st.header("⚙️ 儀表板控制中心")
    uploaded_file = st.file_uploader("📂 上傳產線 RAW DATA", type=["xlsx", "csv"])
    st.markdown("---")

    # ── Appearance toggle ─────────────────────────
    st.markdown("**🎨 Appearance**")
    theme_mode = st.radio(
        "外觀模式", ["Dark", "Light"],
        horizontal=True,
        label_visibility="collapsed",
        key="theme_mode"
    )
    st.markdown("---")

    if uploaded_file:
        st.success("✅ 文件已加載")
        st.caption(f"文件名：{uploaded_file.name}")

# ==========================================
# 🎨 主題系統
# ==========================================
_is_dark = (st.session_state.get("theme_mode", "Dark") == "Dark")

if _is_dark:
    T = dict(
        bg_app="#0a0e17", bg_panel="#101826", bg_chart="#0c1220",
        text_p="#c8dde8", text_s="#5a7a8e", text_dim="#2e4455",
        border="#1c2e42", grid="#1c2e42",
        bar_in="rgba(0,180,220,0.55)", bar_out="rgba(255,59,59,0.75)",
        bar_border="rgba(255,255,255,0.08)",
        curve="#f5a623", line_mean="#39e07a", line_spec="#ff3b3b",
        line_target="#00d4ff", line_dot="rgba(0,212,255,0.12)",
        abnormal="#FFD700", hover_bg="rgba(12,18,32,0.95)",
        legend_bg="rgba(12,18,32,0.85)", card_bg="#101826",
        stat_bg="#101826", ann_bg="rgba(10,16,24,0.85)",
        title_color="#5a7a8e",
    )
else:
    T = dict(
        bg_app="#f4f6f9", bg_panel="#ffffff", bg_chart="#ffffff",
        text_p="#1a2332", text_s="#546e7a", text_dim="#90a4ae",
        border="#e0e7ef", grid="#e8edf2",
        bar_in="rgba(253,211,78,0.88)", bar_out="rgba(220,38,38,0.72)",
        bar_border="rgba(50,50,50,0.12)",
        curve="#1a2332", line_mean="#059669", line_spec="#dc2626",
        line_target="#2563eb", line_dot="rgba(37,99,235,0.06)",
        abnormal="#f59e0b", hover_bg="rgba(255,255,255,0.98)",
        legend_bg="rgba(255,255,255,0.95)", card_bg="#ffffff",
        stat_bg="#f8fafc", ann_bg="rgba(255,255,255,0.92)",
        title_color="#546e7a",
    )

_theme_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Space+Mono:wght@400;700&display=swap');
.stApp {{ background-color: {T['bg_app']} !important; }}
section[data-testid="stSidebar"] {{
    background-color: {T['bg_panel']} !important;
    border-right: 1px solid {T['border']} !important;
}}
.spc-metric-card {{ background: {T['card_bg']} !important; border: 1px solid {T['border']} !important; }}
.spc-card-label, .spc-card-desc {{ color: {T['text_s']} !important; }}
.spc-card-value {{ color: {T['text_p']} !important; }}
.spc-stats-bar {{ background: {T['stat_bg']} !important; border-color: {T['border']} !important; }}
.spc-stat-cell {{ border-color: {T['border']} !important; }}
.spc-stat-val {{ color: {T['text_p']} !important; }}
.spc-stat-label {{ color: {T['text_s']} !important; }}
.spc-gauge-track {{ background: {T['border']} !important; }}
.spc-section-title {{ color: {T['text_s']} !important; }}
</style>
"""

# Light mode overrides for hardcoded dark elements
if not _is_dark:
    _theme_css += """
<style>
.hero-title {
    background-image: linear-gradient(135deg,
        #1a3a5c 0%, #2563eb 30%, #0d9488 60%, #1a3a5c 100%) !important;
    background-size: 200% auto !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}
.hero-subtitle { color: #546e7a !important; }
.glass-card {
    background: rgba(255,255,255,0.7) !important;
    border: 1px solid #e0e7ef !important;
    color: #1a2332 !important;
}
.card-user { color: #2563eb !important; }
.stApp {
    background-color: #f4f6f9 !important;
    background-image:
        linear-gradient(rgba(37,99,235,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(37,99,235,0.04) 1px, transparent 1px) !important;
    background-size: 40px 40px !important;
    animation: none !important;
}
</style>
"""

st.markdown(_theme_css, unsafe_allow_html=True)

# ==========================================
# 🌟 動畫與分析邏輯切換區塊
# ==========================================
if uploaded_file is None:
    # 1. 顯示 AegisCore 漸層大標題與副標題
    st.markdown('<div class="hero-title">AegisCore</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">UNIFYING STEEL DATA. EMPOWERING DECISIONS.</div>', unsafe_allow_html=True)
    
    # 2. 顯示 Lottie 高科技掃描動畫 (放在畫面中間)
    if lottie_scanning:
        # 我把高度稍微調小一點，讓畫面更緊湊
        st_lottie(lottie_scanning, height=200, key="scanning")
        
    # 3. 顯示高級感無限輪播卡片 (放在動畫下方)
    # 把這整塊貼上去，裡面的 HTML 前面不要留空白喔！
    cards_html = """<div class="marquee-container">
<div class="marquee-track">
<div class="glass-card">"這個儀表板真的太狂了！解決了我們產線數據重複的痛點，而且介面超級帥！"<div class="card-user">@廠長_老王</div></div>
<div class="glass-card">"自從用了 AegisCore，我每天看報表的心情都變好了，那個動畫真的百看不厭。"<div class="card-user">@品管_小美</div></div>
<div class="glass-card">"Why is this dashboard so nuts? It's fast, accurate, and looks like a startup."<div class="card-user">@TechBro</div></div>
<div class="glass-card">"伸長率跟鍍層量的分析一目了然，Lottie 動畫簡直是神來一筆！"<div class="card-user">@數據分析師</div></div>
<div class="glass-card">"這個儀表板真的太狂了！解決了我們產線數據重複的痛點，而且介面超級帥！"<div class="card-user">@廠長_老王</div></div>
<div class="glass-card">"自從用了 AegisCore，我每天看報表的心情都變好了，那個動畫真的百看不厭。"<div class="card-user">@品管_小美</div></div>
<div class="glass-card">"Why is this dashboard so nuts? It's fast, accurate, and looks like a startup."<div class="card-user">@TechBro</div></div>
<div class="glass-card">"伸長率跟鍍層量的分析一目了然，Lottie 動畫簡直是神來一筆！"<div class="card-user">@數據分析師</div></div>
</div>
<div class="marquee-track reverse">
<div class="glass-card">"再也不用手動合併 Excel 了，這套系統完全解放了我的雙手！"<div class="card-user">@產線工程師</div></div>
<div class="glass-card">"主管看到這個介面，直接問我是不是發包給外面的專業設計公司做的 😂"<div class="card-user">@開發者本人</div></div>
<div class="glass-card">"The melting lava text is just *chef's kiss*. UI/UX on point."<div class="card-user">@DesignNerd</div></div>
<div class="glass-card">"異常鋼捲的黃色標記超級明顯，抓良率問題的速度直接快了三倍！"<div class="card-user">@QA_Team</div></div>
<div class="glass-card">"再也不用手動合併 Excel 了，這套系統完全解放了我的雙手！"<div class="card-user">@產線工程師</div></div>
<div class="glass-card">"主管看到這個介面，直接問我是不是發包給外面的專業設計公司做的 😂"<div class="card-user">@開發者本人</div></div>
<div class="glass-card">"The melting lava text is just *chef's kiss*. UI/UX on point."<div class="card-user">@DesignNerd</div></div>
<div class="glass-card">"異常鋼捲的黃色標記超級明顯，抓良率問題的速度直接快了三倍！"<div class="card-user">@QA_Team</div></div>
</div>
</div>"""
    st.markdown(cards_html, unsafe_allow_html=True)

else:
    # 狀態 2：檔案已上傳 -> 執行你原本寫好的資料清洗與分析
    raw_df = load_and_clean_data(uploaded_file.read(), uploaded_file.name)
    df = raw_df.copy()
    # 👇👇 下面這些通通都幫你往右縮排好了 (包含 if, else, 側邊欄與函式) 👇👇
    
    # 🧠 模式判定與空值精準過濾
    if '試驗等級' in df.columns:
        df = df.dropna(subset=['試驗等級'])
        df['試驗等級'] = df['試驗等級'].astype(str).str.strip()
        df = df[df['試驗等級'] != '']
        df = df[~df['試驗等級'].str.lower().isin(['nan', 'null', 'none', 'na'])]
        df["比對群組"] = df["生產年月"] + " - " + df["試驗等級"]
    else:
        df["比對群組"] = "全批次數據"

    # 側邊欄：智能連動篩選器
    with st.sidebar:
        st.subheader("🎯 智能連動篩選器")
        st.caption("💡 條件即時連動，支援跨月多選")

        file_key = uploaded_file.name

        def create_cascading_filter(col_name, current_df):
            if col_name not in current_df.columns:
                return []
            
            valid_opts = sorted(current_df[col_name].dropna().astype(str).unique())
            if not valid_opts:
                return []
            
            key_name = f"filter_{file_key}_{col_name}"
            
            if key_name in st.session_state:
                st.session_state[key_name] = [x for x in st.session_state[key_name] if x in valid_opts]
            
            selected = st.multiselect(f"🔹 選擇 {col_name}", options=valid_opts, key=key_name)
            return selected
        
        # (這裡下面應該接著你原本呼叫 create_cascading_filter 的程式碼，請確保它們也跟 def 切齊)
        # 瀑布流連動過濾
        f_month = create_cascading_filter('生產年月', df)
        df_f1 = df.copy()
        if f_month: df_f1 = df_f1[df_f1['生產年月'].astype(str).isin(f_month)]
            
        f_thick = create_cascading_filter('訂單厚度', df_f1)
        df_f2 = df_f1.copy()
        if f_thick: df_f2 = df_f2[df_f2['訂單厚度'].astype(str).isin(f_thick)]
            
        f_width = create_cascading_filter('訂單寬度', df_f2)
        df_f3 = df_f2.copy()
        if f_width: df_f3 = df_f3[df_f3['訂單寬度'].astype(str).isin(f_width)]
            
        f_mat = create_cascading_filter('熱軋材質', df_f3)
        df_f4 = df_f3.copy()
        if f_mat: df_f4 = df_f4[df_f4['熱軋材質'].astype(str).isin(f_mat)]
            
        f_spec = create_cascading_filter('產品規格代碼', df_f4)
        df_f5 = df_f4.copy()
        if f_spec: df_f5 = df_f5[df_f5['產品規格代碼'].astype(str).isin(f_spec)]
            
        f_up_coat = create_cascading_filter('上鍍層', df_f5)
        df_f6 = df_f5.copy()
        if f_up_coat: df_f6 = df_f6[df_f6['上鍍層'].astype(str).isin(f_up_coat)]
        
    filtered_df = df_f6.copy()

    if filtered_df.empty:
        st.warning("⚠️ 目前篩選條件下沒有找到任何數據，請放寬左側的篩選條件！")
    else:
        # ============ 移除 Tabs，直接顯示單一核心分析介面 ============
        st.markdown("### 🔍 選擇分析參數")
        
        numeric_cols = filtered_df.select_dtypes(include=['number']).columns.tolist()
        exclude_sys = ['產出鋼捲號碼', '試驗等級', '投入等級', '生產日期', '比對群組', '生產年月', 'SHIFT_NO', '鍍層下限管制值',
                       '北正面鍍層', '中正面鍍層', '南正面鍍層', '北背面鍍層', '中背面鍍層', '南背面鍍層',
                       'XRAY_A_T_N', 'XRAY_A_T_C', 'XRAY_A_T_S', 'XRAY_A_B_N', 'XRAY_A_B_C', 'XRAY_A_B_S',
                       'NORTH_TOP_COAT_WEIGHT', 'CENTER_TOP_COAT_WEIGHT', 'SOUTH_TOP_COAT_WEIGHT', 
                       'NORTH_BACK_COAT_WEIGHT', 'CENTER_BACK_COAT_WEIGHT', 'SOUTH_BACK_COAT_WEIGHT',
                       '開始時間', '排程單號', '結束時間', '班次', '產出內徑', '上粗糙度', '下粗糙度',
                       '化成', '切除米數', '收捲方向', '藥劑代號[化驗用]', '規範代碼', '鈍化藥劑批號', '訂購量(KG)',
                       '訂單合約限重-下限', '訂單合約限重-上限', '中波(波高)', '邊波(波高)', '橫向翹曲(波高)', '縱向翹曲(波高)', '中波(波長)',
                       '邊波(波長)', '建議套筒厚度', 'AIM符號', 'AIRKNIFE電量', '引帶號碼', '引帶捲入口銲接重量', '引帶出口殘餘銲接重量',
                       '降伏強度[(MIN.)規格值]', '降伏強度[(MAX.)規格值]', '降伏強度[(MIN.)管制值]', '降伏強度[(MAX.)管制值]',
                       '抗拉強度[(MIN.)規格值]', '抗拉強度[(MAX.)規格值]', '抗拉強度[(MIN.)管制值]', '抗拉強度[(MAX.)管制值]',
                       '伸長率[(MIN.)規格值]', '伸長率[(MAX.)規格值]', '伸長率[(MIN.)管制值]', '伸長率[(MAX.)管制值]','伸長率[(MIN.)客戶要求]', '伸長率[(MAX.)客戶要求]',
                       '降伏強度[(MIN.)客戶要求]', '降伏強度[(MAX.)客戶要求]', '抗拉強度[(MIN.)客戶要求]', '抗拉強度[(MAX.)客戶要求]',
                       '抗拉/降伏[(MIN.)標準值]', '抗拉/降伏[(MAX.)標準值]]', '硬度[(MIN.)客戶要求]', '硬度[(MAX.)客戶要求]',
                       '硬度[(MIN.)規格值]', '硬度[(MAX.)規格值]', '硬度[(MIN.)管制值]', '硬度指數[N值]','額外加測','斷裂點',
                       '訂單厚度', '訂單寬度', '原料厚度', '原料寬度','投入厚度','投入寬度','投入重量','實測重量','實測厚度','實測寬度','實測長度',]
        
        available_params = [col for col in numeric_cols if col not in exclude_sys]
        
        if '雙面總鍍層量(AVG)' in available_params:
            available_params = ['雙面總鍍層量(AVG)'] + [x for x in available_params if x != '雙面總鍍層量(AVG)']
        
        if available_params:
            col_select, col_info = st.columns([3, 1])
            with col_select:
                selected_param = st.selectbox("請選擇要查看的指標", available_params, key=f"param_{uploaded_file.name}", label_visibility="collapsed")
            
            plot_df = filtered_df.dropna(subset=[selected_param])
            
            if not plot_df.empty:
                avg_val = plot_df[selected_param].mean()
                std_val = plot_df[selected_param].std()
                median_val = plot_df[selected_param].median()
                
                if pd.isna(avg_val): avg_val = 0.0
                if pd.isna(std_val): std_val = 0.0
                
                # ═══════════════════════════════════════════════
                # SPC 規格設定
                # ═══════════════════════════════════════════════
                st.markdown("### 📐 SPC 規格設定")

                dynamic_key = f"{selected_param}_{len(plot_df)}"
                default_lsl = float(avg_val - 4 * std_val) if std_val > 0 else float(avg_val - 10)
                default_usl = float(avg_val + 4 * std_val) if std_val > 0 else float(avg_val + 10)

                spec_col1, spec_col2, spec_col3 = st.columns(3)
                with spec_col1:
                    lsl = st.number_input("規格下限 (LSL)", value=default_lsl, key=f"lsl_{dynamic_key}")
                with spec_col2:
                    usl = st.number_input("規格上限 (USL)", value=default_usl, key=f"usl_{dynamic_key}")
                with spec_col3:
                    target = st.number_input("規格中心值 (Target)", value=float((default_usl + default_lsl) / 2), key=f"tar_{dynamic_key}")

                # ── 正確公式計算 (依教材 Ca/Cp/Cpk) ──────────────
                cp  = (usl - lsl) / (6 * std_val) if std_val > 0 else 0.0
                ca  = (avg_val - target) / ((usl - lsl) / 2) * 100 if usl != lsl else 0.0   # 有正負號
                cpk = cp * (1 - abs(ca) / 100)                                               # Cpk = Cp × (1 - |Ca|)

                # ── 五級評價函式 ────────────────────────────────
                def grade_ca(ca_abs):
                    if ca_abs < 6.25:  return "A+", "#39e07a", "製程準確極佳"
                    if ca_abs < 12.5:  return "A",  "#00d4ff", "準確度良好"
                    if ca_abs < 25.0:  return "B",  "#f5a623", "尚可，建議調整 Offset"
                    if ca_abs < 50.0:  return "C",  "#ff7c3b", "能力不足，需調整參數"
                    return                     "D",  "#ff3b3b", "能力極差，立即處理"

                def grade_cp(val):
                    if val >= 1.67: return "A+", "#39e07a", "製程精密極佳"
                    if val >= 1.33: return "A",  "#00d4ff", "精密度良好"
                    if val >= 1.00: return "B",  "#f5a623", "尚可，加強管制"
                    if val >= 0.67: return "C",  "#ff7c3b", "能力不足，查原因"
                    return                  "D",  "#ff3b3b", "能力極差，全面檢討"

                ca_grade, ca_color, ca_desc   = grade_ca(abs(ca))
                cp_grade, cp_color, cp_desc   = grade_cp(cp)
                cpk_grade, cpk_color, cpk_desc = grade_cp(cpk)

                # 規格符合率計算
                outside_usl = len(plot_df[plot_df[selected_param] > usl])
                outside_lsl = len(plot_df[plot_df[selected_param] < lsl])
                inside      = len(plot_df) - outside_usl - outside_lsl
                yield_pct   = inside / len(plot_df) * 100 if len(plot_df) > 0 else 0.0
                if yield_pct >= 99.73: yield_grade, yield_color = "A+", "#39e07a"
                elif yield_pct >= 99:  yield_grade, yield_color = "A",  "#00d4ff"
                elif yield_pct >= 95:  yield_grade, yield_color = "B",  "#f5a623"
                else:                  yield_grade, yield_color = "D",  "#ff3b3b"

                # ── 工業儀表卡片 CSS (注入一次) ─────────────────
                st.markdown("""
                <style>
                .spc-section-title {
                    font-family: 'Rajdhani', 'Microsoft JhengHei', sans-serif;
                    font-size: 0.65rem;
                    letter-spacing: 3px;
                    color: #5a7a8e;
                    text-transform: uppercase;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    margin: 18px 0 10px 0;
                }
                .spc-section-title::after {
                    content: '';
                    flex: 1;
                    height: 1px;
                    background: linear-gradient(90deg, #1c2e42, transparent);
                }
                .spc-metric-card {
                    background: #101826;
                    border: 1px solid #1c2e42;
                    border-radius: 8px;
                    padding: 16px 18px 14px 18px;
                    position: relative;
                    overflow: hidden;
                    transition: border-color 0.3s;
                }
                .spc-metric-card::before {
                    content: '';
                    position: absolute;
                    top: 0; left: 0; right: 0;
                    height: 2px;
                    background: var(--card-top, #1c2e42);
                    opacity: 0.8;
                }
                .spc-metric-card::after {
                    content: '';
                    position: absolute;
                    bottom: 0; left: 0; right: 0;
                    height: 2px;
                    background: var(--card-top, #1c2e42);
                    opacity: 0.3;
                }
                .spc-card-label {
                    font-family: 'Space Mono', 'Courier New', monospace;
                    font-size: 0.58rem;
                    letter-spacing: 2px;
                    color: #5a7a8e;
                    text-transform: uppercase;
                    margin-bottom: 6px;
                }
                .spc-card-header {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    margin-bottom: 2px;
                }
                .spc-grade-badge {
                    font-family: 'Rajdhani', monospace;
                    font-size: 0.75rem;
                    font-weight: 700;
                    padding: 2px 9px;
                    border-radius: 3px;
                    border: 1px solid currentColor;
                    letter-spacing: 1px;
                }
                .spc-card-value {
                    font-family: 'Rajdhani', 'Microsoft JhengHei', sans-serif;
                    font-size: 2.0rem;
                    font-weight: 700;
                    line-height: 1.1;
                    letter-spacing: -0.5px;
                    margin: 4px 0 2px 0;
                }
                .spc-card-desc {
                    font-family: 'Space Mono', monospace;
                    font-size: 0.58rem;
                    color: #5a7a8e;
                    margin-bottom: 8px;
                }
                .spc-gauge-track {
                    height: 3px;
                    background: #1c2e42;
                    border-radius: 2px;
                    overflow: hidden;
                    margin-top: 6px;
                }
                .spc-gauge-fill {
                    height: 100%;
                    border-radius: 2px;
                    transition: width 0.6s ease;
                }
                .spc-stats-bar {
                    background: #101826;
                    border: 1px solid #1c2e42;
                    border-radius: 8px;
                    display: grid;
                    grid-template-columns: repeat(6, 1fr);
                    overflow: hidden;
                    margin: 10px 0 0 0;
                }
                .spc-stat-cell {
                    padding: 10px 8px;
                    text-align: center;
                    border-right: 1px solid #1c2e42;
                }
                .spc-stat-cell:last-child { border-right: none; }
                .spc-stat-label {
                    font-family: 'Space Mono', monospace;
                    font-size: 0.52rem;
                    color: #5a7a8e;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                    margin-bottom: 3px;
                }
                .spc-stat-val {
                    font-family: 'Space Mono', monospace;
                    font-size: 0.78rem;
                    color: #c8dde8;
                    font-weight: 700;
                }
                </style>
                """, unsafe_allow_html=True)

                # ── 製程能力指標標題 ─────────────────────────────
                st.markdown('<div class="spc-section-title">▸ 製程能力指標</div>', unsafe_allow_html=True)

                mc1, mc2, mc3, mc4 = st.columns(4)

                # 樣本數卡片
                with mc1:
                    st.markdown(f"""
                    <div class="spc-metric-card" style="--card-top:#00d4ff">
                        <div class="spc-card-label">樣本數 · N</div>
                        <div class="spc-card-value" style="color:#c8dde8">{len(plot_df)}</div>
                        <div class="spc-card-desc">{'✓ 達統計需求 (≥30)' if len(plot_df) >= 30 else '⚠ 樣本數不足 (<30)'}</div>
                        <div class="spc-gauge-track">
                            <div class="spc-gauge-fill" style="width:{min(len(plot_df)/30*100,100):.0f}%;background:#00d4ff;box-shadow:0 0 5px #00d4ff"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Ca 卡片
                with mc2:
                    ca_gauge = min(abs(ca), 100)
                    ca_sign_label = f"{'▲ 偏高' if ca > 0 else '▼ 偏低'}  {abs(ca):.2f}%"
                    st.markdown(f"""
                    <div class="spc-metric-card" style="--card-top:{ca_color}">
                        <div class="spc-card-header">
                            <div class="spc-card-label">Ca · 準確度</div>
                            <span class="spc-grade-badge" style="color:{ca_color};border-color:{ca_color};background:{ca_color}18">{ca_grade}</span>
                        </div>
                        <div class="spc-card-value" style="color:{ca_color}">{abs(ca):.1f}%</div>
                        <div class="spc-card-desc">{ca_sign_label} · {ca_desc}</div>
                        <div class="spc-gauge-track">
                            <div class="spc-gauge-fill" style="width:{ca_gauge:.0f}%;background:{ca_color};box-shadow:0 0 5px {ca_color}"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Cp 卡片
                with mc3:
                    cp_gauge = min(cp / 2.0 * 100, 100)
                    st.markdown(f"""
                    <div class="spc-metric-card" style="--card-top:{cp_color}">
                        <div class="spc-card-header">
                            <div class="spc-card-label">Cp · 精密度</div>
                            <span class="spc-grade-badge" style="color:{cp_color};border-color:{cp_color};background:{cp_color}18">{cp_grade}</span>
                        </div>
                        <div class="spc-card-value" style="color:{cp_color}">{cp:.3f}</div>
                        <div class="spc-card-desc">{cp_desc}</div>
                        <div class="spc-gauge-track">
                            <div class="spc-gauge-fill" style="width:{cp_gauge:.0f}%;background:{cp_color};box-shadow:0 0 5px {cp_color}"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Cpk 卡片
                with mc4:
                    cpk_gauge = min(cpk / 2.0 * 100, 100)
                    st.markdown(f"""
                    <div class="spc-metric-card" style="--card-top:{cpk_color}">
                        <div class="spc-card-header">
                            <div class="spc-card-label">Cpk · 製程能力</div>
                            <span class="spc-grade-badge" style="color:{cpk_color};border-color:{cpk_color};background:{cpk_color}18">{cpk_grade}</span>
                        </div>
                        <div class="spc-card-value" style="color:{cpk_color}">{cpk:.3f}</div>
                        <div class="spc-card-desc">{cpk_desc}</div>
                        <div class="spc-gauge-track">
                            <div class="spc-gauge-fill" style="width:{cpk_gauge:.0f}%;background:{cpk_color};box-shadow:0 0 5px {cpk_color}"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # ── 統計摘要列 ───────────────────────────────────
                cv = (std_val / avg_val * 100) if avg_val != 0 else 0
                st.markdown(f"""
                <div class="spc-stats-bar">
                    <div class="spc-stat-cell">
                        <div class="spc-stat-label">平均值 X̄</div>
                        <div class="spc-stat-val">{avg_val:.4f}</div>
                    </div>
                    <div class="spc-stat-cell">
                        <div class="spc-stat-label">中位數</div>
                        <div class="spc-stat-val">{median_val:.4f}</div>
                    </div>
                    <div class="spc-stat-cell">
                        <div class="spc-stat-label">標準差 σ</div>
                        <div class="spc-stat-val">{std_val:.4f}</div>
                    </div>
                    <div class="spc-stat-cell">
                        <div class="spc-stat-label">變異係數</div>
                        <div class="spc-stat-val">{cv:.2f}%</div>
                    </div>
                    <div class="spc-stat-cell">
                        <div class="spc-stat-label">最小值</div>
                        <div class="spc-stat-val">{plot_df[selected_param].min():.4f}</div>
                    </div>
                    <div class="spc-stat-cell">
                        <div class="spc-stat-label">最大值</div>
                        <div class="spc-stat-val">{plot_df[selected_param].max():.4f}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # ── 視覺分析標題 ─────────────────────────────────
                st.markdown('<div class="spc-section-title" style="margin-top:22px">▸ 視覺分析</div>', unsafe_allow_html=True)

                chart_col1, chart_col2 = st.columns([1.6, 1])

                # ── 直方圖 (規格外自動標紅) ──────────────────────
                with chart_col1:
                    hist_data  = plot_df[selected_param].dropna().values
                    bin_count  = 30
                    data_min, data_max = hist_data.min(), hist_data.max()

                    # 展開軸範圍，讓 LSL/USL 線可見
                    pad        = std_val * 1.5
                    axis_min   = min(data_min, lsl) - pad
                    axis_max   = max(data_max, usl) + pad
                    step       = (axis_max - axis_min) / bin_count
                    edges      = [axis_min + i * step for i in range(bin_count + 1)]
                    counts     = [0] * bin_count

                    for v in hist_data:
                        idx = int((v - axis_min) / step)
                        idx = max(0, min(bin_count - 1, idx))
                        counts[idx] += 1

                    # 依規格著色：規格外 → 紅；規格內 → 主題色
                    bar_colors = []
                    for i in range(bin_count):
                        lo, hi = edges[i], edges[i + 1]
                        if hi <= lsl or lo >= usl:
                            bar_colors.append(T['bar_out'])
                        else:
                            bar_colors.append(T['bar_in'])

                    bar_centers = [(edges[i] + edges[i+1]) / 2 for i in range(bin_count)]

                    fig_hist = go.Figure()

                    # 柱狀圖
                    fig_hist.add_trace(go.Bar(
                        x=bar_centers,
                        y=counts,
                        width=[step * 0.98] * bin_count,
                        marker=dict(
                            color=bar_colors,
                            line=dict(width=0.5, color=T['bar_border'])
                        ),
                        name="分布",
                        hovertemplate="區間中心: %{x:.4f}<br>次數: %{y}<extra></extra>"
                    ))

                    # 常態曲線
                    if std_val > 0:
                        x_curve = np.linspace(axis_min, axis_max, 300)
                        y_pdf   = (1 / (std_val * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_curve - avg_val) / std_val) ** 2)
                        y_curve = y_pdf * len(hist_data) * step
                        fig_hist.add_trace(go.Scatter(
                            x=x_curve, y=y_curve, mode='lines',
                            line=dict(color=T['curve'], width=2.5),
                            name='常態曲線'
                        ))

                    # 規格線
                    max_y = max(counts) * 1.25 if counts else 10
                    for xval, label, color, dash in [
                        (lsl,    f"LSL: {lsl:.4f}",      T['line_spec'],   "solid"),
                        (usl,    f"USL: {usl:.4f}",      T['line_spec'],   "solid"),
                        (target, f"Target: {target:.4f}", T['line_target'], "dash"),
                        (avg_val,f"X̄: {avg_val:.4f}",    T['line_mean'],   "dot"),
                    ]:
                        fig_hist.add_vline(
                            x=xval, line_dash=dash, line_color=color, line_width=1.8,
                            annotation=dict(
                                text=label, font=dict(color=color, size=10),
                                bgcolor=T['ann_bg'], bordercolor=color,
                                borderwidth=1, borderpad=3
                            )
                        )

                    fig_hist.update_layout(
                        title=dict(
                            text=f"【{selected_param}】 直方圖 · 常態分佈",
                            font=dict(color=T['title_color'], size=12, family="Space Mono, monospace"),
                            x=0
                        ),
                        height=420,
                        plot_bgcolor=T['bg_chart'],
                        paper_bgcolor=T['bg_panel'],
                        font=dict(color=T['text_p']),
                        xaxis=dict(
                            gridcolor=T['grid'], zerolinecolor=T['grid'],
                            title=dict(text=selected_param, font=dict(color=T['text_s'], size=10)),
                            tickfont=dict(size=9, color=T['text_s']),
                        ),
                        yaxis=dict(
                            gridcolor=T['grid'], zerolinecolor=T['grid'],
                            title=dict(text="次數 (Frequency)", font=dict(color=T['text_s'], size=10)),
                            tickfont=dict(size=9, color=T['text_s']),
                        ),
                        legend=dict(
                            bgcolor=T['legend_bg'], bordercolor=T['border'], borderwidth=1,
                            font=dict(size=10, color=T['text_p'])
                        ),
                        bargap=0,
                        margin=dict(t=60, b=50, l=50, r=20)
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)

                # ── 規格符合率圓餅圖 ─────────────────────────────
                with chart_col2:
                    pie_values = [inside, outside_usl, outside_lsl]
                    pie_names  = ['符合規格', '超過上限 (>USL)', '低於下限 (<LSL)']
                    pie_colors = ['#00b4dc', '#ff3b3b', '#f5a623'] if _is_dark else ['#2563eb', '#dc2626', '#f59e0b']

                    fig_pie = go.Figure(go.Pie(
                        values=pie_values,
                        labels=pie_names,
                        marker=dict(
                            colors=pie_colors,
                            line=dict(color=T['bg_chart'], width=2)
                        ),
                        textinfo='label+percent',
                        textfont=dict(size=10, color=T['text_p']),
                        hole=0.42,
                        hovertemplate="%{label}<br>數量: %{value} 顆<br>佔比: %{percent}<extra></extra>"
                    ))

                    fig_pie.add_annotation(
                        text=f"<b>{yield_pct:.1f}%</b><br><span style='font-size:10px'>良品率</span>",
                        x=0.5, y=0.5, showarrow=False,
                        font=dict(size=16, color=yield_color, family="Rajdhani, sans-serif"),
                        align="center"
                    )

                    fig_pie.update_layout(
                        title=dict(
                            text="規格符合率",
                            font=dict(color=T['title_color'], size=12, family="Space Mono, monospace"),
                            x=0
                        ),
                        height=420,
                        paper_bgcolor=T['bg_panel'],
                        plot_bgcolor=T['bg_panel'],
                        font=dict(color=T['text_p']),
                        legend=dict(
                            bgcolor=T['legend_bg'], bordercolor=T['border'], borderwidth=1,
                            font=dict(size=10, color=T['text_p']),
                            orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5
                        ),
                        margin=dict(t=60, b=60, l=20, r=20)
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)

                # ═══════════════════════════════════════════════
                # 生產順序異常監控圖（主題化）
                # ═══════════════════════════════════════════════
                st.markdown('<div class="spc-section-title" style="margin-top:22px">▸ 生產順序異常監控圖</div>', unsafe_allow_html=True)

                x_axis_col = "產出鋼捲號碼" if "產出鋼捲號碼" in plot_df.columns else None
                x_data = plot_df[x_axis_col] if x_axis_col else list(range(len(plot_df)))
                x_label = "鋼捲號碼" if x_axis_col else "生產順序"

                fig_line = go.Figure()

                # 主趨勢線
                hover_extra = ("<br><b>試驗等級:</b> %{customdata}"
                               if '試驗等級' in plot_df.columns else "")
                fig_line.add_trace(go.Scatter(
                    x=x_data,
                    y=plot_df[selected_param],
                    mode='lines+markers',
                    line=dict(color=T['line_target'], width=1.4),
                    marker=dict(size=4, color=T['line_target'], opacity=0.7),
                    customdata=plot_df['試驗等級'] if '試驗等級' in plot_df.columns else None,
                    hovertemplate=(
                        f"<b>{x_label}:</b> %{{x}}<br>"
                        f"<b>{selected_param}:</b> %{{y:.4f}}"
                        + hover_extra + "<extra></extra>"
                    ),
                    name=selected_param,
                ))

                # 異常點（7B）
                abnormal_df = pd.DataFrame()
                if '試驗等級' in plot_df.columns:
                    abnormal_df = plot_df[
                        plot_df['試驗等級'].astype(str).str.upper()
                        .str.replace(' ', '').str.contains('7B', na=False)
                    ]
                    if not abnormal_df.empty:
                        x_abn = abnormal_df[x_axis_col] if x_axis_col else abnormal_df.index
                        fig_line.add_trace(go.Scatter(
                            x=x_abn, y=abnormal_df[selected_param],
                            mode='markers',
                            marker=dict(
                                color=T['abnormal'], size=10, symbol='circle',
                                line=dict(color=T['bg_chart'], width=1.5)
                            ),
                            name='異常 (7B)',
                            hovertemplate=f"<b>異常鋼捲</b><br>{x_label}: %{{x}}<br>數值: %{{y:.4f}}<extra></extra>",
                        ))

                # 規格帶、目標線、USL、LSL
                fig_line.add_hrect(
                    y0=lsl, y1=usl, line_width=0,
                    fillcolor=T['line_dot'], opacity=1
                )
                for yval, label, color, dash in [
                    (usl,    f"USL: {usl:.4f}",      T['line_spec'],   "solid"),
                    (lsl,    f"LSL: {lsl:.4f}",      T['line_spec'],   "solid"),
                    (target, f"Target: {target:.4f}", T['line_target'], "dash"),
                ]:
                    fig_line.add_hline(
                        y=yval, line_dash=dash, line_color=color, line_width=1.6,
                        annotation=dict(
                            text=label, font=dict(color=color, size=10),
                            bgcolor=T['ann_bg'], bordercolor=color,
                            borderwidth=1, borderpad=3, xanchor="right"
                        )
                    )

                fig_line.update_layout(
                    title=dict(
                        text=f"【{selected_param}】 單一趨勢管制圖",
                        font=dict(color=T['title_color'], size=12, family="Space Mono, monospace"), x=0
                    ),
                    height=400,
                    plot_bgcolor=T['bg_chart'],
                    paper_bgcolor=T['bg_panel'],
                    font=dict(color=T['text_p']),
                    xaxis=dict(
                        showticklabels=False,
                        title=dict(text=f"生產順序 ({x_label})", font=dict(color=T['text_s'], size=10)),
                        gridcolor=T['grid'], zerolinecolor=T['grid'],
                        tickfont=dict(size=9, color=T['text_s']),
                    ),
                    yaxis=dict(
                        gridcolor=T['grid'], zerolinecolor=T['grid'],
                        title=dict(text=selected_param, font=dict(color=T['text_s'], size=10)),
                        tickfont=dict(size=9, color=T['text_s']),
                    ),
                    legend=dict(
                        bgcolor=T['legend_bg'], bordercolor=T['border'], borderwidth=1,
                        font=dict(size=10, color=T['text_p']),
                        orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                    ),
                    hovermode="closest",
                    margin=dict(t=60, b=50, l=55, r=20),
                )
                st.plotly_chart(fig_line, use_container_width=True)

                if '試驗等級' in plot_df.columns:
                    if not abnormal_df.empty:
                        st.warning(f"⚠️ 共標示了 **{len(abnormal_df)} 顆** 7B 異常鋼捲（橘黃色點）。")
                    else:
                        st.success("✅ 目前顯示的鋼捲中，沒有出現 7B 等級。")

                # ═══════════════════════════════════════════════
                # 群組數據分佈箱型圖（主題化）
                # ═══════════════════════════════════════════════
                st.markdown('<div class="spc-section-title" style="margin-top:22px">▸ 群組數據分佈箱型圖</div>', unsafe_allow_html=True)
                st.caption("依「月份與等級」分群對比，可直觀看出不同群組的變異程度與極端值。")

                groups = sorted(plot_df["比對群組"].dropna().unique())
                box_palette = (
                    ["#00d4ff","#f5a623","#39e07a","#9b59ff","#ff3b3b",
                     "#00bfa5","#ff7c3b","#5c6bc0","#26a69a","#ef5350"]
                    if _is_dark else
                    ["#2563eb","#f59e0b","#059669","#7c3aed","#dc2626",
                     "#0891b2","#ea580c","#4f46e5","#0d9488","#e11d48"]
                )

                fig_box = go.Figure()
                for i, grp in enumerate(groups):
                    grp_data = plot_df[plot_df["比對群組"] == grp][selected_param].dropna()
                    c = box_palette[i % len(box_palette)]
                    # 將 hex 轉成 rgba 透明填色
                    def _hex_to_rgba(h, alpha=0.18):
                        h = h.lstrip("#")
                        r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
                        return f"rgba({r},{g},{b},{alpha})"
                    fill_c = _hex_to_rgba(c)
                    fig_box.add_trace(go.Box(
                        y=grp_data,
                        name=grp,
                        marker=dict(color=c, size=4, opacity=0.7),
                        line=dict(color=c, width=1.5),
                        fillcolor=fill_c,
                        boxpoints="outliers",
                        hovertemplate=f"<b>{grp}</b><br>數值: %{{y:.4f}}<extra></extra>",
                    ))

                for yval, label, color, dash in [
                    (usl,    f"USL: {usl:.4f}",      T['line_spec'],   "solid"),
                    (lsl,    f"LSL: {lsl:.4f}",      T['line_spec'],   "solid"),
                    (target, f"Target: {target:.4f}", T['line_target'], "dash"),
                ]:
                    fig_box.add_hline(
                        y=yval, line_dash=dash, line_color=color, line_width=1.6,
                        annotation=dict(
                            text=label, font=dict(color=color, size=10),
                            bgcolor=T['ann_bg'], bordercolor=color,
                            borderwidth=1, borderpad=3, xanchor="right"
                        )
                    )

                fig_box.update_layout(
                    title=dict(
                        text=f"【{selected_param}】 群組箱型圖對比",
                        font=dict(color=T['title_color'], size=12, family="Space Mono, monospace"), x=0
                    ),
                    height=460,
                    plot_bgcolor=T['bg_chart'],
                    paper_bgcolor=T['bg_panel'],
                    font=dict(color=T['text_p']),
                    xaxis=dict(
                        title=dict(text="群組分類", font=dict(color=T['text_s'], size=10)),
                        gridcolor=T['grid'], zerolinecolor=T['grid'],
                        tickfont=dict(size=9, color=T['text_s']),
                    ),
                    yaxis=dict(
                        gridcolor=T['grid'], zerolinecolor=T['grid'],
                        title=dict(text=selected_param, font=dict(color=T['text_s'], size=10)),
                        tickfont=dict(size=9, color=T['text_s']),
                    ),
                    showlegend=False,
                    margin=dict(t=60, b=80, l=55, r=20),
                )
                st.plotly_chart(fig_box, use_container_width=True)

        # ============ 數據匯出 ============
        st.markdown("---")
        st.markdown("### 💾 數據匯出")
        csv_data = filtered_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 下載目前篩選數據 (CSV)", data=csv_data, file_name='鍍三線_品質分析資料.csv', mime='text/csv')

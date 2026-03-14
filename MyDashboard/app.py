import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title="分析儀表板", layout="wide", page_icon="📈", initial_sidebar_state="expanded")

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
    
    .hero-title {
        font-family: 'Geist Sans', sans-serif;
        font-size: 4.5rem;
        font-weight: 800;
        letter-spacing: -2px;
        text-align: center;
        margin-top: 10px;
        background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-family: 'Geist Sans', sans-serif;
        text-align: center; color: #8b949e; font-size: 1.1rem;
        letter-spacing: 2px; margin-bottom: 20px;
    }
    
    /* 輪播與毛玻璃卡片 */
    .marquee-container { width: 100%; overflow: hidden; padding: 20px 0; }
    .marquee-track { display: flex; animation: scroll 25s linear infinite; }
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
    
    if uploaded_file:
        st.success("✅ 文件已加載")
        st.caption(f"文件名：{uploaded_file.name}")

# ==========================================
# 🌟 動畫與分析邏輯切換區塊
# ==========================================
if uploaded_file is None:
    # 1. 顯示 SteelClaw 漸層大標題
    st.markdown('<div class="hero-title">SteelClaw</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">THE AI DASHBOARD THAT ACTUALLY WORKS.</div>', unsafe_allow_html=True)
    
    # 2. 顯示 Lottie 高科技掃描動畫 (放在畫面中間)
    if lottie_scanning:
        # 我把高度稍微調小一點，讓畫面更緊湊
        st_lottie(lottie_scanning, height=200, key="scanning")
        
    # 3. 顯示高級感無限輪播卡片 (放在動畫下方)
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
                
                # SPC 規格設定
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
                
                cp = (usl - lsl) / (6 * std_val) if std_val > 0 else 0
                ca = (avg_val - target) / ((usl - lsl) / 2) * 100 if usl != lsl else 0
                cpk = min((usl - avg_val) / (3 * std_val), (avg_val - lsl) / (3 * std_val)) if std_val > 0 else 0
                
                st.markdown("### 📊 製程能力指標")
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                
                with metric_col1:
                    st.markdown(f"""
                    <div class="metric-highlight">
                        <strong>樣本數</strong><br>
                        <h2>{len(plot_df)} 顆</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with metric_col2:
                    st.markdown(f"""
                    <div class="metric-highlight">
                        <strong>Cp (精密度)</strong><br>
                        <h2>{cp:.2f}</h2>
                        <small>變異大小</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with metric_col3:
                    st.markdown(f"""
                    <div class="metric-highlight">
                        <strong>Ca (準確度)</strong><br>
                        <h2>{abs(ca):.1f}%</h2>
                        <small>偏離中心值</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                cpk_color = "🟢" if cpk >= 1.33 else ("🟡" if cpk >= 1.0 else "🔴")
                cpk_status = "優良(A)" if cpk >= 1.33 else ("尚可(B)" if cpk >= 1.0 else "需改善(C)")
                
                with metric_col4:
                    st.markdown(f"""
                    <div class="metric-highlight">
                        <strong>Cpk {cpk_color}</strong><br>
                        <h2>{cpk:.2f}</h2>
                        <small>{cpk_status}</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                stats_col1, stats_col2, stats_col3 = st.columns(3)
                with stats_col1:
                    st.write(f"**平均值**: {avg_val:.4f}")
                    st.write(f"**中位數**: {median_val:.4f}")
                with stats_col2:
                    st.write(f"**標準差**: {std_val:.4f}")
                    st.write(f"**變異係數**: {(std_val/avg_val*100) if avg_val != 0 else 0:.2f}%")
                with stats_col3:
                    st.write(f"**最小值**: {plot_df[selected_param].min():.4f}")
                    st.write(f"**最大值**: {plot_df[selected_param].max():.4f}")
                
                st.markdown("---")
                
                st.markdown("### 📉 視覺分析")
                chart_col1, chart_col2 = st.columns([1.5, 1])
                
                with chart_col1:
                    fig_hist = px.histogram(
                        plot_df, x=selected_param, nbins=30, opacity=0.7,
                        histnorm='probability density',
                        color_discrete_sequence=['#667eea'],
                        title=f"【{selected_param}】常態分佈與規格區間"
                    )
                    
                    if std_val > 0:
                        x_min = min(plot_df[selected_param].min(), lsl)
                        x_max = max(plot_df[selected_param].max(), usl)
                        x_curve = np.linspace(x_min - std_val, x_max + std_val, 200)
                        y_pdf = (1 / (std_val * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_curve - avg_val) / std_val) ** 2)
                        fig_hist.add_trace(go.Scatter(x=x_curve, y=y_pdf, mode='lines', 
                                                     line=dict(color='#FF2B2B', width=3), name='常態分佈'))
                    
                    fig_hist.add_vline(x=usl, line_dash="solid", line_color="#FF4B4B", annotation_text=f"USL: {usl:.2f}")
                    fig_hist.add_vline(x=lsl, line_dash="solid", line_color="#FF4B4B", annotation_text=f"LSL: {lsl:.2f}")
                    fig_hist.add_vline(x=target, line_dash="solid", line_color="#00CC96", annotation_text=f"目標: {target:.2f}")
                    
                    fig_hist.update_layout(height=450)
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                with chart_col2:
                    outside_usl = len(plot_df[plot_df[selected_param] > usl])
                    outside_lsl = len(plot_df[plot_df[selected_param] < lsl])
                    inside = len(plot_df) - outside_usl - outside_lsl
                    
                    fig_pie = px.pie(
                        values=[inside, outside_usl, outside_lsl],
                        names=['符合規格', '超過上限', '低於下限'],
                        color_discrete_sequence=['#28a745', '#ff6b6b', '#ffc107'],
                        title="規格符合率"
                    )
                    fig_pie.update_layout(height=450)
                    st.plotly_chart(fig_pie, use_container_width=True)

                # 🌟 生產順序異常監控圖
                st.markdown("---")
                st.markdown("### 📈 生產順序異常監控圖")
                
                x_axis_col = "產出鋼捲號碼" if "產出鋼捲號碼" in plot_df.columns else plot_df.index
                hover_cols = ['試驗等級'] if '試驗等級' in plot_df.columns else None
                
                fig_line = px.line(
                    plot_df, x=x_axis_col, y=selected_param, markers=True, hover_data=hover_cols,
                    title=f"【{selected_param}】 單一趨勢管制圖", color_discrete_sequence=['#667eea'] 
                )
                
                if '試驗等級' in plot_df.columns:
                    fig_line.update_traces(hovertemplate="<b>鋼捲號碼:</b> %{x}<br><b>數值:</b> %{y}<br><b>試驗等級:</b> %{customdata[0]}<extra></extra>")
                else:
                    fig_line.update_traces(hovertemplate="<b>鋼捲號碼:</b> %{x}<br><b>數值:</b> %{y}<extra></extra>")
                
                if '試驗等級' in plot_df.columns:
                    abnormal_df = plot_df[plot_df['試驗等級'].astype(str).str.upper().str.replace(' ', '').str.contains('7B', na=False)]
                    if not abnormal_df.empty:
                        x_data_abnormal = abnormal_df["產出鋼捲號碼"] if "產出鋼捲號碼" in abnormal_df.columns else abnormal_df.index
                        fig_line.add_trace(go.Scatter(
                            x=x_data_abnormal, y=abnormal_df[selected_param], mode='markers',
                            marker=dict(color='#FFD700', size=12, symbol='circle', line=dict(color='black', width=2)),
                            name='異常 (7B)', hoverinfo='skip' 
                        ))
                
                fig_line.add_hrect(y0=lsl, y1=usl, line_width=0, fillcolor="#00CC96", opacity=0.1)
                fig_line.add_hline(y=target, line_dash="dash", line_color="green", annotation_text="中心值")
                fig_line.add_hline(y=usl, line_dash="solid", line_color="red", annotation_text="USL")
                fig_line.add_hline(y=lsl, line_dash="solid", line_color="red", annotation_text="LSL")
                fig_line.update_xaxes(showticklabels=False, title_text="生產順序 (依照時間/鋼捲號碼)")
                fig_line.update_layout(height=400, hovermode="closest")
                st.plotly_chart(fig_line, use_container_width=True)

                if '試驗等級' in plot_df.columns:
                    if not abnormal_df.empty:
                        st.warning(f"⚠️ 在上方趨勢圖中，共標示了 **{len(abnormal_df)} 顆** 7B 異常鋼捲 (黃色點)。")
                    else:
                        st.success("✅ 目前顯示的鋼捲中，沒有出現 7B 等級。")

                # 🌟 新增：群組數據分佈箱型圖
                st.markdown("---")
                st.markdown("### 📦 群組數據分佈箱型圖")
                st.caption("將篩選後的資料依照「月份與等級」分群對比，可直觀看出不同群組的變異程度與極端值。")
                
                fig_box = px.box(
                    plot_df, 
                    x="比對群組", 
                    y=selected_param, 
                    color="比對群組",
                    title=f"【{selected_param}】 群組箱型圖對比",
                    points="all" # 顯示極端值
                )
                
                fig_box.add_hline(y=target, line_dash="dash", line_color="green", annotation_text="中心值")
                fig_box.add_hline(y=usl, line_dash="solid", line_color="red", annotation_text="USL")
                fig_box.add_hline(y=lsl, line_dash="solid", line_color="red", annotation_text="LSL")
                fig_box.update_layout(height=450, showlegend=False, xaxis_title="群組分類")
                
                st.plotly_chart(fig_box, use_container_width=True)

        # ============ 數據匯出 ============
        st.markdown("---")
        st.markdown("### 💾 數據匯出")
        csv_data = filtered_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 下載目前篩選數據 (CSV)", data=csv_data, file_name='鍍三線_品質分析資料.csv', mime='text/csv')


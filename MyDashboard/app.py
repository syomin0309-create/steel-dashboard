import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title="AegisCore", layout="wide", page_icon="👁️", initial_sidebar_state="expanded")

# ── Obsidian Intelligence Theme ──────────────────────────
from ui_theme import inject_theme, render_landing
inject_theme()

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
    render_landing()

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
        tab1, tab2 = st.tabs(["📊 數據總覽 & 趨勢分析", "🔬 製程能力分析 (Ca · Cp · Cpk)"])

        # ════════════════════════════════════════════════════════════
        # TAB 1 — 原有分析（完全不動）
        # ════════════════════════════════════════════════════════════
        with tab1:
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
                
                    fig_line.add_hline(y=avg_val, line_dash="dash", line_color="#00CC96", annotation_text=f"平均值: {avg_val:.4f}")
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
                
                    fig_box.add_hline(y=avg_val, line_dash="dash", line_color="#00CC96", annotation_text=f"平均值: {avg_val:.4f}")
                    fig_box.update_layout(height=450, showlegend=False, xaxis_title="群組分類")
                
                    st.plotly_chart(fig_box, use_container_width=True)

                # ============ 數據匯出 ============
                st.markdown("---")
                st.markdown("### 💾 數據匯出")
                csv_data = filtered_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 下載目前篩選數據 (CSV)", data=csv_data, file_name='鍍三線_品質分析資料.csv', mime='text/csv')


        # ════════════════════════════════════════════════════════════
        # TAB 2 — 製程能力分析 (Ca · Cp · Cpk)
        # ════════════════════════════════════════════════════════════
        with tab2:

            # ── Industrial UI CSS ────────────────────────────────
            st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Space+Mono:wght@400;700&display=swap');
.spc-card {
    background:#101826; border:1px solid #1c2e42; border-radius:8px;
    padding:16px 18px; position:relative; overflow:hidden;
}
.spc-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background:var(--ct,#1c2e42); opacity:.8;
}
.spc-lbl {
    font-family:'Space Mono',monospace; font-size:.58rem;
    letter-spacing:2px; color:#5a7a8e; text-transform:uppercase;
    margin-bottom:4px;
}
.spc-hdr { display:flex; align-items:center; justify-content:space-between; margin-bottom:2px; }
.spc-badge {
    font-family:'Rajdhani',monospace; font-size:.75rem; font-weight:700;
    padding:2px 9px; border-radius:3px; border:1px solid currentColor;
    letter-spacing:1px;
}
.spc-val {
    font-family:'Rajdhani',sans-serif; font-size:2rem; font-weight:700;
    line-height:1.1; margin:4px 0 2px 0;
}
.spc-sub { font-family:'Space Mono',monospace; font-size:.58rem; color:#5a7a8e; margin-bottom:8px; }
.spc-gauge { height:3px; background:#1c2e42; border-radius:2px; overflow:hidden; margin-top:6px; }
.spc-fill  { height:100%; border-radius:2px; transition:width .6s ease; }
.spc-statsbar {
    background:#101826; border:1px solid #1c2e42; border-radius:8px;
    display:grid; grid-template-columns:repeat(6,1fr); overflow:hidden;
}
.spc-cell { padding:10px 8px; text-align:center; border-right:1px solid #1c2e42; }
.spc-cell:last-child { border-right:none; }
.spc-sec {
    font-family:'Space Mono',monospace; font-size:.6rem; letter-spacing:3px;
    color:#5a7a8e; text-transform:uppercase;
    display:flex; align-items:center; gap:8px; margin:18px 0 10px 0;
}
.spc-sec::after { content:''; flex:1; height:1px; background:linear-gradient(90deg,#1c2e42,transparent); }
.diag-item {
    padding:10px 12px; border-radius:4px; border-left:3px solid;
    margin-bottom:8px; background:rgba(0,0,0,.2);
    display:flex; align-items:flex-start; gap:8px;
}
.diag-text { font-size:.72rem; line-height:1.6; color:#c8dde8; }
</style>
""", unsafe_allow_html=True)

            # ── 欄位選擇 ────────────────────────────────────────
            st.markdown('<div class="spc-sec">▸ 選擇量測欄位</div>', unsafe_allow_html=True)

            numeric_cols2 = filtered_df.select_dtypes(include=['number']).columns.tolist()
            exclude_sys2 = [
                '產出鋼捲號碼','試驗等級','投入等級','生產日期','比對群組','生產年月','SHIFT_NO',
                '鍍層下限管制值','北正面鍍層','中正面鍍層','南正面鍍層','北背面鍍層','中背面鍍層','南背面鍍層',
                'XRAY_A_T_N','XRAY_A_T_C','XRAY_A_T_S','XRAY_A_B_N','XRAY_A_B_C','XRAY_A_B_S',
                'NORTH_TOP_COAT_WEIGHT','CENTER_TOP_COAT_WEIGHT','SOUTH_TOP_COAT_WEIGHT',
                'NORTH_BACK_COAT_WEIGHT','CENTER_BACK_COAT_WEIGHT','SOUTH_BACK_COAT_WEIGHT',
                '訂單厚度','訂單寬度','原料厚度','原料寬度','投入厚度','投入寬度',
                '投入重量','實測重量','實測厚度','實測寬度','實測長度',
            ]
            spc_params = [c for c in numeric_cols2 if c not in exclude_sys2]
            if '雙面總鍍層量(AVG)' in spc_params:
                spc_params = ['雙面總鍍層量(AVG)'] + [x for x in spc_params if x != '雙面總鍍層量(AVG)']

            if not spc_params:
                st.warning("⚠️ 找不到可分析的數值欄位，請確認上傳的檔案內容。")
                st.stop()

            s_col1, s_col2 = st.columns([2, 1])
            with s_col1:
                spc_param = st.selectbox(
                    "量測欄位", spc_params,
                    key=f"spc_param_{uploaded_file.name}",
                    label_visibility="collapsed"
                )
            with s_col2:
                spec_type = st.selectbox(
                    "規格類型",
                    ["雙邊 (LSL & USL)", "單邊上限 (USL only)", "單邊下限 (LSL only)"],
                    key=f"spc_spectype_{uploaded_file.name}",
                    label_visibility="collapsed"
                )

            spc_data = filtered_df[spc_param].dropna()
            if len(spc_data) < 2:
                st.warning("⚠️ 數據不足，請放寬篩選條件。")
                st.stop()

            spc_n      = len(spc_data)
            spc_mean   = float(spc_data.mean())
            spc_median = float(spc_data.median())
            spc_std    = float(spc_data.std())
            spc_min    = float(spc_data.min())
            spc_max    = float(spc_data.max())
            spc_cv     = spc_std / spc_mean * 100 if spc_mean != 0 else 0

            # ── 規格輸入 ─────────────────────────────────────────
            st.markdown('<div class="spc-sec">▸ SPC 規格設定（手動輸入）</div>', unsafe_allow_html=True)

            is_both  = "雙邊" in spec_type
            is_upper = "上限" in spec_type
            is_lower = "下限" in spec_type

            g1, g2, g3 = st.columns(3)
            with g1:
                lsl2 = st.number_input(
                    "LSL 規格下限", value=float(spc_mean - 4*spc_std),
                    key=f"spc_lsl_{spc_param}",
                    disabled=is_upper
                )
            with g2:
                usl2 = st.number_input(
                    "USL 規格上限", value=float(spc_mean + 4*spc_std),
                    key=f"spc_usl_{spc_param}",
                    disabled=is_lower
                )
            with g3:
                target2 = st.number_input(
                    "Target 規格中心值", value=float((spc_mean - 4*spc_std + spc_mean + 4*spc_std) / 2),
                    key=f"spc_target_{spc_param}",
                    disabled=(not is_both)
                )

            g4, g5 = st.columns(2)
            with g4:
                spc_bins = st.number_input(
                    "組距 (Bins)", value=12, min_value=5, max_value=50,
                    key=f"spc_bins_{spc_param}"
                )
            with g5:
                spc_prec = st.number_input(
                    "小數位數", value=3, min_value=0, max_value=6,
                    key=f"spc_prec_{spc_param}"
                )

            # ── 顯示選項 ─────────────────────────────────────────
            st.markdown('<div class="spc-sec">▸ 顯示選項</div>', unsafe_allow_html=True)
            tog1, tog2 = st.columns(2)
            with tog1:
                show_mean2   = st.toggle("顯示平均值線", value=True,  key=f"spc_mean_{spc_param}")
                show_curve2  = st.toggle("顯示常態曲線", value=True,  key=f"spc_curve_{spc_param}")
            with tog2:
                show_median2 = st.toggle("顯示中位數線", value=False, key=f"spc_med_{spc_param}")
                show_target2 = st.toggle("顯示目標值線", value=True,  key=f"spc_tgt_{spc_param}")

            # ── Ca / Cp / Cpk 計算 ──────────────────────────────
            # Ca：僅雙邊規格
            if is_both and (usl2 - lsl2) != 0:
                ca2 = (spc_mean - target2) / ((usl2 - lsl2) / 2) * 100
            else:
                ca2 = None

            # Cp
            if spc_std > 0:
                if is_both:
                    cp2 = (usl2 - lsl2) / (6 * spc_std)
                elif is_upper:
                    cp2 = (usl2 - spc_mean) / (3 * spc_std)
                else:
                    cp2 = (spc_mean - lsl2) / (3 * spc_std)
            else:
                cp2 = 0.0

            # Cpk
            if is_both and ca2 is not None:
                cpk2 = cp2 * (1 - abs(ca2) / 100)
            else:
                cpk2 = cp2   # 單邊 Cpk = Cp

            # 規格外計算
            out_usl2 = int((spc_data > usl2).sum()) if not is_lower else 0
            out_lsl2 = int((spc_data < lsl2).sum()) if not is_upper else 0
            in2      = spc_n - out_usl2 - out_lsl2
            yield2   = in2 / spc_n * 100

            # ── 五級評價 ─────────────────────────────────────────
            def _gca(v):
                if v is None: return "—", "#5a7a8e", "需雙邊規格"
                a = abs(v)
                if a < 6.25:  return "A+", "#39e07a", "準確度極佳"
                if a < 12.5:  return "A",  "#00d4ff", "準確度良好"
                if a < 25.0:  return "B",  "#f5a623", "尚可，建議調整 Offset"
                if a < 50.0:  return "C",  "#ff7c3b", "能力不足"
                return             "D",  "#ff3b3b", "能力極差，立即處理"

            def _gcp(v):
                if v >= 1.67: return "A+", "#39e07a", "精密度極佳"
                if v >= 1.33: return "A",  "#00d4ff", "精密度良好"
                if v >= 1.00: return "B",  "#f5a623", "尚可，加強管制"
                if v >= 0.67: return "C",  "#ff7c3b", "能力不足"
                return             "D",  "#ff3b3b", "能力極差，全面檢討"

            ca_g, ca_c, ca_d   = _gca(ca2)
            cp_g, cp_c, cp_d   = _gcp(cp2)
            cpk_g, cpk_c, cpk_d = _gcp(cpk2)

            if yield2 >= 99.73: y_c = "#39e07a"
            elif yield2 >= 99:  y_c = "#00d4ff"
            elif yield2 >= 95:  y_c = "#f5a623"
            else:               y_c = "#ff3b3b"

            # ── 指標卡片 ─────────────────────────────────────────
            st.markdown('<div class="spc-sec">▸ 製程能力指標</div>', unsafe_allow_html=True)
            mc1, mc2, mc3, mc4 = st.columns(4)

            def _card(col, top_color, label, val_str, badge, badge_color, desc, gauge_pct):
                col.markdown(f"""
<div class="spc-card" style="--ct:{top_color}">
  <div class="spc-hdr">
    <div class="spc-lbl">{label}</div>
    <span class="spc-badge" style="color:{badge_color};border-color:{badge_color};background:{badge_color}18">{badge}</span>
  </div>
  <div class="spc-val" style="color:{badge_color}">{val_str}</div>
  <div class="spc-sub">{desc}</div>
  <div class="spc-gauge"><div class="spc-fill" style="width:{min(gauge_pct,100):.0f}%;background:{badge_color};box-shadow:0 0 5px {badge_color}"></div></div>
</div>""", unsafe_allow_html=True)

            _card(mc1, "#00d4ff", "樣本數 · N",
                  f"{spc_n}", "≥30 ✓" if spc_n >= 30 else "<30 ⚠",
                  "#00d4ff" if spc_n >= 30 else "#f5a623",
                  "達統計需求" if spc_n >= 30 else "樣本數不足",
                  min(spc_n/30*100, 100))

            _card(mc2, ca_c, "Ca · 準確度",
                  f"{abs(ca2):.1f}%" if ca2 is not None else "N/A",
                  ca_g, ca_c,
                  f"{'▲偏高' if ca2 and ca2>0 else '▼偏低'}  {abs(ca2):.2f}%" if ca2 is not None else "需雙邊規格",
                  abs(ca2) if ca2 is not None else 0)

            _card(mc3, cp_c, "Cp · 精密度",
                  f"{cp2:.3f}", cp_g, cp_c, cp_d, min(cp2/2*100, 100))

            _card(mc4, cpk_c, "Cpk · 製程能力",
                  f"{cpk2:.3f}", cpk_g, cpk_c, cpk_d, min(cpk2/2*100, 100))

            # ── 統計摘要列 ──────────────────────────────────────
            st.markdown(f"""
<div class="spc-statsbar" style="margin-top:10px">
  <div class="spc-cell"><div class="spc-lbl">平均值 X̄</div><div class="spc-val" style="font-family:'Space Mono',monospace;font-size:.85rem;color:#c8dde8;font-weight:700">{spc_mean:.4f}</div></div>
  <div class="spc-cell"><div class="spc-lbl">中位數</div><div class="spc-val" style="font-family:'Space Mono',monospace;font-size:.85rem;color:#c8dde8;font-weight:700">{spc_median:.4f}</div></div>
  <div class="spc-cell"><div class="spc-lbl">標準差 σ</div><div class="spc-val" style="font-family:'Space Mono',monospace;font-size:.85rem;color:#c8dde8;font-weight:700">{spc_std:.4f}</div></div>
  <div class="spc-cell"><div class="spc-lbl">變異係數</div><div class="spc-val" style="font-family:'Space Mono',monospace;font-size:.85rem;color:#c8dde8;font-weight:700">{spc_cv:.2f}%</div></div>
  <div class="spc-cell"><div class="spc-lbl">最小值</div><div class="spc-val" style="font-family:'Space Mono',monospace;font-size:.85rem;color:#c8dde8;font-weight:700">{spc_min:.4f}</div></div>
  <div class="spc-cell"><div class="spc-lbl">最大值</div><div class="spc-val" style="font-family:'Space Mono',monospace;font-size:.85rem;color:#c8dde8;font-weight:700">{spc_max:.4f}</div></div>
</div>""", unsafe_allow_html=True)

            # ── 圖表區 ───────────────────────────────────────────
            st.markdown('<div class="spc-sec" style="margin-top:20px">▸ 視覺分析</div>', unsafe_allow_html=True)
            ch1, ch2 = st.columns([1.6, 1])

            with ch1:
                # 直方圖
                arr    = spc_data.values
                bins   = int(spc_bins)
                p      = int(spc_prec)
                pad    = spc_std * 1.5
                amin   = min(arr.min(), lsl2) - pad
                amax   = max(arr.max(), usl2) + pad
                step_h = (amax - amin) / bins
                edges  = [amin + i * step_h for i in range(bins + 1)]
                counts = [0] * bins
                for v in arr:
                    idx = int((v - amin) / step_h)
                    idx = max(0, min(bins - 1, idx))
                    counts[idx] += 1

                bar_colors = []
                for i in range(bins):
                    lo, hi = edges[i], edges[i+1]
                    out = False
                    if is_both or is_lower:
                        out = out or (hi <= lsl2)
                    if is_both or is_upper:
                        out = out or (lo >= usl2)
                    bar_colors.append("rgba(220,38,38,0.7)" if out else "rgba(99,102,241,0.45)")

                bar_x = [(edges[i]+edges[i+1])/2 for i in range(bins)]

                fig_h = go.Figure()
                fig_h.add_trace(go.Bar(
                    x=bar_x, y=counts,
                    width=[step_h*0.98]*bins,
                    marker=dict(color=bar_colors, line=dict(width=0.5, color="rgba(255,255,255,0.08)")),
                    name="分布",
                    hovertemplate=f"區間: %{{x:.{p}f}}<br>次數: %{{y}}<extra></extra>"
                ))

                if spc_std > 0 and show_curve2:
                    xc = np.linspace(amin, amax, 300)
                    yc = (1/(spc_std*np.sqrt(2*np.pi))) * np.exp(-0.5*((xc-spc_mean)/spc_std)**2)
                    fig_h.add_trace(go.Scatter(
                        x=xc, y=yc*spc_n*step_h, mode='lines',
                        line=dict(color='#d97706', width=2.5), name='常態曲線'
                    ))

                spec_lines = []
                if is_both or is_lower:
                    spec_lines.append((lsl2, f"LSL:{lsl2:.{p}f}", "#ff3b3b", "solid"))
                if is_both or is_upper:
                    spec_lines.append((usl2, f"USL:{usl2:.{p}f}", "#ff3b3b", "solid"))
                if is_both and show_target2:
                    spec_lines.append((target2, f"Target:{target2:.{p}f}", "#00d4ff", "dash"))
                if show_mean2:
                    spec_lines.append((spc_mean, f"X̄:{spc_mean:.{p}f}", "#39e07a", "dot"))
                if show_median2:
                    spec_lines.append((spc_median, f"Med:{spc_median:.{p}f}", "#9b59ff", "dashdot"))

                for xv, lb, cl, dk in spec_lines:
                    fig_h.add_vline(x=xv, line_dash=dk, line_color=cl, line_width=1.8,
                        annotation=dict(text=lb, font=dict(color=cl, size=10),
                            bgcolor="rgba(255,255,255,0.9)", bordercolor=cl, borderwidth=1, borderpad=3))

                fig_h.update_layout(
                    title=dict(text=f"【{spc_param}】 直方圖 · 常態分佈",
                        font=dict(color="#64748b", size=12, family="Space Mono"), x=0),
                    height=420, plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
                    font=dict(color="#0f172a"), bargap=0,
                    xaxis=dict(gridcolor="#f1f5f9", tickfont=dict(size=9, color="#64748b"),
                        title=dict(text=spc_param, font=dict(color="#64748b", size=10))),
                    yaxis=dict(gridcolor="#f1f5f9", tickfont=dict(size=9, color="#64748b"),
                        title=dict(text="次數 (Frequency)", font=dict(color="#64748b", size=10))),
                    legend=dict(bgcolor="rgba(255,255,255,0.95)", bordercolor="#e2e8f0", borderwidth=1,
                        font=dict(size=10, color="#0f172a")),
                    margin=dict(t=60, b=50, l=50, r=20)
                )
                st.plotly_chart(fig_h, use_container_width=True)

            with ch2:
                # 圓餅圖
                pie_c = ['#00b4dc', '#ff3b3b', '#f5a623']
                fig_p = go.Figure(go.Pie(
                    values=[in2, out_usl2, out_lsl2],
                    labels=['符合規格', '超過 USL', '低於 LSL'],
                    marker=dict(colors=pie_c, line=dict(color='#0c1220', width=2)),
                    textinfo='label+percent',
                    textfont=dict(size=10, color="#c8dde8"),
                    hole=0.44,
                    hovertemplate="%{label}<br>數量: %{value} 顆<br>佔比: %{percent}<extra></extra>"
                ))
                fig_p.add_annotation(
                    text=f"<b>{yield2:.1f}%</b><br><span style='font-size:10px'>良品率</span>",
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(size=15, color=y_c, family="Rajdhani, sans-serif"), align="center"
                )
                fig_p.update_layout(
                    title=dict(text="規格符合率", font=dict(color="#64748b", size=12, family="Space Mono"), x=0),
                    height=420, paper_bgcolor="#ffffff", plot_bgcolor="#101826",
                    font=dict(color="#0f172a"),
                    legend=dict(bgcolor="rgba(255,255,255,0.95)", bordercolor="#e2e8f0", borderwidth=1,
                        font=dict(size=10, color="#0f172a"),
                        orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
                    margin=dict(t=60, b=60, l=20, r=20)
                )
                st.plotly_chart(fig_p, use_container_width=True)

            # ── 製程診斷報告 ─────────────────────────────────────
            st.markdown('<div class="spc-sec">▸ 製程診斷報告</div>', unsafe_allow_html=True)
            diags = []

            if spc_n < 30:
                diags.append(("#f5a623", "⚠", f"樣本數僅 {spc_n} 筆，建議至少 30 筆，分析結果可信度有限。"))
            else:
                diags.append(("#39e07a", "✓", f"樣本數 {spc_n} 筆，符合統計分析基本需求（≥30）。"))

            if ca2 is not None:
                a = abs(ca2)
                if a < 12.5:
                    diags.append(("#39e07a", "✓", f"Ca = {a:.1f}%（{ca_g} 級）：製程平均值接近目標中心值，偏移程度良好。"))
                elif a < 25:
                    diags.append(("#f5a623", "△", f"Ca = {a:.1f}%（{ca_g} 級）：平均值{'偏高' if ca2>0 else '偏低'} {a:.1f}%，建議調整機台 Offset 參數。"))
                elif a < 50:
                    diags.append(("#ff7c3b", "✕", f"Ca = {a:.1f}%（{ca_g} 級）：嚴重偏移！製程中心偏差過大，應立即檢查機台設定。"))
                else:
                    diags.append(("#ff3b3b", "✕", f"Ca = {a:.1f}%（{ca_g} 級）：偏移極差，須全面停機檢討。"))

            if cp2 >= 1.67:
                diags.append(("#39e07a", "✓", f"Cp = {cp2:.3f}（{cp_g} 級）：製程變異極小，精密度優秀，可考慮降低管制成本。"))
            elif cp2 >= 1.33:
                diags.append(("#00d4ff", "✓", f"Cp = {cp2:.3f}（{cp_g} 級）：精密度良好，請繼續維持當前製程穩定性。"))
            elif cp2 >= 1.00:
                diags.append(("#f5a623", "△", f"Cp = {cp2:.3f}（{cp_g} 級）：精密度尚可，建議加強製程管制以達 A 級目標。"))
            elif cp2 >= 0.67:
                diags.append(("#ff7c3b", "✕", f"Cp = {cp2:.3f}（{cp_g} 級）：製程變異偏大，建議檢查機台老化、原材料穩定性。"))
            else:
                diags.append(("#ff3b3b", "✕", f"Cp = {cp2:.3f}（{cp_g} 級）：製程變異極差，須全面檢討生產能力。"))

            if ca2 is not None and cp2 >= 1.33 and abs(ca2) >= 25:
                diags.append(("#f5a623", "△", f"Cpk = {cpk2:.3f}：Cp 高但 Ca 差，製程穩定但位置偏移，優先調整 Offset 對準目標值。"))
            elif cp2 < 1.00:
                diags.append(("#ff3b3b", "!", f"Cpk = {cpk2:.3f}：Cp 不足導致 Cpk 不良，需同時改善精密度與準確度。"))
            elif cpk2 >= 1.33:
                diags.append(("#39e07a", "★", f"Cpk = {cpk2:.3f}（{cpk_g} 級）：準確且精密，製程能力優秀！"))

            if out_usl2 > 0 or out_lsl2 > 0:
                diags.append(("#ff3b3b", "!", f"規格外品：超過 USL {out_usl2} 顆 · 低於 LSL {out_lsl2} 顆，共 {out_usl2+out_lsl2} 顆不良。"))

            diag_html = ""
            for clr, icon, txt in diags:
                diag_html += f'<div class="diag-item" style="border-left-color:{clr}"><span style="color:{clr};font-size:.9rem;flex-shrink:0">{icon}</span><span class="diag-text">{txt}</span></div>'
            st.markdown(diag_html, unsafe_allow_html=True)

            # ── 評價基準速查表 ───────────────────────────────────
            with st.expander("📋 評價基準對照表", expanded=False):
                grade_data = {
                    "等級": ["A+", "A", "B", "C", "D"],
                    "Cp / Cpk": ["≥ 1.67", "1.33 – 1.67", "1.00 – 1.33", "0.67 – 1.00", "< 0.67"],
                    "|Ca|": ["< 6.25%", "6.25 – 12.5%", "12.5 – 25%", "25 – 50%", "> 50%"],
                    "判斷": ["製程極佳", "製程良好", "製程尚可", "能力不足", "能力極差"],
                    "建議處置": ["可考慮降低管制成本", "繼續維持", "加強管制，目標 A 級", "加強訓練依 SOP 操作", "全面停機檢討"],
                }
                st.dataframe(
                    pd.DataFrame(grade_data),
                    use_container_width=True, hide_index=True
                )

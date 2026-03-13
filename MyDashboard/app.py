import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="鍍三線高階分析儀表板", layout="wide", page_icon="📈")

# 視覺優化補丁
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Microsoft JhengHei', 'Segoe UI', sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
    }
    div[data-baseweb="select"] {
        font-size: 16px !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_clean_data(file):
    if file.name.endswith('.csv'):
        try:
            df = pd.read_csv(file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file, encoding='big5') 
    else:
        df = pd.read_excel(file)
        
    # 統一將標題轉為大寫並去除隱藏空白，避免因為大小寫不同而找不到
    df.columns = df.columns.astype(str).str.strip().str.upper()
    
    # ---------------------------------------------------------
    # 📖 終極官方翻譯字典：結合您提供的對照表與系統標準
    # ---------------------------------------------------------
    rename_dict = {
        # 識別資訊
        'COIL_NO': '產出鋼捲號碼',
        '鋼捲號碼': '產出鋼捲號碼',
        'PRODUCTION_DATE': '生產日期',
        'QUALITY_CLASS': '試驗等級',
        
        # 尺寸與規格
        'BASE_METAL_THICK': '訂單厚度',
        'REAL_WIDTH': '訂單寬度',
        '投入厚度': '訂單厚度',
        '實測寬度': '訂單寬度',
        
        # 鍍層專用 (將英文與XRAY代碼統一對應到簡化中文)
        'NORTH_TOP_COAT_WEIGHT': '北正面鍍層',
        'CENTER_TOP_COAT_WEIGHT': '中正面鍍層',
        'SOUTH_TOP_COAT_WEIGHT': '南正面鍍層',
        'NORTH_BACK_COAT_WEIGHT': '北背面鍍層',
        'CENTER_BACK_COAT_WEIGHT': '中背面鍍層',
        'SOUTH_BACK_COAT_WEIGHT': '南背面鍍層',
        
        'XRAY_A_T_N': '北正面鍍層',
        'XRAY_A_T_C': '中正面鍍層',
        'XRAY_A_T_S': '南正面鍍層',
        'XRAY_A_B_N': '北背面鍍層',
        'XRAY_A_B_C': '中背面鍍層',
        'XRAY_A_B_S': '南背面鍍層'
    }
    
    # 執行官方翻譯替換
    df.rename(columns=rename_dict, inplace=True)

    # ---------------------------------------------------------
    # 🚀 自動計算雙面總鍍層量 
    # (只要經過上面的翻譯，有這6個欄位就直接算！)
    # ---------------------------------------------------------
    coat_cols = ['北正面鍍層', '中正面鍍層', '南正面鍍層', '北背面鍍層', '中背面鍍層', '南背面鍍層']
    
    if all(col in df.columns for col in coat_cols):
        for col in coat_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
        # 完美公式：(正北+正中+正南)/3 + (背北+背中+背南)/3
        df['雙面總鍍層量(AVG)'] = (df['北正面鍍層'] + df['中正面鍍層'] + df['南正面鍍層']) / 3 + \
                                (df['北背面鍍層'] + df['中背面鍍層'] + df['南背面鍍層']) / 3

    # 日期與群組處理
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

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2040/2040504.png", width=60)
    st.header("⚙️ 儀表板控制中心")
    uploaded_file = st.file_uploader("📂 上傳產線 RAW DATA", type=["xlsx", "csv"])

st.title("📊 鍍三線品質與製程能力 (SPC) 儀表板")

if uploaded_file is not None:
    raw_df = load_and_clean_data(uploaded_file)
    df = raw_df.copy()

    # ---------------------------------------------------------
    # 🧠 模式自動判定
    # ---------------------------------------------------------
    is_standard_mode = '試驗等級' in df.columns and not df['試驗等級'].dropna().empty
    
    if is_standard_mode:
        df = df[df['試驗等級'].astype(str).str.strip() != ''] 
        df = df[df['試驗等級'].astype(str).str.lower() != 'nan']
        df["比對群組"] = df["生產年月"] + " - " + df["試驗等級"].astype(str)
        st.success("✅ 已偵測到『試驗等級』欄位，啟動【多維度旗艦分析模式】")
    else:
        df["比對群組"] = "全批次數據"
        st.info("ℹ️ 未偵測到『試驗等級』，系統自動切換為【CPK 製程能力專用模式】")

    with st.sidebar:
        st.markdown("---")
        st.subheader("🎯 規格交叉比對 (可多選)")
            
        def create_filter(col_name):
            if col_name in df.columns:
                options = df[col_name].dropna().unique().tolist()
                return st.multiselect(f"過濾 {col_name}", options)
            return []
            
        # 有的檔案可能沒有材質，沒有關係，系統會自動略過不顯示錯誤
        f_month = create_filter('生產年月')
        f_thick = create_filter('訂單厚度')
        f_width = create_filter('訂單寬度')
        f_mat   = create_filter('熱軋材質')
        f_spec  = create_filter('產品規格代碼')
        
    if f_month: df = df[df['生產年月'].isin(f_month)]
    if f_thick: df = df[df['訂單厚度'].isin(f_thick)]
    if f_width: df = df[df['訂單寬度'].isin(f_width)]
    if f_mat:   df = df[df['熱軋材質'].isin(f_mat)]
    if f_spec:  df = df[df['產品規格代碼'].isin(f_spec)]

    # ---------------------------------------------------------
    # 自動抓取數值欄位 (把翻譯完的英文原始欄位保留，但過濾掉系統用的)
    # ---------------------------------------------------------
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    exclude_sys = ['產出鋼捲號碼', '試驗等級', '生產日期', '比對群組', '生產年月', 'SHIFT_NO'] 
    available_params = [col for col in numeric_cols if col not in exclude_sys]
    
    if available_params and not df.empty:
        # 如果有算好總鍍層，強勢置頂第一順位！
        if '雙面總鍍層量(AVG)' in available_params:
            available_params.insert(0, available_params.pop(available_params.index('雙面總鍍層量(AVG)')))
            
        selected_param = st.selectbox("🔍 選擇分析參數 (自動過濾非數值欄位)", available_params)
        plot_df = df.dropna(subset=[selected_param])
        
        if not plot_df.empty:
            avg_val = plot_df[selected_param].mean()
            std_val = plot_df[selected_param].std()
            ucl = avg_val + 3 * std_val
            lcl = avg_val - 3 * std_val
            
            st.markdown("---")
            st.markdown("### 📐 SPC 規格設定 (用於計算 Cpk)")
            
            col_usl, col_tar, col_lsl = st.columns(3)
            with col_usl:
                usl = st.number_input("規格上限 (USL)", value=float(avg_val + 4 * std_val) if std_val else float(avg_val + 10))
            with col_lsl:
                lsl = st.number_input("規格下限 (LSL)", value=float(avg_val - 4 * std_val) if std_val else float(avg_val - 10))
            with col_tar:
                target = st.number_input("規格中心值 (Target)", value=float((usl + lsl) / 2))
                
            cp = (usl - lsl) / (6 * std_val) if std_val > 0 else 0
            ca = (avg_val - target) / ((usl - lsl) / 2) * 100 if usl != lsl else 0
            cpk = min((usl - avg_val) / (3 * std_val), (avg_val - lsl) / (3 * std_val)) if std_val > 0 else 0
            
            st.markdown("### 📊 製程能力 (Capability) 診斷結果")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("實際樣本數", f"{len(plot_df)} 顆")
            c2.metric("Cp (精密度: 變異大小)", f"{cp:.2f}")
            c3.metric("Ca (準確度: 偏離中心)", f"{ca:.1f} %")
            
            cpk_status = "🟢 優良 (等級A)" if cpk >= 1.33 else ("🟡 尚可 (等級B)" if cpk >= 1.0 else "🔴 需改善 (等級C)")
            c4.metric("Cpk (綜合製程能力)", f"{cpk:.2f}", cpk_status)
            st.markdown("---")
            
            def draw_cpk_chart(data, param_name, c_color):
                fig = px.histogram(
                    data, x=param_name, nbins=30, opacity=0.6, 
                    histnorm='probability density', 
                    color_discrete_sequence=[c_color], 
                    title=f"【{param_name}】 數據常態分佈與 SPC 規格區間 (CPK 分析)"
                )
                if std_val > 0:
                    x_min = min(data[param_name].min(), lsl)
                    x_max = max(data[param_name].max(), usl)
                    x_curve = np.linspace(x_min - std_val, x_max + std_val, 200)
                    y_pdf = (1 / (std_val * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_curve - avg_val) / std_val) ** 2)
                    fig.add_trace(go.Scatter(x=x_curve, y=y_pdf, mode='lines', line=dict(color='#FF2B2B', width=3), name='常態分佈曲線'))

                fig.add_vline(x=usl, line_dash="solid", line_color="#FF4B4B", annotation_text=f"USL: {usl:.2f}", annotation_position="top right")
                fig.add_vline(x=lsl, line_dash="solid", line_color="#FF4B4B", annotation_text=f"LSL: {lsl:.2f}", annotation_position="top left")
                fig.add_vline(x=target, line_dash="solid", line_color="#00CC96", annotation_text=f"Target: {target:.2f}", annotation_position="top right")
                fig.add_vline(x=avg_val, line_dash="dash", line_color="blue", annotation_text=f"實際平均: {avg_val:.2f}", annotation_position="bottom right")

                fig.update_layout(height=500, yaxis_title="機率密度")
                return fig

            if is_standard_mode:
                unique_groups = plot_df['比對群組'].unique()
                color_map = {grp: "#FFD700" if "7B" in str(grp) else px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)] for i, grp in enumerate(unique_groups)}
                
                tab1, tab2, tab3 = st.tabs(["📈 趨勢折線圖", "📦 箱型圖對比", "📊 CPK 製程能力分佈圖"])
                with tab1:
                    fig_line = px.line(plot_df, x="產出鋼捲號碼", y=selected_param, color="比對群組", markers=True, color_discrete_map=color_map, title=f"【{selected_param}】 SPC 管制走勢圖")
                    fig_line.add_hrect(y0=lcl, y1=ucl, line_width=0, fillcolor="#00CC96", opacity=0.08)
                    fig_line.add_hline(y=avg_val, line_dash="dash", line_color="green")        
                    fig_line.add_hline(y=ucl, line_dash="dot", line_color="red")        
                    fig_line.add_hline(y=lcl, line_dash="dot", line_color="red") 
                    fig_line.update_xaxes(showticklabels=False, title_text="生產順序 (游標移至點上可查看鋼捲號碼)")
                    fig_line.update_traces(connectgaps=True)
                    st.plotly_chart(fig_line, use_container_width=True)
                with tab2:
                    fig_box = px.box(plot_df, x="比對群組", y=selected_param, color="比對群組", color_discrete_map=color_map, points="all")
                    st.plotly_chart(fig_box, use_container_width=True)
                with tab3:
                    st.plotly_chart(draw_cpk_chart(plot_df, selected_param, '#4B8BBE'), use_container_width=True)
            else:
                tab1, = st.tabs(["📊 CPK 製程能力分佈圖 (專用模式)"])
                with tab1:
                    st.plotly_chart(draw_cpk_chart(plot_df, selected_param, '#4B8BBE'), use_container_width=True)
                
        else:
            st.warning(f"⚠️ 這些篩選出來的鋼捲中，沒有任何一顆擁有【{selected_param}】的數據！")
            
        st.markdown("---")
        st.subheader("💾 篩選資料匯出")
        csv_data = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 下載目前篩選鋼捲完整資料 (CSV檔)", data=csv_data, file_name='鍍三線_品質分析資料.csv', mime='text/csv')
        
    elif df.empty:
        st.warning("⚠️ 目前的篩選條件下沒有找到任何鋼捲資料，請放寬左側的篩選條件！")

else:
    st.info("👈 請從左側邊欄上傳產線的 RAW DATA，系統將自動判別檔案類型並產生圖表。")

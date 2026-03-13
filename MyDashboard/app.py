import streamlit as st
import pandas as pd
import plotly.express as px

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
        
    df.columns = df.columns.str.replace('\n', '', regex=False).str.replace('\r', '', regex=False).str.strip()
    
    whitelist = [
        '產出鋼捲號碼', '生產日期', '試驗等級', '訂單厚度', '訂單寬度', 
        '熱軋材質', '產品規格代碼', 'RTF板溫', '線速度', 
        '硬度HRB', 'YPE', '抗拉強度(原始)', '降伏強度(原始)', 
        '伸長率(EL)', '硬度HRB(原始)', '抗拉強度(TS)', '降伏強度(YS)', 
        '碳(%x100)', '錳(%x100)', '磷(%x1000)', '硫(%x1000)', 
        '矽(%x100)', '鋁(%x1000)', '銅(%x100)', '鎳(%x100)', 
        '鉻(%x100)', '鉬(%x100)', '錫(%x1000)'
    ]
    target_cols = [col for col in whitelist if col in df.columns]
    df = df[target_cols]
    
    if '試驗等級' in df.columns:
        df = df.dropna(subset=['試驗等級']) 
        df = df[df['試驗等級'].astype(str).str.strip() != ''] 
        df = df[df['試驗等級'].astype(str).str.lower() != 'nan']
    
    def extract_year_month(date_val):
        try:
            dt = pd.to_datetime(date_val)
            return f"{dt.year}年{dt.month}月"
        except:
            return str(date_val)
            
    if '生產日期' in df.columns:        
        df['生產年月'] = df['生產日期'].apply(extract_year_month)
        df["比對群組"] = df["生產年月"] + " - " + df["試驗等級"].astype(str)
        
    return df

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2040/2040504.png", width=60)
    st.header("⚙️ 儀表板控制中心")
    uploaded_file = st.file_uploader("📂 上傳產線 RAW DATA", type=["xlsx", "csv"])

st.title("📊 鍍三線品質與製程能力 (SPC) 儀表板")

if uploaded_file is not None:
    raw_df = load_and_clean_data(uploaded_file)
    df = raw_df.copy()

    with st.sidebar:
        st.markdown("---")
        st.subheader("🎯 規格交叉比對 (可多選)")
        
        with st.expander("🛠️ 找不到篩選？點我看系統讀到的真實欄位名"):
            st.write("目前白名單成功抓到的欄位有：")
            st.write(df.columns.tolist())
            
        def create_filter(col_name):
            if col_name in df.columns:
                options = df[col_name].dropna().unique().tolist()
                return st.multiselect(f"過濾 {col_name}", options)
            else:
                st.error(f"找不到欄位：{col_name}")
            return []
            
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

    exclude_cols = ['產出鋼捲號碼', '試驗等級', '生產日期', '訂單厚度', '訂單寬度', '熱軋材質', '產品規格代碼', '比對群組', '生產年月'] 
    available_params = [col for col in df.columns if col not in exclude_cols]
    
    if available_params and not df.empty:
        selected_param = st.selectbox("🔍 選擇分析參數 (Y軸)", available_params)
        
        plot_df = df.dropna(subset=[selected_param])
        
        if not plot_df.empty:
            avg_val = plot_df[selected_param].mean()
            std_val = plot_df[selected_param].std()
            
            # SPC 管制線 (Control Limits)
            ucl = avg_val + 3 * std_val
            lcl = avg_val - 3 * std_val
            
            st.markdown("---")
            st.markdown("### 📐 SPC 規格設定 (用於計算 Cpk)")
            st.caption("💡 請依照實際產品規範，輸入該參數的上限與下限。系統預設填入 ±4σ 作為參考。")
            
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
            
            unique_groups = plot_df['比對群組'].unique()
            color_map = {}
            for i, group in enumerate(unique_groups):
                if "7B" in str(group):
                    color_map[group] = "#FFD700"  # 鮮艷黃色凸顯異常
                else:
                    color_map[group] = px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)]
            
            # 🌟 新增第三個分頁：CPK 直方圖
            tab1, tab2, tab3 = st.tabs(["📈 趨勢折線圖 (SPC 管制圖)", "📦 箱型圖對比", "📊 CPK 製程能力分佈圖"])
            
            with tab1:
                fig_line = px.line(
                    plot_df, x="產出鋼捲號碼", y=selected_param, color="比對群組", 
                    markers=True, color_discrete_map=color_map,
                    title=f"【{selected_param}】 SPC 管制走勢圖"
                )
                
                fig_line.add_hrect(
                    y0=lcl, y1=ucl, 
                    line_width=0, fillcolor="#00CC96", opacity=0.08,
                    annotation_text="±3σ 正常變異範圍", annotation_position="top left"
                )

                # 🌟 平均線改為綠色虛線 (dash)
                fig_line.add_hline(y=avg_val, line_dash="dash", line_color="green", 
                                   annotation_text=f"平均: {avg_val:.3f}", annotation_position="bottom right")        
                fig_line.add_hline(y=ucl, line_dash="dot", line_color="red", 
                                   annotation_text=f"+3σ: {ucl:.3f}", annotation_position="top right")        
                fig_line.add_hline(y=lcl, line_dash="dot", line_color="red", 
                                   annotation_text=f"-3σ: {lcl:.3f}", annotation_position="bottom right") 
                
                fig_line.update_xaxes(
                    categoryorder='array', 
                    categoryarray=plot_df['產出鋼捲號碼'].unique(),
                    showticklabels=False,  
                    title_text="生產順序 (將游標移至點上可查看詳細鋼捲號碼)" 
                )
                fig_line.update_traces(connectgaps=True)
                fig_line.update_layout(plot_bgcolor="rgba(0,0,0,0.02)", height=500)
                st.plotly_chart(fig_line, use_container_width=True)
                
            with tab2:
                fig_box = px.box(
                    plot_df, x="比對群組", y=selected_param, color="比對群組",
                    color_discrete_map=color_map, points="all", 
                    title=f"【{selected_param}】 數據分佈對比"
                )
                st.plotly_chart(fig_box, use_container_width=True)

            with tab3:
                # 🌟 新增：CPK 直方圖 (常態分佈分佈圖)
                fig_hist = px.histogram(
                    plot_df, x=selected_param, color="比對群組",
                    color_discrete_map=color_map,
                    nbins=30, opacity=0.7, barmode="overlay",
                    title=f"【{selected_param}】 數據常態分佈與 SPC 規格區間 (CPK 分析)"
                )
                
                # 畫出 USL (規格上限) 與 LSL (規格下限) - 絕對不能超出的紅線
                fig_hist.add_vline(x=usl, line_dash="solid", line_color="#FF4B4B", annotation_text=f"USL: {usl:.2f}", annotation_position="top right")
                fig_hist.add_vline(x=lsl, line_dash="solid", line_color="#FF4B4B", annotation_text=f"LSL: {lsl:.2f}", annotation_position="top left")
                
                # 畫出 Target (目標中心) - 理想狀態的綠線
                fig_hist.add_vline(x=target, line_dash="solid", line_color="#00CC96", annotation_text=f"Target: {target:.2f}", annotation_position="top right")
                
                # 畫出實際生產平均值 - 藍色點線，方便和 Target 比對看偏移量 (Ca)
                fig_hist.add_vline(x=avg_val, line_dash="dot", line_color="blue", annotation_text=f"實際平均: {avg_val:.2f}", annotation_position="bottom right")

                fig_hist.update_layout(height=500)
                st.plotly_chart(fig_hist, use_container_width=True)
                
                st.caption("💡 **直方圖判讀秘訣：** <br>1. **看 Ca (準確度)：** 藍色虛線（實際平均）距離綠色實線（目標 Target）越近越好。<br>2. **看 Cp (精密度)：** 彩色的柱狀分佈圖越集中越好，絕對不能溢出左右兩邊的紅色實線 (USL/LSL)。", unsafe_allow_html=True)
                
        else:
            st.warning(f"⚠️ 這些篩選出來的鋼捲中，沒有任何一顆擁有【{selected_param}】的數據！")
            
        st.markdown("---")
        st.subheader("💾 篩選資料匯出")
        csv_data = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 下載目前篩選鋼捲完整資料 (CSV檔)",
            data=csv_data,
            file_name='鍍三線_SPC分析資料.csv',
            mime='text/csv'
        )
        
    elif df.empty:
        st.warning("⚠️ 目前的篩選條件下沒有找到任何鋼捲資料，請放寬左側的篩選條件！")
    else:
        st.warning("⚠️ 找不到數值欄位，請檢查資料來源。")

else:
    st.info("👈 請從左側邊欄上傳產線的 RAW DATA，系統將自動進行清洗與分析。")

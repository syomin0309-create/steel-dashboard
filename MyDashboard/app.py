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
        
    df.columns = df.columns.str.replace('\n', '', regex=False).str.replace('\r', '', regex=False).str.strip()
    
    # 🛡️ 擴充白名單：把 X-Ray 的 6 個原始欄位加進來
    whitelist = [
        '產出鋼捲號碼', '生產日期', '試驗等級', '訂單厚度', '訂單寬度', 
        '熱軋材質', '產品規格代碼', 'RTF板溫', '線速度', 
        '硬度HRB', 'YPE', '抗拉強度(原始)', '降伏強度(原始)', 
        '伸長率(EL)', '硬度HRB(原始)', '抗拉強度(TS)', '降伏強度(YS)', 
        '碳(%x100)', '錳(%x100)', '磷(%x1000)', '硫(%x1000)', 
        '矽(%x100)', '鋁(%x1000)', '銅(%x100)', '鎳(%x100)', 
        '鉻(%x100)', '鉬(%x100)', '錫(%x1000)',
        'XRAY_A_T_N', 'XRAY_A_T_C', 'XRAY_A_T_S',  # 正面北中南
        'XRAY_A_B_N', 'XRAY_A_B_C', 'XRAY_A_B_S'   # 背面北中南
    ]
    target_cols = [col for col in whitelist if col in df.columns]
    df = df[target_cols]
    
    # === 🚀 新增魔法：自動計算雙面總鍍層量 ===
    xray_cols = ['XRAY_A_T_N', 'XRAY_A_T_C', 'XRAY_A_T_S', 'XRAY_A_B_N', 'XRAY_A_B_C', 'XRAY_A_B_S']
    
    # 檢查 Excel 裡面是不是真的有這 6 個欄位
    if all(col in df.columns for col in xray_cols):
        # 防呆機制：確保這 6 個欄位都是純數字，遇到奇怪的文字或空白會自動轉成空值 (NaN)
        for col in xray_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
        # 執行計算公式：(正面三點平均) + (背面三點平均)
        df['雙面總鍍層量(AVG)'] = (df['XRAY_A_T_N'] + df['XRAY_A_T_C'] + df['XRAY_A_T_S']) / 3 + \
                                (df['XRAY_A_B_N'] + df['XRAY_A_B_C'] + df['XRAY_A_B_S']) / 3
    # ==========================================

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

    # 把那 6 個原始單點數值排除在下拉選單外，以免版面太亂，我們只看計算出來的總和
    exclude_cols = ['產出鋼捲號碼', '試驗等級', '生產日期', '訂單厚度', '訂單寬度', '熱軋材質', '產品規格代碼', '比對群組', '生產年月',
                    'XRAY_A_T_N', 'XRAY_A_T_C', 'XRAY_A_T_S', 'XRAY_A_B_N', 'XRAY_A_B_C', 'XRAY_A_B_S'] 
    available_params = [col for col in df.columns if col not in exclude_cols]
    
    if available_params and not df.empty:
        selected_param = st.selectbox("🔍 選擇分析參數 (Y軸)", available_params)
        
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
            
            unique_groups = plot_df['比對群組'].unique()
            color_map = {}
            for i, group in enumerate(unique_groups):
                if "7B" in str(group):
                    color_map[group] = "#FFD700"  
                else:
                    color_map[group] = px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)]
            
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
                fig_hist = px.histogram(
                    plot_df, x=selected_param,
                    nbins=30, opacity=0.6, 
                    histnorm='probability density', 
                    color_discrete_sequence=['#4B8BBE'], 
                    title=f"【{selected_param}】 數據常態分佈與 SPC 規格區間 (CPK 分析)"
                )
                
                if std_val > 0:
                    x_min = min(plot_df[selected_param].min(), lsl)
                    x_max = max(plot_df[selected_param].max(), usl)
                    x_curve = np.linspace(x_min - std_val, x_max + std_val, 200)
                    
                    y_pdf = (1 / (std_val * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_curve - avg_val) / std_val) ** 2)
                    
                    fig_hist.add_trace(go.Scatter(
                        x=x_curve, y=y_pdf, mode='lines',
                        line=dict(color='#FF2B2B', width=3),
                        name='常態分佈曲線 (Bell Curve)'
                    ))

                fig_hist.add_vline(x=usl, line_dash="solid", line_color="#FF4B4B", annotation_text=f"USL: {usl:.2f}", annotation_position="top right")
                fig_hist.add_vline(x=lsl, line_dash="solid", line_color="#FF4B4B", annotation_text=f"LSL: {lsl:.2f}", annotation_position="top left")
                fig_hist.add_vline(x=target, line_dash="solid", line_color="#00CC96", annotation_text=f"Target: {target:.2f}", annotation_position="top right")
                fig_hist.add_vline(x=avg_val, line_dash="dash", line_color="blue", annotation_text=f"實際平均: {avg_val:.2f}", annotation_position="bottom right")

                fig_hist.update_layout(height=500, yaxis_title="機率密度 (Probability Density)")
                st.plotly_chart(fig_hist, use_container_width=True)
                
                st.caption("💡 **直方圖判讀秘訣：** <br>1. **看 Ca (準確度)：** 藍色虛線（實際平均）距離綠色實線（目標 Target）越近越好。<br>2. **看 Cp (精密度)：** 藍色柱子與紅色曲線越瘦高越好，絕對不能溢出左右兩邊的紅色死線 (USL/LSL)。", unsafe_allow_html=True)
                
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

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

st.title("📊 鍍三線鋼捲品質異常分析儀表板")

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
        
        # 🌟 關鍵邏輯：過濾掉該參數是「空白」的鋼捲，準備畫圖專用的乾淨資料！
        plot_df = df.dropna(subset=[selected_param])
        
        st.markdown("### 📊 篩選結果總覽")
        # 將 KPI 擴充為 4 格，讓數據對比更透明
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("符合篩選之總鋼捲", f"{len(df)} 顆")
        col2.metric(f"實際具備【{selected_param}】數據", f"{len(plot_df)} 顆", delta="畫在圖上的真實數量", delta_color="off")
        
        avg_val = plot_df[selected_param].mean() if not plot_df.empty else 0
        col3.metric("有效數據平均值", f"{avg_val:.2f}" if not plot_df.empty else "無資料")
        col4.metric("涵蓋規格數量", f"{plot_df['產品規格代碼'].nunique() if '產品規格代碼' in plot_df.columns else 0} 種")
        st.markdown("---")
        
        if not plot_df.empty:
            unique_groups = plot_df['比對群組'].unique()
            color_map = {}
            for i, group in enumerate(unique_groups):
                if "7B" in str(group):
                    color_map[group] = "#ff4b4b"  
                else:
                    color_map[group] = px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)]
            
            tab1, tab2 = st.tabs(["📈 趨勢折線圖 (看生產順序)", "📦 箱型圖對比 (看群組分佈與離群值)"])
            
            with tab1:
                # 注意：現在全部改用 plot_df 來畫圖，確保圖表和 KPI 卡片第二格的數字完全吻合！
                fig_line = px.line(
                    plot_df, x="產出鋼捲號碼", y=selected_param, color="比對群組", 
                    markers=True, color_discrete_map=color_map,
                    title=f"【{selected_param}】 跨區間分布趨勢圖"
                )
                fig_line.add_hline(y=avg_val, line_dash="dash", line_color="green", 
                                   annotation_text=f"全體平均: {avg_val:.2f}", annotation_position="bottom right")
                
                # 強制使用原始順序
                fig_line.update_xaxes(categoryorder='array', categoryarray=plot_df['產出鋼捲號碼'].unique())
                fig_line.update_traces(connectgaps=True)
                st.plotly_chart(fig_line, use_container_width=True)
                st.caption("💡 如果覺得 X 軸號碼太少，是因為系統會自動隱藏部分文字避免重疊；您可以試著用滑鼠『框選』圖表放大，就能看到每一顆鋼捲的號碼了！")
                
            with tab2:
                fig_box = px.box(
                    plot_df, x="比對群組", y=selected_param, color="比對群組",
                    color_discrete_map=color_map,
                    points="all", 
                    title=f"【{selected_param}】 正常品 vs 異常品 (7B) 數據分佈對比"
                )
                st.plotly_chart(fig_box, use_container_width=True)
                st.caption("💡 提示：箱型圖可一眼看出 7B 異常品的數值是否整體偏低/偏高，或是變異數(波動)過大。")
        else:
            st.warning(f"⚠️ 這些篩選出來的鋼捲中，沒有任何一顆擁有【{selected_param}】的數據！")
            
        st.markdown("---")
        st.subheader("💾 篩選資料匯出")
        
        # 匯出時，還是給您完整的 df (保留所有測試項目，不僅限於您現在正在看的項目)
        csv_data = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 下載目前篩選鋼捲完整資料 (CSV檔)",
            data=csv_data,
            file_name='鍍三線_副總級篩選分析資料.csv',
            mime='text/csv'
        )
        
    elif df.empty:
        st.warning("⚠️ 目前的篩選條件下沒有找到任何鋼捲資料，請放寬左側的篩選條件！")
    else:
        st.warning("⚠️ 找不到數值欄位，請檢查資料來源。")

else:
    st.info("👈 請從左側邊欄上傳產線的 RAW DATA，系統將自動進行清洗與分析。")

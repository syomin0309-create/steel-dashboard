import streamlit as st
import pandas as pd
import plotly.express as px

# 設定網頁為寬螢幕模式，標題設定
st.set_page_config(page_title="鍍三線高階分析儀表板", layout="wide", page_icon="📈")

# ---------------------------------------------------------
# 🎛️ 左側邊欄 (Sidebar) - 專屬控制與篩選區
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2040/2040504.png", width=60) # 放個質感的小圖示
    st.header("⚙️ 儀表板控制中心")
    uploaded_file = st.file_uploader("📂 上傳產線 RAW DATA", type=["xlsx", "csv"])

# ---------------------------------------------------------
# 📊 主畫面 (Main Area)
# ---------------------------------------------------------
st.title("📊 鍍三線鋼捲品質異常分析儀表板")

if uploaded_file is not None:
    # 讀取檔案與自動清洗換行符號
    if uploaded_file.name.endswith('.csv'):
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding='big5') 
    else:
        df = pd.read_excel(uploaded_file)
        
    df.columns = df.columns.str.replace('\n', '', regex=False).str.replace('\r', '', regex=False).str.strip()
    
    # 🛡️ 白名單 (已加入您要求的寬度、材質、規格等條件)
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
    
    # 🧹 清除空白等級
    if '試驗等級' in df.columns:
        df = df.dropna(subset=['試驗等級']) 
        df = df[df['試驗等級'].astype(str).str.strip() != ''] 
        df = df[df['試驗等級'].astype(str).str.lower() != 'nan']
    
    # 📅 升級版：將日期轉換為「YYYY年M月」
    def extract_year_month(date_val):
        try:
            dt = pd.to_datetime(date_val)
            return f"{dt.year}年{dt.month}月"
        except:
            return str(date_val)
            
    if '生產日期' in df.columns:        
        df['生產年月'] = df['生產日期'].apply(extract_year_month)
        df["比對群組"] = df["生產年月"] + " - " + df["試驗等級"].astype(str)
    
    # ---------------------------------------------------------
    # 🎯 動態多重篩選器 (放在左側邊欄)
    # ---------------------------------------------------------
    with st.sidebar:
        st.markdown("---")
        st.subheader("🎯 規格交叉比對 (可多選)")
        
        # 使用者不選代表「全選」，選了就進行過濾
        def create_filter(col_name):
            if col_name in df.columns:
                options = df[col_name].dropna().unique().tolist()
                return st.multiselect(f"過濾 {col_name}", options)
            return []
            
        f_month = create_filter('生產年月')
        f_thick = create_filter('訂單厚度')
        f_width = create_filter('訂單寬度')
        f_mat   = create_filter('熱軋材質')
        f_spec  = create_filter('產品規格代碼')
        
    # 套用篩選條件
    if f_month: df = df[df['生產年月'].isin(f_month)]
    if f_thick: df = df[df['訂單厚度'].isin(f_thick)]
    if f_width: df = df[df['訂單寬度'].isin(f_width)]
    if f_mat:   df = df[df['熱軋材質'].isin(f_mat)]
    if f_spec:  df = df[df['產品規格代碼'].isin(f_spec)]

    # ---------------------------------------------------------
    # 📈 主畫面圖表與 KPI 呈現
    # ---------------------------------------------------------
    exclude_cols = ['產出鋼捲號碼', '試驗等級', '生產日期', '訂單厚度', '訂單寬度', '熱軋材質', '產品規格代碼', '比對群組', '生產年月'] 
    available_params = [col for col in df.columns if col not in exclude_cols]
    
    if available_params and not df.empty:
        # 將參數選擇移到主畫面最上方
        selected_param = st.selectbox("🔍 選擇分析參數 (Y軸)", available_params)
        
        # 👑 C-Level 專屬 KPI 數據卡
        st.markdown("### 📊 篩選結果總覽")
        col1, col2, col3 = st.columns(3)
        col1.metric("總比對鋼捲數", f"{len(df)} 顆")
        col2.metric("分析參數平均值", f"{df[selected_param].mean():.2f}")
        col3.metric("涵蓋規格數量", f"{df['產品規格代碼'].nunique() if '產品規格代碼' in df.columns else 0} 種")
        st.markdown("---")
        
        # 智慧顏色對應：只要群組名稱包含 "7B" 就顯示橘紅色凸顯，其他用不同深淺的藍灰色
        unique_groups = df['比對群組'].unique()
        color_map = {}
        for i, group in enumerate(unique_groups):
            if "7B" in str(group):
                color_map[group] = "#ff4b4b"  # 亮橘紅色 (Streamlit 官方紅)
            else:
                color_map[group] = px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)]
        
        fig = px.line(
            df, 
            x="產出鋼捲號碼", 
            y=selected_param, 
            color="比對群組", 
            markers=True, 
            color_discrete_map=color_map,
            title=f"📈 【{selected_param}】 跨區間分布趨勢圖"
        )
        
        fig.update_xaxes(categoryorder='array', categoryarray=df['產出鋼捲號碼'].unique())
        fig.update_traces(connectgaps=True)
        fig.update_layout(legend_title_text='年份月份 - 試驗等級', height=500)
        
        st.plotly_chart(fig, use_container_width=True)
        
    elif df.empty:
        st.warning("⚠️ 目前的篩選條件下沒有找到任何鋼捲資料，請放寬左側的篩選條件！")
    else:
        st.warning("⚠️ 找不到數值欄位，請檢查資料來源。")

else:
    # 尚未上傳檔案時的歡迎畫面
    st.info("👈 請從左側邊欄上傳產線的 RAW DATA，系統將自動進行清洗與分析。")


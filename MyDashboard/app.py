import streamlit as st
import pandas as pd
import plotly.express as px

# 設定網頁標題與寬螢幕
st.set_page_config(page_title="鍍三線品質異常分析儀表板", layout="wide", page_icon="📊")

# 解決 Windows 中文字體模糊的隱藏補丁
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

# 快取與清洗資料引擎 (保留最核心的過濾功能)
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

# ==========================================
# 網頁主畫面開始
# ==========================================
st.title("📊 鍍三線鋼捲品質異常分析儀表板")

uploaded_file = st.file_uploader("📂 請上傳產線 RAW DATA (支援 Excel 或 CSV 檔)", type=["xlsx", "csv"])

if uploaded_file is not None:
    df = load_and_clean_data(uploaded_file)
    
    # 準備下拉選單
    exclude_cols = ['產出鋼捲號碼', '試驗等級', '生產日期', '訂單厚度', '訂單寬度', '熱軋材質', '產品規格代碼', '比對群組', '生產年月'] 
    available_params = [col for col in df.columns if col not in exclude_cols]
    
    if available_params and not df.empty:
        # 1. 簡潔的下拉選單
        selected_param = st.selectbox("🔍 請選擇要分析的品質參數：", available_params)
        st.markdown("---")
        
        # 2. 顏色設定 (7B 永遠是橘紅色)
        unique_groups = df['比對群組'].unique()
        color_map = {}
        for i, group in enumerate(unique_groups):
            if "7B" in str(group):
                color_map[group] = "#ff4b4b"  # 亮橘紅色
            else:
                color_map[group] = px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)]
        
        # 3. 繪製乾淨的折線圖
        fig = px.line(
            df, 
            x="產出鋼捲號碼", 
            y=selected_param, 
            color="比對群組", 
            markers=True, 
            color_discrete_map=color_map,
            title=f"📈 【{selected_param}】 分布趨勢圖"
        )
        
        fig.update_xaxes(categoryorder='array', categoryarray=df['產出鋼捲號碼'].unique())
        fig.update_traces(connectgaps=True)
        fig.update_layout(legend_title_text='年份月份 - 試驗等級', height=500)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # ---------------------------------------------------------
        # 📥 新增功能：資料匯出區塊
        # ---------------------------------------------------------
        st.markdown("---")
        st.subheader("💾 資料匯出")
        st.write("您可以將目前網頁上處理過、過濾掉空白的乾淨資料下載回去備存。")
        
        # 將 DataFrame 轉成 CSV 格式 (使用 utf-8-sig 確保 Excel 打開中文不會亂碼)
        csv_data = df.to_csv(index=False).encode('utf-8-sig')
        
        st.download_button(
            label="📥 下載乾淨資料 (CSV檔)",
            data=csv_data,
            file_name='鍍三線_異常分析清洗資料.csv',
            mime='text/csv'
        )
        
    else:
        st.warning("⚠️ 找不到可以用來分析的數值欄位，請檢查上傳的資料。")

else:
    st.info("請從上方上傳資料檔案，圖表就會自動生成囉！")

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="異常比對系統", layout="wide")
st.title("📊 鋼捲品質異常分析儀表板")

# 升級：現在可以同時接受 Excel 和 CSV 檔案了！
uploaded_file = st.file_uploader("請上傳您的鋼捲原始資料 (Excel 或 CSV 檔)", type=["xlsx", "csv"])

if uploaded_file is not None:
    # 智慧讀取：判斷是 Excel 還是 CSV
    if uploaded_file.name.endswith('.csv'):
        # 台灣企業系統常見的 CSV 中文編碼防呆機制
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding='big5') 
    else:
        df = pd.read_excel(uploaded_file)
        
    # ---------------------------------------------------------
    # ✨ 【新增這行大絕招：自動清洗欄位名稱的換行與空白】 ✨
    df.columns = df.columns.str.replace('\n', '', regex=False).str.replace('\r', '', regex=False).str.strip()
    # ---------------------------------------------------------
        
    # ---------------------------------------------------------
    # 🛡️ 懶人救星：自動過濾不需要的欄位 (白名單機制)
    # ---------------------------------------------------------
    # 在這裡列出您「真正需要」的欄位清單。
    # 只要沒寫在這裡面的欄位，匯入瞬間就會被系統自動刪除！
    whitelist = [
        '產出鋼捲號碼', '生產日期', '試驗等級', '訂單厚度', 
        'RTF板溫', '線速度', '硬度HRB(原始)', 'YPE',
        '降伏強度(原始)', '伸長率(原始)', '硬度HRB',
        '降伏強度(YS)', '伸長率(TS)', '"伸長率(EL)',
        '碳(%x100)', '錳(%x100)', '磷(%x1000)', '硫(%x1000)', 
        '矽(%x100)', '鋁(%x1000)', '銅(%x100)', '鎳(%x100)', 
        '鉻(%x100)', '鉬(%x100)', '錫(%x1000)'
    ]
    
    # 比對原始資料，只保留白名單內確實存在的欄位，避免報錯
    target_cols = [col for col in whitelist if col in df.columns]
    df = df[target_cols]
    
    # ---------------------------------------------------------
    # 🧹 資料清洗與優化區塊
    # ---------------------------------------------------------
    
    # 剔除「試驗等級」為空白的鋼捲
    if '試驗等級' in df.columns:
        df = df.dropna(subset=['試驗等級']) 
        df = df[df['試驗等級'].astype(str).str.strip() != ''] 
        df = df[df['試驗等級'].astype(str).str.lower() != 'nan']
    
    # 將詳細日期轉換為「X月」格式
    def extract_month(date_val):
        try:
            if hasattr(date_val, 'month'):
                return f"{date_val.month}月"
            else:
                return f"{pd.to_datetime(date_val).month}月"
        except:
            return str(date_val)
            
    if '生產日期' in df.columns:        
        df['生產月份'] = df['生產日期'].apply(extract_month)
        # 將「生產月份」和「試驗等級」合併為一個新欄位，用於圖例分類
        df["比對群組"] = df["生產月份"] + " - " + df["試驗等級"].astype(str)
    
    # ---------------------------------------------------------
    
    # 排除不需要出現在下拉選單的「文字型」標籤欄位
    exclude_cols = ['產出鋼捲號碼', '試驗等級', '生產日期', '訂單厚度', '比對群組', '生產月份'] 
    available_params = [col for col in df.columns if col not in exclude_cols]
    
    if available_params:
        selected_param = st.selectbox("🔍 請選擇要分析的品質參數：", available_params)
        
        st.markdown("---")
        
        # 設定指定的顏色 (3月-7B 固定為橘色，凸顯異常)
        color_map = {
            "3月 - 7B": "orange",
            "3月 - 1": "#1f77b4", 
            "12月 - 1": "gray"    
        }
        
        # 繪製圖表
        fig = px.line(
            df, 
            x="產出鋼捲號碼", 
            y=selected_param, 
            color="比對群組", 
            markers=True, 
            color_discrete_map=color_map,
            title=f"📈 【{selected_param}】 分布趨勢圖"
        )
        
        # 強制 X 軸鎖定為 Excel 裡的原始生產順序
        fig.update_xaxes(categoryorder='array', categoryarray=df['產出鋼捲號碼'].unique())
        
        # 讓線條在遇到沒有資料的點時也能連貫起來
        fig.update_traces(connectgaps=True)
        
        fig.update_layout(legend_title_text='生產月份 - 試驗等級')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ 在您上傳的資料中，找不到可以用來分析的數值欄位，請檢查白名單設定！")

else:
    st.info("請先從上方上傳資料檔案，圖表就會自動生成囉！")

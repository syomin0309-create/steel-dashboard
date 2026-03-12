import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 設定網頁標題
st.set_page_config(page_title="鍍三線異常比對系統", layout="wide")
st.title("📊 鍍三線鋼捲品質異常分析儀表板")

# 2. 建立檔案上傳區塊
uploaded_file = st.file_uploader("請上傳您的鋼捲原始資料 (Excel 檔)", type=["xlsx"])

if uploaded_file is not None:
    # 讀取 Excel 資料
    df = pd.read_excel(uploaded_file)
    
    # 3. 建立下拉選單，讓您隨時切換想看的參數
    # 這裡自動抓取除了號碼、等級之外的所有數值欄位作為選項
    exclude_cols = ['產出鋼捲號碼', '試驗等級', '生產日期', '訂單厚度'] 
    available_params = [col for col in df.columns if col not in exclude_cols]
    
    selected_param = st.selectbox("🔍 請選擇要分析的品質參數（包含化學成分）：", available_params)
    
    st.markdown("---")
    
    # 4. 繪製互動式折線圖 (完美鎖定 3月-7B 為橘色，其他為藍色/灰色)
    # 這裡可以自訂您想要的顏色對應
    color_map = {
        "3月 - 7B": "orange",
        "3月 - 1": "#1f77b4", # 預設藍色
        "12月 - 1": "gray"
    }
    
    # 使用 Plotly 畫圖，內建滑鼠游標懸停顯示詳細數值的功能
    fig = px.line(
        df, 
        x="產出鋼捲號碼", 
        y=selected_param, 
        color="試驗等級", 
        markers=True, # 顯示資料點
        color_discrete_map=color_map,
        title=f"📈 【{selected_param}】 分布趨勢圖"
    )
    
    # 將圖表顯示在網頁上
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("請先從上方上傳資料檔案，圖表就會自動生成囉！")
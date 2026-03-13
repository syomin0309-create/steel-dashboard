import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="鍍三線異常比對系統", layout="wide")
st.title("📊 鍍三線鋼捲品質異常分析儀表板")

uploaded_file = st.file_uploader("請上傳您的鋼捲原始資料 (Excel 檔)", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    # 【新增步驟】將「生產日期」和「試驗等級」合併為一個新欄位，用於圖例分類
    # 確保兩者都是字串格式，然後用 " - " 連接
    df["比對群組"] = df["生產日期"].astype(str) + " - " + df["試驗等級"].astype(str)
    
    exclude_cols = ['產出鋼捲號碼', '試驗等級', '生產日期', '訂單厚度', '比對群組'] 
    available_params = [col for col in df.columns if col not in exclude_cols]
    
    selected_param = st.selectbox("🔍 請選擇要分析的品質參數：", available_params)
    
    st.markdown("---")
    
    # 這裡的 key 必須跟您合併出來的結果一模一樣
    # 假設您的生產日期內容是 "3月"，合併後就會是 "3月 - 7B"
    color_map = {
        "3月 - 7B": "orange",
        "3月 - 1": "#1f77b4", # 藍色
        "12月 - 1": "gray"    # 灰色
    }
    
    fig = px.line(
        df, 
        x="產出鋼捲號碼", 
        y=selected_param, 
        color="比對群組",  # <--- 改用合併後的新欄位來分類顏色
        markers=True, 
        color_discrete_map=color_map, # 如果資料中的群組名稱有對上，就會套用這裡的顏色
        title=f"📈 【{selected_param}】 分布趨勢圖"
    )
    
    # 設定圖例標題
    fig.update_layout(legend_title_text='生產日期 - 試驗等級')
    
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("請先從上方上傳資料檔案，圖表就會自動生成囉！")

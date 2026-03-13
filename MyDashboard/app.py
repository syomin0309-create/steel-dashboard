import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="鍍三線異常比對系統", layout="wide")
st.title("📊 鍍三線鋼捲品質異常分析儀表板")

uploaded_file = st.file_uploader("請上傳您的鋼捲原始資料 (Excel 檔)", type=["xlsx"])

if uploaded_file is not None:
    # 讀取 Excel 資料
    df = pd.read_excel(uploaded_file)
    
    # ---------------------------------------------------------
    # 🧹 資料清洗與優化區塊
    # ---------------------------------------------------------
    
    # 【優化 1：剔除「試驗等級」為空白的鋼捲】
    df = df.dropna(subset=['試驗等級']) # 刪除 NaN (空值)
    df = df[df['試驗等級'].astype(str).str.strip() != ''] # 刪除只包含空白鍵的假資料
    df = df[df['試驗等級'].astype(str).str.lower() != 'nan']
    
    # 【優化 2：將詳細日期轉換為「X月」格式】
    def extract_month(date_val):
        try:
            # 如果是標準日期格式，直接抽取月份並加上"月"
            if hasattr(date_val, 'month'):
                return f"{date_val.month}月"
            # 如果是字串格式的日期，嘗試轉換後抽取
            else:
                return f"{pd.to_datetime(date_val).month}月"
        except:
            # 如果轉換失敗(例如原本就已經寫"3月")，就保持原樣
            return str(date_val)
            
    df['生產月份'] = df['生產日期'].apply(extract_month)
    
    # ---------------------------------------------------------
    
    # 將「生產月份」和「試驗等級」合併為一個新欄位，用於圖例分類
    df["比對群組"] = df["生產月份"] + " - " + df["試驗等級"].astype(str)
    
    # 排除不需要出現在下拉選單的欄位
    exclude_cols = ['產出鋼捲號碼', '試驗等級', '生產日期', '訂單厚度', '比對群組', '生產月份'] 
    available_params = [col for col in df.columns if col not in exclude_cols]
    
    selected_param = st.selectbox("🔍 請選擇要分析的品質參數：", available_params)
    
    st.markdown("---")
    
    # 設定指定的顏色 (3月-7B 固定為橘色，藉此凸顯異常)
    color_map = {
        "3月 - 7B": "orange",
        "3月 - 1": "#1f77b4", # 預設藍色
        "12月 - 1": "gray"    # 灰色
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
    
    # 讓線條在遇到沒有資料的點時也能連貫起來（模擬 Excel 的視覺效果）
    fig.update_traces(connectgaps=True)
    
    # 更新圖例標題
    fig.update_layout(legend_title_text='生產月份 - 試驗等級')
    
    # 顯示圖表
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("請先從上方上傳資料檔案，圖表就會自動生成囉！")

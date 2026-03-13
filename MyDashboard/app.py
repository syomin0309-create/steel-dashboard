import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import io

st.set_page_config(page_title="鋼捲品質分析儀表板", layout="wide", page_icon="📈")

st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Microsoft JhengHei', 'Noto Sans TC', 'Segoe UI', sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
    }
    div[data-baseweb="select"] {
        font-size: 15px !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="popover"] {
        font-family: 'Microsoft JhengHei', sans-serif !important;
    }
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 12px 16px;
    }
    div[data-testid="stAlert"] {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_clean_data(file_bytes: bytes, file_name: str) -> pd.DataFrame:
    try:
        if file_name.endswith('.csv'):
            try:
                df = pd.read_csv(io.BytesIO(file_bytes), encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(io.BytesIO(file_bytes), encoding='big5')
        else:
            df = pd.read_excel(io.BytesIO(file_bytes))
    except Exception as e:
        st.error(f"❌ 檔案讀取失敗：{e}")
        st.stop()

    df.columns = (
        df.columns.str.replace('\n', '', regex=False)
        .str.replace('\r', '', regex=False)
        .str.strip()
    )

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

    if not target_cols:
        st.error("❌ 找不到任何匹配欄位，請確認 RAW DATA 格式正確。")
        st.stop()

    df = df[target_cols]

    if '試驗等級' in df.columns:
        df = df.dropna(subset=['試驗等級'])
        df = df[df['試驗等級'].astype(str).str.strip() != '']
        df = df[df['試驗等級'].astype(str).str.lower() != 'nan']

    if '生產日期' in df.columns:
        def extract_year_month(date_val):
            try:
                dt = pd.to_datetime(date_val)
                return f"{dt.year}年{dt.month:02d}月"
            except Exception:
                return str(date_val)

        df['生產年月'] = df['生產日期'].apply(extract_year_month)
        df['比對群組'] = df['生產年月'] + " - " + df['試驗等級'].astype(str)

    return df


with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2040/2040504.png", width=60)
    st.header("⚙️ 儀表板控制中心")
    uploaded_file = st.file_uploader("📂 上傳產線 RAW DATA", type=["xlsx", "csv"])

st.title("📊 鋼捲品質異常分析儀表板")

if uploaded_file is not None:
    raw_df = load_and_clean_data(uploaded_file.read(), uploaded_file.name)
    df = raw_df.copy()

    with st.sidebar:
        st.markdown("---")
        st.subheader("🎯 規格交叉比對（可多選）")

        def create_filter(col_name, label=None):
            if col_name in df.columns:
                options = sorted(df[col_name].dropna().unique().tolist(), key=str)
                return st.multiselect(label or f"過濾 {col_name}", options)
            return []

        f_month = create_filter('生產年月')
        f_thick = create_filter('訂單厚度')
        f_width = create_filter('訂單寬度')
        f_mat   = create_filter('熱軋材質')
        f_spec  = create_filter('產品規格代碼')

        st.markdown("---")
        st.subheader("⚠️ 異常品標記設定")
        abnormal_keyword = st.text_input(
            "異常品試驗等級關鍵字",
            value="7B",
            help="含此關鍵字的試驗等級將被標示為黃色異常品"
        )

    if f_month: df = df[df['生產年月'].isin(f_month)]
    if f_thick: df = df[df['訂單厚度'].isin(f_thick)]
    if f_width: df = df[df['訂單寬度'].isin(f_width)]
    if f_mat:   df = df[df['熱軋材質'].isin(f_mat)]
    if f_spec:  df = df[df['產品規格代碼'].isin(f_spec)]

    if df.empty:
        st.warning("⚠️ 目前篩選條件下無資料，請放寬左側篩選條件！")
        st.stop()

    exclude_cols = {
        '產出鋼捲號碼', '試驗等級', '生產日期', '訂單厚度', '訂單寬度',
        '熱軋材質', '產品規格代碼', '比對群組', '生產年月'
    }
    available_params = [col for col in df.columns if col not in exclude_cols]

    if not available_params:
        st.warning("⚠️ 找不到數值欄位，請檢查資料來源。")
        st.stop()

    # 資料健康度
    with st.expander("🩺 資料健康度報告", expanded=False):
        total_raw = len(raw_df)
        total_filtered = len(df)

        hc1, hc2, hc3, hc4 = st.columns(4)
        hc1.metric("原始筆數", f"{total_raw:,}")
        hc2.metric("篩選後筆數", f"{total_filtered:,}")

        if '試驗等級' in df.columns and abnormal_keyword:
            abnormal_count = df['試驗等級'].astype(str).str.contains(abnormal_keyword).sum()
            hc3.metric(f"異常品數 ({abnormal_keyword})", f"{abnormal_count:,}",
                       delta=f"{abnormal_count/total_filtered*100:.1f}%", delta_color="inverse")

        if '生產日期' in raw_df.columns:
            try:
                date_range = pd.to_datetime(df['生產日期'], errors='coerce')
                hc4.metric("日期範圍",
                           f"{date_range.min().strftime('%Y/%m/%d')} ~ {date_range.max().strftime('%Y/%m/%d')}")
            except Exception:
                pass

        missing = df[available_params].isnull().mean().mul(100).round(1)
        missing = missing[missing > 0]
        if not missing.empty:
            st.markdown("**⚠️ 以下欄位存在缺值：**")
            st.dataframe(
                missing.rename("缺值率(%)").reset_index().rename(columns={"index": "欄位"}),
                use_container_width=True, hide_index=True
            )
        else:
            st.success("✅ 所有數值欄位均無缺值。")

    selected_param = st.selectbox("🔍 選擇分析參數（Y 軸）", available_params)

    st.markdown("### 📊 篩選結果總覽")
    col1, col2, col3, col4 = st.columns(4)
    avg_val = df[selected_param].mean()
    std_val = df[selected_param].std()

    col1.metric("總比對鋼捲數", f"{len(df):,} 顆")
    col2.metric(f"【{selected_param}】平均值", f"{avg_val:.3f}")
    col3.metric("標準差 (σ)", f"{std_val:.3f}")
    col4.metric("涵蓋規格數量",
                f"{df['產品規格代碼'].nunique() if '產品規格代碼' in df.columns else 0} 種")

    st.markdown("---")

    # 顏色對應（7B 為黃色）
    unique_groups = df['比對群組'].unique()
    color_map = {}
    palette = px.colors.qualitative.Set1
    for i, group in enumerate(unique_groups):
        if abnormal_keyword and abnormal_keyword in str(group):
            color_map[group] = "#FFD700"  # 黃色標示異常品
        else:
            color_map[group] = palette[i % len(palette)]

    is_abnormal = df['試驗等級'].astype(str).str.contains(abnormal_keyword) if abnormal_keyword else pd.Series([False] * len(df))
    df_normal   = df[~is_abnormal][selected_param].dropna()
    df_abnormal = df[is_abnormal][selected_param].dropna()

    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 趨勢折線圖",
        "📦 箱型圖對比",
        "🌡️ 相關性熱力圖",
        "📐 統計顯著性"
    ])

    with tab1:
        fig_line = px.line(
            df, x="產出鋼捲號碼", y=selected_param, color="比對群組",
            markers=True, color_discrete_map=color_map,
            title=f"【{selected_param}】 跨區間分布趨勢圖（含管制界限）"
        )
        fig_line.update_xaxes(categoryorder='array', categoryarray=df['產出鋼捲號碼'].unique())
        fig_line.update_traces(connectgaps=True)

        # 去除重複圖例
        seen_names = set()
        for trace in fig_line.data:
            if trace.name in seen_names:
                trace.showlegend = False
            else:
                seen_names.add(trace.name)

        fig_line.add_hline(y=avg_val, line_dash="dash", line_color="green",
                           annotation_text=f"平均: {avg_val:.3f}", annotation_position="bottom right")
        ucl = avg_val + 3 * std_val
        lcl = avg_val - 3 * std_val
        fig_line.add_hline(y=ucl, line_dash="dot", line_color="red",
                           annotation_text=f"+3σ: {ucl:.3f}", annotation_position="top right")
        fig_line.add_hline(y=lcl, line_dash="dot", line_color="red",
                           annotation_text=f"-3σ: {lcl:.3f}", annotation_position="bottom right")
        fig_line.update_layout(height=500)
        st.plotly_chart(fig_line, use_container_width=True)
        st.caption("💡 紅色虛線為 ±3σ 管制界限（SPC），超出範圍的點需重點追蹤。")

    with tab2:
        fig_box = px.box(
            df, x="比對群組", y=selected_param, color="比對群組",
            color_discrete_map=color_map, points="all",
            title=f"【{selected_param}】 正常品 vs 異常品數據分佈對比"
        )
        fig_box.update_xaxes(categoryorder='category ascending')
        fig_box.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)
        st.caption("💡 箱型圖可一眼看出異常品數值是否整體偏移，或變異數（波動）過大。")

    with tab3:
        numeric_df = df[available_params].select_dtypes(include='number')
        if len(numeric_df.columns) >= 2:
            corr_matrix = numeric_df.corr()
            fig_corr = px.imshow(
                corr_matrix, text_auto=".2f", color_continuous_scale="RdBu_r",
                zmin=-1, zmax=1, title="數值參數相關性矩陣（Pearson 相關係數）", aspect="auto"
            )
            fig_corr.update_layout(height=600)
            st.plotly_chart(fig_corr, use_container_width=True)
            st.caption("💡 數值接近 +1 表示正相關，接近 -1 表示負相關，接近 0 表示無線性關係。")

            if selected_param in corr_matrix.columns:
                top_corr = (
                    corr_matrix[selected_param].drop(selected_param)
                    .abs().sort_values(ascending=False).head(5)
                )
                st.markdown(f"**🔗 與【{selected_param}】相關性最高的參數：**")
                st.dataframe(
                    top_corr.rename("相關係數(絕對值)").reset_index().rename(columns={"index": "參數"}),
                    use_container_width=True, hide_index=True
                )
        else:
            st.info("需要至少 2 個數值欄位才能繪製相關性矩陣。")

    with tab4:
        if abnormal_keyword and len(df_normal) > 1 and len(df_abnormal) > 1:
            t_stat, p_val = stats.ttest_ind(df_normal, df_abnormal, equal_var=False)

            sc1, sc2, sc3 = st.columns(3)
            sc1.metric("正常品樣本數", f"{len(df_normal):,}")
            sc2.metric(f"異常品樣本數 ({abnormal_keyword})", f"{len(df_abnormal):,}")
            significance = "✅ 差異顯著（p < 0.05）" if p_val < 0.05 else "⚠️ 差異不顯著（p ≥ 0.05）"
            sc3.metric("統計顯著性", significance, delta=f"p-value = {p_val:.4f}", delta_color="off")

            summary = pd.DataFrame({
                "統計量": ["平均值", "標準差", "最小值", "最大值", "中位數"],
                f"正常品 (n={len(df_normal)})": [
                    f"{df_normal.mean():.3f}", f"{df_normal.std():.3f}",
                    f"{df_normal.min():.3f}", f"{df_normal.max():.3f}", f"{df_normal.median():.3f}"
                ],
                f"異常品 (n={len(df_abnormal)})": [
                    f"{df_abnormal.mean():.3f}", f"{df_abnormal.std():.3f}",
                    f"{df_abnormal.min():.3f}", f"{df_abnormal.max():.3f}", f"{df_abnormal.median():.3f}"
                ]
            })
            st.markdown(f"#### 【{selected_param}】兩組統計量比較")
            st.dataframe(summary, use_container_width=True, hide_index=True)

            if p_val < 0.05:
                diff = df_abnormal.mean() - df_normal.mean()
                direction = "偏高" if diff > 0 else "偏低"
                st.success(f"📌 結論：異常品【{selected_param}】均值比正常品 **{direction} {abs(diff):.3f}**，差異具統計顯著性（Welch's t-test, p={p_val:.4f}）。")
            else:
                st.info(f"📌 結論：兩組【{selected_param}】均值差異在統計上不顯著（p={p_val:.4f}），可能需要擴大樣本數或改變分析維度。")
        elif len(df_abnormal) <= 1:
            st.info(f"ℹ️ 異常品樣本數不足（≤1），請確認關鍵字「{abnormal_keyword}」設定是否正確。")
        else:
            st.info("ℹ️ 請在左側邊欄設定「異常品試驗等級關鍵字」以啟用此分析。")

    st.markdown("---")
    st.markdown("### ⬇️ 匯出資料")
    dl1, dl2 = st.columns(2)
    with dl1:
        st.download_button(
            label="📥 下載篩選後資料 (CSV)",
            data=df.to_csv(index=False).encode('utf-8-sig'),
            file_name="filtered_steel_data.csv",
            mime="text/csv"
        )
    with dl2:
        if abnormal_keyword:
            export_summary = df.groupby(
                df['試驗等級'].astype(str).str.contains(abnormal_keyword).map({True: '異常品', False: '正常品'})
            )[available_params].describe().round(3)
            st.download_button(
                label="📊 下載統計摘要 (CSV)",
                data=export_summary.to_csv().encode('utf-8-sig'),
                file_name="steel_summary_stats.csv",
                mime="text/csv"
            )

else:
    st.info("👈 請從左側邊欄上傳產線的 RAW DATA，系統將自動進行清洗與分析。")
    st.markdown("---")
    st.markdown("### 📋 本儀表板功能說明")
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        st.markdown("""
        **📈 趨勢折線圖**
        - 顯示各鋼捲的數值走勢
        - 內建 ±3σ SPC 管制線
        - 超出管制界限的點一目了然
        """)
    with fc2:
        st.markdown("""
        **📦 箱型圖對比**
        - 正常品 vs 異常品分佈比較
        - 顯示中位數、四分位距、離群值
        - 快速判斷整體偏移或變異過大
        """)
    with fc3:
        st.markdown("""
        **📐 統計顯著性分析**
        - Welch's t-test 統計檢定
        - 量化正常品與異常品差異
        - 提供具統計依據的分析結論
        """)

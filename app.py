import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import io

st.set_page_config(page_title="鋼捲品質跨期比對儀表板", layout="wide", page_icon="📊")

st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Microsoft JhengHei', 'Noto Sans TC', 'Segoe UI', sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
    }
    div[data-baseweb="select"] { font-size: 15px !important; font-weight: 600 !important; }
    div[data-baseweb="popover"] { font-family: 'Microsoft JhengHei', sans-serif !important; }

    .spec-banner {
        background: linear-gradient(135deg, #1e3a5f, #2d6a9f);
        color: white;
        border-radius: 12px;
        padding: 18px 28px;
        margin-bottom: 20px;
        font-size: 15px;
        line-height: 2.2;
    }
    .spec-banner b { color: #FFD700; font-size: 16px; }

    div[data-testid="metric-container"] {
        background-color: #f0f4fa;
        border: 1px solid #cdd8ea;
        border-radius: 10px;
        padding: 12px 16px;
    }

    .signal-table { width: 100%; border-collapse: collapse; font-size: 14px; }
    .signal-table th {
        background-color: #1e3a5f;
        color: white;
        padding: 10px 14px;
        text-align: center;
    }
    .signal-table td { padding: 9px 14px; text-align: center; border-bottom: 1px solid #e0e0e0; }
    .signal-table tr:nth-child(even) { background-color: #f8f9fa; }
    .sig-green  { color: #28a745; font-weight: bold; font-size: 18px; }
    .sig-yellow { color: #e6b800; font-weight: bold; font-size: 18px; }
    .sig-red    { color: #dc3545; font-weight: bold; font-size: 18px; }
    .sig-gray   { color: #aaa; font-size: 16px; }

    div[data-testid="stAlert"] { border-radius: 8px; }

    .section-title {
        font-size: 18px; font-weight: 700; color: #1e3a5f;
        border-left: 5px solid #2d6a9f;
        padding-left: 12px; margin: 28px 0 14px 0;
    }
</style>
""", unsafe_allow_html=True)


# ── 快取讀檔 ──────────────────────────────────────────────
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
        def extract_year_month(v):
            try:
                dt = pd.to_datetime(v)
                return f"{dt.year}年{dt.month:02d}月"
            except Exception:
                return str(v)
        df['生產年月'] = df['生產日期'].apply(extract_year_month)
        df['比對群組'] = df['生產年月'] + " - " + df['試驗等級'].astype(str)

    return df


# ── 側邊欄 ───────────────────────────────────────────────
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2040/2040504.png", width=60)
    st.header("⚙️ 儀表板控制中心")
    uploaded_file = st.file_uploader("📂 上傳產線 RAW DATA", type=["xlsx", "csv"])

st.title("📊 鋼捲品質跨期比對儀表板")

if uploaded_file is None:
    st.info("👈 請從左側邊欄上傳產線的 RAW DATA，系統將自動進行清洗與分析。")

    st.markdown("---")
    st.markdown("### 📋 本儀表板功能說明")
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        st.markdown("""
        **🔍 規格鎖定比對**
        - 先鎖定厚度、寬度、材質、規格
        - 再選擇要比對的月份
        - 同規格跨期品質一目了然
        """)
    with fc2:
        st.markdown("""
        **🚦 異常燈號總表**
        - 綠燈：數值穩定正常
        - 黃燈：輕微偏移需注意
        - 紅燈：顯著異常需追蹤
        """)
    with fc3:
        st.markdown("""
        **📐 統計顯著性分析**
        - Welch's t-test 統計檢定
        - 量化正常品與異常品差異
        - 提供具統計依據的分析結論
        """)
    st.stop()

# ── 讀取資料 ─────────────────────────────────────────────
raw_df = load_and_clean_data(uploaded_file.read(), uploaded_file.name)

exclude_cols = {
    '產出鋼捲號碼', '試驗等級', '生產日期', '訂單厚度', '訂單寬度',
    '熱軋材質', '產品規格代碼', '比對群組', '生產年月'
}
available_params = [col for col in raw_df.columns if col not in exclude_cols]

# ── 側邊欄篩選（規格鎖定 → 月份選擇） ────────────────────
with st.sidebar:
    st.markdown("---")
    st.subheader("🔒 Step 1｜鎖定規格條件")
    st.caption("先選好規格，再比對月份")

    def make_filter(df, col, label):
        if col not in df.columns:
            return []
        opts = sorted(df[col].dropna().unique().tolist(), key=str)
        return st.multiselect(label, opts)

    f_thick = make_filter(raw_df, '訂單厚度',    "📏 訂單厚度")
    f_width = make_filter(raw_df, '訂單寬度',    "↔️ 訂單寬度")
    f_mat   = make_filter(raw_df, '熱軋材質',    "🪨 熱軋材質")
    f_spec  = make_filter(raw_df, '產品規格代碼', "📋 產品規格代碼")

    st.markdown("---")
    st.subheader("📅 Step 2｜選擇比對月份")
    st.caption("可多選，進行跨月比對")

    # 先套用規格篩選，再提供月份選項
    spec_df = raw_df.copy()
    if f_thick: spec_df = spec_df[spec_df['訂單厚度'].isin(f_thick)]
    if f_width: spec_df = spec_df[spec_df['訂單寬度'].isin(f_width)]
    if f_mat:   spec_df = spec_df[spec_df['熱軋材質'].isin(f_mat)]
    if f_spec:  spec_df = spec_df[spec_df['產品規格代碼'].isin(f_spec)]

    month_opts = []
    if '生產年月' in spec_df.columns:
        month_opts = sorted(spec_df['生產年月'].dropna().unique().tolist(), key=str)

    f_month = st.multiselect("🗓️ 生產年月", month_opts,
                              help="建議選 2 個月以上以利比對")

    st.markdown("---")
    st.subheader("⚠️ 異常品標記")
    abnormal_keyword = st.text_input(
        "異常品試驗等級關鍵字", value="7B",
        help="含此關鍵字的試驗等級將標示為黃色"
    )

# ── 套用所有篩選 ─────────────────────────────────────────
df = raw_df.copy()
if f_thick:  df = df[df['訂單厚度'].isin(f_thick)]
if f_width:  df = df[df['訂單寬度'].isin(f_width)]
if f_mat:    df = df[df['熱軋材質'].isin(f_mat)]
if f_spec:   df = df[df['產品規格代碼'].isin(f_spec)]
if f_month:  df = df[df['生產年月'].isin(f_month)]

if df.empty:
    st.warning("⚠️ 目前篩選條件下無資料，請放寬左側的篩選條件！")
    st.stop()

if not available_params:
    st.warning("⚠️ 找不到數值欄位，請檢查資料來源。")
    st.stop()

# ── 頂部規格摘要 Banner ──────────────────────────────────
spec_parts = []
if f_thick:  spec_parts.append(f"厚度 <b>{' / '.join(str(x) for x in f_thick)}</b>")
if f_width:  spec_parts.append(f"寬度 <b>{' / '.join(str(x) for x in f_width)}</b>")
if f_mat:    spec_parts.append(f"材質 <b>{' / '.join(str(x) for x in f_mat)}</b>")
if f_spec:   spec_parts.append(f"規格 <b>{' / '.join(str(x) for x in f_spec)}</b>")
month_str = " vs ".join(f_month) if f_month else "<i>（全部月份）</i>"

banner_spec = "　｜　".join(spec_parts) if spec_parts else "<i>（未鎖定規格，顯示全部）</i>"

st.markdown(f"""
<div class="spec-banner">
    🔍 &nbsp;<b>當前比對條件</b><br>
    📦 規格條件：{banner_spec}<br>
    📅 比對月份：<b style="color:#FFD700">{month_str}</b>　　
    🔢 符合鋼捲數：<b style="color:#FFD700">{len(df):,} 顆</b>
</div>
""", unsafe_allow_html=True)

# ── 顏色對應 ─────────────────────────────────────────────
months_in_data = sorted(df['生產年月'].unique().tolist(), key=str) if '生產年月' in df.columns else []
month_palette  = px.colors.qualitative.Bold
month_color_map = {m: month_palette[i % len(month_palette)] for i, m in enumerate(months_in_data)}

unique_groups = df['比對群組'].unique() if '比對群組' in df.columns else []
group_color_map = {}
palette = px.colors.qualitative.Set1
for i, g in enumerate(unique_groups):
    if abnormal_keyword and abnormal_keyword in str(g):
        group_color_map[g] = "#FFD700"
    else:
        group_color_map[g] = palette[i % len(palette)]

is_abnormal = (
    df['試驗等級'].astype(str).str.contains(abnormal_keyword, na=False)
    if abnormal_keyword else pd.Series([False] * len(df), index=df.index)
)

# ── 分析參數選擇 ─────────────────────────────────────────
st.markdown('<div class="section-title">🔍 選擇分析參數</div>', unsafe_allow_html=True)
selected_param = st.selectbox("Y 軸參數", available_params, label_visibility="collapsed")

# 總覽指標
avg_val = df[selected_param].mean()
std_val = df[selected_param].std()
c1, c2, c3, c4 = st.columns(4)
c1.metric("符合鋼捲總數",   f"{len(df):,} 顆")
c2.metric(f"平均值",        f"{avg_val:.3f}")
c3.metric("標準差 (σ)",     f"{std_val:.3f}")
c4.metric("涵蓋月份數",     f"{len(months_in_data)} 個月")

st.markdown("---")

# ── 主圖表分頁 ───────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🚦 異常燈號總表",
    "📈 趨勢折線圖",
    "📦 月份箱型圖",
    "📐 統計顯著性",
])

# ════════════════════════════════════════════════
# Tab 1：異常燈號總表（層峰最需要的）
# ════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">🚦 各參數跨月異常燈號總表</div>', unsafe_allow_html=True)
    st.caption("以全期數據為基準，判斷各月各參數是否偏移（綠=正常 / 黃=輕微偏移 / 紅=顯著異常）")

    if len(months_in_data) < 2:
        st.info("ℹ️ 請在左側選擇至少 2 個月份，以啟用燈號比對。")
    else:
        numeric_params = [p for p in available_params
                          if pd.api.types.is_numeric_dtype(df[p])]

        global_means = {p: df[p].mean() for p in numeric_params}
        global_stds  = {p: df[p].std()  for p in numeric_params}

        rows = []
        for param in numeric_params:
            row = {"參數": param}
            g_mean = global_means[param]
            g_std  = global_stds[param]
            for month in months_in_data:
                mdf = df[df['生產年月'] == month][param].dropna()
                if len(mdf) == 0:
                    row[month] = "sig-gray|—"
                    continue
                m_mean = mdf.mean()
                if g_std == 0:
                    row[month] = "sig-green|●"
                    continue
                z = abs(m_mean - g_mean) / g_std
                if z < 0.5:
                    row[month] = f"sig-green|● {m_mean:.2f}"
                elif z < 1.5:
                    row[month] = f"sig-yellow|▲ {m_mean:.2f}"
                else:
                    row[month] = f"sig-red|✖ {m_mean:.2f}"
            rows.append(row)

        # 渲染 HTML 表格
        header_months = "".join(f"<th>{m}</th>" for m in months_in_data)
        legend = """
        <div style="margin-bottom:10px; font-size:13px;">
            <span class="sig-green">●</span> 正常（偏移 &lt; 0.5σ）&nbsp;&nbsp;
            <span class="sig-yellow">▲</span> 輕微偏移（0.5～1.5σ）&nbsp;&nbsp;
            <span class="sig-red">✖</span> 顯著異常（&gt; 1.5σ）
        </div>
        """
        table_html = f"""
        <style>
        .sig-green  {{ color: #28a745; font-weight: bold; }}
        .sig-yellow {{ color: #e6b800; font-weight: bold; }}
        .sig-red    {{ color: #dc3545; font-weight: bold; }}
        .sig-gray   {{ color: #aaa; }}
        </style>
        {legend}
        <table class="signal-table">
          <tr><th>參數</th>{header_months}</tr>
        """
        for row in rows:
            tds = f"<td><b>{row['參數']}</b></td>"
            for month in months_in_data:
                val = row.get(month, "sig-gray|—")
                css, text = val.split("|", 1)
                tds += f'<td><span class="{css}">{text}</span></td>'
            table_html += f"<tr>{tds}</tr>"
        table_html += "</table>"
        st.markdown(table_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 紅燈參數快速摘要
        red_items = []
        for row in rows:
            for month in months_in_data:
                val = row.get(month, "")
                if val.startswith("sig-red"):
                    red_items.append(f"**{month}** 的 【{row['參數']}】")
        if red_items:
            st.error("🔴 **需要重點追蹤的異常項目：**\n\n" + "\n\n".join(f"- {x}" for x in red_items))
        else:
            st.success("✅ 所選條件下，各月份數值均在合理範圍內，無顯著異常。")


# ════════════════════════════════════════════════
# Tab 2：趨勢折線圖
# ════════════════════════════════════════════════
with tab2:
    fig_line = px.line(
        df, x="產出鋼捲號碼", y=selected_param, color="比對群組",
        markers=True, color_discrete_map=group_color_map,
        title=f"【{selected_param}】 跨月生產趨勢圖（含 ±3σ 管制線）"
    )
    fig_line.update_xaxes(categoryorder='array', categoryarray=df['產出鋼捲號碼'].unique())
    fig_line.update_traces(connectgaps=True)

    seen = set()
    for trace in fig_line.data:
        if trace.name in seen:
            trace.showlegend = False
        else:
            seen.add(trace.name)

    ucl = avg_val + 3 * std_val
    lcl = avg_val - 3 * std_val
    fig_line.add_hline(y=avg_val, line_dash="dash", line_color="green",
                       annotation_text=f"全期平均: {avg_val:.3f}", annotation_position="bottom right")
    fig_line.add_hline(y=ucl, line_dash="dot", line_color="red",
                       annotation_text=f"+3σ: {ucl:.3f}", annotation_position="top right")
    fig_line.add_hline(y=lcl, line_dash="dot", line_color="red",
                       annotation_text=f"-3σ: {lcl:.3f}", annotation_position="bottom right")
    fig_line.update_layout(height=520)
    st.plotly_chart(fig_line, use_container_width=True)
    st.caption("💡 紅色虛線為 ±3σ 管制界限（SPC），黃色線條為異常品（7B）。")


# ════════════════════════════════════════════════
# Tab 3：月份並排箱型圖
# ════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">📦 各月份數值分佈並排比對</div>', unsafe_allow_html=True)

    if '生產年月' not in df.columns:
        st.info("ℹ️ 無生產年月欄位，無法繪製月份箱型圖。")
    else:
        fig_box = px.box(
            df, x="生產年月", y=selected_param,
            color="生產年月", color_discrete_map=month_color_map,
            points="all",
            title=f"【{selected_param}】 月份分佈並排箱型圖"
        )
        fig_box.update_xaxes(categoryorder='category ascending')
        fig_box.update_layout(height=520, showlegend=False)

        # 加上全期平均線
        fig_box.add_hline(y=avg_val, line_dash="dash", line_color="green",
                          annotation_text=f"全期平均: {avg_val:.3f}",
                          annotation_position="bottom right")
        st.plotly_chart(fig_box, use_container_width=True)
        st.caption("💡 每個月的箱型圖顯示中位數、四分位距與離群值，可一眼看出哪個月份品質波動異常。")

        # 各月均值比較表
        st.markdown('<div class="section-title">📋 各月份統計摘要</div>', unsafe_allow_html=True)
        month_summary = (
            df.groupby('生產年月')[selected_param]
            .agg(鋼捲數='count', 平均值='mean', 標準差='std', 最小值='min', 最大值='max', 中位數='median')
            .round(3)
            .reset_index()
            .rename(columns={'生產年月': '月份'})
        )
        st.dataframe(month_summary, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════
# Tab 4：統計顯著性（正常品 vs 異常品）
# ════════════════════════════════════════════════
with tab4:
    df_normal   = df[~is_abnormal][selected_param].dropna()
    df_abnormal = df[is_abnormal][selected_param].dropna()

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
            st.success(
                f"📌 結論：異常品【{selected_param}】均值比正常品 **{direction} {abs(diff):.3f}**，"
                f"差異具統計顯著性（Welch's t-test, p={p_val:.4f}）。"
            )
        else:
            st.info(
                f"📌 結論：兩組【{selected_param}】均值差異在統計上不顯著（p={p_val:.4f}），"
                f"可能需要擴大樣本數或改變分析維度。"
            )
    elif len(df_abnormal) <= 1:
        st.info(f"ℹ️ 異常品樣本數不足（≤1），請確認關鍵字「{abnormal_keyword}」設定是否正確。")
    else:
        st.info("ℹ️ 請在左側邊欄設定「異常品試驗等級關鍵字」以啟用此分析。")


# ── 匯出區 ───────────────────────────────────────────────
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
    if abnormal_keyword and '試驗等級' in df.columns:
        export_summary = df.groupby(
            df['試驗等級'].astype(str).str.contains(abnormal_keyword).map({True: '異常品', False: '正常品'})
        )[available_params].describe().round(3)
        st.download_button(
            label="📊 下載統計摘要 (CSV)",
            data=export_summary.to_csv().encode('utf-8-sig'),
            file_name="steel_summary_stats.csv",
            mime="text/csv"
        )

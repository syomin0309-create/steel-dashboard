import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re
import base64, os
from theme import THEME_CSS, render_landing, CHART_THEME

st.set_page_config(page_title="AegisCore", layout="wide", page_icon="👁️", initial_sidebar_state="expanded")
st.markdown(THEME_CSS, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  資料讀取
# ══════════════════════════════════════════════════════
@st.cache_data
def load_and_clean_data(file_bytes: bytes, file_name: str):
    import io
    if file_name.endswith('.csv'):
        try:
            df = pd.read_csv(io.BytesIO(file_bytes), encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(io.BytesIO(file_bytes), encoding='big5')
    else:
        df = pd.read_excel(io.BytesIO(file_bytes))

    df.columns = df.columns.astype(str).str.replace(r'\s+', '', regex=True).str.upper()

    rename_mapping = [
        (['鋼捲號碼', 'COIL_NO'],    '產出鋼捲號碼'),
        (['PRODUCTION_DATE'],         '生產日期'),
        (['QUALITY_CLASS'],           '試驗等級'),
        (['BASE_METAL_THICK'],        '訂單厚度'),
        (['REAL_WIDTH'],              '訂單寬度'),
    ]
    rename_dict = {}
    for source_cols, target_name in rename_mapping:
        for col in source_cols:
            if col in df.columns:
                rename_dict[col] = target_name
                break
    df.rename(columns=rename_dict, inplace=True)

    if df.columns.duplicated().any():
        for col in df.columns[df.columns.duplicated(keep=False)].unique():
            indices = [i for i, x in enumerate(df.columns) if x == col]
            for idx in indices[1:]:
                df = df.drop(df.columns[idx], axis=1)

    xray_sets = [
        ['XRAY_A_T_N','XRAY_A_T_C','XRAY_A_T_S','XRAY_A_B_N','XRAY_A_B_C','XRAY_A_B_S'],
        ['NORTH_TOP_COAT_WEIGHT','CENTER_TOP_COAT_WEIGHT','SOUTH_TOP_COAT_WEIGHT',
         'NORTH_BACK_COAT_WEIGHT','CENTER_BACK_COAT_WEIGHT','SOUTH_BACK_COAT_WEIGHT'],
        ['北正面鍍層','中正面鍍層','南正面鍍層','北背面鍍層','中背面鍍層','南背面鍍層'],
    ]
    best_set, max_valid = None, -1
    for cols in xray_sets:
        if all(c in df.columns for c in cols):
            v = df[cols].apply(pd.to_numeric, errors='coerce').notna().sum().sum()
            if v > max_valid:
                max_valid, best_set = v, cols
    if best_set and max_valid > 0:
        for c in best_set:
            df[c] = pd.to_numeric(df[c], errors='coerce')
        df['雙面總鍍層量(AVG)'] = (
            (df[best_set[0]] + df[best_set[1]] + df[best_set[2]]) / 3 +
            (df[best_set[3]] + df[best_set[4]] + df[best_set[5]]) / 3
        )

    if '生產日期' in df.columns:
        def _ym(v):
            try:
                dt = pd.to_datetime(v)
                return f"{dt.year}年{dt.month:02d}月"
            except Exception:
                return str(v)
        df['生產年月'] = df['生產日期'].apply(_ym)
    else:
        df['生產年月'] = '全區間'

    return df


# ══════════════════════════════════════════════════════
#  側邊欄
# ══════════════════════════════════════════════════════
_logo_candidates = ["logo_zheng.png", "MyDashboard/logo_zheng.png"]
_logo_path = next((p for p in _logo_candidates if os.path.exists(p)), None)
if _logo_path:
    try:
        with open(_logo_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
<style>
.glowing-logo {{
    position:fixed; bottom:80px; right:28px; width:72px; z-index:9999;
    opacity:0.55; filter:drop-shadow(0 2px 8px rgba(26,115,232,0.3));
    transition:all 0.3s ease; cursor:pointer;
}}
.glowing-logo:hover {{ opacity:1; transform:scale(1.1) translateY(-4px); }}
</style>
<img src="data:image/png;base64,{img_b64}" class="glowing-logo">
""", unsafe_allow_html=True)
    except Exception:
        pass

with st.sidebar:
    st.header("⚙️ 儀表板控制中心")
    uploaded_file = st.file_uploader("📂 上傳產線 RAW DATA", type=["xlsx", "csv"])
    st.markdown("---")
    if uploaded_file:
        st.success("✅ 文件已加載")
        st.caption(f"文件名：{uploaded_file.name}")


# ══════════════════════════════════════════════════════
#  未上傳：封面頁
# ══════════════════════════════════════════════════════
if uploaded_file is None:
    render_landing()
    st.stop()


# ══════════════════════════════════════════════════════
#  已上傳：資料處理
# ══════════════════════════════════════════════════════
raw_df = load_and_clean_data(uploaded_file.read(), uploaded_file.name)
df = raw_df.copy()

if '試驗等級' in df.columns:
    df = df.dropna(subset=['試驗等級'])
    df['試驗等級'] = df['試驗等級'].astype(str).str.strip()
    df = df[df['試驗等級'] != '']
    df = df[~df['試驗等級'].str.lower().isin(['nan','null','none','na'])]
    df["比對群組"] = df["生產年月"] + " - " + df["試驗等級"]
else:
    df["比對群組"] = "全批次數據"

# ── 側邊欄篩選器 ─────────────────────────────────────
with st.sidebar:
    st.subheader("🎯 智能連動篩選器")
    st.caption("💡 條件即時連動，支援跨月多選")

    file_key = uploaded_file.name

    def cascading_filter(col, cur_df, label):
        if col not in cur_df.columns:
            return []
        opts = sorted(cur_df[col].dropna().astype(str).unique())
        if not opts:
            return []
        k = f"filter_{file_key}_{col}"
        if k in st.session_state:
            st.session_state[k] = [x for x in st.session_state[k] if x in opts]
        return st.multiselect(label, options=opts, key=k)

    f_month  = cascading_filter('生產年月',    df,   "🗓️ 生產年月")
    df_f1 = df[df['生產年月'].astype(str).isin(f_month)] if f_month else df.copy()

    f_thick  = cascading_filter('訂單厚度',   df_f1, "📏 訂單厚度")
    df_f2 = df_f1[df_f1['訂單厚度'].astype(str).isin(f_thick)] if f_thick else df_f1.copy()

    f_width  = cascading_filter('訂單寬度',   df_f2, "↔️ 訂單寬度")
    df_f3 = df_f2[df_f2['訂單寬度'].astype(str).isin(f_width)] if f_width else df_f2.copy()

    f_mat    = cascading_filter('熱軋材質',   df_f3, "🪨 熱軋材質")
    df_f4 = df_f3[df_f3['熱軋材質'].astype(str).isin(f_mat)] if f_mat else df_f3.copy()

    f_spec   = cascading_filter('產品規格代碼', df_f4, "📋 產品規格代碼")
    df_f5 = df_f4[df_f4['產品規格代碼'].astype(str).isin(f_spec)] if f_spec else df_f4.copy()

    f_coat   = cascading_filter('上鍍層',     df_f5, "🔩 上鍍層")
    filtered_df = df_f5[df_f5['上鍍層'].astype(str).isin(f_coat)] if f_coat else df_f5.copy()

    # ── 快速比對入口（上傳後才出現）────────────────
    st.markdown("---")
    st.subheader("⚡ 快速月份比對")
    st.caption("選兩個月份，直接跳到燈號比對")

    month_opts_all = sorted(df['生產年月'].dropna().unique().tolist(), key=str)
    if len(month_opts_all) >= 2:
        qc_a = st.selectbox("比對月份 A", month_opts_all,
                             index=max(0, len(month_opts_all)-2),
                             key=f"qc_a_{file_key}")
        qc_b = st.selectbox("比對月份 B", month_opts_all,
                             index=len(month_opts_all)-1,
                             key=f"qc_b_{file_key}")
        if st.button("立即比對 →", key=f"qc_go_{file_key}"):
            st.session_state[f"filter_{file_key}_生產年月"] = [qc_a, qc_b]
            st.rerun()
    else:
        st.caption("需要至少 2 個月份的資料")

if filtered_df.empty:
    st.warning("⚠️ 目前篩選條件下沒有找到任何數據，請放寬左側的篩選條件！")
    st.stop()

# ── 可分析參數清單 ────────────────────────────────────
_EXCLUDE = {
    '產出鋼捲號碼','試驗等級','投入等級','生產日期','比對群組','生產年月','SHIFT_NO',
    '鍍層下限管制值','北正面鍍層','中正面鍍層','南正面鍍層','北背面鍍層','中背面鍍層','南背面鍍層',
    'XRAY_A_T_N','XRAY_A_T_C','XRAY_A_T_S','XRAY_A_B_N','XRAY_A_B_C','XRAY_A_B_S',
    'NORTH_TOP_COAT_WEIGHT','CENTER_TOP_COAT_WEIGHT','SOUTH_TOP_COAT_WEIGHT',
    'NORTH_BACK_COAT_WEIGHT','CENTER_BACK_COAT_WEIGHT','SOUTH_BACK_COAT_WEIGHT',
    '訂單厚度','訂單寬度','原料厚度','原料寬度','投入厚度','投入寬度',
    '投入重量','實測重量','實測厚度','實測寬度','實測長度',
    '開始時間','排程單號','結束時間','班次','產出內徑','上粗糙度','下粗糙度',
    '化成','切除米數','收捲方向','AIM符號','引帶號碼',
}
numeric_cols = filtered_df.select_dtypes(include=['number']).columns.tolist()
available_params = [c for c in numeric_cols if c not in _EXCLUDE]
if '雙面總鍍層量(AVG)' in available_params:
    available_params = ['雙面總鍍層量(AVG)'] + [x for x in available_params if x != '雙面總鍍層量(AVG)']

if not available_params:
    st.warning("⚠️ 找不到可分析的數值欄位，請確認上傳的檔案內容。")
    st.stop()

# ══════════════════════════════════════════════════════
#  參數選擇
# ══════════════════════════════════════════════════════
selected_param = st.selectbox(
    "🔍 選擇分析參數",
    available_params,
    key=f"param_{file_key}",
    label_visibility="collapsed"
)

plot_df = filtered_df.dropna(subset=[selected_param])
if plot_df.empty:
    st.warning(f"⚠️ 篩選後的鋼捲中，沒有任何一顆擁有【{selected_param}】的有效數據！")
    st.stop()

avg_val    = float(plot_df[selected_param].mean())
std_val    = float(plot_df[selected_param].std())
median_val = float(plot_df[selected_param].median())

# 異常品（7B）
is_7b = plot_df['試驗等級'].astype(str).str.upper().str.replace(' ','').str.contains('7B', na=False) \
        if '試驗等級' in plot_df.columns else pd.Series([False]*len(plot_df), index=plot_df.index)
abnormal_count = int(is_7b.sum())
yield_rate = (len(plot_df) - abnormal_count) / len(plot_df) * 100 if len(plot_df) > 0 else 100.0
months_count = plot_df['生產年月'].nunique() if '生產年月' in plot_df.columns else 0

# ── 5 指標卡片（無趨勢箭頭）────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("總鋼捲數",   f"{len(plot_df):,} 顆")
c2.metric("平均值",     f"{avg_val:.3f}")
c3.metric("異常品數量", f"{abnormal_count:,} 顆",
          delta=f"{abnormal_count/len(plot_df)*100:.1f}%" if abnormal_count > 0 else "0%",
          delta_color="inverse")
c4.metric("涵蓋月份",   f"{months_count} 個月")
c5.metric("良品率",     f"{yield_rate:.1f}%")

st.markdown("---")

# ══════════════════════════════════════════════════════
#  主分頁
# ══════════════════════════════════════════════════════
tab1, tab2 = st.tabs(["📊 數據總覽 & 趨勢分析", "📐 製程能力分析 (Ca · Cp · Cpk)"])


# ────────────────────────────────────────────────────
# TAB 1：趨勢 + 月份高亮
# ────────────────────────────────────────────────────
with tab1:
    st.markdown("### 📈 生產順序異常監控圖")

    # 月份高亮按鈕列
    months_list = sorted(plot_df['生產年月'].unique().tolist(), key=str) \
                  if '生產年月' in plot_df.columns else []

    hl_key = f"hl_month_{file_key}_{selected_param}"
    if hl_key not in st.session_state:
        # 預設：最新一個月高亮
        st.session_state[hl_key] = months_list[-1] if months_list else "全部"

    if months_list:
        btn_cols = st.columns(len(months_list) + 1)
        for i, m in enumerate(months_list):
            is_active = st.session_state[hl_key] == m
            if btn_cols[i].button(
                m,
                key=f"hl_btn_{file_key}_{selected_param}_{m}",
                type="primary" if is_active else "secondary"
            ):
                st.session_state[hl_key] = m
                st.rerun()
        is_all = st.session_state[hl_key] == "全部"
        if btn_cols[-1].button("全部", key=f"hl_btn_all_{file_key}_{selected_param}",
                                type="primary" if is_all else "secondary"):
            st.session_state[hl_key] = "全部"
            st.rerun()

    selected_month = st.session_state.get(hl_key, "全部")

    x_col = "產出鋼捲號碼" if "產出鋼捲號碼" in plot_df.columns else None

    # 趨勢折線圖（選中月份全彩，其他月份半透明）
    fig_line = go.Figure()
    month_palette = px.colors.qualitative.Bold

    for i, month in enumerate(months_list if months_list else ["全部"]):
        m_df = plot_df[plot_df['生產年月'] == month] if months_list else plot_df
        if m_df.empty:
            continue
        x_data = m_df[x_col] if x_col else m_df.index
        is_highlighted = (selected_month == "全部") or (selected_month == month)
        opacity = 1.0 if is_highlighted else 0.15
        color   = month_palette[i % len(month_palette)]

        fig_line.add_trace(go.Scatter(
            x=x_data, y=m_df[selected_param],
            mode='lines+markers',
            name=month,
            line=dict(color=color, width=2 if is_highlighted else 1),
            marker=dict(size=6 if is_highlighted else 4, color=color, opacity=opacity),
            opacity=opacity,
            connectgaps=True,
            hovertemplate="<b>%{x}</b><br>數值: %{y:.3f}<extra></extra>"
        ))

    # 7B 異常點
    if '試驗等級' in plot_df.columns:
        ab_df = plot_df[is_7b]
        if not ab_df.empty:
            x_ab = ab_df[x_col] if x_col else ab_df.index
            fig_line.add_trace(go.Scatter(
                x=x_ab, y=ab_df[selected_param],
                mode='markers',
                name='異常 (7B)',
                marker=dict(color='#FFD700', size=12, symbol='circle',
                            line=dict(color='black', width=1.5)),
                hovertemplate="<b>%{x}</b><br>7B 異常: %{y:.3f}<extra></extra>"
            ))

    ucl = avg_val + 3 * std_val
    lcl = avg_val - 3 * std_val
    fig_line.add_hline(y=avg_val, line_dash="dash",  line_color="#3D6B4A",
                       annotation_text=f"平均值: {avg_val:.3f}", annotation_position="bottom right")
    fig_line.add_hline(y=ucl,     line_dash="dot",   line_color="#9A3B2E",
                       annotation_text=f"+3σ: {ucl:.3f}", annotation_position="top right")
    fig_line.add_hline(y=lcl,     line_dash="dot",   line_color="#9A3B2E",
                       annotation_text=f"-3σ: {lcl:.3f}", annotation_position="bottom right")
    fig_line.update_xaxes(showticklabels=False, title_text="生產順序（依照時間/鋼捲號碼）")
    fig_line.update_layout(
        template="simple_white",
        plot_bgcolor="#FDFAF6", paper_bgcolor="#FDFAF6",
        title=dict(text=f"【{selected_param}】 單一趨勢管制圖", font=dict(color="#2C1F14", size=15)),
        height=420, hovermode="closest",
        font=dict(color="#2C1F14"),
        xaxis=dict(gridcolor="#DABEA7", tickfont=dict(color="#2C1F14", size=12),
                   title=dict(font=dict(color="#2C1F14", size=13)),
                   linecolor="#A98B73", showgrid=True),
        yaxis=dict(gridcolor="#DABEA7", tickfont=dict(color="#2C1F14", size=12),
                   title=dict(font=dict(color="#2C1F14", size=13)),
                   linecolor="#A98B73", showgrid=True),
        legend=dict(bgcolor="#FDFAF6", bordercolor="#A98B73", borderwidth=1,
                    font=dict(color="#2C1F14", size=13),
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_line, use_container_width=True)

    if abnormal_count > 0:
        st.warning(f"⚠️ 在趨勢圖中，共標示了 **{abnormal_count} 顆** 7B 異常鋼捲（黃色點）。")
    else:
        st.success("✅ 目前顯示的鋼捲中，沒有出現 7B 等級。")

    # 箱型圖
    st.markdown("---")
    st.markdown("### 📦 群組數據分佈箱型圖")
    st.caption("依照「月份與等級」分群對比，可直觀看出不同群組的變異程度與極端值。")

    group_palette = {g: month_palette[i % len(month_palette)]
                     for i, g in enumerate(plot_df['比對群組'].unique())}
    fig_box = px.box(
        plot_df, x="比對群組", y=selected_param, color="比對群組",
        color_discrete_map=group_palette,
        title=f"【{selected_param}】 群組箱型圖對比",
        points="all"
    , template="simple_white")
    fig_box.add_hline(y=avg_val, line_dash="dash", line_color="#3D6B4A",
                      annotation_text=f"平均值: {avg_val:.3f}")
    fig_box.update_layout(
        template="simple_white",
        plot_bgcolor="#FDFAF6", paper_bgcolor="#FDFAF6",
        height=450, showlegend=False,
        font=dict(color="#2C1F14"),
        xaxis=dict(title=dict(text="群組分類", font=dict(color="#2C1F14", size=13)),
                   gridcolor="#DABEA7", tickfont=dict(color="#2C1F14", size=11),
                   linecolor="#A98B73"),
        yaxis=dict(gridcolor="#DABEA7", tickfont=dict(color="#2C1F14", size=12),
                   linecolor="#A98B73"),
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # 匯出
    st.markdown("---")
    st.markdown("### 💾 數據匯出")
    st.download_button(
        "📥 下載目前篩選數據 (CSV)",
        data=filtered_df.to_csv(index=False).encode('utf-8-sig'),
        file_name='AegisCore_品質分析資料.csv',
        mime='text/csv'
    )


# ────────────────────────────────────────────────────
# TAB 2：製程能力分析
# ────────────────────────────────────────────────────
with tab2:

    spc_data = plot_df[selected_param].dropna()
    if len(spc_data) < 2:
        st.warning("⚠️ 數據不足，請放寬篩選條件。")
        st.stop()

    spc_n      = len(spc_data)
    spc_mean   = float(spc_data.mean())
    spc_median = float(spc_data.median())
    spc_std    = float(spc_data.std())
    spc_min    = float(spc_data.min())
    spc_max    = float(spc_data.max())
    spc_cv     = spc_std / spc_mean * 100 if spc_mean != 0 else 0

    # 左右分欄：設定面板 | 主內容
    left_col, right_col = st.columns([1, 2.5])

    with left_col:
        # 基本設定
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
          <div style="width:4px;height:16px;background:#0d9488;border-radius:2px;"></div>
          <span style="font-size:11px;font-weight:600;color:#5f6368;letter-spacing:1px;text-transform:uppercase;">基本設定</span>
        </div>
        """, unsafe_allow_html=True)

        spec_type = st.selectbox(
            "規格類型",
            ["雙邊 (LSL & USL)", "單邊上限 (USL only)", "單邊下限 (LSL only)"],
            key=f"spc_spectype_{file_key}"
        )
        col_bins, col_prec = st.columns(2)
        with col_bins:
            spc_bins = st.number_input("組距 Bins", value=12, min_value=5, max_value=50,
                                        key=f"spc_bins_{selected_param}")
        with col_prec:
            spc_prec = st.number_input("小數位數", value=3, min_value=0, max_value=6,
                                        key=f"spc_prec_{selected_param}")

        show_mean2   = st.toggle("顯示平均值線", value=True,  key=f"spc_mean_{selected_param}")
        show_curve2  = st.toggle("顯示常態曲線", value=True,  key=f"spc_curve_{selected_param}")
        show_median2 = st.toggle("顯示中位數線", value=False, key=f"spc_med_{selected_param}")
        show_target2 = st.toggle("顯示目標值線", value=True,  key=f"spc_tgt_{selected_param}")

        st.markdown("---")

        # 規格設定
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
          <div style="width:4px;height:16px;background:#0d9488;border-radius:2px;"></div>
          <span style="font-size:11px;font-weight:600;color:#5f6368;letter-spacing:1px;text-transform:uppercase;">規格設定</span>
        </div>
        """, unsafe_allow_html=True)

        is_both  = "雙邊" in spec_type
        is_upper = "上限" in spec_type
        is_lower = "下限" in spec_type

        lsl2 = st.number_input("LSL 規格下限", value=float(spc_mean - 4*spc_std),
                                key=f"spc_lsl_{selected_param}", disabled=is_upper)
        usl2 = st.number_input("USL 規格上限", value=float(spc_mean + 4*spc_std),
                                key=f"spc_usl_{selected_param}", disabled=is_lower)
        target2 = st.number_input("Target 中心值", value=float((spc_mean - 4*spc_std + spc_mean + 4*spc_std) / 2),
                                   key=f"spc_target_{selected_param}", disabled=(not is_both))

    with right_col:

        # ── Ca / Cp / Cpk 計算 ──────────────────────
        if is_both and (usl2 - lsl2) != 0:
            ca2 = (spc_mean - target2) / ((usl2 - lsl2) / 2) * 100
        else:
            ca2 = None

        if spc_std > 0:
            if is_both:
                cp2  = (usl2 - lsl2) / (6 * spc_std)
            elif is_upper:
                cp2  = (usl2 - spc_mean) / (3 * spc_std)
            else:
                cp2  = (spc_mean - lsl2) / (3 * spc_std)
        else:
            cp2 = 0.0

        cpk2 = cp2 * (1 - abs(ca2) / 100) if (is_both and ca2 is not None) else cp2

        out_usl2 = int((spc_data > usl2).sum()) if not is_lower else 0
        out_lsl2 = int((spc_data < lsl2).sum()) if not is_upper else 0
        in2      = spc_n - out_usl2 - out_lsl2
        yield2   = in2 / spc_n * 100

        def _grade_ca(v):
            if v is None: return "—", "#5f6368", "需雙邊規格"
            a = abs(v)
            if a < 6.25:  return "A+", "#0f766e", "準確度極佳"
            if a < 12.5:  return "A",  "#1a73e8", "準確度良好"
            if a < 25.0:  return "B",  "#f29900", "建議調整 Offset"
            if a < 50.0:  return "C",  "#d93025", "能力不足"
            return             "D",  "#991b1b", "能力極差"

        def _grade_cp(v):
            if v >= 1.67: return "A+", "#0f766e", "精密度極佳"
            if v >= 1.33: return "A",  "#1a73e8", "精密度良好"
            if v >= 1.00: return "B",  "#f29900", "尚可，加強管制"
            if v >= 0.67: return "C",  "#d93025", "能力不足"
            return             "D",  "#991b1b", "能力極差"

        ca_g, ca_c, ca_d   = _grade_ca(ca2)
        cp_g, cp_c, cp_d   = _grade_cp(cp2)
        cpk_g, cpk_c, cpk_d = _grade_cp(cpk2)

        # σ / Ca / Cp / Cpk 卡片
        k1, k2, k3, k4 = st.columns(4)

        k1.markdown(f"""
        <div style="background:#FDFAF6;border:1.5px solid #DABEA7;border-radius:10px;padding:14px;border-top:3px solid #0d9488;">
          <div style="font-size:10px;color:#5C4033;letter-spacing:.8px;text-transform:uppercase;margin-bottom:4px;">標準差 σ</div>
          <div style="font-size:20px;font-weight:500;color:#2C1F14;">{spc_std:.3f}</div>
          <div style="font-size:11px;color:#5C4033;margin-top:2px;">變異係數 {spc_cv:.1f}%</div>
        </div>""", unsafe_allow_html=True)

        k2.markdown(f"""
        <div style="background:#FDFAF6;border:1.5px solid #DABEA7;border-radius:10px;padding:14px;border-top:3px solid {ca_c};">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px;">
            <span style="font-size:10px;color:#5C4033;letter-spacing:.8px;text-transform:uppercase;">Ca 準確度</span>
            <span style="font-size:10px;font-weight:700;color:{ca_c};background:{ca_c}18;border:1px solid {ca_c};border-radius:3px;padding:1px 7px;">{ca_g}</span>
          </div>
          <div style="font-size:20px;font-weight:500;color:{ca_c};">{f'{abs(ca2):.1f}%' if ca2 is not None else 'N/A'}</div>
          <div style="font-size:11px;color:#5C4033;margin-top:2px;">{ca_d}</div>
        </div>""", unsafe_allow_html=True)

        k3.markdown(f"""
        <div style="background:#FDFAF6;border:1.5px solid #DABEA7;border-radius:10px;padding:14px;border-top:3px solid {cp_c};">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px;">
            <span style="font-size:10px;color:#5C4033;letter-spacing:.8px;text-transform:uppercase;">Cp 精密度</span>
            <span style="font-size:10px;font-weight:700;color:{cp_c};background:{cp_c}18;border:1px solid {cp_c};border-radius:3px;padding:1px 7px;">{cp_g}</span>
          </div>
          <div style="font-size:20px;font-weight:500;color:{cp_c};">{cp2:.3f}</div>
          <div style="font-size:11px;color:#5C4033;margin-top:2px;">{cp_d}</div>
        </div>""", unsafe_allow_html=True)

        k4.markdown(f"""
        <div style="background:#FDFAF6;border:1.5px solid #DABEA7;border-radius:10px;padding:14px;border-top:3px solid {cpk_c};">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px;">
            <span style="font-size:10px;color:#5C4033;letter-spacing:.8px;text-transform:uppercase;">Cpk 製程能力</span>
            <span style="font-size:10px;font-weight:700;color:{cpk_c};background:{cpk_c}18;border:1px solid {cpk_c};border-radius:3px;padding:1px 7px;">{cpk_g}</span>
          </div>
          <div style="font-size:20px;font-weight:500;color:{cpk_c};">{cpk2:.3f}</div>
          <div style="font-size:11px;color:#5C4033;margin-top:2px;">{cpk_d}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 統計摘要列
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(5,1fr);background:#EFE3D5;border:1.5px solid #DABEA7;border-radius:10px;overflow:hidden;margin-bottom:16px;">
          <div style="padding:10px 12px;text-align:center;border-right:0.5px solid #e8eaed;">
            <div style="font-size:10px;color:#5f6368;letter-spacing:.5px;margin-bottom:4px;">平均值 X̄</div>
            <div style="font-size:13px;font-weight:500;color:#2C1F14;">{spc_mean:.{int(spc_prec)}f}</div>
          </div>
          <div style="padding:10px 12px;text-align:center;border-right:0.5px solid #e8eaed;">
            <div style="font-size:10px;color:#5f6368;letter-spacing:.5px;margin-bottom:4px;">中位數</div>
            <div style="font-size:13px;font-weight:500;color:#2C1F14;">{spc_median:.{int(spc_prec)}f}</div>
          </div>
          <div style="padding:10px 12px;text-align:center;border-right:0.5px solid #e8eaed;">
            <div style="font-size:10px;color:#5f6368;letter-spacing:.5px;margin-bottom:4px;">標準差 σ</div>
            <div style="font-size:13px;font-weight:500;color:#2C1F14;">{spc_std:.{int(spc_prec)}f}</div>
          </div>
          <div style="padding:10px 12px;text-align:center;border-right:0.5px solid #e8eaed;">
            <div style="font-size:10px;color:#5f6368;letter-spacing:.5px;margin-bottom:4px;">最小值</div>
            <div style="font-size:13px;font-weight:500;color:#2C1F14;">{spc_min:.{int(spc_prec)}f}</div>
          </div>
          <div style="padding:10px 12px;text-align:center;">
            <div style="font-size:10px;color:#5f6368;letter-spacing:.5px;margin-bottom:4px;">最大值</div>
            <div style="font-size:13px;font-weight:500;color:#2C1F14;">{spc_max:.{int(spc_prec)}f}</div>
          </div>
        </div>""", unsafe_allow_html=True)

        # 圖表：直方圖 + 圓餅圖
        ch1, ch2 = st.columns([1.6, 1])

        with ch1:
            arr   = spc_data.values
            bins  = int(spc_bins)
            p     = int(spc_prec)
            pad   = spc_std * 1.5
            amin  = min(arr.min(), lsl2) - pad
            amax  = max(arr.max(), usl2) + pad
            step_h = (amax - amin) / bins
            edges  = [amin + i * step_h for i in range(bins + 1)]
            counts = [0] * bins
            for v in arr:
                idx = max(0, min(bins-1, int((v - amin) / step_h)))
                counts[idx] += 1

            bar_colors = []
            for i in range(bins):
                out = False
                if is_both or is_lower: out = out or (edges[i+1] <= lsl2)
                if is_both or is_upper: out = out or (edges[i]   >= usl2)
                bar_colors.append("rgba(154,59,46,0.75)" if out else "rgba(205,165,129,0.80)")

            bar_x = [(edges[i]+edges[i+1])/2 for i in range(bins)]
            fig_h = go.Figure()
            fig_h.add_trace(go.Bar(
                x=bar_x, y=counts, width=[step_h*0.98]*bins,
                marker=dict(color=bar_colors, line=dict(width=1, color="#A98B73")),
                name="分布",
                hovertemplate=f"區間: %{{x:.{p}f}}<br>次數: %{{y}}<extra></extra>"
            ))
            if spc_std > 0 and show_curve2:
                xc = np.linspace(amin, amax, 300)
                yc = (1/(spc_std*np.sqrt(2*np.pi))) * np.exp(-0.5*((xc-spc_mean)/spc_std)**2)
                fig_h.add_trace(go.Scatter(
                    x=xc, y=yc*spc_n*step_h, mode='lines',
                    line=dict(color='#5C4033', width=2.5), name='常態曲線'
                ))
            spec_lines = []
            if is_both or is_lower: spec_lines.append((lsl2, f"LSL:{lsl2:.{p}f}", "#9A3B2E", "solid"))
            if is_both or is_upper: spec_lines.append((usl2, f"USL:{usl2:.{p}f}", "#9A3B2E", "solid"))
            if is_both and show_target2: spec_lines.append((target2, f"Target:{target2:.{p}f}", "#2B5084", "dash"))
            if show_mean2:   spec_lines.append((spc_mean,   f"X̄:{spc_mean:.{p}f}",     "#3D6B4A", "dot"))
            if show_median2: spec_lines.append((spc_median, f"Med:{spc_median:.{p}f}", "#876D5A", "dashdot"))

            for xv, lb, cl, dk in spec_lines:
                fig_h.add_vline(x=xv, line_dash=dk, line_color=cl, line_width=2,
                    annotation=dict(text=lb, font=dict(color=cl, size=10),
                        bgcolor="#FDFAF6", bordercolor=cl, borderwidth=1, borderpad=3))

            fig_h.update_layout(
                template="simple_white",
                plot_bgcolor="#FDFAF6", paper_bgcolor="#FDFAF6",
                title=dict(text=f"【{selected_param}】 直方圖 · 常態分佈",
                    font=dict(color="#5C4033", size=13), x=0),
                height=380,
                font=dict(color="#2C1F14"),
                xaxis=dict(gridcolor="#DABEA7", tickfont=dict(color="#2C1F14", size=11),
                           title=dict(text=selected_param, font=dict(color="#2C1F14", size=12)),
                           linecolor="#A98B73", showgrid=False),
                yaxis=dict(gridcolor="#DABEA7", tickfont=dict(color="#2C1F14", size=11),
                           title=dict(text="次數 (Frequency)", font=dict(color="#2C1F14", size=12)),
                           linecolor="#A98B73"),
                legend=dict(bgcolor="#FDFAF6", bordercolor="#A98B73", borderwidth=1,
                    font=dict(size=11, color="#2C1F14")),
                bargap=0, margin=dict(t=60, b=50, l=50, r=20)
            )
            st.plotly_chart(fig_h, use_container_width=True)

        with ch2:
            yc_color = "#0f766e" if yield2 >= 99.73 else ("#1a73e8" if yield2 >= 99 else
                        "#f29900" if yield2 >= 95 else "#d93025")
            fig_p = go.Figure(go.Pie(
                values=[in2, out_usl2, out_lsl2],
                labels=['符合規格', '超過 USL', '低於 LSL'],
                marker=dict(colors=['#876D5A','#9A3B2E','#CDA581'],
                            line=dict(color='#ffffff', width=2)),
                textinfo='label+percent',
                textfont=dict(size=13, color="#2C1F14"),
                hole=0.46,
                hovertemplate="%{label}<br>%{value} 顆 (%{percent})<extra></extra>"
            ))
            fig_p.add_annotation(
                text=f"<b>{yield2:.1f}%</b><br><span style='font-size:10px'>良品率</span>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=15, color='#2C1F14'), align="center"
            )
            fig_p.update_layout(
                template="simple_white",
                paper_bgcolor="#FDFAF6",
                title=dict(text="規格符合率", font=dict(color="#5C4033", size=13), x=0),
                height=380,
                font=dict(color="#2C1F14"),
                legend=dict(orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5,
                    font=dict(size=12, color="#2C1F14"),
                    bgcolor="#FDFAF6", bordercolor="#A98B73", borderwidth=1),
                margin=dict(t=60, b=60, l=10, r=10)
            )
            st.plotly_chart(fig_p, use_container_width=True)

        # ── 診斷摘要卡（可展開）────────────────────
        st.markdown("<br>", unsafe_allow_html=True)

        # 建立診斷項目
        diags = []
        # 建議行動對照
        _actions = {
            "A+": "繼續維持，可考慮每季降低抽樣頻率以節省管制成本。",
            "A":  "繼續維持，持續監控趨勢變化。",
            "B":  "加強製程管制，目標達到 A 級。",
            "C":  "立即啟動改善，排查機台老化與原材料穩定性。",
            "D":  "全面停機檢討，需系統性改善後方可復產。",
        }

        if spc_n < 30:
            diags.append(("warning", "⚠", f"樣本數僅 {spc_n} 筆（建議 ≥30），分析結果可信度有限。",
                          "建議：增加取樣數量後重新分析。"))
        else:
            diags.append(("ok", "✓", f"樣本數 {spc_n} 筆，符合統計基本需求。", ""))

        if ca2 is not None:
            a = abs(ca2)
            diags.append((
                "ok" if a < 12.5 else "warning" if a < 25 else "error",
                "✓" if a < 12.5 else "△" if a < 25 else "✕",
                f"Ca = {a:.1f}%（{ca_g} 級）：{ca_d}。",
                _actions.get(ca_g, "")
            ))

        diags.append((
            "ok" if cp2 >= 1.33 else "warning" if cp2 >= 1.0 else "error",
            "✓" if cp2 >= 1.33 else "△" if cp2 >= 1.0 else "✕",
            f"Cp = {cp2:.3f}（{cp_g} 級）：{cp_d}。",
            _actions.get(cp_g, "")
        ))

        diags.append((
            "ok" if cpk2 >= 1.33 else "warning" if cpk2 >= 1.0 else "error",
            "★" if cpk2 >= 1.33 else "△" if cpk2 >= 1.0 else "✕",
            f"Cpk = {cpk2:.3f}（{cpk_g} 級）：{cpk_d}。",
            _actions.get(cpk_g, "")
        ))

        if out_usl2 + out_lsl2 > 0:
            diags.append(("error", "!",
                f"規格外品：超過 USL {out_usl2} 顆、低於 LSL {out_lsl2} 顆，共 {out_usl2+out_lsl2} 顆不良。",
                "建議：立即隔離不良品，追蹤生產批次根因。"))

        # 最嚴重等級
        has_error   = any(d[0] == "error"   for d in diags)
        has_warning = any(d[0] == "warning" for d in diags)

        if has_error:
            summary_bg, summary_border, summary_icon_bg, summary_icon, summary_title_color, summary_action_color = \
                "#fef2f2","#fecaca","#fee2e2","✕","#7f1d1d","#991b1b"
            worst = next(d for d in diags if d[0]=="error")
        elif has_warning:
            summary_bg, summary_border, summary_icon_bg, summary_icon, summary_title_color, summary_action_color = \
                "#fffbeb","#fde68a","#fef9c3","△","#78350f","#92400e"
            worst = next(d for d in diags if d[0]=="warning")
        else:
            summary_bg, summary_border, summary_icon_bg, summary_icon, summary_title_color, summary_action_color = \
                "#f0fdf4","#bbf7d0","#dcfce7","✓","#14532d","#166534"
            worst = diags[-1]

        # 摘要卡
        st.markdown(f"""
        <div style="background:{summary_bg};border:1px solid {summary_border};border-radius:10px;padding:16px 20px;margin-bottom:8px;">
          <div style="display:flex;align-items:flex-start;gap:12px;">
            <div style="width:32px;height:32px;border-radius:50%;background:{summary_icon_bg};display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0;">{summary_icon}</div>
            <div style="flex:1;">
              <div style="font-size:13px;font-weight:500;color:{summary_title_color};margin-bottom:4px;">{worst[2]}</div>
              <div style="font-size:12px;color:{summary_action_color};">建議行動：{worst[3]}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # 展開詳細診斷
        _color_map = {"ok": "#1e8e3e", "warning": "#d97706", "error": "#d93025"}
        with st.expander("查看完整診斷報告", expanded=False):
            for lvl, icon, msg, action in diags:
                clr = _color_map[lvl]
                st.markdown(f"""
                <div style="border-left:4px solid {clr};background:#EFE3D5;border-radius:0 6px 6px 0;padding:9px 14px;margin-bottom:6px;">
                  <span style="color:{clr};font-weight:600;margin-right:8px;">{icon}</span>
                  <span style="font-size:13px;color:#2C1F14;">{msg}</span>
                  {"<div style='font-size:12px;color:#5f6368;margin-top:4px;padding-left:20px;'>→ " + action + "</div>" if action else ""}
                </div>
                """, unsafe_allow_html=True)

        # 評價對照表
        with st.expander("📋 評價基準對照表", expanded=False):
            st.dataframe(pd.DataFrame({
                "等級":   ["A+",    "A",         "B",       "C",     "D"],
                "Cp/Cpk": ["≥1.67", "1.33–1.67", "1.00–1.33","0.67–1.00","<0.67"],
                "|Ca|":   ["<6.25%","6.25–12.5%","12.5–25%","25–50%",">50%"],
                "判斷":   ["製程極佳","製程良好","製程尚可","能力不足","能力極差"],
                "建議":   ["可降低管制成本","繼續維持","加強管制","加強訓練","全面停機檢討"],
            }), use_container_width=True, hide_index=True)

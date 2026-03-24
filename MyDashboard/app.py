import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import base64, os
from theme import THEME_CSS, render_landing, show_loading, CHART_THEME

st.set_page_config(page_title="AegisCore", layout="wide", page_icon="👁️", initial_sidebar_state="expanded")
st.markdown(THEME_CSS, unsafe_allow_html=True)

# ── 全域圖表色盤 ──────────────────────────────────────────
CHART_BG      = "#ffffff"
CHART_GRID    = "#e2e8f0"
CHART_TEXT    = "#1e293b"
CHART_AXIS    = "#cbd5e1"
CHART_AVG     = "#10b981"   # 翠綠：平均線
CHART_UCL     = "#ef4444"   # 紅：管制上下限
CHART_NORMAL  = "rgba(96,165,250,0.65)"   # 藍：直方圖正常範圍
CHART_OUTLIER = "rgba(239,68,68,0.70)"    # 紅：規格外
CHART_CURVE   = "#0ea5e9"   # 天藍：常態曲線

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
_logo_candidates = ["logo_zheng.svg", "MyDashboard/logo_zheng.svg"]
_logo_path = next((p for p in _logo_candidates if os.path.exists(p)), None)
if _logo_path:
    try:
        with open(_logo_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        mime = "image/svg+xml" if _logo_path.endswith(".svg") else "image/png"
        st.markdown(f"""
<style>
.glowing-logo {{
    position:fixed; bottom:80px; right:28px; width:64px; z-index:9999;
    opacity:0.60; filter:drop-shadow(0 2px 10px rgba(14,165,233,0.35));
    transition:all 0.3s ease; cursor:pointer;
}}
.glowing-logo:hover {{ opacity:1; transform:scale(1.12) translateY(-4px); }}
</style>
<img src="data:{mime};base64,{img_b64}" class="glowing-logo">
""", unsafe_allow_html=True)
    except Exception:
        pass

with st.sidebar:
    st.header("⚙️ 儀表板控制中心")
    uploaded_file = st.file_uploader("📂 上傳 RAW DATA", type=["xlsx", "csv"])
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
file_id = uploaded_file.name + str(uploaded_file.size)

if st.session_state.get("loaded_file_id") != file_id:
    show_loading()
    st.session_state["raw_df"] = load_and_clean_data(
        uploaded_file.read(), uploaded_file.name
    )
    st.session_state["loaded_file_id"] = file_id
    st.rerun()

raw_df = st.session_state["raw_df"]
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
    st.markdown("""
    <div style="margin-bottom:8px;">
      <div style="font-size:16px;font-weight:700;color:#0f172a;margin-bottom:4px;">
        🎯 篩選器
      </div>
      <div style="font-size:13px;color:#64748b;">💡 條件即時連動，支援跨月多選</div>
    </div>
    """, unsafe_allow_html=True)

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
        st.markdown(
            f'<div style="font-size:14px;font-weight:600;color:#1e293b;'
            f'margin-bottom:4px;margin-top:8px;">{label}</div>',
            unsafe_allow_html=True
        )
        return st.multiselect("", options=opts, key=k,
                              placeholder="ALL",
                              label_visibility="collapsed")

    f_month  = cascading_filter('生產年月',      df,    "🗓️ 生產年月")
    df_f1 = df[df['生產年月'].astype(str).isin(f_month)] if f_month else df.copy()

    f_order  = cascading_filter('訂單號碼',      df_f1, "📝 訂單號碼")
    df_f2 = df_f1[df_f1['訂單號碼'].astype(str).isin(f_order)] if f_order else df_f1.copy()

    f_thick  = cascading_filter('訂單厚度',      df_f2, "📏 訂單厚度")
    df_f3 = df_f2[df_f2['訂單厚度'].astype(str).isin(f_thick)] if f_thick else df_f2.copy()

    f_width  = cascading_filter('訂單寬度',      df_f3, "↔️ 訂單寬度")
    df_f4 = df_f3[df_f3['訂單寬度'].astype(str).isin(f_width)] if f_width else df_f3.copy()

    f_mat    = cascading_filter('熱軋材質',      df_f4, "🪨 熱軋材質")
    df_f5 = df_f4[df_f4['熱軋材質'].astype(str).isin(f_mat)] if f_mat else df_f4.copy()

    f_spec   = cascading_filter('產品規格代碼',  df_f5, "📋 產品規格代碼")
    df_f6 = df_f5[df_f5['產品規格代碼'].astype(str).isin(f_spec)] if f_spec else df_f5.copy()

    f_maker  = cascading_filter('原料製造廠商',  df_f6, "🏭 原料製造廠商")
    df_f7 = df_f6[df_f6['原料製造廠商'].astype(str).isin(f_maker)] if f_maker else df_f6.copy()

    f_plate  = cascading_filter('取板位置',      df_f7, "📍 取板位置")
    df_f8 = df_f7[df_f7['取板位置'].astype(str).isin(f_plate)] if f_plate else df_f7.copy()

    f_coat_type = cascading_filter('鍍製別',     df_f8, "🏷️ 鍍製別")
    df_f9 = df_f8[df_f8['鍍製別'].astype(str).isin(f_coat_type)] if f_coat_type else df_f8.copy()

    f_coat   = cascading_filter('上鍍層',        df_f9, "🔩 上鍍層")
    df_f10 = df_f9[df_f9['上鍍層'].astype(str).isin(f_coat)] if f_coat else df_f9.copy()

    f_usage  = cascading_filter('用途中文說明',  df_f10, "📌 用途中文說明")
    filtered_df = df_f10[df_f10['用途中文說明'].astype(str).isin(f_usage)] if f_usage else df_f10.copy()

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

is_7b = plot_df['試驗等級'].astype(str).str.upper().str.replace(' ','').str.contains('7B', na=False) \
        if '試驗等級' in plot_df.columns else pd.Series([False]*len(plot_df), index=plot_df.index)
abnormal_count = int(is_7b.sum())
yield_rate = (len(plot_df) - abnormal_count) / len(plot_df) * 100 if len(plot_df) > 0 else 100.0
months_count = plot_df['生產年月'].nunique() if '生產年月' in plot_df.columns else 0

# ── 頂部資訊列 ─────────────────────────────────────
st.markdown(f"""
<div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:14px;
    padding:16px 24px;margin-bottom:14px;
    display:flex;align-items:center;justify-content:space-between;">
  <div style="display:flex;align-items:center;gap:14px;">
    <div style="width:10px;height:10px;border-radius:50%;background:#10b981;
        box-shadow:0 0 0 3px #d1fae5;flex-shrink:0;"></div>
    <div>
      <div style="font-size:17px;font-weight:700;color:#0f172a;">{uploaded_file.name}</div>
      <div style="font-size:14px;color:#94a3b8;margin-top:2px;">共 {len(raw_df):,} 筆原始資料</div>
    </div>
  </div>
  <div style="display:flex;gap:28px;align-items:center;">
    <div style="text-align:center;">
      <div style="font-size:12px;color:#94a3b8;font-weight:700;text-transform:uppercase;
          letter-spacing:.8px;margin-bottom:4px;">月份涵蓋</div>
      <div style="font-size:20px;font-weight:800;color:#0ea5e9;">
          {df['生產年月'].nunique() if '生產年月' in df.columns else '—'} 個月</div>
    </div>
    <div style="width:1px;height:36px;background:#e2e8f0;"></div>
    <div style="text-align:center;">
      <div style="font-size:12px;color:#94a3b8;font-weight:700;text-transform:uppercase;
          letter-spacing:.8px;margin-bottom:4px;">可分析參數</div>
      <div style="font-size:20px;font-weight:800;color:#0ea5e9;">{len(available_params)} 項</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# ── 指標卡片 ───────────────────────────────────────
abnormal_pct = abnormal_count / len(plot_df) * 100 if len(plot_df) > 0 else 0
yield_bar    = min(yield_rate, 100)

c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"""
<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;
    padding:16px 18px;border-left:4px solid #0ea5e9;">
  <div style="font-size:12px;color:#94a3b8;font-weight:700;text-transform:uppercase;
      letter-spacing:.8px;margin-bottom:8px;">總鋼捲數</div>
  <div style="font-size:26px;font-weight:800;color:#0f172a;line-height:1.1;">{len(plot_df):,}</div>
  <div style="font-size:14px;color:#64748b;margin-top:6px;">顆</div>
</div>""", unsafe_allow_html=True)

c2.markdown(f"""
<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;
    padding:16px 18px;border-left:4px solid #0ea5e9;">
  <div style="font-size:12px;color:#94a3b8;font-weight:700;text-transform:uppercase;
      letter-spacing:.8px;margin-bottom:8px;">平均值</div>
  <div style="font-size:26px;font-weight:800;color:#0f172a;line-height:1.1;">{avg_val:.3f}</div>
  <div style="font-size:14px;color:#64748b;margin-top:6px;">{selected_param}</div>
</div>""", unsafe_allow_html=True)

c3.markdown(f"""
<div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;
    padding:16px 18px;border-left:4px solid #10b981;">
  <div style="font-size:12px;color:#94a3b8;font-weight:700;text-transform:uppercase;
      letter-spacing:.8px;margin-bottom:8px;">良品率</div>
  <div style="font-size:26px;font-weight:800;color:#10b981;line-height:1.1;">{yield_rate:.1f}%</div>
  <div style="font-size:14px;color:#10b981;font-weight:600;margin-top:6px;">{"✓ 全數合格" if yield_rate == 100 else f"良品 {len(plot_df) - abnormal_count:,} 顆"}</div>
</div>""", unsafe_allow_html=True)

_ab_bg     = "#fffafa" if abnormal_count > 0 else "#fff"
_ab_border = "#fecaca" if abnormal_count > 0 else "#e2e8f0"
_ab_left   = "#ef4444" if abnormal_count > 0 else "#0ea5e9"
_ab_numclr = "#ef4444" if abnormal_count > 0 else "#0f172a"
_ab_sub    = f'↑ {abnormal_pct:.1f}%' if abnormal_count > 0 else "✓ 無異常"
_ab_subclr = "#ef4444" if abnormal_count > 0 else "#10b981"

c4.markdown(f"""
<div style="background:{_ab_bg};border:1px solid {_ab_border};border-radius:12px;
    padding:16px 18px;border-left:4px solid {_ab_left};">
  <div style="font-size:12px;color:#94a3b8;font-weight:700;text-transform:uppercase;
      letter-spacing:.8px;margin-bottom:8px;">異常品數量</div>
  <div style="font-size:26px;font-weight:800;color:{_ab_numclr};line-height:1.1;">{abnormal_count:,}</div>
  <div style="font-size:14px;color:{_ab_subclr};font-weight:600;margin-top:6px;">{_ab_sub}</div>
</div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
st.markdown("---")

# ══════════════════════════════════════════════════════
#  全域規格設定（趨勢圖與製程能力分析共用）
# ══════════════════════════════════════════════════════
st.markdown("""
<div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
  <div style="width:3px;height:18px;background:#ef4444;border-radius:2px;"></div>
  <span style="font-size:15px;font-weight:700;color:#0f172a;letter-spacing:.5px;">規格設定</span>
  <span style="font-size:12px;color:#94a3b8;margin-left:2px;">— 趨勢圖與製程能力分析共用</span>
</div>
""", unsafe_allow_html=True)

_gs1, _gs2, _gs3, _gs4 = st.columns([2, 2, 2, 2])
with _gs1:
    st.markdown("<div style='font-size:13px;font-weight:600;color:#475569;margin-bottom:3px;'>📐 規格類型</div>", unsafe_allow_html=True)
    spec_type = st.selectbox(
        "",
        ["雙邊 (LSL & USL)", "單邊上限 (USL only)", "單邊下限 (LSL only)", "僅目標值 (Target only)"],
        key=f"spc_spectype_{file_key}",
        label_visibility="collapsed"
    )

is_both        = "雙邊" in spec_type
is_upper       = "上限" in spec_type
is_lower       = "下限" in spec_type
is_target_only = "僅目標值" in spec_type

with _gs2:
    st.markdown("<div style='font-size:13px;font-weight:600;color:#475569;margin-bottom:3px;'>📉 LSL　規格下限</div>", unsafe_allow_html=True)
    lsl2 = st.number_input(
        "", value=float(avg_val - 4*std_val),
        key=f"spc_lsl_{selected_param}",
        disabled=is_upper or is_target_only,
        format="%.3f", label_visibility="collapsed"
    )
with _gs3:
    st.markdown("<div style='font-size:13px;font-weight:600;color:#475569;margin-bottom:3px;'>📈 USL　規格上限</div>", unsafe_allow_html=True)
    usl2 = st.number_input(
        "", value=float(avg_val + 4*std_val),
        key=f"spc_usl_{selected_param}",
        disabled=is_lower or is_target_only,
        format="%.3f", label_visibility="collapsed"
    )
with _gs4:
    st.markdown("<div style='font-size:13px;font-weight:600;color:#475569;margin-bottom:3px;'>🎯 目標值</div>", unsafe_allow_html=True)
    target2 = st.number_input(
        "", value=float(avg_val),
        key=f"spc_target_{selected_param}",
        format="%.3f", label_visibility="collapsed"
    )

st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  主分頁
# ══════════════════════════════════════════════════════
tab1, tab2 = st.tabs(["📊 數據總覽 & 趨勢分析", "📐 製程能力分析 (Ca · Cp · Cpk)"])


# ────────────────────────────────────────────────────
# TAB 1：趨勢 + 月份高亮
# ────────────────────────────────────────────────────
with tab1:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
        <div style="width:4px;height:22px;background:#0ea5e9;border-radius:2px;"></div>
        <span style="font-size:20px;font-weight:700;color:#0f172a;">生產順序異常監控圖</span>
        <span style="font-size:13px;color:#64748b;margin-left:4px;">SPC 規格上下限 (USL / LSL)</span>
    </div>
    """, unsafe_allow_html=True)

    months_list = sorted(plot_df['生產年月'].unique().tolist(), key=str) \
                  if '生產年月' in plot_df.columns else []

    hl_key = f"hl_

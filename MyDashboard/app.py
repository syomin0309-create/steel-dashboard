import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import re

st.set_page_config(page_title="鍍三線高階分析儀表板", layout="wide", page_icon="📈", initial_sidebar_state="expanded")

# 🎨 專業級視覺優化
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Microsoft JhengHei', 'Segoe UI', sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [aria-selected="true"] {
        color: #667eea;
        border-bottom: 3px solid #667eea;
    }
    .metric-highlight {
        padding: 15px;
        border-radius: 8px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-left: 4px solid #667eea;
    }
    .compare-section {
        background: #f8f9ff;
        padding: 20px;
        border-radius: 8px;
        margin: 15px 0;
    }
    .anomaly-badge {
        background: #ffe6e6;
        border-left: 4px solid #ff4444;
        padding: 12px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .normal-badge {
        background: #e6ffe6;
        border-left: 4px solid #44aa44;
        padding: 12px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .warning-badge {
        background: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 12px;
        border-radius: 5px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

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
        
    # 🌟 終極殺手鐧：徹底清除欄位名稱中的所有「空白、換行(\n)、不可見字元」
    df.columns = df.columns.astype(str).str.replace(r'\s+', '', regex=True).str.upper()
    
    # 📖 中文列名對應 (已移除會干擾的「投入厚度」、「實測寬度」，讓他精準抓取「訂單厚度」)
    rename_mapping = [
        (['鋼捲號碼', 'COIL_NO'], '產出鋼捲號碼'),
        (['PRODUCTION_DATE'], '生產日期'),
        (['QUALITY_CLASS', '投入等級'], '試驗等級'),
        (['BASE_METAL_THICK'], '訂單厚度'),
        (['REAL_WIDTH'], '訂單寬度'),
        (['COAT_STD_MIN', 'MIN_COAT_WEIGHT', '鍍層下限', '理論鍍層重', '鍍層下限值'], '鍍層下限管制值')
    ]
    
    # ✅ 智能重命名：避免重複列名
    rename_dict = {}
    for source_cols, target_name in rename_mapping:
        for col in source_cols:
            if col in df.columns:
                rename_dict[col] = target_name
                break
    
    df.rename(columns=rename_dict, inplace=True)
    
    # 🔍 移除重複列
    if df.columns.duplicated().any():
        duplicated_cols = df.columns[df.columns.duplicated(keep=False)].unique()
        for col in duplicated_cols:
            indices = [i for i, x in enumerate(df.columns) if x == col]
            for idx in indices[1:]:
                df = df.drop(df.columns[idx], axis=1)

    # 🚀 自動計算雙面總鍍層量 
    xray_sets = [
        ['XRAY_A_T_N', 'XRAY_A_T_C', 'XRAY_A_T_S', 'XRAY_A_B_N', 'XRAY_A_B_C', 'XRAY_A_B_S'],
        ['NORTH_TOP_COAT_WEIGHT', 'CENTER_TOP_COAT_WEIGHT', 'SOUTH_TOP_COAT_WEIGHT', 
         'NORTH_BACK_COAT_WEIGHT', 'CENTER_BACK_COAT_WEIGHT', 'SOUTH_BACK_COAT_WEIGHT'],
        ['北正面鍍層', '中正面鍍層', '南正面鍍層', '北背面鍍層', '中背面鍍層', '南背面鍍層']
    ]
    
    best_set = None
    max_valid = -1
    
    for cols in xray_sets:
        if all(col in df.columns for col in cols):
            valid_count = df[cols].apply(pd.to_numeric, errors='coerce').notna().sum().sum()
            if valid_count > max_valid:
                max_valid = valid_count
                best_set = cols
                
    if best_set and max_valid > 0:
        for col in best_set:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df['雙面總鍍層量(AVG)'] = (df[best_set[0]] + df[best_set[1]] + df[best_set[2]]) / 3 + \
                                (df[best_set[3]] + df[best_set[4]] + df[best_set[5]]) / 3

    def extract_year_month(date_val):
        try:
            dt = pd.to_datetime(date_val)
            return f"{dt.year}年{dt.month}月"
        except:
            return str(date_val)
            
    if '生產日期' in df.columns:        
        df['生產年月'] = df['生產日期'].apply(extract_year_month)
    else:
        df['生產年月'] = '全區間'
        
    return df

# ============ 主頁面開始 ============

col_logo, col_title = st.columns([1, 9])
with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/2040/2040504.png", width=60)
with col_title:
    st.title("📊 鍍三線品質與製程能力儀表板")
    st.markdown("**層峰決策版 · 多維度對比分析**")

# ============ 側邊欄：文件上傳 ============

with st.sidebar:
    st.header("⚙️ 儀表板控制中心")
    uploaded_file = st.file_uploader("📂 上傳產線 RAW DATA", type=["xlsx", "csv"])
    st.markdown("---")
    
    if uploaded_file:
        st.success("✅ 文件已加載")
        st.caption(f"文件名：{uploaded_file.name}")

if uploaded_file is not None:
    raw_df = load_and_clean_data(uploaded_file.read(), uploaded_file.name)
    df = raw_df.copy()

    # 🧠 模式判定
    is_standard_mode = '試驗等級' in df.columns and not df['試驗等級'].dropna().empty
    
    if is_standard_mode:
        df = df[df['試驗等級'].astype(str).str.strip() != ''] 
        df = df[df['試驗等級'].astype(str).str.lower() != 'nan']
        df["比對群組"] = df["生產年月"] + " - " + df["試驗等級"].astype(str)
    else:
        df["比對群組"] = "全批次數據"

    # ============ 側邊欄：智能級聯篩選器 ============
    with st.sidebar:
        st.subheader("🎯 智能連動篩選器")
        st.caption("💡 絕對不會出現不存在的規格！上方選擇後，下方選單將即時連動。")
        
        file_key = uploaded_file.name
        
        def create_cascading_filter(col_name, current_df):
            if col_name not in current_df.columns:
                return []
            
            # 獲取該數據集中實際存在的選項 (強制轉為字串)
            valid_opts = sorted(current_df[col_name].dropna().astype(str).unique())
            
            if not valid_opts:
                st.warning(f"⚠️ 查無 {col_name} 數據")
                return []
            
            key_name = f"filter_{file_key}_{col_name}"
            
            # 🌟 神級防呆：清理失效的 Session State，防止 Streamlit 當機
            if key_name in st.session_state:
                st.session_state[key_name] = [x for x in st.session_state[key_name] if x in valid_opts]
            
            selected = st.multiselect(
                f"🔹 選擇 {col_name}",
                options=valid_opts,
                key=key_name
            )
            return selected

        # ========== 瀑布流連動核心 ==========
        
        # 1. 生產年月
        f_month = create_cascading_filter('生產年月', df)
        df_f1 = df.copy()
        if f_month:
            df_f1 = df_f1[df_f1['生產年月'].astype(str).isin(f_month)]
            
        # 2. 訂單厚度 (只抓 df_f1 剩下的)
        f_thick = create_cascading_filter('訂單厚度', df_f1)
        df_f2 = df_f1.copy()
        if f_thick:
            df_f2 = df_f2[df_f2['訂單厚度'].astype(str).isin(f_thick)]
            
        # 3. 訂單寬度 (只抓 df_f2 剩下的)
        f_width = create_cascading_filter('訂單寬度', df_f2)
        df_f3 = df_f2.copy()
        if f_width:
            df_f3 = df_f3[df_f3['訂單寬度'].astype(str).isin(f_width)]
            
        # 4. 熱軋材質
        f_mat = create_cascading_filter('熱軋材質', df_f3)
        df_f4 = df_f3.copy()
        if f_mat:
            df_f4 = df_f4[df_f4['熱軋材質'].astype(str).isin(f_mat)]
            
        # 5. 產品規格代碼
        f_spec = create_cascading_filter('產品規格代碼', df_f4)
        df_f5 = df_f4.copy()
        if f_spec:
            df_f5 = df_f5[df_f5['產品規格代碼'].astype(str).isin(f_spec)]
            
        # 6. 上鍍層
        f_up_coat = create_cascading_filter('上鍍層', df_f5)
        df_f6 = df_f5.copy()
        if f_up_coat:
            df_f6 = df_f6[df_f6['上鍍層'].astype(str).isin(f_up_coat)]
            
        # 7. 鍍層下限管制值
        f_coat_limit = create_cascading_filter('鍍層下限管制值', df_f6)
        
    # 🌟 將最後過濾完的資料集交給主畫面
    filtered_df = df_f6.copy()
    if f_coat_limit:
        filtered_df = filtered_df[filtered_df['鍍層下限管制值'].astype(str).isin(f_coat_limit)]

    if filtered_df.empty:
        st.warning("⚠️ 目前篩選條件下沒有找到任何數據，請放寬左側的篩選條件！")
    else:
        # ============ 核心儀表板 ============
        
        # 📊 數據概覽卡片
        st.markdown("### 📊 數據概覽")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("鋼捲總數", f"{len(filtered_df)} 顆", delta=f"+{len(filtered_df) - len(df) if len(filtered_df) < len(df) else 0}")
        with col2:
            prod_months = filtered_df['生產年月'].nunique() if '生產年月' in filtered_df.columns else 0
            st.metric("生產月份", f"{prod_months} 個月")
        with col3:
            spec_count = filtered_df['產品規格代碼'].nunique() if '產品規格代碼' in filtered_df.columns else 0
            st.metric("規格種類", f"{spec_count} 種")
        with col4:
            if '試驗等級' in filtered_df.columns:
                grade_count = filtered_df['試驗等級'].nunique()
                st.metric("試驗等級", f"{grade_count} 級")
            else:
                st.metric("試驗等級", "N/A")

        st.markdown("---")

        # ============ 標籤頁：單一分析 vs 對比分析 ============
        tab_analysis, tab_comparison = st.tabs(["📈 單一參數分析", "🔄 多時段對比分析"])

        # ============ 標籤 1：單一參數分析 ============
        with tab_analysis:
            st.markdown("### 選擇分析參數")
            
            numeric_cols = filtered_df.select_dtypes(include=['number']).columns.tolist()
            exclude_sys = ['產出鋼捲號碼', '試驗等級', '投入等級', '生產日期', '比對群組', '生產年月', 'SHIFT_NO', '鍍層下限管制值',
                           '北正面鍍層', '中正面鍍層', '南正面鍍層', '北背面鍍層', '中背面鍍層', '南背面鍍層',
                           'XRAY_A_T_N', 'XRAY_A_T_C', 'XRAY_A_T_S', 'XRAY_A_B_N', 'XRAY_A_B_C', 'XRAY_A_B_S',
                           'NORTH_TOP_COAT_WEIGHT', 'CENTER_TOP_COAT_WEIGHT', 'SOUTH_TOP_COAT_WEIGHT', 
                           'NORTH_BACK_COAT_WEIGHT', 'CENTER_BACK_COAT_WEIGHT', 'SOUTH_BACK_COAT_WEIGHT']
            
            available_params = [col for col in numeric_cols if col not in exclude_sys]
            
            # 置頂防呆
            if '雙面總鍍層量(AVG)' in available_params:
                available_params = ['雙面總鍍層量(AVG)'] + [x for x in available_params if x != '雙面總鍍層量(AVG)']
            
            if available_params:
                col_select, col_info = st.columns([3, 1])
                with col_select:
                    selected_param = st.selectbox("🔍 選擇分析參數", available_params, key=f"param_{uploaded_file.name}")
                
                plot_df = filtered_df.dropna(subset=[selected_param])
                
                if not plot_df.empty:
                    avg_val = plot_df[selected_param].mean()
                    std_val = plot_df[selected_param].std()
                    median_val = plot_df[selected_param].median()
                    
                    if pd.isna(avg_val): avg_val = 0.0
                    if pd.isna(std_val): std_val = 0.0
                    
                    ucl = avg_val + 3 * std_val
                    lcl = avg_val - 3 * std_val
                    
                    # SPC 規格設定
                    st.markdown("### 📐 SPC 規格設定")
                    
                    default_lsl = float(avg_val - 4 * std_val) if std_val > 0 else float(avg_val - 10)
                    if f_coat_limit and len(f_coat_limit) == 1:
                        try:
                            default_lsl = float(f_coat_limit[0])
                        except:
                            pass
                    
                    spec_col1, spec_col2, spec_col3 = st.columns(3)
                    with spec_col1:
                        lsl = st.number_input("規格下限 (LSL)", value=default_lsl, key="lsl_single")
                    with spec_col2:
                        usl = st.number_input("規格上限 (USL)", value=float(lsl + 40) if f_coat_limit else (float(avg_val + 4 * std_val) if std_val > 0 else float(avg_val + 10)), key="usl_single")
                    with spec_col3:
                        target = st.number_input("規格中心值 (Target)", value=float((avg_val + lsl) / 2), key="target_single")
                    
                    # 計算製程能力指數
                    cp = (usl - lsl) / (6 * std_val) if std_val > 0 else 0
                    ca = (avg_val - target) / ((usl - lsl) / 2) * 100 if usl != lsl else 0
                    cpk = min((usl - avg_val) / (3 * std_val), (avg_val - lsl) / (3 * std_val)) if std_val > 0 else 0
                    
                    # 製程能力卡片
                    st.markdown("### 📊 製程能力指標")
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    
                    with metric_col1:
                        st.markdown(f"""
                        <div class="metric-highlight">
                            <strong>樣本數</strong><br>
                            <h2>{len(plot_df)} 顆</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with metric_col2:
                        st.markdown(f"""
                        <div class="metric-highlight">
                            <strong>Cp (精密度)</strong><br>
                            <h2>{cp:.2f}</h2>
                            <small>變異大小</small>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with metric_col3:
                        st.markdown(f"""
                        <div class="metric-highlight">
                            <strong>Ca (準確度)</strong><br>
                            <h2>{abs(ca):.1f}%</h2>
                            <small>偏離中心值</small>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    cpk_color = "🟢" if cpk >= 1.33 else ("🟡" if cpk >= 1.0 else "🔴")
                    cpk_status = "優良(A)" if cpk >= 1.33 else ("尚可(B)" if cpk >= 1.0 else "需改善(C)")
                    
                    with metric_col4:
                        st.markdown(f"""
                        <div class="metric-highlight">
                            <strong>Cpk {cpk_color}</strong><br>
                            <h2>{cpk:.2f}</h2>
                            <small>{cpk_status}</small>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    # 統計資訊
                    stats_col1, stats_col2, stats_col3 = st.columns(3)
                    with stats_col1:
                        st.write(f"**平均值**: {avg_val:.4f}")
                        st.write(f"**中位數**: {median_val:.4f}")
                    with stats_col2:
                        st.write(f"**標準差**: {std_val:.4f}")
                        st.write(f"**變異係數**: {(std_val/avg_val*100) if avg_val != 0 else 0:.2f}%")
                    with stats_col3:
                        st.write(f"**最小值**: {plot_df[selected_param].min():.4f}")
                        st.write(f"**最大值**: {plot_df[selected_param].max():.4f}")
                    
                    st.markdown("---")
                    
                    # 圖表
                    st.markdown("### 📉 視覺分析")
                    chart_col1, chart_col2 = st.columns([1.5, 1])
                    
                    with chart_col1:
                        # CPK 分佈圖
                        fig_hist = px.histogram(
                            plot_df, x=selected_param, nbins=30, opacity=0.7,
                            histnorm='probability density',
                            color_discrete_sequence=['#667eea'],
                            title=f"【{selected_param}】常態分佈與規格區間"
                        )
                        
                        if std_val > 0:
                            x_min = min(plot_df[selected_param].min(), lsl)
                            x_max = max(plot_df[selected_param].max(), usl)
                            x_curve = np.linspace(x_min - std_val, x_max + std_val, 200)
                            y_pdf = (1 / (std_val * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_curve - avg_val) / std_val) ** 2)
                            fig_hist.add_trace(go.Scatter(x=x_curve, y=y_pdf, mode='lines', 
                                                         line=dict(color='#FF2B2B', width=3), name='常態分佈'))
                        
                        fig_hist.add_vline(x=usl, line_dash="solid", line_color="#FF4B4B", annotation_text=f"USL: {usl:.2f}")
                        fig_hist.add_vline(x=lsl, line_dash="solid", line_color="#FF4B4B", annotation_text=f"LSL: {lsl:.2f}")
                        fig_hist.add_vline(x=target, line_dash="solid", line_color="#00CC96", annotation_text=f"目標: {target:.2f}")
                        
                        fig_hist.update_layout(height=450)
                        st.plotly_chart(fig_hist, use_container_width=True)
                    
                    with chart_col2:
                        # 分佈統計圓餅圖
                        outside_usl = len(plot_df[plot_df[selected_param] > usl])
                        outside_lsl = len(plot_df[plot_df[selected_param] < lsl])
                        inside = len(plot_df) - outside_usl - outside_lsl
                        
                        fig_pie = px.pie(
                            values=[inside, outside_usl, outside_lsl],
                            names=['符合規格', '超過上限', '低於下限'],
                            color_discrete_sequence=['#28a745', '#ff6b6b', '#ffc107'],
                            title="規格符合率"
                        )
                        fig_pie.update_layout(height=450)
                        st.plotly_chart(fig_pie, use_container_width=True)
                    
                    # 趨勢走勢圖
                    st.markdown("### 📈 生產順序趨勢")
                    x_axis_col = "產出鋼捲號碼" if "產出鋼捲號碼" in plot_df.columns else plot_df.index
                    
                    fig_line = px.line(plot_df, x=x_axis_col, y=selected_param, color="比對群組", 
                                      markers=True, title=f"【{selected_param}】 SPC 管制走勢圖")
                    
                    fig_line.add_hrect(y0=lcl, y1=ucl, line_width=0, fillcolor="#00CC96", opacity=0.08)
                    fig_line.add_hline(y=avg_val, line_dash="dash", line_color="green")
                    fig_line.add_hline(y=ucl, line_dash="dot", line_color="red")
                    fig_line.add_hline(y=lcl, line_dash="dot", line_color="red")
                    fig_line.update_xaxes(showticklabels=False)
                    fig_line.update_layout(height=400)
                    
                    st.plotly_chart(fig_line, use_container_width=True)

        # ============ 標籤 2：多時段對比分析 ============
        with tab_comparison:
            st.markdown("### 🔄 多時段對比分析 (層峰決策版)")
            st.markdown("比對不同時段、規格的生產品質差異，識別異常點")
            
            # 對比條件設置
            comp_col1, comp_col2 = st.columns(2)
            
            with comp_col1:
                period_a_months = st.multiselect("📅 選擇時段 A 的月份", sorted(filtered_df['生產年月'].astype(str).unique()), key="comp_a_m")
            
            with comp_col2:
                period_b_months = st.multiselect("📅 選擇時段 B 的月份", sorted(filtered_df['生產年月'].astype(str).unique()), key="comp_b_m")
            
            if period_a_months and period_b_months:
                df_a = filtered_df[filtered_df['生產年月'].astype(str).isin(period_a_months)].copy()
                df_b = filtered_df[filtered_df['生產年月'].astype(str).isin(period_b_months)].copy()
                
                numeric_cols_comp = filtered_df.select_dtypes(include=['number']).columns.tolist()
                available_params_comp = [col for col in numeric_cols_comp if col not in exclude_sys]
                if '雙面總鍍層量(AVG)' in available_params_comp:
                    available_params_comp = ['雙面總鍍層量(AVG)'] + [x for x in available_params_comp if x != '雙面總鍍層量(AVG)']
                
                st.markdown("---")
                selected_param_comp = st.selectbox("🔍 選擇要對比的參數", available_params_comp, key="param_comp")
                
                if selected_param_comp and not df_a.empty and not df_b.empty:
                    df_a_clean = df_a.dropna(subset=[selected_param_comp])
                    df_b_clean = df_b.dropna(subset=[selected_param_comp])
                    
                    if len(df_a_clean) > 0 and len(df_b_clean) > 0:
                        stats_a = {
                            'mean': df_a_clean[selected_param_comp].mean(),
                            'std': df_a_clean[selected_param_comp].std(),
                            'median': df_a_clean[selected_param_comp].median(),
                            'count': len(df_a_clean)
                        }
                        
                        stats_b = {
                            'mean': df_b_clean[selected_param_comp].mean(),
                            'std': df_b_clean[selected_param_comp].std(),
                            'median': df_b_clean[selected_param_comp].median(),
                            'count': len(df_b_clean)
                        }
                        
                        st.markdown("---")
                        st.markdown("### 📊 對比結果")
                        
                        # 🌟 先在外面把字串算好，徹底避開 f-string 引號衝突
                        str_period_a = " + ".join(period_a_months)
                        str_period_b = " + ".join(period_b_months)
                        
                        comp_card_col1, comp_card_col2, comp_card_col3 = st.columns(3)
                        
                        with comp_card_col1:
                            st.markdown(f"""
                            <div class="compare-section">
                                <h4>時段 A</h4>
                                <strong>{str_period_a}</strong><br><br>
                                🔹 樣本數: <strong>{stats_a['count']}</strong><br>
                                🔹 平均值: <strong>{stats_a['mean']:.4f}</strong><br>
                                🔹 標準差: <strong>{stats_a['std']:.4f}</strong>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with comp_card_col2:
                            mean_diff = stats_b['mean'] - stats_a['mean']
                            mean_diff_pct = (mean_diff / stats_a['mean'] * 100) if stats_a['mean'] != 0 else 0
                            diff_color = "🔴" if abs(mean_diff_pct) > 5 else "🟡" if abs(mean_diff_pct) > 2 else "🟢"
                            
                            std_ratio = (stats_b['std']/stats_a['std']) if stats_a['std']!=0 else 0
                            
                            st.markdown(f"""
                            <div class="compare-section" style="background: #f0f7ff;">
                                <h4>變化 (B vs A)</h4>
                                <strong>{diff_color} 平均值差異</strong><br><br>
                                差值: <strong>{mean_diff:+.4f}</strong><br>
                                變化率: <strong>{mean_diff_pct:+.2f}%</strong><br>
                                標準差比: <strong>{std_ratio:.2f}x</strong>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with comp_card_col3:
                            st.markdown(f"""
                            <div class="compare-section">
                                <h4>時段 B</h4>
                                <strong>{str_period_b}</strong><br><br>
                                🔹 樣本數: <strong>{stats_b['count']}</strong><br>
                                🔹 平均值: <strong>{stats_b['mean']:.4f}</strong><br>
                                🔹 標準差: <strong>{stats_b['std']:.4f}</strong>
                            </div>
                            """, unsafe_allow_html=True)

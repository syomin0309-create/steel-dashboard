import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

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
    
    # 📖 中文列名對應
    rename_mapping = [
        (['鋼捲號碼'], '產出鋼捲號碼'),
        (['投入厚度'], '訂單厚度'),
        (['實測寬度'], '訂單寬度'),
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

    # ============ 側邊欄：篩選器 ============
    with st.sidebar:
        st.subheader("🎯 Excel風格篩選器")
        st.caption("💡 灰色項目表示無數據 | 數字表示該條件下的鋼捲數")
        
        file_key = uploaded_file.name
        
        def create_excel_filter(col_name, current_df):
            """
            Excel風格篩選器：顯示每個選項的數據量
            灰顯無數據項，允許多選
            """
            if col_name not in current_df.columns:
                return []
            
            try:
                # 獲取所有可能的選項及其計數
                all_options = current_df[col_name].dropna().astype(str).unique()
                option_counts = current_df[col_name].astype(str).value_counts().to_dict()
                
                # 建立顯示文本（帶數據量）
                display_options = {}
                for opt in sorted(all_options):
                    count = option_counts.get(opt, 0)
                    if count > 0:
                        display_options[f"✓ {opt} ({count})"] = opt
                    else:
                        display_options[f"✗ {opt} (0)"] = opt  # 灰顯
                
                if not display_options:
                    st.warning(f"⚠️ {col_name} 無可用選項")
                    return []
                
                # 使用自訂的多選框，顯示數據量
                selected = st.multiselect(
                    f"🔹 {col_name}",
                    options=list(display_options.keys()),
                    key=f"filter_{file_key}_{col_name}"
                )
                
                # 返回實際的值（不含計數和符號）
                return [display_options[s] for s in selected]
            
            except Exception as e:
                st.error(f"⚠️ {col_name} 讀取失敗：{str(e)}")
                return []
        
        # 關鍵篩選項
        st.markdown("**📍 關鍵篩選條件：**")
        f_month = create_excel_filter('生產年月', df)
        f_thick = create_excel_filter('訂單厚度', df)
        f_width = create_excel_filter('訂單寬度', df)
        f_mat   = create_excel_filter('熱軋材質', df)
        f_spec  = create_excel_filter('產品規格代碼', df)
        
        st.markdown("**📍 其他篩選：**")
        f_up_coat = create_excel_filter('上鍍層', df)
        
    # 應用篩選
    filtered_df = df.copy()
    if f_month: filtered_df = filtered_df[filtered_df['生產年月'].isin(f_month)]
    if f_thick: filtered_df = filtered_df[filtered_df['訂單厚度'].isin(f_thick)]
    if f_width: filtered_df = filtered_df[filtered_df['訂單寬度'].isin(f_width)]
    if f_mat:   filtered_df = filtered_df[filtered_df['熱軋材質'].isin(f_mat)]
    if f_spec:  filtered_df = filtered_df[filtered_df['產品規格代碼'].isin(f_spec)]
    if f_up_coat: filtered_df = filtered_df[filtered_df['上鍍層'].isin(f_up_coat)]

    if filtered_df.empty:
        st.warning("⚠️ 目前篩選條件下沒有找到任何數據，請調整篩選條件")
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
            exclude_sys = ['產出鋼捲號碼', '試驗等級', '投入等級', '生產日期', '比對群組', '生產年月', 'SHIFT_NO',
                           '北正面鍍層', '中正面鍍層', '南正面鍍層', '北背面鍍層', '中背面鍍層', '南背面鍍層',
                           'XRAY_A_T_N', 'XRAY_A_T_C', 'XRAY_A_T_S', 'XRAY_A_B_N', 'XRAY_A_B_C', 'XRAY_A_B_S',
                           'NORTH_TOP_COAT_WEIGHT', 'CENTER_TOP_COAT_WEIGHT', 'SOUTH_TOP_COAT_WEIGHT', 
                           'NORTH_BACK_COAT_WEIGHT', 'CENTER_BACK_COAT_WEIGHT', 'SOUTH_BACK_COAT_WEIGHT']
            
            available_params = [col for col in numeric_cols if col not in exclude_sys]
            
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
                    
                    spec_col1, spec_col2, spec_col3 = st.columns(3)
                    with spec_col1:
                        lsl = st.number_input("規格下限 (LSL)", value=default_lsl, key="lsl_single")
                    with spec_col2:
                        target = st.number_input("規格中心值 (Target)", value=float((avg_val + lsl) / 2), key="target_single")
                    with spec_col3:
                        usl = st.number_input("規格上限 (USL)", value=float(avg_val + 4 * std_val) if std_val > 0 else float(avg_val + 10), key="usl_single")
                    
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
                        st.write(f"**變異係數**: {(std_val/avg_val*100):.2f}%")
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
                        # 分佈統計
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
                    
                    # 趨勢圖
                    if is_standard_mode and '比對群組' in plot_df.columns:
                        st.markdown("### 📈 時間序列趨勢")
                        
                        x_axis_col = "產出鋼捲號碼" if "產出鋼捲號碼" in plot_df.columns else plot_df.index
                        
                        fig_line = px.line(plot_df, x=x_axis_col, y=selected_param, color="比對群組", 
                                          markers=True, title=f"【{selected_param}】生產趨勢")
                        
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
            st.markdown("💡 **動態篩選提示**：當您選定時段後，規格篩選菜單將只顯示該時段內**實際存在**的條件，無需盲目試錯！")
            
            # 對比條件設置
            comp_col1, comp_col2 = st.columns(2)
            
            with comp_col1:
                st.markdown("**時段 A：**")
                period_a_months = st.multiselect("選擇時段A的月份", 
                                                  sorted(filtered_df['生產年月'].unique()), 
                                                  key="period_a_months")
            
            with comp_col2:
                st.markdown("**時段 B：**")
                period_b_months = st.multiselect("選擇時段B的月份", 
                                                  sorted(filtered_df['生產年月'].unique()), 
                                                  key="period_b_months")
            
            if period_a_months and period_b_months:
                # ✨ 動態篩選：根據選定時段獲取可用的規格選項
                df_a_all = filtered_df[filtered_df['生產年月'].isin(period_a_months)]
                df_b_all = filtered_df[filtered_df['生產年月'].isin(period_b_months)]
                
                st.markdown("**精確規格篩選 (Excel風格) - ✨ 顯示數據量，灰色表示無數據**")
                
                # ========== Excel 風格的動態篩選函數 ==========
                def create_dynamic_excel_filter(col_name, df_a, df_b, period_a, period_b):
                    """
                    動態 Excel 風格篩選器：
                    - 顯示時段A中該選項的數據量
                    - 顯示時段B中該選項的數據量
                    - 灰顯無數據的選項
                    """
                    if col_name not in df_a.columns or col_name not in df_b.columns:
                        return []
                    
                    try:
                        # 獲取兩個時段的所有選項及計數
                        options_a = df_a[col_name].dropna().astype(str).value_counts().to_dict()
                        options_b = df_b[col_name].dropna().astype(str).value_counts().to_dict()
                        
                        # 合併所有選項
                        all_options = sorted(set(options_a.keys()) | set(options_b.keys()))
                        
                        # 建立顯示文本
                        display_options = {}
                        for opt in all_options:
                            count_a = options_a.get(opt, 0)
                            count_b = options_b.get(opt, 0)
                            total = count_a + count_b
                            
                            if total > 0:
                                label = f"✓ {opt} (A:{count_a} | B:{count_b})"
                                display_options[label] = opt
                            else:
                                label = f"✗ {opt} (無)"
                                display_options[label] = opt
                        
                        if not display_options:
                            st.warning(f"⚠️ {col_name} 無可用選項")
                            return []
                        
                        # 多選框
                        selected = st.multiselect(
                            f"🔹 {col_name}",
                            options=list(display_options.keys()),
                            key=f"comp_{col_name}_{period_a}_{period_b}"
                        )
                        
                        return [display_options[s] for s in selected]
                    
                    except Exception as e:
                        st.error(f"⚠️ {col_name} 讀取失敗：{str(e)}")
                        return []
                
                # 應用動態 Excel 風格篩選
                comp_thick = create_dynamic_excel_filter('訂單厚度', df_a_all, df_b_all, period_a_months, period_b_months)
                comp_width = create_dynamic_excel_filter('訂單寬度', df_a_all, df_b_all, period_a_months, period_b_months)
                comp_mat = create_dynamic_excel_filter('熱軋材質', df_a_all, df_b_all, period_a_months, period_b_months)
                comp_spec = create_dynamic_excel_filter('產品規格代碼', df_a_all, df_b_all, period_a_months, period_b_months)
                
                # 篩選數據
                df_a = filtered_df[filtered_df['生產年月'].isin(period_a_months)].copy()
                df_b = filtered_df[filtered_df['生產年月'].isin(period_b_months)].copy()
                
                if comp_thick:
                    df_a = df_a[df_a['訂單厚度'].isin(comp_thick)]
                    df_b = df_b[df_b['訂單厚度'].isin(comp_thick)]
                if comp_width:
                    df_a = df_a[df_a['訂單寬度'].isin(comp_width)]
                    df_b = df_b[df_b['訂單寬度'].isin(comp_width)]
                if comp_mat:
                    df_a = df_a[df_a['熱軋材質'].isin(comp_mat)]
                    df_b = df_b[df_b['熱軋材質'].isin(comp_mat)]
                if comp_spec:
                    df_a = df_a[df_a['產品規格代碼'].isin(comp_spec)]
                    df_b = df_b[df_b['產品規格代碼'].isin(comp_spec)]
                
                # 選擇對比參數
                numeric_cols_comp = filtered_df.select_dtypes(include=['number']).columns.tolist()
                exclude_sys_comp = ['產出鋼捲號碼', '試驗等級', '投入等級', '生產日期', '比對群組', '生產年月', 'SHIFT_NO',
                                   '北正面鍍層', '中正面鍍層', '南正面鍍層', '北背面鍍層', '中背面鍍層', '南背面鍍層',
                                   'XRAY_A_T_N', 'XRAY_A_T_C', 'XRAY_A_T_S', 'XRAY_A_B_N', 'XRAY_A_B_C', 'XRAY_A_B_S',
                                   'NORTH_TOP_COAT_WEIGHT', 'CENTER_TOP_COAT_WEIGHT', 'SOUTH_TOP_COAT_WEIGHT',
                                   'NORTH_BACK_COAT_WEIGHT', 'CENTER_BACK_COAT_WEIGHT', 'SOUTH_BACK_COAT_WEIGHT']
                
                available_params_comp = [col for col in numeric_cols_comp if col not in exclude_sys_comp]
                
                if '雙面總鍍層量(AVG)' in available_params_comp:
                    available_params_comp = ['雙面總鍍層量(AVG)'] + [x for x in available_params_comp if x != '雙面總鍍層量(AVG)']
                
                st.markdown("---")
                st.markdown("**選擇對比參數：**")
                selected_param_comp = st.selectbox("🔍 分析參數", available_params_comp, key="param_comp")
                
                if selected_param_comp and not df_a.empty and not df_b.empty:
                    # 計算統計數據
                    df_a_clean = df_a.dropna(subset=[selected_param_comp])
                    df_b_clean = df_b.dropna(subset=[selected_param_comp])
                    
                    if len(df_a_clean) > 0 and len(df_b_clean) > 0:
                        stats_a = {
                            'mean': df_a_clean[selected_param_comp].mean(),
                            'std': df_a_clean[selected_param_comp].std(),
                            'median': df_a_clean[selected_param_comp].median(),
                            'min': df_a_clean[selected_param_comp].min(),
                            'max': df_a_clean[selected_param_comp].max(),
                            'count': len(df_a_clean)
                        }
                        
                        stats_b = {
                            'mean': df_b_clean[selected_param_comp].mean(),
                            'std': df_b_clean[selected_param_comp].std(),
                            'median': df_b_clean[selected_param_comp].median(),
                            'min': df_b_clean[selected_param_comp].min(),
                            'max': df_b_clean[selected_param_comp].max(),
                            'count': len(df_b_clean)
                        }
                        
                        st.markdown("---")
                        st.markdown("### 📊 對比結果")
                        
                        # 對比卡片
                        compare_period_a = " + ".join(period_a_months)
                        compare_period_b = " + ".join(period_b_months)
                        
                        comp_card_col1, comp_card_col2, comp_card_col3 = st.columns(3)
                        
                        with comp_card_col1:
                            st.markdown(f"""
                            <div class="compare-section">
                                <h4>📅 時段 A</h4>
                                <strong>{compare_period_a}</strong><br>
                                🔹 樣本數: <strong>{stats_a['count']}</strong><br>
                                🔹 平均值: <strong>{stats_a['mean']:.4f}</strong><br>
                                🔹 標準差: <strong>{stats_a['std']:.4f}</strong><br>
                                🔹 中位數: <strong>{stats_a['median']:.4f}</strong>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with comp_card_col2:
                            mean_diff = stats_b['mean'] - stats_a['mean']
                            mean_diff_pct = (mean_diff / stats_a['mean'] * 100) if stats_a['mean'] != 0 else 0
                            
                            diff_color = "🔴" if abs(mean_diff_pct) > 5 else "🟡" if abs(mean_diff_pct) > 2 else "🟢"
                            
                            st.markdown(f"""
                            <div class="compare-section" style="background: #f0f7ff;">
                                <h4>📊 變化 (B vs A)</h4>
                                <strong>{diff_color} 平均值差異</strong><br>
                                差值: <strong>{mean_diff:+.4f}</strong><br>
                                變化率: <strong>{mean_diff_pct:+.2f}%</strong><br>
                                標準差比: <strong>{(stats_b['std']/stats_a['std']):.2f}x</strong>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with comp_card_col3:
                            st.markdown(f"""
                            <div class="compare-section">
                                <h4>📅 時段 B</h4>
                                <strong>{compare_period_b}</strong><br>
                                🔹 樣本數: <strong>{stats_b['count']}</strong><br>
                                🔹 平均值: <strong>{stats_b['mean']:.4f}</strong><br>
                                🔹 標準差: <strong>{stats_b['std']:.4f}</strong><br>
                                🔹 中位數: <strong>{stats_b['median']:.4f}</strong>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("---")
                        
                        # 對比圖表
                        chart_col1, chart_col2 = st.columns(2)
                        
                        with chart_col1:
                            # 並排直方圖
                            fig_comp_hist = go.Figure()
                            fig_comp_hist.add_trace(go.Histogram(x=df_a_clean[selected_param_comp], name=f"時段A {period_a_months[0]}", 
                                                                  opacity=0.7, marker_color='#667eea', nbinsx=20))
                            fig_comp_hist.add_trace(go.Histogram(x=df_b_clean[selected_param_comp], name=f"時段B {period_b_months[0]}", 
                                                                  opacity=0.7, marker_color='#ff6b6b', nbinsx=20))
                            fig_comp_hist.update_layout(barmode='overlay', height=400, title=f"【{selected_param_comp}】分佈對比",
                                                       xaxis_title=selected_param_comp, yaxis_title="頻數")
                            st.plotly_chart(fig_comp_hist, use_container_width=True)
                        
                        with chart_col2:
                            # 箱型圖
                            df_comparison = pd.concat([
                                df_a_clean.assign(時段='A'),
                                df_b_clean.assign(時段='B')
                            ])
                            
                            fig_box_comp = px.box(df_comparison, x='時段', y=selected_param_comp, 
                                                 color='時段', color_discrete_map={'A': '#667eea', 'B': '#ff6b6b'},
                                                 title=f"【{selected_param_comp}】箱型圖對比", points='outliers')
                            fig_box_comp.update_layout(height=400, showlegend=False)
                            st.plotly_chart(fig_box_comp, use_container_width=True)
                        
                        # 異常點識別
                        st.markdown("---")
                        st.markdown("### 🔍 異常點識別")
                        
                        def identify_anomalies(data, param, z_threshold=3):
                            mean = data[param].mean()
                            std = data[param].std()
                            z_scores = np.abs((data[param] - mean) / std)
                            return data[z_scores > z_threshold]
                        
                        anomalies_a = identify_anomalies(df_a_clean, selected_param_comp)
                        anomalies_b = identify_anomalies(df_b_clean, selected_param_comp)
                        
                        ano_col1, ano_col2 = st.columns(2)
                        
                        with ano_col1:
                            if len(anomalies_a) > 0:
                                st.markdown(f"""<div class="anomaly-badge">
                                    <strong>時段A 異常點：{len(anomalies_a)} 顆</strong><br>
                                    占比: {(len(anomalies_a)/len(df_a_clean)*100):.1f}%
                                </div>""", unsafe_allow_html=True)
                                with st.expander("查看詳細"):
                                    st.dataframe(anomalies_a[['產出鋼捲號碼', '生產日期', selected_param_comp]].head(10), use_container_width=True)
                            else:
                                st.markdown(f"""<div class="normal-badge">
                                    <strong>時段A 正常 ✓</strong><br>
                                    未發現異常點
                                </div>""", unsafe_allow_html=True)
                        
                        with ano_col2:
                            if len(anomalies_b) > 0:
                                st.markdown(f"""<div class="anomaly-badge">
                                    <strong>時段B 異常點：{len(anomalies_b)} 顆</strong><br>
                                    占比: {(len(anomalies_b)/len(df_b_clean)*100):.1f}%
                                </div>""", unsafe_allow_html=True)
                                with st.expander("查看詳細"):
                                    st.dataframe(anomalies_b[['產出鋼捲號碼', '生產日期', selected_param_comp]].head(10), use_container_width=True)
                            else:
                                st.markdown(f"""<div class="normal-badge">
                                    <strong>時段B 正常 ✓</strong><br>
                                    未發現異常點
                                </div>""", unsafe_allow_html=True)
                    
                    else:
                        st.warning("⚠️ 所選時段的數據不足，無法進行對比分析")
                else:
                    st.info("💡 請完整選擇時段和參數進行對比分析")
            else:
                st.info("💡 請選擇時段A和時段B開始對比分析")

        # ============ 數據匯出 ============
        st.markdown("---")
        st.markdown("### 💾 數據匯出")
        
        csv_data = filtered_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 下載篩選數據 (CSV)", data=csv_data, file_name='鍍三線_品質分析資料.csv', mime='text/csv')

else:
    # 初始提示頁面
    st.info("👈 請從左側邊欄上傳產線的 RAW DATA，系統將自動進行分析")
    
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.markdown("""
        ### ✨ 主要功能
        - 📊 單一參數的詳細 SPC 分析
        - 🔄 多時段對比分析
        - 🔍 異常點自動識別
        - 📈 趨勢走勢可視化
        """)
    
    with col_info2:
        st.markdown("""
        ### 🎯 層峰視角
        - 快速掌握品質狀況
        - 不同時段的對比評估
        - 規格條件精確篩選
        - 異常點精準定位
        """)

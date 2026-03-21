import streamlit as st
import streamlit.components.v1 as components

# ── 主題 CSS（米白底色，SkyAgent 天藍色系）────────────────
THEME_CSS = """
<style>
/* ── 全域底色與文字 ─────────────────────────────── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="block-container"] {
    background-color: #f5f7fa !important;
    color: #1e293b !important;
}

/* ── 字體 ───────────────────────────────────────── */
html, body, [class*="css"], button, input, select, textarea {
    font-family: 'Microsoft JhengHei', 'Noto Sans TC', 'Inter', 'Segoe UI', sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
}

/* ── 側邊欄 ─────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}
[data-testid="stSidebar"] * { color: #1e293b !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #0ea5e9 !important;
    font-weight: 700 !important;
}

/* ── 主標題 ─────────────────────────────────────── */
h1 { color: #0f172a !important; font-weight: 800 !important; }
h2 { color: #1e293b !important; font-weight: 700 !important; }
h3 { color: #334155 !important; font-weight: 600 !important; }

/* ── 指標卡片 ─────────────────────────────────────*/
[data-testid="metric-container"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
}
[data-testid="metric-container"] label {
    color: #64748b !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #0f172a !important;
    font-size: 26px !important;
    font-weight: 700 !important;
}

/* ── 分頁 Tab ────────────────────────────────────── */
[data-testid="stTabs"] button {
    color: #64748b !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border-radius: 8px 8px 0 0 !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #0ea5e9 !important;
    border-bottom: 2px solid #0ea5e9 !important;
    background: #f0f9ff !important;
}

/* ── 下拉選單 ────────────────────────────────────── */
div[data-baseweb="select"] * {
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #1e293b !important;
    background-color: #ffffff !important;
}
div[data-baseweb="select"] > div {
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    background-color: #ffffff !important;
}
div[data-baseweb="popover"] {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.10) !important;
}
div[data-baseweb="popover"] li { color: #1e293b !important; }
div[data-baseweb="popover"] li:hover { background-color: #f0f9ff !important; }

/* ── 輸入框 ─────────────────────────────────────── */
input[type="number"], input[type="text"], textarea {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
}

/* ── 按鈕 ────────────────────────────────────────── */
[data-testid="stDownloadButton"] button,
[data-testid="stButton"] button {
    background-color: #0ea5e9 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
[data-testid="stDownloadButton"] button:hover,
[data-testid="stButton"] button:hover {
    background-color: #0284c7 !important;
}

/* ── 提示訊息框 ─────────────────────────────────── */
[data-testid="stAlert"] { border-radius: 10px !important; }

/* ── File uploader ──────────────────────────────── */
[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 2px dashed #cbd5e1 !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"] * { color: #475569 !important; }

/* ── Expander ───────────────────────────────────── */
[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary {
    color: #334155 !important;
    font-weight: 600 !important;
}

/* ── Dataframe ──────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ── 自訂元件 ────────────────────────────────────── */
.spec-banner {
    background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    padding: 18px 28px !important;
    margin-bottom: 20px !important;
    font-size: 15px !important;
    line-height: 2.2 !important;
    box-shadow: 0 4px 14px rgba(14,165,233,0.25) !important;
}
.spec-banner b { color: #fef9c3 !important; }

.section-title {
    font-size: 17px !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    border-left: 4px solid #0ea5e9 !important;
    padding-left: 12px !important;
    margin: 24px 0 12px 0 !important;
}

.signal-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.signal-table th {
    background-color: #0ea5e9;
    color: #ffffff;
    padding: 10px 14px;
    text-align: center;
    font-weight: 600;
}
.signal-table td {
    padding: 9px 14px;
    text-align: center;
    border-bottom: 1px solid #e2e8f0;
    color: #1e293b;
}
.signal-table tr:nth-child(even) { background-color: #f8fafc; }
.sig-green  { color: #16a34a; font-weight: 700; }
.sig-yellow { color: #d97706; font-weight: 700; }
.sig-red    { color: #dc2626; font-weight: 700; }
.sig-gray   { color: #94a3b8; }

/* ── 隱藏頁腳 ────────────────────────────────────── */
footer { visibility: hidden !important; }
</style>
"""

# ── Lottie 動畫 JSON（Growth Chart）─────────────────────
_LOTTIE_JSON = r"""{"v":"5.6.4","fr":60,"ip":0,"op":80,"w":1080,"h":1080,"nm":"Chart Up","ddd":0,"assets":[],"layers":[{"ddd":0,"ind":1,"ty":4,"nm":"Layer 4 Outlines","sr":1,"ks":{"o":{"a":0,"k":100,"ix":11},"r":{"a":1,"k":[{"i":{"x":[0.6],"y":[1]},"o":{"x":[0.2],"y":[0]},"t":30,"s":[30]},{"t":60,"s":[0]}],"ix":10},"p":{"a":1,"k":[{"i":{"x":0.833,"y":0.833},"o":{"x":0.167,"y":0.167},"t":30,"s":[231.122,474,0],"to":[9,3.699,0],"ti":[-9,-3.699,0]},{"t":58,"s":[285.122,496.194,0]}],"ix":2},"a":{"a":0,"k":[16,420,0],"ix":1},"s":{"a":1,"k":[{"i":{"x":[0.6,0.6,0.6],"y":[1,1,1]},"o":{"x":[0.2,0.2,0.2],"y":[0,0,0]},"t":30,"s":[0,0,100]},{"t":60,"s":[75,75,100]}],"ix":6}},"ao":0,"ef":[{"ty":5,"nm":"Change to Color","np":13,"mn":"ADBE Change To Color","ix":1,"en":1,"ef":[{"ty":2,"nm":"From","mn":"ADBE Change To Color-0001","ix":1,"v":{"a":0,"k":[0.301960796118,0.305882364511,0.313725501299,1],"ix":1}},{"ty":2,"nm":"To","mn":"ADBE Change To Color-0002","ix":2,"v":{"a":0,"k":[0,0.61960786581,0.968627512455,1],"ix":2}},{"ty":7,"nm":"Change","mn":"ADBE Change To Color-0003","ix":3,"v":{"a":0,"k":4,"ix":3}},{"ty":7,"nm":"Change By","mn":"ADBE Change To Color-0004","ix":4,"v":{"a":0,"k":2,"ix":4}},{"ty":6,"nm":"Tolerance","mn":"ADBE Change To Color-0010","ix":5,"v":0},{"ty":0,"nm":"Hue","mn":"ADBE Change To Color-0005","ix":6,"v":{"a":0,"k":0.1,"ix":6}},{"ty":0,"nm":"Lightness","mn":"ADBE Change To Color-0006","ix":7,"v":{"a":0,"k":1,"ix":7}},{"ty":0,"nm":"Saturation","mn":"ADBE Change To Color-0007","ix":8,"v":{"a":0,"k":1,"ix":8}},{"ty":6,"nm":"Saturation","mn":"ADBE Change To Color-0011","ix":9,"v":0},{"ty":0,"nm":"Softness","mn":"ADBE Change To Color-0008","ix":10,"v":{"a":0,"k":0.5,"ix":10}},{"ty":7,"nm":"View Correction Matte","mn":"ADBE Change To Color-0009","ix":11,"v":{"a":0,"k":0,"ix":11}}]}],"shapes":[{"ty":"gr","it":[{"ind":0,"ty":"sh","ix":1,"ks":{"a":0,"k":{"i":[[0,0],[0,0],[0,0],[-89.97,152.932],[0,0],[0,0]],"o":[[0,0],[-144.548,342.612],[362.206,78.864],[0,0],[0,0],[0,0]],"v":[[120.048,-174.759],[187.234,-141.965],[-330.094,170.842],[264.268,-91.832],[330.094,-52.335],[296.719,-249.707]],"c":true},"ix":2},"nm":"Path 1","mn":"ADBE Vector Shape - Group","hd":false},{"ty":"fl","c":{"a":0,"k":[0,0.619607843137,0.968627510819,1],"ix":4},"o":{"a":0,"k":100,"ix":5},"r":1,"bm":0,"nm":"Fill 1","mn":"ADBE Vector Graphic - Fill","hd":false},{"ty":"tr","p":{"a":0,"k":[330.343,249.956],"ix":2},"a":{"a":0,"k":[0,0],"ix":1},"s":{"a":0,"k":[100,100],"ix":3},"r":{"a":0,"k":0,"ix":6},"o":{"a":0,"k":100,"ix":7},"sk":{"a":0,"k":0,"ix":4},"sa":{"a":0,"k":0,"ix":5},"nm":"Transform"}],"nm":"Group 1","np":2,"cix":2,"bm":0,"ix":1,"mn":"ADBE Vector Group","hd":false}],"ip":0,"op":80,"st":0,"bm":0},{"ddd":0,"ind":2,"ty":4,"nm":"Shape Layer 3","td":1,"sr":1,"ks":{"o":{"a":0,"k":100,"ix":11},"r":{"a":0,"k":0,"ix":10},"p":{"a":0,"k":[540,504,0],"ix":2},"a":{"a":0,"k":[0,0,0],"ix":1},"s":{"a":0,"k":[100,100,100],"ix":6}},"ao":0,"shapes":[{"ty":"gr","it":[{"ty":"rc","d":1,"s":{"a":0,"k":[835.953,303.891],"ix":2},"p":{"a":0,"k":[0,0],"ix":3},"r":{"a":0,"k":0,"ix":4},"nm":"Rectangle Path 1","mn":"ADBE Vector Shape - Rect","hd":false},{"ty":"st","c":{"a":0,"k":[1,1,1,1],"ix":3},"o":{"a":0,"k":100,"ix":4},"w":{"a":0,"k":8,"ix":5},"lc":1,"lj":1,"ml":4,"bm":0,"nm":"Stroke 1","mn":"ADBE Vector Graphic - Stroke","hd":true},{"ty":"fl","c":{"a":0,"k":[1,0,0,1],"ix":4},"o":{"a":0,"k":100,"ix":5},"r":1,"bm":0,"nm":"Fill 1","mn":"ADBE Vector Graphic - Fill","hd":false},{"ty":"tr","p":{"a":0,"k":[61.977,491.945],"ix":2},"a":{"a":0,"k":[0,0],"ix":1},"s":{"a":0,"k":[100,100],"ix":3},"r":{"a":0,"k":0,"ix":6},"o":{"a":0,"k":100,"ix":7},"sk":{"a":0,"k":0,"ix":4},"sa":{"a":0,"k":0,"ix":5},"nm":"Transform"}],"nm":"Rectangle 1","np":3,"cix":2,"bm":0,"ix":1,"mn":"ADBE Vector Group","hd":false}],"ip":0,"op":80,"st":0,"bm":0},{"ddd":0,"ind":3,"ty":4,"nm":"Shape Layer 2","tt":2,"sr":1,"ks":{"o":{"a":0,"k":100,"ix":11},"r":{"a":0,"k":0,"ix":10},"p":{"a":0,"k":[540,535,0],"ix":2},"a":{"a":0,"k":[0,0,0],"ix":1},"s":{"a":0,"k":[100,100,100],"ix":6}},"ao":0,"shapes":[{"ty":"gr","it":[{"ty":"rc","d":1,"s":{"a":0,"k":[168.039,373.422],"ix":2},"p":{"a":0,"k":[0,0],"ix":3},"r":{"a":0,"k":0,"ix":4},"nm":"Rectangle Path 1","mn":"ADBE Vector Shape - Rect","hd":false},{"ty":"st","c":{"a":0,"k":[1,1,1,1],"ix":3},"o":{"a":0,"k":100,"ix":4},"w":{"a":0,"k":8,"ix":5},"lc":1,"lj":1,"ml":4,"bm":0,"nm":"Stroke 1","mn":"ADBE Vector Graphic - Stroke","hd":true},{"ty":"fl","c":{"a":0,"k":[1,0.713725490196,0.301960784314,1],"ix":4},"o":{"a":0,"k":100,"ix":5},"r":1,"bm":0,"nm":"Fill 1","mn":"ADBE Vector Graphic - Fill","hd":false},{"ty":"tr","p":{"a":1,"k":[{"i":{"x":0.6,"y":1},"o":{"x":0.2,"y":0},"t":10,"s":[-189.98,500],"to":[0,-30.382],"ti":[0,30.382]},{"t":22.5,"s":[-189.98,317.711]}],"ix":2},"a":{"a":0,"k":[0,0],"ix":1},"s":{"a":0,"k":[100,100],"ix":3},"r":{"a":0,"k":0,"ix":6},"o":{"a":0,"k":100,"ix":7},"sk":{"a":0,"k":0,"ix":4},"sa":{"a":0,"k":0,"ix":5},"nm":"Transform"}],"nm":"Rectangle 3","np":3,"cix":2,"bm":0,"ix":1,"mn":"ADBE Vector Group","hd":false},{"ty":"gr","it":[{"ty":"rc","d":1,"s":{"a":0,"k":[168.039,373.422],"ix":2},"p":{"a":0,"k":[0,0],"ix":3},"r":{"a":0,"k":0,"ix":4},"nm":"Rectangle Path 1","mn":"ADBE Vector Shape - Rect","hd":false},{"ty":"st","c":{"a":0,"k":[1,1,1,1],"ix":3},"o":{"a":0,"k":100,"ix":4},"w":{"a":0,"k":8,"ix":5},"lc":1,"lj":1,"ml":4,"bm":0,"nm":"Stroke 1","mn":"ADBE Vector Graphic - Stroke","hd":true},{"ty":"fl","c":{"a":0,"k":[0.972549079446,0.537254901961,0.317647058824,1],"ix":4},"o":{"a":0,"k":100,"ix":5},"r":1,"bm":0,"nm":"Fill 1","mn":"ADBE Vector Graphic - Fill","hd":false},{"ty":"tr","p":{"a":1,"k":[{"i":{"x":0.6,"y":1},"o":{"x":0.2,"y":0},"t":16.25,"s":[1.02,500],"to":[0,-45.048],"ti":[0,45.048]},{"t":28.75,"s":[1.02,229.711]}],"ix":2},"a":{"a":0,"k":[0,0],"ix":1},"s":{"a":0,"k":[100,100],"ix":3},"r":{"a":0,"k":0,"ix":6},"o":{"a":0,"k":100,"ix":7},"sk":{"a":0,"k":0,"ix":4},"sa":{"a":0,"k":0,"ix":5},"nm":"Transform"}],"nm":"Rectangle 2","np":3,"cix":2,"bm":0,"ix":2,"mn":"ADBE Vector Group","hd":false},{"ty":"gr","it":[{"ty":"rc","d":1,"s":{"a":0,"k":[168.039,373.422],"ix":2},"p":{"a":0,"k":[0,0],"ix":3},"r":{"a":0,"k":0,"ix":4},"nm":"Rectangle Path 1","mn":"ADBE Vector Shape - Rect","hd":false},{"ty":"st","c":{"a":0,"k":[1,1,1,1],"ix":3},"o":{"a":0,"k":100,"ix":4},"w":{"a":0,"k":8,"ix":5},"lc":1,"lj":1,"ml":4,"bm":0,"nm":"Stroke 1","mn":"ADBE Vector Graphic - Stroke","hd":true},{"ty":"fl","c":{"a":0,"k":[0.898039275525,0.258823529412,0.505882352941,1],"ix":4},"o":{"a":0,"k":100,"ix":5},"r":1,"bm":0,"nm":"Fill 1","mn":"ADBE Vector Graphic - Fill","hd":false},{"ty":"tr","p":{"a":1,"k":[{"i":{"x":0.6,"y":1},"o":{"x":0.2,"y":0},"t":22.5,"s":[192.02,500],"to":[0,-62.715],"ti":[0,62.715]},{"t":35,"s":[192.02,123.711]}],"ix":2},"a":{"a":0,"k":[0,0],"ix":1},"s":{"a":0,"k":[100,100],"ix":3},"r":{"a":0,"k":0,"ix":6},"o":{"a":0,"k":100,"ix":7},"sk":{"a":0,"k":0,"ix":4},"sa":{"a":0,"k":0,"ix":5},"nm":"Transform"}],"nm":"Rectangle 1","np":3,"cix":2,"bm":0,"ix":3,"mn":"ADBE Vector Group","hd":false}],"ip":0,"op":80,"st":0,"bm":0},{"ddd":0,"ind":4,"ty":4,"nm":"Shape Layer 1","sr":1,"ks":{"o":{"a":0,"k":100,"ix":11},"r":{"a":0,"k":0,"ix":10},"p":{"a":0,"k":[237,879.955,0],"ix":2},"a":{"a":0,"k":[-303,345.955,0],"ix":1},"s":{"a":1,"k":[{"i":{"x":[0.239,0.6,0.6],"y":[1.008,1,1]},"o":{"x":[0.724,0.2,0.2],"y":[-0.001,0,0]},"t":0,"s":[0,100,100]},{"t":20,"s":[100,100,100]}],"ix":6}},"ao":0,"shapes":[{"ty":"gr","it":[{"ty":"rc","d":1,"s":{"a":0,"k":[614.609,29.91],"ix":2},"p":{"a":0,"k":[0,0],"ix":3},"r":{"a":0,"k":0,"ix":4},"nm":"Rectangle Path 1","mn":"ADBE Vector Shape - Rect","hd":false},{"ty":"st","c":{"a":0,"k":[1,1,1,1],"ix":3},"o":{"a":0,"k":100,"ix":4},"w":{"a":0,"k":8,"ix":5},"lc":1,"lj":1,"ml":4,"bm":0,"nm":"Stroke 1","mn":"ADBE Vector Graphic - Stroke","hd":true},{"ty":"fl","c":{"a":0,"k":[0,0.831372608858,0.741176470588,1],"ix":4},"o":{"a":0,"k":100,"ix":5},"r":1,"bm":0,"nm":"Fill 1","mn":"ADBE Vector Graphic - Fill","hd":false},{"ty":"tr","p":{"a":0,"k":[4.305,345.955],"ix":2},"a":{"a":0,"k":[0,0],"ix":1},"s":{"a":0,"k":[100,100],"ix":3},"r":{"a":0,"k":0,"ix":6},"o":{"a":0,"k":100,"ix":7},"sk":{"a":0,"k":0,"ix":4},"sa":{"a":0,"k":0,"ix":5},"nm":"Transform"}],"nm":"Rectangle 1","np":3,"cix":2,"bm":0,"ix":1,"mn":"ADBE Vector Group","hd":false}],"ip":0,"op":80,"st":0,"bm":0}],"markers":[]}"""


# ── 封面頁（Landing Page）────────────────────────────────
def render_landing():
    """上傳檔案前顯示的歡迎封面，含 Lottie 動畫"""

    # 上半部：左文字 右動畫
    left_col, right_col = st.columns([1.2, 1])

    with left_col:
        st.markdown("""
        <div style="padding: 48px 0 24px 0;">
            <div style="
                display: inline-block;
                background: linear-gradient(135deg, #0ea5e9, #0284c7);
                border-radius: 14px;
                padding: 12px 18px;
                margin-bottom: 24px;
                box-shadow: 0 6px 18px rgba(14,165,233,0.28);
            ">
                <span style="font-size: 32px; letter-spacing: 2px; color: #fff; font-weight: 800;">
                    ⬡ AegisCore
                </span>
            </div>
            <h1 style="
                font-size: 40px;
                font-weight: 800;
                color: #0f172a;
                margin: 0 0 14px 0;
                line-height: 1.2;
                letter-spacing: -1px;
            ">智能鋼捲<br>品質監控平台</h1>
            <p style="
                font-size: 16px;
                color: #64748b;
                line-height: 1.9;
                margin: 0 0 36px 0;
                max-width: 420px;
            ">
                上傳產線 RAW DATA，即時呈現品質趨勢、<br>
                跨月比對與製程能力（Cpk）分析報告
            </p>
            <div style="
                display: inline-block;
                background: #0ea5e9;
                color: white;
                border-radius: 10px;
                padding: 12px 28px;
                font-size: 15px;
                font-weight: 700;
                box-shadow: 0 4px 12px rgba(14,165,233,0.35);
            ">👈 從左側上傳 RAW DATA 開始分析</div>
        </div>
        """, unsafe_allow_html=True)

    with right_col:
        # Lottie 動畫（透過 lottie-web CDN，無需安裝套件）
        lottie_html = f"""
        <div style="display:flex; justify-content:center; align-items:center; padding: 20px 0;">
            <div id="lottie-container" style="width:300px; height:300px;"></div>
        </div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js"></script>
        <script>
            var animData = {_LOTTIE_JSON};
            lottie.loadAnimation({{
                container: document.getElementById('lottie-container'),
                renderer: 'svg',
                loop: true,
                autoplay: true,
                animationData: animData
            }});
        </script>
        """
        components.html(lottie_html, height=340)

    st.markdown("<hr style='border-color:#e2e8f0; margin: 8px 0 28px 0;'>", unsafe_allow_html=True)

    # 下半部：三個功能卡片
    c1, c2, c3 = st.columns(3)
    cards = [
        ("📊", "趨勢監控", "即時追蹤各參數生產走勢，±3σ 管制線一眼辨識異常點"),
        ("🚦", "跨月比對", "鎖定規格條件，對比不同月份品質表現與異常燈號"),
        ("📐", "製程能力", "自動計算 Cp、Ca、Cpk，評估製程穩定性與改善方向"),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3], cards):
        col.markdown(f"""
        <div style="
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 32px 24px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        ">
            <div style="font-size: 34px; margin-bottom: 14px;">{icon}</div>
            <div style="font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 10px;">{title}</div>
            <div style="font-size: 13px; color: #64748b; line-height: 1.7;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)


# ── Plotly 圖表主題（CHART_THEME）────────────────────────
CHART_THEME = {
    'plot_bgcolor': '#ffffff',
    'paper_bgcolor': '#ffffff',
    'font': {'family': 'Microsoft JhengHei, Noto Sans TC, sans-serif', 'color': '#1e293b'},
    'colorway': ['#0ea5e9', '#f59e0b', '#10b981', '#ef4444', '#8b5cf6', '#f97316'],
    'xaxis': {'gridcolor': '#e2e8f0', 'linecolor': '#cbd5e1', 'zerolinecolor': '#e2e8f0'},
    'yaxis': {'gridcolor': '#e2e8f0', 'linecolor': '#cbd5e1', 'zerolinecolor': '#e2e8f0'},
}

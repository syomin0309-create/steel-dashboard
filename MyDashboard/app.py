#!/usr/bin/env python3
"""
AegisCore app.py auto-patcher
用法：python apply_patches.py          （預設修改 ./app.py）
      python apply_patches.py path/to/app.py
"""
import sys, re, shutil

path = sys.argv[1] if len(sys.argv) > 1 else "app.py"
shutil.copy2(path, path + ".bak")
print(f"✅ 備份 → {path}.bak")

src = open(path, "r", encoding="utf-8").read()
count = 0

# ── Patch 1: 月份按鈕改 on_click callback ──────────────
old1 = """\
    if months_list:
        btn_cols = st.columns(len(months_list) + 1)
        for i, m in enumerate(months_list):
            is_active = st.session_state[hl_key] == m
            if btn_cols[i].button(m, key=f"hl_btn_{file_key}_{selected_param}_{m}",
                                   type="primary" if is_active else "secondary"):
                st.session_state[hl_key] = m
                st.rerun()
        is_all = st.session_state[hl_key] == "全部"
        if btn_cols[-1].button("全部", key=f"hl_btn_all_{file_key}_{selected_param}",
                                type="primary" if is_all else "secondary"):
            st.session_state[hl_key] = "全部"
            st.rerun()"""

new1 = """\
    def _set_hl(month, key):
        st.session_state[key] = month

    if months_list:
        btn_cols = st.columns(len(months_list) + 1)
        for i, m in enumerate(months_list):
            is_active = st.session_state[hl_key] == m
            btn_cols[i].button(m, key=f"hl_btn_{file_key}_{selected_param}_{m}",
                               type="primary" if is_active else "secondary",
                               on_click=_set_hl, args=(m, hl_key))
        is_all = st.session_state[hl_key] == "全部"
        btn_cols[-1].button("全部", key=f"hl_btn_all_{file_key}_{selected_param}",
                            type="primary" if is_all else "secondary",
                            on_click=_set_hl, args=("全部", hl_key))"""

if old1 in src:
    src = src.replace(old1, new1, 1)
    count += 1
    print("✅ Patch 1: 月份按鈕 on_click callback")
else:
    print("⚠️  Patch 1: 找不到目標，跳過")

# ── Patch 2: SPC 趨勢圖 uirevision ─────────────────────
old2 = 'height=500, hovermode="closest",'
new2 = 'height=500, hovermode="closest",\n        uirevision=selected_param,'

if old2 in src:
    src = src.replace(old2, new2, 1)
    count += 1
    print("✅ Patch 2: SPC 趨勢圖 uirevision")
else:
    print("⚠️  Patch 2: 找不到目標，跳過")

# ── Patch 3: 箱型圖 uirevision ─────────────────────────
old3 = """\
        height=500, showlegend=False,
        font=dict(color=CHART_TEXT, size=14),
        title=dict(font=dict(color=CHART_TEXT, size=17)),
        xaxis=dict(title=dict(text="群組分類", font=dict(color="#64748b", size=14)),
                   gridcolor=CHART_GRID, tickfont=dict(color=CHART_TEXT, size=14),
                   linecolor=CHART_AXIS),"""

new3 = """\
        height=500, showlegend=False,
        uirevision=selected_param,
        font=dict(color=CHART_TEXT, size=14),
        title=dict(font=dict(color=CHART_TEXT, size=17)),
        xaxis=dict(title=dict(text="群組分類", font=dict(color="#64748b", size=14)),
                   gridcolor=CHART_GRID, tickfont=dict(color=CHART_TEXT, size=14),
                   linecolor=CHART_AXIS),"""

if old3 in src:
    src = src.replace(old3, new3, 1)
    count += 1
    print("✅ Patch 3: 箱型圖 uirevision")
else:
    print("⚠️  Patch 3: 找不到目標，跳過")

# ── Patch 4: 直方圖 uirevision ─────────────────────────
old4 = """\
            showlegend=False,
            bargap=0.04, margin=dict(t=70, b=55, l=65, r=30)"""

new4 = """\
            showlegend=False,
            uirevision=f"{selected_param}_{lsl2}_{usl2}_{spc_bins}",
            bargap=0.04, margin=dict(t=70, b=55, l=65, r=30)"""

if old4 in src:
    src = src.replace(old4, new4, 1)
    count += 1
    print("✅ Patch 4: 直方圖 uirevision")
else:
    print("⚠️  Patch 4: 找不到目標，跳過")

open(path, "w", encoding="utf-8").write(src)
print(f"\n🎯 完成！套用 {count}/4 個 patch → {path}")

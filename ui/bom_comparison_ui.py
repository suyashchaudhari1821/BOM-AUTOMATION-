"""
bom_comparison_ui.py — Expleo Tooling BOM Comparison System UI.

Theme & Aesthetics:
  - Official Expleo theme (https://expleo.com/global/en/#contact)
  - Colors: Expleo Violet (#6846C6), Radiant Violet (#805CE5), Electric Cyan (#6EC1E4), Deep Obsidian (#090710)
  - Glassmorphic panels, responsive upload dropzones, animated CTAs
  - No emojis — clean corporate engineering icons and typography
  - Active Back to Login navigation, user@expleogroup.com account, and report export
"""

from __future__ import annotations

import base64
import io
from pathlib import Path
import traceback

import pandas as pd
import streamlit as st

from tooling_bom.column_config import CORE_TRACKED_COLUMNS
from tooling_bom.comparator import compare, rows_to_dataframe
from tooling_bom.exporter import export_to_excel
from tooling_bom.loader import load_bom

_STATE_VERSION = "v8_expleo"
EXPLEO_LOGO_PATH = Path(__file__).parent / "expleo_logo.png"
EXPLEO_ICON_PATH = Path(__file__).parent / "expleo_icon.png"


def _get_icon_data_uri() -> str:
    """Return Expleo circular icon as a base64 data URI if available."""
    if EXPLEO_ICON_PATH.exists():
        try:
            with open(EXPLEO_ICON_PATH, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
                return f"data:image/png;base64,{b64}"
        except Exception:
            pass
    return ""


def _get_logo_data_uri() -> str:
    """Return Expleo logo as a base64 data URI if available."""
    if EXPLEO_LOGO_PATH.exists():
        try:
            with open(EXPLEO_LOGO_PATH, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
                return f"data:image/png;base64,{b64}"
        except Exception:
            pass
    return "https://expleo.com/global/en/wp-content/uploads/2019/02/expleo-logo-and-tagline.png"


# ─────────────────────────────────────────────────────────────────────────────
def render(user_name: str = "user@expleogroup.com", user_login: str = "user@expleogroup.com") -> None:
    """Entry point called from app.py."""
    if st.session_state.get("_state_version") != _STATE_VERSION:
        for key in ["comparison_results", "comparison_error", "comparison_traceback"]:
            st.session_state.pop(key, None)
        st.session_state["_state_version"] = _STATE_VERSION

    _inject_css()
    _render_topbar(user_name)
    _render_upload_bar()
    _render_main()
    _render_footer()


# ── Top Bar ───────────────────────────────────────────────────────────────────
def _render_topbar(user_name: str) -> None:
    logo_uri = _get_logo_data_uri()

    col_brand, col_actions = st.columns([6, 6])
    with col_brand:
        st.markdown(
            f"""
            <div class="expleo-nav-brand">
                <img src="{logo_uri}" class="nav-logo" alt="Expleo" />
                <div class="nav-divider"></div>
                <div>
                    <div class="nav-title">BOM Intelligence Platform</div>
                    <div class="nav-sub">Expleo Engineering &middot; Automated Change Detection</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_actions:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        c_back, c_user = st.columns([4, 8])
        
        with c_back:
            if st.button("&larr; Back to Login", key="back_btn", use_container_width=True):
                st.session_state["authenticated"] = False
                st.session_state.pop("user_name", None)
                st.session_state.pop("user_login", None)
                st.session_state.pop("comparison_results", None)
                st.rerun()

        with c_user:
            display_user = "user@expleogroup.com" if "suyash" in user_name.lower() else user_name
            st.markdown(
                f'<div class="user-pill"><span class="user-dot"></span><span class="user-text">{display_user}</span></div>',
                unsafe_allow_html=True,
            )


# ── Upload / Action Bar ───────────────────────────────────────────────────────
def _render_upload_bar() -> None:
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([5, 5, 2.5], gap="medium")

    with c1:
        st.markdown('<div class="file-card-label">Old / Reference BOM (.xlsx, .xlsm)</div>', unsafe_allow_html=True)
        old_file = st.file_uploader(
            "Upload Old BOM",
            type=["xlsx", "xlsm"],
            key="old_bom_upload",
            label_visibility="collapsed",
            help="Previous / baseline BOM file",
        )
    with c2:
        st.markdown('<div class="file-card-label">New / Updated BOM (.xlsx, .xlsm)</div>', unsafe_allow_html=True)
        new_file = st.file_uploader(
            "Upload New BOM",
            type=["xlsx", "xlsm"],
            key="new_bom_upload",
            label_visibility="collapsed",
            help="Revised BOM file to compare against",
        )
    with c3:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        both_uploaded = old_file is not None and new_file is not None
        run_clicked = st.button(
            "Run Comparison",
            type="primary",
            use_container_width=True,
            disabled=not both_uploaded,
            key="run_btn",
        )
        if not both_uploaded:
            st.caption("Upload both BOM files to enable")
        else:
            if st.button("Clear Files", use_container_width=True, key="clear_files_btn"):
                for key in ["comparison_results", "comparison_error", "comparison_traceback",
                            "old_bom_upload", "new_bom_upload"]:
                    st.session_state.pop(key, None)
                st.rerun()

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    if run_clicked and both_uploaded:
        _run_comparison(old_file, new_file)


# ── Main Area ─────────────────────────────────────────────────────────────────
def _render_main() -> None:
    results = st.session_state.get("comparison_results")
    error   = st.session_state.get("comparison_error")

    if error:
        tb = st.session_state.get("comparison_traceback", "")
        st.error(f"**Comparison failed:** {error}")
        with st.expander("Show error details"):
            st.code(tb)
        return

    if results is None:
        st.markdown(
            """
            <div class="empty-state-card">
                <div class="empty-state-icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#805CE5" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="15" y2="17"/></svg>
                </div>
                <div class="empty-state-title">Ready for Comparison</div>
                <div class="empty-state-desc">
                    Upload your baseline and updated BOM files above, then click <b>Run Comparison</b>.<br>
                    The automated engine evaluates all part records, detects additions and deletions, and highlights field-level modifications.
                </div>
                <div class="empty-state-badges">
                    <span class="badge-pill">Automated Change Detection</span>
                    <span class="badge-pill">Multi-Attribute Comparison</span>
                    <span class="badge-pill">Bilingual Excel Report</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        _render_results(results)


# ── Results Presentation ──────────────────────────────────────────────────────
def _render_results(results: dict) -> None:
    summary      = results["summary"]
    std_rows     = results["standard"]
    nonstd_rows  = results["non_standard"]
    old_filename = results.get("old_filename", "Old BOM")
    new_filename = results.get("new_filename", "New BOM")
    export_bytes = results.get("export_bytes")

    # Breadcrumb Banner
    st.markdown(
        f"""
        <div class="diff-banner">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="banner-pill banner-old">OLD BOM</span>
                <span class="banner-file">{old_filename}</span>
            </div>
            <div class="banner-arrow">&rarr;</div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="banner-pill banner-new">NEW BOM</span>
                <span class="banner-file">{new_filename}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Download Bar
    dl_col, _, reset_col = st.columns([4, 5, 2.5])
    with dl_col:
        if export_bytes:
            st.download_button(
                label="Download Executive Excel Report",
                data=export_bytes,
                file_name="Expleo_BOM_Comparison_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary",
                use_container_width=True,
            )
    with reset_col:
        if st.button("Start New Comparison", use_container_width=True, key="reset_btn"):
            for key in ["comparison_results", "comparison_error", "comparison_traceback"]:
                st.session_state.pop(key, None)
            st.rerun()

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Expleo-Themed KPI Section (Inspired by Expleo Counter Style)
    col_std, col_nonstd = st.columns(2, gap="large")

    with col_std:
        _render_kpi_block(
            "Standard Parts",
            "Standard category components (Fasteners, pins, springs, guides)",
            summary["std_new"],
            summary["std_deleted"],
            summary["std_modified"],
            summary["std_changed_fields"],
            accent="#10B981",
        )

    with col_nonstd:
        _render_kpi_block(
            "Non-Standard Parts",
            "Non-standard category components (Die shoes, custom machined plates)",
            summary["nonstd_new"],
            summary["nonstd_deleted"],
            summary["nonstd_modified"],
            summary["nonstd_changed_fields"],
            accent="#805CE5",
        )

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # Tabbed Tables
    tab_std, tab_nonstd = st.tabs(
        [
            f"Standard Parts ({summary['std_new'] + summary['std_deleted'] + summary['std_changed_fields']} changes)",
            f"Non-Standard Parts ({summary['nonstd_new'] + summary['nonstd_deleted'] + summary['nonstd_changed_fields']} changes)",
        ]
    )

    with tab_std:
        _render_table(std_rows, "Standard")
    with tab_nonstd:
        _render_table(nonstd_rows, "Non-Standard")


def _render_kpi_block(
    title: str, subtitle: str,
    new: int, deleted: int, modified: int, fields: int,
    accent: str = "#805CE5",
) -> None:
    st.markdown(
        f"""
        <div class="kpi-panel" style="border-top: 4px solid {accent};">
            <div class="kpi-panel-title">{title}</div>
            <div class="kpi-panel-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4 = st.columns(4)
    kpis = [
        (c1, new,      "New Items",      "#10B981", "rgba(16, 185, 129, 0.12)"),
        (c2, deleted,  "Deleted Items",  "#EF4444", "rgba(239, 68, 68, 0.12)"),
        (c3, modified, "Modified Items", "#F59E0B", "rgba(245, 158, 11, 0.12)"),
        (c4, fields,   "Changed Fields", "#6EC1E4", "rgba(110, 193, 228, 0.12)"),
    ]
    for col, val, label, color, bg in kpis:
        with col:
            st.markdown(
                f"""
                <div class="kpi-metric-box" style="background: {bg}; border: 1px solid {color}40;">
                    <div class="kpi-number" style="color: {color};">{val}</div>
                    <div class="kpi-tag">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_table(rows: list[dict], partition: str) -> None:
    if not rows:
        st.markdown(
            f"""
            <div style="padding: 24px; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 14px; text-align: center; color: #6EE7B7; font-weight: 600;">
                No differences detected in {partition} Parts.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    df_internal = rows_to_dataframe(rows)

    # Filter Controls
    f1, f2, _ = st.columns([3, 4, 3])
    with f1:
        change_types = ["All"] + sorted(df_internal["change_type_en"].unique().tolist())
        selected_type = st.selectbox(
            "Filter Change Type",
            options=change_types,
            key=f"filter_type_{partition}",
        )
    with f2:
        search_item = st.text_input(
            "Search Item No.",
            placeholder="e.g. 4001 or 3044",
            key=f"search_item_{partition}",
        )

    filtered = df_internal.copy()
    if selected_type != "All":
        filtered = filtered[filtered["change_type_en"] == selected_type]
    if search_item.strip():
        filtered = filtered[filtered["item_no"].str.contains(search_item.strip(), case=False, na=False)]

    st.markdown(f"<div style='color: #94A3B8; font-size: 0.82rem; margin: 6px 0 12px 0;'>Showing <b>{len(filtered)}</b> of <b>{len(df_internal)}</b> changes</div>", unsafe_allow_html=True)

    if filtered.empty:
        st.info("No records match the selected filter.")
        return

    # Visual Highlight Styler
    def _highlight(row: pd.Series):
        ct = row.get("change_type_en", "")
        if ct == "New Item":
            return ["background-color: rgba(16, 185, 129, 0.18); color: #6EE7B7; font-weight: 600;"] * len(row)
        if ct == "Deleted Item":
            return ["background-color: rgba(239, 68, 68, 0.18); color: #FCA5A5; font-weight: 600;"] * len(row)

        styles = []
        for col_name in row.index:
            if col_name in ("change_type_en", "change_type_fr"):
                styles.append("background-color: rgba(245, 158, 11, 0.18); color: #FCD34D; font-weight: 600;")
            elif col_name in ("column_en", "column_fr"):
                styles.append("background-color: rgba(249, 115, 22, 0.15); color: #FDBA74; font-weight: 500;")
            elif col_name == "old_value":
                styles.append("background-color: rgba(239, 68, 68, 0.18); color: #FCA5A5; font-weight: 500;")
            elif col_name == "new_value":
                styles.append("background-color: rgba(16, 185, 129, 0.18); color: #6EE7B7; font-weight: 600;")
            elif col_name == "part_category":
                styles.append("color: #E2E8F0; font-weight: 600;")
            else:
                styles.append("color: #F1F5F9;")
        return styles

    styled = filtered.style.apply(_highlight, axis=1)

    col_labels = {
        "item_no":        "Item No.",
        "part_category":  "Part Category",
        "change_type_en": "Change Type",
        "change_type_fr": "Change Type (FR)",
        "column_en":      "Changed Column",
        "column_fr":      "Nom de Colonne (FR)",
        "old_value":      "Old Value",
        "new_value":      "New Value",
    }

    st.dataframe(
        styled,
        use_container_width=True,
        hide_index=True,
        column_config={k: st.column_config.TextColumn(v) for k, v in col_labels.items()},
    )


# ── Comparison Runner ─────────────────────────────────────────────────────────
def _run_comparison(old_file, new_file) -> None:
    try:
        with st.spinner("Parsing Old BOM..."):
            old_bytes = io.BytesIO(old_file.read())
            old_result = load_bom(old_bytes)

        with st.spinner("Parsing New BOM..."):
            new_bytes = io.BytesIO(new_file.read())
            new_result = load_bom(new_bytes)

        columns_to_compare = CORE_TRACKED_COLUMNS

        with st.spinner("Running Comparison Engine..."):
            results = compare(old_result["df"], new_result["df"], columns_to_compare)

        with st.spinner("Building Executive Excel Report..."):
            export_bytes = export_to_excel(
                std_rows     = results["standard"],
                nonstd_rows  = results["non_standard"],
                summary      = results["summary"],
                old_filename = old_file.name,
                new_filename = new_file.name,
            )

        results["old_filename"] = old_file.name
        results["new_filename"] = new_file.name
        results["export_bytes"] = export_bytes

        st.session_state["comparison_results"] = results
        st.session_state.pop("comparison_error", None)
        st.session_state.pop("comparison_traceback", None)
        st.rerun()

    except Exception as e:
        st.session_state["comparison_error"]     = str(e)
        st.session_state["comparison_traceback"] = traceback.format_exc()
        st.session_state.pop("comparison_results", None)
        st.rerun()


# ── Footer ────────────────────────────────────────────────────────────────────
def _render_footer() -> None:
    st.markdown(
        """
        <div class="expleo-footer">
            <div style="text-align: center;">
                <b>Expleo Group</b> &copy; 2026 &middot; Engineering, Quality &amp; Digital Transformation
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── CSS Theme Injection ───────────────────────────────────────────────────────
def _inject_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

        /* App Background */
        .stApp {
            background: #090710 !important;
            background-image: 
                radial-gradient(circle at 10% 15%, rgba(104, 70, 198, 0.22) 0%, transparent 40%),
                radial-gradient(circle at 90% 85%, rgba(110, 193, 228, 0.12) 0%, transparent 45%),
                linear-gradient(135deg, rgba(13, 9, 24, 0.88) 0%, rgba(7, 5, 14, 0.94) 100%),
                url('https://expleo.com/global/en/wp-content/uploads/2026/10/power-of-ai_bfsi_homepage-slider_desktop.jpg') !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
            font-family: 'Montserrat', 'Inter', -apple-system, sans-serif !important;
            color: #F8FAFC !important;
        }

        [data-testid="stHeader"], #MainMenu, footer, section[data-testid="stSidebar"] {
            display: none !important;
        }

        .main .block-container {
            max-width: 1440px !important;
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            margin: auto !important;
        }

        /* Top Navigation Bar */
        .expleo-nav-brand {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 10px 0;
        }

        .nav-icon {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            object-fit: contain;
            filter: drop-shadow(0 2px 10px rgba(104, 70, 198, 0.6));
            flex-shrink: 0;
            transition: transform 0.25s ease;
        }

        .nav-icon:hover {
            transform: scale(1.08);
        }

        .nav-logo {
            height: 36px;
            object-fit: contain;
            filter: drop-shadow(0 2px 8px rgba(104, 70, 198, 0.45));
        }

        .nav-divider {
            width: 1px;
            height: 32px;
            background: rgba(104, 70, 198, 0.4);
        }

        .nav-title {
            font-size: 1.25rem;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.01em;
            line-height: 1.2;
        }

        .nav-sub {
            font-size: 0.76rem;
            color: #6EC1E4;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .nav-contact-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 8px 16px;
            background: rgba(104, 70, 198, 0.2);
            border: 1px solid rgba(104, 70, 198, 0.45);
            border-radius: 9999px;
            color: #6EC1E4;
            text-decoration: none;
            font-size: 0.8rem;
            font-weight: 600;
            transition: all 0.25s ease;
            height: 38px;
            box-sizing: border-box;
            width: 100%;
        }

        .nav-contact-btn:hover {
            background: rgba(104, 70, 198, 0.4);
            color: #FFFFFF;
            border-color: #805CE5;
        }

        .user-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 9999px;
            padding: 8px 14px;
            height: 38px;
            box-sizing: border-box;
            width: 100%;
            overflow: hidden;
        }

        .user-dot {
            width: 8px;
            height: 8px;
            background: #10B981;
            border-radius: 50%;
            box-shadow: 0 0 8px #10B981;
            flex-shrink: 0;
        }

        .user-text {
            font-size: 0.78rem;
            font-weight: 600;
            color: #E2E8F0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* Upload Container */
        .upload-container {
            background: rgba(26, 20, 48, 0.65);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(104, 70, 198, 0.35);
            border-radius: 20px;
            padding: 22px 26px 14px 26px;
            margin: 18px 0 22px 0;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.35);
        }

        .file-card-label {
            font-size: 0.82rem;
            font-weight: 700;
            color: #E2E8F0;
            letter-spacing: 0.04em;
            margin-bottom: 8px;
        }

        /* Custom File Uploader styling */
        [data-testid="stFileUploader"] {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }

        [data-testid="stFileUploader"] section,
        [data-testid="stFileUploadDropzone"],
        div[data-testid="stFileUploader"] > section,
        div[data-testid="stFileUploaderDropzone"],
        section[data-testid="stFileUploadDropzone"] {
            background: rgba(22, 17, 38, 0.82) !important;
            border: 1px dashed rgba(104, 70, 198, 0.55) !important;
            border-radius: 16px !important;
            padding: 16px 20px !important;
            color: #F8FAFC !important;
            transition: all 0.25s ease !important;
        }

        [data-testid="stFileUploadDropzone"]:hover,
        [data-testid="stFileUploader"] section:hover {
            border-color: #805CE5 !important;
            background: rgba(28, 20, 52, 0.95) !important;
            box-shadow: 0 0 24px rgba(104, 70, 198, 0.3) !important;
        }

        [data-testid="stFileUploadDropzone"] *,
        [data-testid="stFileUploader"] section * {
            color: #E2E8F0 !important;
        }

        [data-testid="stFileUploadDropzone"] small,
        [data-testid="stFileUploader"] section small {
            color: #94A3B8 !important;
        }

        [data-testid="stFileUploadDropzone"] button,
        [data-testid="stFileUploader"] section button {
            background: rgba(104, 70, 198, 0.3) !important;
            border: 1px solid rgba(104, 70, 198, 0.55) !important;
            color: #FFFFFF !important;
            border-radius: 9999px !important;
            padding: 6px 18px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }

        [data-testid="stFileUploadDropzone"] button:hover,
        [data-testid="stFileUploader"] section button:hover {
            background: rgba(104, 70, 198, 0.6) !important;
            border-color: #805CE5 !important;
            color: #FFFFFF !important;
        }

        /* Primary Button */
        div[data-testid="stButton"] button[kind="primary"] {
            background: linear-gradient(135deg, #6846C6 0%, #805CE5 100%) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            border-radius: 9999px !important;
            border: none !important;
            padding: 12px 22px !important;
            box-shadow: 0 8px 24px rgba(104, 70, 198, 0.45) !important;
            transition: all 0.25s ease !important;
        }

        div[data-testid="stButton"] button[kind="primary"]:hover {
            background: linear-gradient(135deg, #7853DD 0%, #906DF0 100%) !important;
            box-shadow: 0 12px 30px rgba(104, 70, 198, 0.65) !important;
            transform: translateY(-2px) !important;
        }

        /* Secondary Button */
        div[data-testid="stButton"] button[kind="secondary"] {
            background: rgba(255, 255, 255, 0.05) !important;
            color: #E2E8F0 !important;
            border: 1px solid rgba(104, 70, 198, 0.35) !important;
            border-radius: 9999px !important;
            font-weight: 600 !important;
            transition: all 0.25s ease !important;
        }

        div[data-testid="stButton"] button[kind="secondary"]:hover {
            background: rgba(104, 70, 198, 0.25) !important;
            color: #FFFFFF !important;
            border-color: #805CE5 !important;
        }

        /* Diff Banner */
        .diff-banner {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 14px;
            background: rgba(22, 17, 38, 0.7);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(104, 70, 198, 0.3);
            border-radius: 14px;
            padding: 12px 20px;
            margin-bottom: 16px;
        }

        .banner-pill {
            font-size: 0.72rem;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 6px;
            letter-spacing: 0.05em;
        }

        .banner-old { background: #374151; color: #F3F4F6; }
        .banner-new { background: #6846C6; color: #FFFFFF; }
        .banner-file { font-size: 0.9rem; font-weight: 600; color: #FFFFFF; }
        .banner-arrow { font-size: 1.2rem; color: #6EC1E4; font-weight: 800; }

        /* KPI Panel */
        .kpi-panel {
            background: rgba(26, 20, 48, 0.55);
            backdrop-filter: blur(20px);
            border-radius: 18px 18px 0 0;
            padding: 16px 20px 8px 20px;
            margin-bottom: 8px;
        }

        .kpi-panel-title {
            font-size: 1.15rem;
            font-weight: 800;
            color: #FFFFFF;
        }

        .kpi-panel-sub {
            font-size: 0.76rem;
            color: #94A3B8;
            margin-top: 2px;
        }

        .kpi-metric-box {
            border-radius: 14px;
            padding: 14px 10px;
            text-align: center;
            backdrop-filter: blur(12px);
            transition: transform 0.2s ease;
        }

        .kpi-metric-box:hover {
            transform: translateY(-2px);
        }

        .kpi-number {
            font-size: 2.2rem;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 4px;
            letter-spacing: -0.02em;
        }

        .kpi-tag {
            font-size: 0.75rem;
            color: #CBD5E1;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        /* Empty State */
        .empty-state-card {
            text-align: center;
            padding: 70px 30px;
            background: rgba(26, 20, 48, 0.45);
            backdrop-filter: blur(20px);
            border: 1px dashed rgba(104, 70, 198, 0.3);
            border-radius: 24px;
            margin: 20px 0;
        }

        .empty-state-icon {
            margin-bottom: 14px;
        }

        .empty-state-title {
            font-size: 1.5rem;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 8px;
        }

        .empty-state-desc {
            color: #94A3B8;
            font-size: 0.95rem;
            line-height: 1.6;
            max-width: 650px;
            margin: auto;
            margin-bottom: 24px;
        }

        .empty-state-badges {
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
        }

        .badge-pill {
            background: rgba(104, 70, 198, 0.18);
            border: 1px solid rgba(104, 70, 198, 0.35);
            border-radius: 9999px;
            padding: 6px 14px;
            font-size: 0.78rem;
            font-weight: 600;
            color: #E2D9FC;
        }

        /* Tabs */
        button[data-baseweb="tab"] {
            color: #94A3B8 !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: #FFFFFF !important;
            border-bottom-color: #805CE5 !important;
        }

        /* Hide InputInstructions */
        [data-testid="InputInstructions"],
        .stForm [data-testid="InputInstructions"],
        [data-testid="stFormSubmitButton"] small,
        [data-testid="stForm"] small,
        div[class*="InputInstructions"],
        span:has(> small) {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

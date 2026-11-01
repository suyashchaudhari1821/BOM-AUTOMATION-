"""
app.py — Tooling BOM Comparison System — Expleo Engineering Platform.
"""

from pathlib import Path
from PIL import Image
import streamlit as st

from ui.bom_comparison_ui import render as render_bom_comparison
from ui.login_view import render_login_page

# Load Expleo icon for browser tab
favicon_path = Path(__file__).parent / "ui" / "favicon.png"
if favicon_path.exists():
    try:
        tab_icon = Image.open(favicon_path)
    except Exception:
        tab_icon = str(favicon_path)
else:
    tab_icon = "ui/expleo_logo.png"

st.set_page_config(
    page_title="Expleo | Tooling BOM Intelligence",
    page_icon=tab_icon,
    layout="wide",
    initial_sidebar_state="collapsed",
)

if not st.session_state.get("authenticated", False):
    render_login_page()
else:
    user_name = st.session_state.get("user_name", "user@expleogroup.com")
    user_login = st.session_state.get("user_login", "user@expleogroup.com")
    render_bom_comparison(user_name=user_name, user_login=user_login)

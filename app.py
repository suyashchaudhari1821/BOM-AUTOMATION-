"""
app.py — Tooling BOM Comparison System — Expleo Engineering Platform.
"""

import sys
from pathlib import Path
from PIL import Image
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ui.bom_comparison_ui import render as render_bom_comparison
from ui.login_view import render_login_page

# Official Expleo favicon for browser tab (loads local high-res PNG for 100% offline & online reliability)
FAVICON_PATH = ROOT_DIR / "ui" / "favicon.png"
if FAVICON_PATH.exists():
    try:
        tab_icon = Image.open(FAVICON_PATH)
    except Exception:
        tab_icon = str(FAVICON_PATH)
else:
    tab_icon = "https://expleo.com/global/en/wp-content/uploads/2026/06/expleo-favicon.svg"

st.set_page_config(
    page_title="Expleo | BOM Intelligence",
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

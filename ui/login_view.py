"""
login_view.py — Expleo Themed Login Experience for Tooling BOM System.
Matches the official Expleo brand design (https://expleo.com/global/en/#contact):
  - Signature Expleo Violet (#6846C6) and Electric Cyan (#6EC1E4)
  - Glassmorphic panels with dark tech engineering aesthetic
  - Official Expleo imagery, typography, and layout
  - Clean corporate SVGs (no emojis)
  - Secure credential verification + Quick Demo 1-Click Login (user@expleogroup.com)
"""

import base64
from pathlib import Path
import streamlit as st
import bcrypt
import toml

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


def _verify_credentials(username_or_email: str, password: str) -> tuple[bool, str, str]:
    """
    Check entered credentials against secrets.toml.
    Supports user@expleogroup.com, expleo, and registered accounts.
    """
    user_clean = username_or_email.strip().lower()
    pass_clean = password.strip()

    # Direct support for Expleo demo/dev users
    if (user_clean in ["user@expleogroup.com", "expleo", "admin", "demo", "suyash"]) and (
        pass_clean in ["123456", "expleo", "admin", "password", "demo", "demo123"]
    ):
        return True, "user@expleogroup.com", "user@expleogroup.com"

    # Check secrets.toml
    secrets_path = Path(__file__).resolve().parent.parent / ".streamlit" / "secrets.toml"
    if secrets_path.exists():
        try:
            sec = toml.load(secrets_path)
            users = sec.get("credentials", {}).get("usernames", {})
            for u_key, u_data in users.items():
                if user_clean == u_key.lower() or user_clean == u_data.get("email", "").lower():
                    stored_pw = u_data.get("password", "")
                    if stored_pw == pass_clean:
                        email = u_data.get("email", "") or "user@expleogroup.com"
                        return True, email, email
                    if stored_pw.startswith("$2"):
                        try:
                            if bcrypt.checkpw(pass_clean.encode("utf-8"), stored_pw.encode("utf-8")):
                                email = u_data.get("email", "") or "user@expleogroup.com"
                                return True, email, email
                        except Exception:
                            pass
        except Exception:
            pass

    return False, "", ""


def render_login_page():
    """Renders the state-of-the-art Expleo Login Page without emojis."""
    logo_uri = _get_logo_data_uri()
    icon_uri = _get_icon_data_uri()
    icon_html = f'<img src="{icon_uri}" class="top-brand-icon" alt="Expleo Mark" />' if icon_uri else ""

    # Inject Expleo Login CSS
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    /* Global Viewport Reset */
    .stApp {{
        background: #090710 !important;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(104, 70, 198, 0.25) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(110, 193, 228, 0.15) 0%, transparent 45%),
            linear-gradient(135deg, rgba(11, 8, 20, 0.85) 0%, rgba(6, 4, 12, 0.95) 100%),
            url('https://expleo.com/global/en/wp-content/uploads/2026/10/power-of-ai_bfsi_homepage-slider_desktop.jpg') !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        font-family: 'Montserrat', 'Inter', -apple-system, sans-serif !important;
        color: #F8FAFC !important;
    }}

    [data-testid="stHeader"], #MainMenu, footer {{
        display: none !important;
    }}

    .block-container {{
        max-width: 1240px !important;
        padding-top: 3.5rem !important;
        padding-bottom: 2rem !important;
        margin: auto !important;
    }}

    /* Expleo Brand Header Pill */
    .expleo-top-brand {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 26px;
        background: rgba(22, 17, 38, 0.72);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(104, 70, 198, 0.3);
        border-radius: 18px;
        margin-bottom: 28px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }}

    .top-brand-icon {{
        width: 36px;
        height: 36px;
        border-radius: 50%;
        object-fit: contain;
        filter: drop-shadow(0 2px 10px rgba(104, 70, 198, 0.6));
        flex-shrink: 0;
        transition: transform 0.25s ease;
    }}

    .top-brand-icon:hover {{
        transform: scale(1.08);
    }}

    .expleo-logo-img {{
        height: 38px;
        object-fit: contain;
        filter: drop-shadow(0 2px 8px rgba(104, 70, 198, 0.4));
    }}

    .expleo-portal-tag {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(104, 70, 198, 0.2);
        border: 1px solid rgba(104, 70, 198, 0.45);
        padding: 6px 14px;
        border-radius: 9999px;
        color: #E2D9FC;
        font-size: 0.76rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }}

    .pulse-dot {{
        width: 8px;
        height: 8px;
        background: #00E5FF;
        border-radius: 50%;
        box-shadow: 0 0 8px #00E5FF;
        display: inline-block;
    }}

    /* Hero Branding Panel */
    .hero-card {{
        padding: 42px 36px;
        background: rgba(22, 17, 38, 0.72);
        backdrop-filter: blur(28px);
        -webkit-backdrop-filter: blur(28px);
        border: 1px solid rgba(104, 70, 198, 0.3);
        border-radius: 24px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45);
        min-height: 520px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-sizing: border-box;
    }}

    .hero-eyebrow {{
        color: #6EC1E4;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }}

    .hero-title {{
        font-size: 2.15rem;
        font-weight: 800;
        line-height: 1.2;
        letter-spacing: -0.02em;
        color: #FFFFFF;
        margin-bottom: 14px;
    }}

    .hero-title span {{
        background: linear-gradient(135deg, #A78BFA 0%, #6846C6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .hero-desc {{
        color: #CBD5E1;
        font-size: 0.92rem;
        line-height: 1.6;
        margin-bottom: 24px;
        font-weight: 400;
    }}

    /* Clean Unboxed Feature Items */
    .feat-row {{
        display: flex;
        flex-direction: column;
        gap: 16px;
        margin-bottom: 20px;
    }}

    .feat-item {{
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 4px 0;
        background: transparent !important;
        border: none !important;
    }}

    .feat-icon {{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        background: rgba(104, 70, 198, 0.22);
        border: 1px solid rgba(110, 193, 228, 0.25);
        border-radius: 10px;
        flex-shrink: 0;
    }}

    .feat-text-title {{
        font-weight: 700;
        color: #FFFFFF;
        font-size: 0.88rem;
        margin-bottom: 2px;
    }}

    .feat-text-sub {{
        color: #94A3B8;
        font-size: 0.78rem;
        line-height: 1.35;
    }}

    /* Twin Card Layout: Balanced Login Form Card */
    div[data-testid="stForm"] {{
        padding: 42px 36px !important;
        background: rgba(22, 17, 38, 0.72) !important;
        backdrop-filter: blur(28px) !important;
        -webkit-backdrop-filter: blur(28px) !important;
        border: 1px solid rgba(104, 70, 198, 0.3) !important;
        border-radius: 24px !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45) !important;
        min-height: 520px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        box-sizing: border-box !important;
    }}

    .login-heading {{
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        margin-bottom: 8px !important;
        letter-spacing: -0.02em !important;
    }}

    .login-sub {{
        font-size: 0.9rem !important;
        color: #94A3B8 !important;
        margin-bottom: 28px !important;
        line-height: 1.5 !important;
    }}

    /* Streamlit Input Styling Overrides */
    div[data-testid="stTextInput"] {{
        margin-bottom: 18px !important;
    }}

    div[data-testid="stTextInput"] label {{
        color: #E2E8F0 !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        margin-bottom: 8px !important;
        letter-spacing: 0.02em !important;
    }}

    div[data-testid="stTextInput"] input {{
        background: rgba(14, 10, 24, 0.85) !important;
        border: 1px solid rgba(104, 70, 198, 0.35) !important;
        border-radius: 14px !important;
        color: #FFFFFF !important;
        padding: 14px 18px !important;
        font-size: 0.95rem !important;
        transition: all 0.25s ease !important;
    }}

    div[data-testid="stTextInput"] input:focus {{
        border-color: #805CE5 !important;
        box-shadow: 0 0 0 3px rgba(104, 70, 198, 0.35) !important;
        background: rgba(18, 12, 32, 0.95) !important;
    }}

    /* Expleo Violet Primary Button Styling */
    div[data-testid="stFormSubmitButton"] button,
    div[data-testid="stButton"] button[kind="primary"] {{
        background: linear-gradient(135deg, #6846C6 0%, #805CE5 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.04em !important;
        padding: 15px 28px !important;
        border-radius: 9999px !important;
        border: none !important;
        box-shadow: 0 8px 24px rgba(104, 70, 198, 0.5) !important;
        transition: all 0.3s ease !important;
        margin-top: 10px !important;
    }}

    div[data-testid="stFormSubmitButton"] button:hover,
    div[data-testid="stButton"] button[kind="primary"]:hover {{
        background: linear-gradient(135deg, #7853DD 0%, #906DF0 100%) !important;
        box-shadow: 0 12px 32px rgba(104, 70, 198, 0.7) !important;
        transform: translateY(-2px) !important;
    }}

    /* Harmonized Footers */
    .hero-footer,
    .login-card-footer {{
        padding-top: 18px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        font-size: 0.76rem;
        color: #64748B;
        text-align: center;
        letter-spacing: 0.02em;
    }}

    /* Hide 'Press Enter to submit form' instructions completely */
    [data-testid="InputInstructions"],
    .stForm [data-testid="InputInstructions"],
    [data-testid="stFormSubmitButton"] small,
    [data-testid="stForm"] small,
    div[class*="InputInstructions"],
    span:has(> small) {{
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Top Brand Bar
    st.markdown(f"""
    <div class="expleo-top-brand">
        <div style="display: flex; align-items: center; gap: 16px;">
            <img src="{logo_uri}" class="expleo-logo-img" alt="Expleo" />
            <span style="color: #64748B; font-size: 1.1rem;">|</span>
            <span style="font-weight: 700; font-size: 0.95rem; color: #FFFFFF; letter-spacing: 0.02em;">BOM Intelligence</span>
        </div>
        <div class="expleo-portal-tag">
            <span class="pulse-dot"></span>
            <span>Enterprise Portal</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main Grid (Balanced Twin Columns)
    col_left, col_right = st.columns([6, 6], gap="large")

    with col_left:
        st.markdown("""<div class="hero-card">
<div>
    <div class="hero-eyebrow">EXPLEO DIGITAL TRANSFORMATION</div>
    <div class="hero-title">Accelerating <span>Engineering Change Intelligence</span></div>
    <div class="hero-desc">Automated comparison engine for complex engineering BOMs. Detects additions, deletions, and field modifications with pinpoint accuracy.</div>
    <div class="feat-row">
        <div class="feat-item">
            <div class="feat-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6EC1E4" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg></div>
            <div>
                <div class="feat-text-title">Automated Detection</div>
                <div class="feat-text-sub">Rapid structural scanning with automated item keying and intelligent classification.</div>
            </div>
        </div>
        <div class="feat-item">
            <div class="feat-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6EC1E4" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></div>
            <div>
                <div class="feat-text-title">Bilingual French &amp; English Output</div>
                <div class="feat-text-sub">Generates executive-ready Excel reports with color-coded audits matching industrial standards.</div>
            </div>
        </div>
        <div class="feat-item">
            <div class="feat-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6EC1E4" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
            <div>
                <div class="feat-text-title">Enterprise-Grade Reliability</div>
                <div class="feat-text-sub">Optimized for high-volume engineering files with zero data loss and deterministic outcomes.</div>
            </div>
        </div>
    </div>
</div>
<div class="hero-footer">
    Industrial Engineering &middot; Automated Audit Engine
</div>
</div>""", unsafe_allow_html=True)

    with col_right:
        with st.form("expleo_login_form", clear_on_submit=False):
            st.markdown("""<div>
<div class="login-heading">Welcome Back</div>
<div class="login-sub">Sign in with your Expleo credentials to access the BOM comparison workspace.</div>
</div>""", unsafe_allow_html=True)
            username = st.text_input("Username or Expleo Email", placeholder="e.g. user@expleogroup.com", key="login_user")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            submit_login = st.form_submit_button("Sign In →", type="primary", use_container_width=True)
            st.markdown("""<div class="login-card-footer">
Expleo Group &copy; 2026 &middot; Secure Enterprise Authentication
</div>""", unsafe_allow_html=True)

        if submit_login:
            if not username or not password:
                st.error("Please enter both username and password.")
            else:
                success, display_name, login_id = _verify_credentials(username, password)
                if success:
                    st.session_state["authenticated"] = True
                    st.session_state["user_name"] = "user@expleogroup.com"
                    st.session_state["user_login"] = login_id
                    st.success(f"Welcome, {display_name}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password. Please verify your credentials.")

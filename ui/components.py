import streamlit as st

def render_login_branding():
    """Returns the HTML string for the left side branding panel on the login page."""
    return (
        '<div class="login-brand-panel">'
        '<div class="login-icon">\u2699\ufe0f</div>'
        '<div class="login-brand-title">Industrial<br>Comparison<br>Analysis System</div>'
        '<div class="login-brand-sub">Automated Engineering Change<br>Detection Platform</div>'
        
        '<div class="feature-card">'
        '<div class="feature-icon-wrapper">\U0001f3af</div>'
        '<div>'
        '<div class="feature-text-title">High Accuracy</div>'
        '<div class="feature-text-sub">99%+ comparison accuracy</div>'
        '</div></div>'
        
        '<div class="feature-card">'
        '<div class="feature-icon-wrapper">\u26a1</div>'
        '<div>'
        '<div class="feature-text-title">Fast Processing</div>'
        '<div class="feature-text-sub">15 min for 100K+ records</div>'
        '</div></div>'
        
        '<div class="feature-card">'
        '<div class="feature-icon-wrapper">\U0001f512</div>'
        '<div>'
        '<div class="feature-text-title">Secure &amp; Reliable</div>'
        '<div class="feature-text-sub">Enterprise-grade security</div>'
        '</div></div>'
        
        '<div class="login-footer">\u00a9 2026 Expleo Group. All rights reserved.</div>'
        '</div>'
    )

def render_sidebar_branding():
    """Renders the top branding section inside the Streamlit sidebar."""
    st.sidebar.markdown(
        '<div class="sidebar-brand">'
        '<div style="font-size:1.5rem;margin-bottom:6px;">\u2699\ufe0f</div>'
        '<div class="sidebar-brand-title">Industrial Comparison<br>Analysis System</div>'
        '<div class="sidebar-brand-subtitle">Engineering Platform</div>'
        '</div>',
        unsafe_allow_html=True,
    )

def render_sidebar_profile(user_name: str, user_login: str, user_role: str, last_login: str):
    """Renders the user profile card inside the Streamlit sidebar."""
    initials = "".join([n[0].upper() for n in user_name.split() if n][:2]) if user_name else "U"
    st.sidebar.markdown(
        '<div class="profile-card">'
        '<div class="profile-row">'
        f'<div class="profile-avatar">{initials}</div>'
        '<div>'
        f'<div class="profile-name">{user_name}</div>'
        f'<div class="profile-login">@{user_login}</div>'
        f'<div class="profile-role">{user_role}</div>'
        '</div>'
        '</div>'
        f'<div class="profile-last-login">Last Login: {last_login}</div>'
        '</div>',
        unsafe_allow_html=True,
    )

def render_main_header():
    """Renders the main header bar for the application pages."""
    st.markdown(
        '<div class="main-header">'
        '<div class="main-header-title">'
        '\u2699\ufe0f &nbsp; Industrial Comparison Analysis System'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

import streamlit as st

def inject_global_css():
    """Inject custom CSS for the entire application."""
    st.markdown("""
    <style>
    /* -- Import Google Font -- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* -- Global Font Override -- */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    /* -- Sidebar Styling -- */
    section[data-testid="stSidebar"] {
        width: 260px !important;
        min-width: 260px !important;
        max-width: 260px !important;
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    section[data-testid="stSidebar"] > div {
        width: 260px !important;
    }
    section[data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.1) !important;
    }

    /* -- Sidebar Branding -- */
    .sidebar-brand {
        padding: 20px 16px 16px 16px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 20px;
    }
    .sidebar-brand-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #FFFFFF !important;
        line-height: 1.3;
        margin: 0;
    }
    .sidebar-brand-subtitle {
        font-size: 0.72rem;
        color: #64748B !important;
        font-weight: 400;
        margin-top: 4px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    .sidebar-nav-label {
        font-size: 0.74rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #94A3B8 !important;
        margin: 0 0 8px 2px;
        font-weight: 600;
    }

    .sidebar-nav-spacer {
        height: 14vh;
        min-height: 72px;
    }

    /* -- Navigation Item Styling -- */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] > div {
        gap: 8px;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
        border-radius: 12px;
        padding: 8px 10px;
        margin: 2px 0;
        transition: all 0.2s ease;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
        background: rgba(124, 58, 237, 0.14);
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label p {
        color: #CBD5E1 !important;
        font-weight: 500;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(135deg, #6D28D9 0%, #7C3AED 100%) !important;
        box-shadow: 0 8px 20px rgba(124,58,237,0.30);
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) p {
        color: #FFFFFF !important;
        font-weight: 600;
    }

    /* -- Logout Button in Navigation -- */
    section[data-testid="stSidebar"] div[data-testid="stButton"] button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.12) !important;
        background: rgba(255,255,255,0.02) !important;
        color: #E2E8F0 !important;
        font-weight: 500;
        transition: all 0.2s ease;
        text-align: left;
        padding: 10px 12px;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {
        background: rgba(239, 68, 68, 0.18) !important;
        border-color: rgba(239, 68, 68, 0.35) !important;
        color: #FEE2E2 !important;
    }

    /* -- Profile Card -- */
    .profile-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 16px;
        margin-top: 12px;
    }
    .profile-row {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .profile-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.85rem;
        color: #FFFFFF !important;
        flex-shrink: 0;
    }
    .profile-name {
        font-weight: 600;
        font-size: 0.9rem;
        color: #F1F5F9 !important;
        margin: 0;
    }
    .profile-login {
        font-size: 0.75rem;
        color: #CBD5E1 !important;
        margin: 2px 0 2px 0;
    }
    .profile-role {
        font-size: 0.75rem;
        color: #64748B !important;
        margin: 0;
    }
    .profile-last-login {
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid rgba(255,255,255,0.08);
        font-size: 0.7rem;
        color: #94A3B8 !important;
    }

    /* -- Main Header Bar -- */
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
        padding: 20px 32px;
        border-radius: 14px;
        margin-bottom: 8px;
        border: 1px solid rgba(255,255,255,0.06);
    }
    .main-header-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0;
        letter-spacing: -0.5px;
    }

    /* -- Page Sub-Header -- */
    .page-subheader {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 6px;
        padding: 0;
    }
    .page-subheader-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1E293B;
        margin: 0;
    }
    .page-subheader-desc {
        color: #64748B;
        font-size: 0.95rem;
        margin: 0 0 16px 0;
    }

    /* -- Metric Card Improvements -- */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    div[data-testid="stMetric"] label {
        color: #64748B !important;
        font-weight: 500 !important;
        font-size: 0.82rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        color: #1E293B !important;
    }

    /* -- File Uploader Improvements -- */
    section[data-testid="stFileUploader"] {
        border: 2px dashed #CBD5E1 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        transition: border-color 0.2s ease;
    }
    section[data-testid="stFileUploader"]:hover {
        border-color: #2563EB !important;
    }

    /* -- Expander Improvements -- */
    details[data-testid="stExpander"] {
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        border-left: 4px solid #2563EB !important;
        overflow: hidden;
    }

    /* -- Hide Streamlit default elements -- */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


def inject_login_css():
    """Inject CSS ONLY for the login page - layout, master card, and styling."""
    st.markdown("""
    <style>
    /* ================================================================
       LOGIN PAGE LAYOUT OVERRIDES
       ================================================================ */

    /* -- Lock viewport: edge-to-edge, no scroll -- */
    .stApp {
        background-color: #E2E8F0 !important; /* Outer page background */
        height: 100vh !important;
        overflow: hidden !important;
    }
    
    [data-testid="stHeader"] {
        display: none !important;
    }

    /* -- Remove all Streamlit default top/bottom padding -- */
    .stApp > div:first-child,
    .stMainBlockContainer,
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
        height: 100vh !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* -- Master card: the single centered container -- */
    [data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"] {
        width: 90vw !important;
        max-width: 1200px !important;
        height: 85vh !important;
        min-height: 600px !important;
        background: #FFFFFF !important; /* The entire right side should be white workspace */
        border-radius: 24px !important;
        box-shadow: 0 24px 80px rgba(0,0,0,0.1), 0 4px 20px rgba(0,0,0,0.05) !important;
        overflow: hidden !important;
        margin: auto !important;
        gap: 0 !important;
        border: none !important;
        display: flex !important;
        flex-wrap: nowrap !important;
        align-items: stretch !important; /* Ensure both columns are 100% height */
    }

    /* -- Left column (brand panel): 40% -- */
    [data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child {
        flex: 0 0 40% !important;
        max-width: 40% !important;
        width: 40% !important;
        padding: 0 !important;
        margin: 0 !important;
        height: 100% !important;
        min-height: 100% !important;
        background-color: #4338CA !important;
    }

    /* -- Right column (login area workspace): 60% -- */
    [data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child {
        flex: 0 0 60% !important;
        max-width: 60% !important;
        width: 60% !important;
        padding: 0 !important;
        margin: 0 !important;
        height: 100% !important;
        min-height: 100% !important;
        background-color: transparent !important; /* Shows the #FFFFFF master card background */
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: flex-start !important; /* Align from top, we'll use margin on the child */
    }

    /* -- Center content inside right column & constrain width -- */
    [data-testid="stMainBlockContainer"] [data-testid="stColumn"]:last-child > div[data-testid="stVerticalBlock"] {
        background: transparent !important; /* Removed nested card background */
        border-radius: 0 !important; /* Removed nested card radius */
        box-shadow: none !important; /* Removed nested card shadow */
        border: none !important; /* Removed nested card border */
        width: 100% !important;
        max-width: 450px !important;
        margin: 14vh auto auto auto !important; /* Pushed down from top, centered horizontally */
        padding: 0 32px !important; /* Replaced massive 40px padding with standard side padding */
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }

    /* -- Brand panel inner -- */
    .login-brand-panel {
        background-color: transparent !important;
        background-image: 
            linear-gradient(160deg, rgba(67, 56, 202, 0.90) 0%, rgba(99, 102, 241, 0.90) 40%, rgba(129, 140, 248, 0.92) 100%),
            url('https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=1200&auto=format&fit=crop');
        background-size: cover;
        background-position: center bottom;
        padding: 80px 40px 40px 40px !important; /* Move content up with top padding */
        height: 100% !important;
        width: 100% !important;
        box-sizing: border-box !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important; /* Align from top instead of center */
        position: relative !important;
    }
    
    .login-icon {
        font-size: 2.5rem;
        margin-bottom: 24px;
        position: relative;
        z-index: 1;
    }
    
    .login-brand-title {
        font-size: 2rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.15;
        margin-bottom: 12px;
        position: relative;
        z-index: 1;
        letter-spacing: -0.5px;
    }
    
    .login-brand-sub {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.85);
        margin-bottom: 32px;
        position: relative;
        z-index: 1;
        line-height: 1.5;
        font-weight: 400;
    }
    
    /* -- Glassmorphism Feature Cards -- */
    .feature-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 16px;
        position: relative;
        z-index: 1;
    }
    
    .feature-icon-wrapper {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.15);
        font-size: 1rem;
        flex-shrink: 0;
    }
    
    .feature-text-title {
        color: #FFFFFF;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 2px;
    }
    
    .feature-text-sub {
        color: rgba(255, 255, 255, 0.65);
        font-size: 0.7rem;
    }

    .login-footer {
        margin-top: auto;
        font-size: 12px;
        color: rgba(255,255,255,0.7);
        position: relative;
        z-index: 1;
        padding-top: 32px;
    }

    /* -- Right panel form elements -- */
    .login-form-heading {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 4px;
        text-align: left;
    }
    
    .login-form-sub {
        font-size: 0.95rem;
        color: #64748B;
        margin-bottom: 24px;
        text-align: left;
    }
    
    /* Hide the default Form "Login" heading from authenticator */
    [data-testid="stMainBlockContainer"] [data-testid="stColumn"]:last-child [data-testid="stForm"] h1,
    [data-testid="stMainBlockContainer"] [data-testid="stColumn"]:last-child [data-testid="stForm"] h2,
    [data-testid="stMainBlockContainer"] [data-testid="stColumn"]:last-child [data-testid="stForm"] h3 {
        display: none !important;
    }
    
    /* Remove default stForm border/styling */
    [data-testid="stMainBlockContainer"] [data-testid="stColumn"]:last-child [data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        box-shadow: none !important;
        background: transparent !important;
    }
    
    /* ================================================================
       DEFINITIVE BUTTON SQUISHING FIX (Hard pixel width override)
       ================================================================ */
    [data-testid="stForm"] {
        position: relative !important;
    }
    
    /* Make ALL wrappers inside the form full-width since Streamlit flex collapses them */
    [data-testid="stForm"] div[data-testid="element-container"],
    [data-testid="stForm"] .stButton {
        width: 100% !important;
        min-width: 386px !important; /* Match constrained content width exactly */
        max-width: 100% !important;
        display: block !important;
    }
    
    /* Space for the pseudo elements */
    [data-testid="stFormSubmitButton"] {
        margin-top: 60px !important; 
        position: relative !important;
    }
    
    /* Attach links directly to the wrapper */
    [data-testid="stFormSubmitButton"]::before {
        content: '\\2611 Remember me';
        position: absolute;
        top: -32px;
        left: 4px;
        font-size: 0.85rem;
        color: #64748B;
        cursor: pointer;
    }
    
    [data-testid="stFormSubmitButton"]::after {
        content: 'Forgot password?';
        position: absolute;
        top: -32px;
        right: 4px;
        font-size: 0.85rem;
        color: #4338CA;
        cursor: pointer;
        font-weight: 500;
    }
    
    /* Force the button to be exactly 386px wide (450px card width minus 64px padding) */
    [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #4338CA 0%, #6366F1 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        height: 48px !important;
        width: 386px !important; /* HARD PIXEL WIDTH PREVENTS COLLAPSE */
        min-width: 386px !important; 
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s ease !important;
        position: relative !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    
    [data-testid="stFormSubmitButton"] button p {
        color: transparent !important; /* Hide original text */
        display: none !important; /* Remove from flow so it doesn't affect centering */
    }
    
    [data-testid="stFormSubmitButton"] button:hover {
        box-shadow: 0 8px 20px rgba(67, 56, 202, 0.25) !important;
        transform: translateY(-1px) !important;
    }
    
    [data-testid="stFormSubmitButton"] button::after {
        content: 'Sign In \u2192';
        position: absolute;
        left: 0; right: 0; top: 0; bottom: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF !important;
        font-weight: 600;
        font-size: 1.05rem;
    }
    
    /* Better styling for text inputs and labels */
    .stTextInput input {
        border-radius: 8px !important;
        border: 1px solid #E2E8F0 !important;
        padding: 12px 16px !important;
        background: #F8FAFC !important;
        color: #1E293B !important;
        width: 100% !important;
    }
    .stTextInput input:focus {
        border-color: #4338CA !important;
        box-shadow: 0 0 0 2px rgba(67, 56, 202, 0.15) !important;
    }
    .stTextInput label {
        color: #475569 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        margin-bottom: 4px !important;
    }

    /* Secure access badge inside footer */
    .login-secure-badge {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        color: #64748B;
        font-size: 0.85rem;
        margin-top: 16px !important;
        padding-top: 16px !important;
        border-top: 1px solid #E2E8F0;
        width: 100%;
    }

    /* Hide sidebar on login page */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

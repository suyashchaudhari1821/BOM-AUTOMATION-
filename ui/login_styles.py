import streamlit as st

def inject_login_css():
    """Injects the CSS specifically for the ICAS V2 Login Page design."""
    st.markdown("""
    <style>
    /* ================================================================
       GLOBAL LOGIN PAGE LOCKDOWN
       ================================================================ */
    
    /* Lock the viewport, apply background, prevent scrolling */
    .stApp {
        background-color: #F5F7FB !important;
        height: 100vh !important;
        width: 100vw !important;
        overflow: hidden !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
    }

    /* Hide Streamlit top header and padding */
    [data-testid="stHeader"] {
        display: none !important;
    }
    
    .stApp > div:first-child,
    .stMainBlockContainer,
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        width: 100vw !important;
        height: 100vh !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* Hide sidebar and bottom components completely */
    section[data-testid="stSidebar"], 
    #MainMenu, 
    footer {
        display: none !important;
    }

    /* ================================================================
       MASTER CONTAINER
       ================================================================ */
    
    /* The main wrapper holding both panels */
    [data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"] {
        width: 92vw !important;
        max-width: 1500px !important;
        height: 92vh !important;
        margin: auto !important;
        background: #FFFFFF !important;
        border-radius: 28px !important;
        box-shadow: 0 20px 60px rgba(0,0,0,0.08), 0 4px 16px rgba(0,0,0,0.04) !important;
        overflow: hidden !important;
        gap: 0 !important;
        border: none !important;
        display: flex !important;
        flex-wrap: nowrap !important;
        align-items: stretch !important;
    }

    /* ================================================================
       LEFT BRANDING PANEL (38%)
       ================================================================ */
    
    [data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child {
        flex: 0 0 38% !important;
        max-width: 38% !important;
        width: 38% !important;
        padding: 0 !important;
        margin: 0 !important;
        height: 100% !important;
        min-height: 100% !important;
        background-color: #5B5BD6 !important;
        position: relative !important;
        z-index: 1 !important;
    }

    /* Branding Panel Inner Container */
    .branding-panel {
        background-image: 
            linear-gradient(150deg, #2E3192 0%, #5B5BD6 45%, #6C63FF 100%),
            url('https://images.unsplash.com/photo-1565514158740-11ada98fd11b?q=80&w=1400&auto=format&fit=crop');
        background-size: cover;
        background-position: center bottom;
        background-blend-mode: overlay; /* Softly blends image with gradient */
        height: 100% !important;
        width: 100% !important;
        box-sizing: border-box !important;
        padding: 64px 48px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
        position: relative !important;
    }
    
    /* Ensure the background image looks industrial but doesn't overpower text */
    .branding-panel::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(46, 49, 146, 0.85); /* 85% opacity gradient fallback */
        z-index: -1;
    }

    .brand-icon {
        font-size: 3rem;
        color: #FFFFFF;
        margin-bottom: 24px;
        line-height: 1;
    }

    .brand-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.15;
        margin-bottom: 12px;
        letter-spacing: -0.5px;
    }

    .brand-subtitle {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.85);
        font-weight: 400;
        margin-bottom: 48px;
        line-height: 1.4;
    }

    /* Glassmorphism Feature Cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 16px;
        display: flex;
        align-items: flex-start; /* Align top for multiline text */
        gap: 16px;
        transition: transform 0.2s ease, background 0.2s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        background: rgba(255, 255, 255, 0.12);
    }

    .feature-icon {
        font-size: 1.25rem;
        line-height: 1;
        margin-top: 2px;
    }

    .feature-content {
        display: flex;
        flex-direction: column;
    }

    .feature-title {
        color: #FFFFFF;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 4px;
    }

    .feature-desc {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.8rem;
        line-height: 1.4;
    }

    .brand-footer {
        margin-top: auto;
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.6);
    }

    /* ================================================================
       RIGHT AUTHENTICATION WORKSPACE (62%)
       ================================================================ */
    
    [data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child {
        flex: 0 0 62% !important;
        max-width: 62% !important;
        width: 62% !important;
        padding: 0 !important;
        margin: 0 !important;
        height: 100% !important;
        min-height: 100% !important;
        background-color: #FFFFFF !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: flex-start !important;
    }

    /* Center the login section horizontally and 45-48% vertically */
    [data-testid="stMainBlockContainer"] [data-testid="stColumn"]:last-child > div[data-testid="stVerticalBlock"] {
        width: 100% !important;
        max-width: 460px !important;
        margin: 18vh auto auto auto !important; /* Positions vertically around ~45% visual center */
        padding: 0 24px !important;
        display: flex !important;
        flex-direction: column !important;
    }

    .welcome-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 8px;
        text-align: left;
    }

    .welcome-subtitle {
        font-size: 1rem;
        color: #6B7280;
        margin-bottom: 32px;
        text-align: left;
    }

    /* Hide the default Streamlit Form title rendered by authenticator */
    [data-testid="stForm"] h1,
    [data-testid="stForm"] h2,
    [data-testid="stForm"] h3 {
        display: none !important;
    }

    /* Remove border and padding from the stForm */
    [data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        box-shadow: none !important;
        background: transparent !important;
    }

    /* Input Fields */
    .stTextInput {
        margin-bottom: 24px !important;
    }
    
    .stTextInput label {
        color: #1F2937 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        margin-bottom: 8px !important;
    }
    
    .stTextInput input {
        border-radius: 8px !important;
        border: 1px solid #E5E7EB !important;
        background-color: #F9FAFB !important;
        padding: 14px 16px !important;
        color: #1F2937 !important;
        font-size: 1rem !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }
    
    .stTextInput input:focus {
        border-color: #5B5BD6 !important;
        box-shadow: 0 0 0 3px rgba(91, 91, 214, 0.1) !important;
        background-color: #FFFFFF !important;
    }

    /* ================================================================
       OPTIONS ROW & BUTTON
       ================================================================ */
       
    [data-testid="stForm"] {
        position: relative !important;
    }

    /* Force button and all its wrappers to absolute full width to prevent flex-collapse */
    [data-testid="stForm"],
    [data-testid="stForm"] > div,
    [data-testid="stForm"] div[data-testid="stVerticalBlock"],
    [data-testid="stForm"] div[data-testid="element-container"],
    [data-testid="stFormSubmitButton"] {
        width: 100% !important;
        min-width: 100% !important;
        display: block !important;
    }

    [data-testid="stFormSubmitButton"] {
        margin-top: 56px !important; /* Space for Remember Me / Forgot Password */
        position: relative !important;
    }

    /* Horizontal Options Row (Remember me / Forgot password) */
    [data-testid="stFormSubmitButton"]::before {
        content: '\\2611 Remember me';
        position: absolute;
        top: -36px;
        left: 2px;
        font-size: 0.9rem;
        color: #6B7280;
        cursor: pointer;
    }

    [data-testid="stFormSubmitButton"]::after {
        content: 'Forgot Password?';
        position: absolute;
        top: -36px;
        right: 2px;
        font-size: 0.9rem;
        color: #5B5BD6;
        cursor: pointer;
        font-weight: 600;
    }

    /* Sign In Button */
    [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #5B5BD6 0%, #6C63FF 100%) !important;
        border: none !important;
        border-radius: 8px !important;
        height: 50px !important;
        
        /* HARD PIXEL WIDTH TO PREVENT COLLAPSE */
        width: calc(100vw - 48px) !important;
        max-width: 412px !important;
        min-width: 300px !important;
        
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: transparent !important; /* Hide default text */
        position: relative !important;
        cursor: pointer !important;
        transition: opacity 0.2s ease !important;
    }

    [data-testid="stFormSubmitButton"] button p {
        display: none !important; /* Hide internal text node completely */
    }

    [data-testid="stFormSubmitButton"] button::after {
        content: 'Sign In \\2192';
        position: absolute;
        left: 0; right: 0; top: 0; bottom: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF !important;
        font-weight: 600;
        font-size: 1rem;
    }

    [data-testid="stFormSubmitButton"] button:hover {
        opacity: 0.9 !important;
    }

    /* ================================================================
       SECURITY FOOTER
       ================================================================ */
       
    .security-footer {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 32px;
        width: 100%;
    }

    .security-divider {
        width: 100%;
        height: 1px;
        background-color: #E5E7EB;
        margin-bottom: 24px;
    }

    .security-text {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #6B7280;
        font-size: 0.85rem;
    }

    /* ================================================================
       RESPONSIVENESS
       ================================================================ */
       
    @media (max-width: 1024px) {
        /* Tablet: Reduce branding width */
        [data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child {
            flex: 0 0 30% !important;
            max-width: 30% !important;
            width: 30% !important;
        }
        [data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child {
            flex: 0 0 70% !important;
            max-width: 70% !important;
            width: 70% !important;
        }
    }

    @media (max-width: 768px) {
        /* Mobile: Stack vertically */
        .stApp {
            overflow: auto !important;
        }
        [data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            height: auto !important;
            min-height: 100vh !important;
            width: 100vw !important;
            border-radius: 0 !important;
            margin: 0 !important;
        }
        [data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child {
            flex: 1 1 auto !important;
            max-width: 100% !important;
            width: 100% !important;
            padding: 40px 24px !important;
        }
        [data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child {
            flex: 1 1 auto !important;
            max-width: 100% !important;
            width: 100% !important;
            padding: 40px 24px !important;
        }
        [data-testid="stMainBlockContainer"] [data-testid="stColumn"]:last-child > div[data-testid="stVerticalBlock"] {
            margin: 0 auto !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

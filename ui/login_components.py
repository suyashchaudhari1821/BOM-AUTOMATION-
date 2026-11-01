import streamlit as st

def render_branding_panel():
    """Returns the HTML string for the left side branding panel on the login page."""
    return (
        '<div class="branding-panel">'
        '<div class="brand-icon">\u2699\ufe0f</div>'
        '<div class="brand-title">Industrial<br>Comparison<br>Analysis System</div>'
        '<div class="brand-subtitle">Automated Engineering Change Detection Platform</div>'
        
        '<div class="feature-card">'
        '<div class="feature-icon">\U0001f3af</div>'
        '<div class="feature-content">'
        '<div class="feature-title">High Accuracy</div>'
        '<div class="feature-desc">99%+ comparison accuracy</div>'
        '</div></div>'
        
        '<div class="feature-card">'
        '<div class="feature-icon">\u26a1</div>'
        '<div class="feature-content">'
        '<div class="feature-title">Fast Processing</div>'
        '<div class="feature-desc">Processes 100K+ engineering records efficiently</div>'
        '</div></div>'
        
        '<div class="feature-card">'
        '<div class="feature-icon">\U0001f512</div>'
        '<div class="feature-content">'
        '<div class="feature-title">Secure &amp; Reliable</div>'
        '<div class="feature-desc">Enterprise-grade engineering workflow platform</div>'
        '</div></div>'
        
        '<div class="brand-footer">\u00a9 2026 Expleo Group. All rights reserved.</div>'
        '</div>'
    )

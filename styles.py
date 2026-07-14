import streamlit as st

def apply_custom_styles():
    """
    Applies modern, rich dark-mode glassmorphism aesthetics and responsive styling
    for RoadGuard Pro using Streamlit CSS injection.
    """
    st.markdown("""
    <style>
    /* Import modern Inter Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global Body & Typography overrides */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        color: #F8FAFC !important;
    }

    /* Main Header Styling */
    .main-header {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 50%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
        line-height: 1.2;
        margin-bottom: 0.4rem;
        text-shadow: 0px 4px 20px rgba(6, 182, 212, 0.25);
    }

    /* Sub Header Styling */
    .sub-header {
        font-size: 1.15rem;
        font-weight: 400;
        color: #94A3B8;
        letter-spacing: -0.01em;
        margin-bottom: 2rem;
        padding-bottom: 1.2rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Premium Glassmorphic Cards */
    .premium-card {
        background: rgba(17, 24, 39, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.75rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .premium-card:hover {
        border-color: rgba(6, 182, 212, 0.35);
    }

    /* Pill Badge for Categories & Assessment Status */
    .pill-badge {
        display: inline-block;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        letter-spacing: 0.02em;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }

    /* Streamlit Tab Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: rgba(15, 23, 42, 0.5);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 8px;
        padding: 0 20px;
        font-weight: 600;
        color: #94A3B8;
        background-color: transparent;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%) !important;
        color: #38BDF8 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
    }

    /* Sidebar Glassmorphism */
    section[data-testid="stSidebar"] {
        background: rgba(11, 15, 25, 0.85) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* Metric Cards Override */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    div[data-testid="stMetricValue"] {
        color: #38BDF8 !important;
        font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

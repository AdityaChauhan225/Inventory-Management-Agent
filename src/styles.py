"""
Custom CSS for IMA-V3 Application
"""


CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers */
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #64B5F6, #2196F3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #B0BEC5;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    /* Metrics Styling - Dark Mode */
    [data-testid="stMetric"] {
        background-color: #262730;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #444;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.5);
        border-color: #64B5F6;
    }
    
    [data-testid="stMetricLabel"] {
        color: #CFD8DC !important;
        font-size: 0.9rem !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    
    /* DataFrame/Table Styling - Dark Mode */
    [data-testid="stDataFrame"] {
        border: 1px solid #444;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    /* Analysis/Processing Box - Dark Mode */
    .analysis-box {
        background-color: #1E2838;
        border-left: 5px solid #64B5F6;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 1rem;
        color: #FFFFFF;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background-color: #1976D2;
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        border: none;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        background-color: #1565C0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-weight: 700;
    }
    
    /* Global Text Fix */
    p, li, span {
        color: #FAFAFA;
    }
</style>
"""


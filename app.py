"""
IMA-V3 - Inventory Management & AI Forecasting
Minimalistic Streamlit Application
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_processor import DataProcessor
from scaledown_client import ScaleDownClient
from ollama_agent import InventoryAgent
from forecaster import Forecaster


# Page configuration
st.set_page_config(
    page_title="Inventory Management Agent",
    page_icon="assets/fav2.png",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for modern design
from styles import CUSTOM_CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def main():
    # State management for analysis results
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'compression_stats' not in st.session_state:
        st.session_state.compression_stats = None
    if 'processed_data_hash' not in st.session_state:
        st.session_state.processed_data_hash = None

    # Header
    st.markdown('<div class="main-header">Inventory Management Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Inventory Management & AI Forecasting System</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Check environment variables
        st.subheader("System Status")
        ollama_configured = bool(os.getenv('OLLAMA_API_KEY') or os.getenv('OLLAMA_HOST') or os.getenv('OLLAMA_API_BASE')) # Flexible check
        scaledown_configured = bool(os.getenv('SCALEDOWN_API_KEY'))
        
        st.markdown(f"""
        - Ollama: {'✅' if ollama_configured else '❌ Not configured'}
        - ScaleDown: {'✅' if scaledown_configured else '⚠️ Will use fallback'}
        """)
        
        st.markdown("---")
        
        # Optional user question
        st.subheader("Custom Analysis")
        user_question = st.text_area(
            "Ask a specific question (optional)",
            placeholder="e.g., Which products should I prioritize for restocking?",
            height=100
        )
        
        # Analyze button in sidebar
        col_sb1, col_sb2 = st.columns(2)
        with col_sb1:
            analyze_sidebar = st.button("🔍 Analyze", key="sidebar_analyze", use_container_width=True)
        with col_sb2:
            if st.button("🔄 Reset", key="sidebar_reset", use_container_width=True):
                st.session_state.analysis_results = None
                st.session_state.compression_stats = None
                st.rerun()
    
    # Main content
    st.header("1️⃣ Upload Your Inventory CSV")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload any CSV file with inventory data. The system will auto-detect relevant columns."
    )
    
    if uploaded_file is not None:
        try:
            # Initialize components
            processor = DataProcessor()
            scaledown = ScaleDownClient()
            agent = InventoryAgent()
            forecaster = Forecaster()
            
            # Step 1: Load CSV with caching
            @st.cache_data
            def load_and_process(file) -> pd.DataFrame:
                return processor.load_csv(file)

            with st.spinner("Loading CSV..."):
                df = load_and_process(uploaded_file)
            
            # Check if new file uploaded (reset analysis)
            current_hash = hash(uploaded_file.getvalue())
            if st.session_state.processed_data_hash != current_hash:
                st.session_state.analysis_results = None
                st.session_state.compression_stats = None
                st.session_state.processed_data_hash = current_hash
            
            st.success(f"✅ Loaded {len(df)} rows")
            
            # Step 2: Preview data
            st.header("2️⃣ Data Preview")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Raw Data")
                st.dataframe(df.head(10), use_container_width=True)
            
            with col2:
                st.subheader("CSV Info")
                st.metric("Total Rows", len(df))
                st.metric("Total Columns", len(df.columns))
                
                # Detect columns
                detected = processor.detect_columns(df)
                if detected:
                    st.markdown("**Detected Columns:**")
                    for key, val in detected.items():
                        st.markdown(f"- `{key}` → `{val}`")
                else:
                    st.warning("⚠️ No standard columns detected. Analysis may be limited.")
            
            # Step 3: Calculate metrics
            st.header("3️⃣ Processing & Analysis")
            
            with st.spinner("Calculating inventory metrics..."):
                processed_df = processor.calculate_metrics(df)
                stats = processor.get_summary_stats(processed_df)
            
            # Display key metrics
            if 'urgency' in processed_df.columns:
                col1, col2, col3, col4 = st.columns(4)
                
                urgency_counts = processed_df['urgency'].value_counts().to_dict()
                
                with col1:
                    st.metric("🔴 Critical", urgency_counts.get('CRITICAL', 0))
                with col2:
                    st.metric("🟡 Warning", urgency_counts.get('WARNING', 0))
                with col3:
                    st.metric("🟠 Monitor", urgency_counts.get('MONITOR', 0))
                with col4:
                    st.metric("🟢 OK", urgency_counts.get('OK', 0))
            
            # Step 4: AI Analysis
            st.header("4️⃣ AI-Powered Insights")
            
            analyze_button = st.button("🤖 Generate AI Analysis", type="primary")
            
            # Trigger analysis if button clicked OR sidebar button clicked
            if analyze_button or analyze_sidebar:
                with st.spinner("Compressing data with ScaleDown..."):
                    # Format data for AI
                    data_text = processor.format_for_ai(processed_df)
                    
                    # Compress with ScaleDown
                    compression_result = scaledown.compress_prompt(data_text)
                    st.session_state.compression_stats = scaledown.get_stats(compression_result)
                
                with st.spinner("Analyzing with Ollama AI (Streaming)..."):
                    with st.chat_message("assistant"):
                        analysis_container = st.empty()
                        full_response = ""
                        
                        try:
                            # Get generator
                            stream = agent.analyze_inventory(
                                compression_result['compressed_text'],
                                user_question if user_question else None
                            )
                            
                            # Consume stream
                            for chunk in stream:
                                full_response += chunk
                                analysis_container.markdown(full_response + "▌")
                            
                            # Final update without cursor
                            analysis_container.markdown(full_response)
                            st.session_state.analysis_results = full_response
                        
                        except Exception as e:
                            st.error(f"Analysis failed: {str(e)}")
                            st.session_state.analysis_results = None
            
            # Display results if available (and not just shown above)
            if st.session_state.analysis_results and not (analyze_button or analyze_sidebar):
                if st.session_state.compression_stats:
                    st.info(st.session_state.compression_stats)
                
                st.markdown("### 📊 Analysis Results")
                with st.chat_message("assistant"):
                    st.markdown(st.session_state.analysis_results)
                
                # Generate report
                st.header("5️⃣ Download Report")
                
                report = forecaster.format_report(st.session_state.analysis_results, processed_df, stats)
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.download_button(
                        label="📥 Download Full Report (Markdown)",
                        data=report,
                        file_name=f"inventory_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
                
                with col2:
                    st.download_button(
                        label="📥 Download CSV",
                        data=processed_df.to_csv(index=False),
                        file_name=f"processed_inventory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            
            # Show processed data table
            st.header("📋 Processed Data")
            
            # Filter options
            filter_col1, filter_col2 = st.columns(2)
            
            with filter_col1:
                if 'urgency' in processed_df.columns:
                    urgency_filter = st.multiselect(
                        "Filter by Urgency",
                        options=['CRITICAL', 'WARNING', 'MONITOR', 'OK'],
                        default=['CRITICAL', 'WARNING']
                    )
                    
                    if urgency_filter:
                        filtered_df = processed_df[processed_df['urgency'].isin(urgency_filter)]
                    else:
                        filtered_df = processed_df
                else:
                    filtered_df = processed_df
            
            st.dataframe(filtered_df, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.expander("Detailed Error").exception(e)  # Hide detailed stack trace in expander
    
    else:
        # Show instructions when no file uploaded
        st.info("""
        👋 **Welcome to IMA-V3!**
        
        This system helps you:
        - 📊 Analyze inventory levels
        - 🔮 Forecast demand
        - ⚠️ Identify items needing restock
        - 📈 Understand demand patterns
        
        **Getting Started:**
        1. Upload your inventory CSV file (any format)
        2. System will auto-detect columns
        3. Get AI-powered insights
        4. Download actionable reports
        
        **CSV Requirements:**
        - Your CSV should ideally contain columns for: product name, stock quantity, sales data
        - Column names can be flexible (e.g., 'stock', 'Stock Qty', 'inventory' all work)
        - The system will work with whatever data you provide!
        """)


if __name__ == "__main__":
    main()

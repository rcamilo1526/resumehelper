import streamlit as st
from config.settings import PAGE_CONFIG
from utils.ui_components import setup_sidebar, setup_main_interface
from config.agents import create_cv_agents
from config.tasks import create_cv_tasks
from utils.file_utils import extract_text_from_pdf
from crewai import Crew
from datetime import datetime

# Page configuration
st.set_page_config(**PAGE_CONFIG)

def main():
    # Initialize session state
    if "cv_analysis" not in st.session_state:
        st.session_state.cv_analysis = None
    if "improved_cv" not in st.session_state:
        st.session_state.improved_cv = None

    # Setup sidebar
    api_key = setup_sidebar()
    
    # Main app interface
    st.title("📄 CV Enhancement Multi-Agent System")
    st.markdown("**Transform your CV with AI-powered analysis and optimization**")
    
    # Setup main interface
    setup_main_interface(api_key)

if __name__ == "__main__":
    main()

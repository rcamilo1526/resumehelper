import streamlit as st
from datetime import datetime
from config.settings import INDUSTRY_OPTIONS
from utils.file_utils import get_cv_text
from config.agents import create_cv_agents
from config.tasks import create_cv_tasks
from crewai import Crew

def setup_sidebar():
    """Setup sidebar with API key input and information"""
    api_key = st.sidebar.text_input(
        "Enter your Perplexity API Key:",
        type="password",
        help="Get your API key from https://www.perplexity.ai/settings/api"
    )
    
    st.sidebar.markdown("### 🎯 How it Works")
    st.sidebar.markdown("""
    1. **Upload** your CV (PDF or text)
    2. **Specify** your target role/industry
    3. **Analysis** by expert agents
    4. **Receive** improved CV version
    """)

    st.sidebar.markdown("### 🤖 Our Agents")
    st.sidebar.markdown("""
    - **Analyst**: Reviews your current CV
    - **Researcher**: Studies industry trends  
    - **Optimizer**: Enhances ATS compatibility
    - **Writer**: Creates improved version
    """)
    
    return api_key

def setup_upload_tab(api_key):
    """Setup the CV upload tab"""
    st.header("Upload Your CV")
    
    # Target role input
    target_role = st.text_input(
        "Target Role/Position:",
        placeholder="e.g., Senior Data Engineer, Marketing Manager, Software Developer"
    )
    
    # Industry selection
    industry = st.selectbox("Industry:", INDUSTRY_OPTIONS)
    
    # CV upload options
    st.subheader("Choose your CV format:")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload CV (PDF format)",
        type=['pdf'],
        help="Upload your CV in PDF format"
    )
    
    # Text input option
    st.markdown("**OR**")
    cv_text_input = st.text_area(
        "Paste your CV text:",
        height=300,
        placeholder="Paste your CV content here..."
    )
    
    # Process CV
    if st.button("🚀 Analyze & Improve CV", type="primary"):
        if not api_key:
            st.error("Please enter your Perplexity API key in the sidebar.")
        elif not target_role:
            st.error("Please specify your target role.")
        else:
            process_cv(api_key, uploaded_file, cv_text_input, target_role, industry)

def process_cv(api_key, uploaded_file, text_input, target_role, industry):
    """Process the CV through the multi-agent system"""
    cv_text = get_cv_text(uploaded_file, text_input)
    
    if not cv_text:
        st.error("Please upload a CV or paste CV text.")
        return
    
    if cv_text.startswith("Error"):
        st.error("❌ Could not extract text from the CV. Please try uploading a different file or pasting text directly.")
        return
    
    with st.spinner("🤖 Our agents are analyzing your CV..."):
        try:
            # Create agents and tasks
            agents = create_cv_agents(api_key)
            tasks = create_cv_tasks(agents, cv_text, target_role, industry)
            
            # Create and run crew
            cv_crew = Crew(
                agents=list(agents),
                tasks=list(tasks),
                verbose=True
            )
            
            # Execute the crew
            results = cv_crew.kickoff()
            
            # Store results in session state
            analysis_task, research_task, optimization_task, writing_task = tasks
            st.session_state.cv_analysis = {
                'analysis': str(analysis_task.output) if analysis_task.output else "Analysis completed",
                'research': str(research_task.output) if research_task.output else "Research completed", 
                'optimization': str(optimization_task.output) if optimization_task.output else "Optimization completed",
                'improved_cv': str(writing_task.output) if writing_task.output else "Improved CV created"
            }
            
            st.success("✅ CV analysis and improvement completed!")
            st.info("👉 Check the 'Analysis' and 'Improved CV' tabs to see the results.")
            
        except Exception as e:
            st.error(f"❌ Error during CV processing: {str(e)}")

def setup_analysis_tab():
    """Setup the analysis results tab"""
    st.header("📊 CV Analysis Results")
    
    if st.session_state.cv_analysis:
        with st.expander("🔍 Detailed CV Analysis", expanded=True):
            st.markdown(st.session_state.cv_analysis['analysis'])
        
        with st.expander("📈 Industry Research Insights"):
            st.markdown(st.session_state.cv_analysis['research'])
        
        with st.expander("⚡ ATS Optimization Recommendations"):
            st.markdown(st.session_state.cv_analysis['optimization'])
    else:
        st.info("👈 Please upload and analyze your CV first in the 'Upload CV' tab.")

def setup_improved_cv_tab():
    """Setup the improved CV display tab"""
    st.header("✨ Your Improved CV")
    
    if st.session_state.cv_analysis:
        improved_cv_content = st.session_state.cv_analysis['improved_cv']
        
        # Display improved CV
        st.subheader("📄 Enhanced CV Version")
        st.markdown("---")
        st.markdown(improved_cv_content)
        
        # Download options
        st.subheader("💾 Download Options")
        col1, col2 = st.columns(2)
        
        with col1:
            # Download as text
            st.download_button(
                label="📝 Download as Text",
                data=improved_cv_content,
                file_name=f"improved_cv_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        with col2:
            # Copy to clipboard button
            if st.button("📋 Copy to Clipboard"):
                st.code(improved_cv_content, language=None)
                st.success("CV content ready to copy!")
    else:
        st.info("👈 Please upload and analyze your CV first to see the improved version.")

def setup_main_interface(api_key):
    """Setup the main tabbed interface"""
    tab1, tab2, tab3 = st.tabs(["📤 Upload CV", "🔍 Analysis", "✨ Improved CV"])
    
    with tab1:
        setup_upload_tab(api_key)
    
    with tab2:
        setup_analysis_tab()
    
    with tab3:
        setup_improved_cv_tab()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ using Streamlit, CrewAI, and Perplexity Sonar API</p>
        <p>🤖 Multi-Agent System: Analysis → Research → Optimization → Writing</p>
    </div>
    """, unsafe_allow_html=True)

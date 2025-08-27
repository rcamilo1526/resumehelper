import streamlit as st
import requests
import os
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Data Engineer Job Hunter AI",
    page_icon="💼",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# API Key configuration
PERPLEXITY_API_KEY = st.sidebar.text_input(
    "Enter your Perplexity API Key:",
    type="password",
    help="Get your API key from https://www.perplexity.ai/settings/api"
)

# Custom tool for job searching using Perplexity Sonar
@tool
def search_data_engineer_jobs(query: str) -> str:
    """
    Search for data engineer jobs using Perplexity Sonar API.
    This tool provides real-time job market information with citations.
    """
    if not PERPLEXITY_API_KEY:
        return "Please provide a Perplexity API key to search for jobs."
    
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Enhanced prompt for job searching
    enhanced_query = f"""
    Find current data engineer job opportunities related to: {query}
    
    Please provide:
    - Job titles and companies
    - Required skills and technologies
    - Salary ranges (if available)
    - Location information
    - Application links or contact information
    - Recent posting dates
    
    Focus on legitimate job postings from reputable sources like LinkedIn, Indeed, Glassdoor, company websites, etc.
    """
    
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system", 
                "content": "You are a specialized job search assistant focused on data engineering roles. Provide accurate, up-to-date job information with proper citations and sources."
            },
            {
                "role": "user", 
                "content": enhanced_query
            }
        ],
        "max_tokens": 1500,
        "temperature": 0.2,
        "top_p": 0.9
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error searching for jobs: {str(e)}"

# Create LLM instance for Perplexity Sonar
if PERPLEXITY_API_KEY:
    sonar_llm = LLM(
        model="perplexity/sonar",
        api_key=PERPLEXITY_API_KEY,
        base_url="https://api.perplexity.ai"
    )
else:
    sonar_llm = None

# Create the Data Engineer Job Hunter Agent
data_engineer_job_agent = Agent(
    role="Senior Data Engineer Job Specialist",
    goal="Help users find the best data engineer job opportunities by providing comprehensive, up-to-date job market information",
    backstory="""You are an expert recruiter and career advisor specializing in data engineering roles. 
    You have deep knowledge of the data engineering job market, including required skills, salary trends, 
    top companies, and emerging technologies in the field. You provide personalized job search advice 
    and help candidates find opportunities that match their skills and career goals.""",
    tools=[search_data_engineer_jobs],
    llm=sonar_llm if sonar_llm else None,
    verbose=True,
    allow_delegation=False,
    max_iter=3
)

# Main app interface
st.title("💼 Data Engineer Job Hunter AI")
st.markdown("**Your AI assistant for finding the perfect data engineering job**")

# Sidebar with helpful information
st.sidebar.markdown("### 🔍 Search Tips")
st.sidebar.markdown("""
- Ask about specific technologies (Python, Spark, Kafka, etc.)
- Specify locations (remote, NYC, SF, etc.)
- Mention experience level (junior, senior, lead)
- Ask about salary ranges
- Inquire about specific companies
""")

st.sidebar.markdown("### 📝 Example Questions")
st.sidebar.markdown("""
- "Find remote Python data engineer jobs"
- "What are the salary ranges for senior data engineers in NYC?"
- "Show me data engineer jobs at FAANG companies"
- "Find entry-level data engineering positions"
""")

# Chat interface
st.markdown("### 💬 Chat with your Job Hunter")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_input := st.chat_input("Ask me about data engineer jobs..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate response
    with st.chat_message("assistant"):
        if not PERPLEXITY_API_KEY:
            response = "⚠️ Please enter your Perplexity API key in the sidebar to start searching for jobs."
            st.markdown(response)
        else:
            with st.spinner("🔍 Searching for the best data engineering opportunities..."):
                try:
                    # Create task for the agent
                    job_search_task = Task(
                        description=f"""
                        The user is asking: "{user_input}"
                        
                        Use your job search tool to find relevant data engineering positions and provide:
                        1. Specific job opportunities with details
                        2. Required skills and qualifications
                        3. Salary information (if available)
                        4. Application guidance
                        5. Market insights and trends
                        
                        Make your response helpful, detailed, and actionable.
                        """,
                        agent=data_engineer_job_agent,
                        expected_output="A comprehensive response about data engineering job opportunities based on the user's query"
                    )
                    
                    # Create and run crew
                    crew = Crew(
                        agents=[data_engineer_job_agent],
                        tasks=[job_search_task],
                        verbose=True
                    )
                    
                    result = crew.kickoff()
                    response = str(result)
                    
                except Exception as e:
                    response = f"❌ Sorry, I encountered an error while searching for jobs: {str(e)}"
            
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Additional features
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎯 Quick Actions")
    if st.button("🔍 Search Remote Jobs"):
        st.session_state.messages.append({"role": "user", "content": "Find remote data engineer jobs"})
        st.rerun()
    
    if st.button("💰 Salary Trends"):
        st.session_state.messages.append({"role": "user", "content": "What are the current salary trends for data engineers?"})
        st.rerun()
    
    if st.button("🏢 Top Companies"):
        st.session_state.messages.append({"role": "user", "content": "Which companies are actively hiring data engineers?"})
        st.rerun()

with col2:
    st.markdown("### 📊 Market Insights")
    if st.button("🔧 Hot Skills"):
        st.session_state.messages.append({"role": "user", "content": "What are the most in-demand skills for data engineers in 2025?"})
        st.rerun()
    
    if st.button("📍 Best Locations"):
        st.session_state.messages.append({"role": "user", "content": "What are the best locations for data engineer jobs?"})
        st.rerun()
    
    if st.button("🆕 Entry Level"):
        st.session_state.messages.append({"role": "user", "content": "Find entry-level data engineer positions for new graduates"})
        st.rerun()

# Clear chat button
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, Crew AI, and Perplexity Sonar API")

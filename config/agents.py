from crewai import Agent, LLM
from config.tools import analyze_cv_content, research_industry_trends, optimize_cv_keywords
from config.settings import AGENT_CONFIG, PERPLEXITY_BASE_URL, SONAR_MODEL

def create_llm_instance(api_key):
    """Create LLM instance for agents"""
    if api_key:
        return LLM(
            model=f"perplexity/{SONAR_MODEL}",
            api_key=api_key,
            base_url=PERPLEXITY_BASE_URL
        )
    return None

def create_cv_agents(api_key):
    """Create all CV enhancement agents"""
    sonar_llm = create_llm_instance(api_key)
    
    cv_analyst_agent = Agent(
        role="CV Analysis Expert",
        goal="Thoroughly analyze CV content and identify areas for improvement",
        backstory="""You are a senior HR professional with 15+ years of experience in talent acquisition. 
        You have reviewed thousands of CVs across various industries and know exactly what recruiters 
        and hiring managers look for. You provide detailed, constructive feedback to help job seekers 
        improve their CVs.""",
        tools=[analyze_cv_content],
        llm=sonar_llm,
        **AGENT_CONFIG
    )

    industry_researcher_agent = Agent(
        role="Industry Research Specialist",
        goal="Research current industry trends and requirements to inform CV improvements",
        backstory="""You are a market research analyst specializing in employment trends. 
        You stay updated on the latest industry developments, skill requirements, and hiring patterns. 
        You provide data-driven insights to help job seekers align their CVs with market demands.""",
        tools=[research_industry_trends],
        llm=sonar_llm,
        **AGENT_CONFIG
    )

    cv_optimizer_agent = Agent(
        role="CV Optimization Expert", 
        goal="Create optimized, ATS-friendly versions of CVs based on analysis and research",
        backstory="""You are a professional CV writer and career coach with expertise in ATS optimization. 
        You have helped hundreds of professionals land their dream jobs by crafting compelling, 
        keyword-optimized CVs. You know how to balance ATS requirements with human readability.""",
        tools=[optimize_cv_keywords],
        llm=sonar_llm,
        **AGENT_CONFIG
    )

    cv_writer_agent = Agent(
        role="Professional CV Writer",
        goal="Write improved CV versions incorporating all feedback and optimizations",
        backstory="""You are an expert CV writer with a background in professional writing and HR. 
        You excel at transforming analysis and recommendations into polished, professional CV content 
        that stands out to both ATS systems and human recruiters.""",
        llm=sonar_llm,
        **AGENT_CONFIG
    )
    
    return cv_analyst_agent, industry_researcher_agent, cv_optimizer_agent, cv_writer_agent

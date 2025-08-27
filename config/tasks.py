from crewai import Task

def create_cv_tasks(agents, cv_text, target_role, industry):
    """Create all CV enhancement tasks"""
    cv_analyst_agent, industry_researcher_agent, cv_optimizer_agent, cv_writer_agent = agents
    
    analysis_task = Task(
        description=f"""
        Analyze the following CV for a {target_role} position in the {industry} industry:
        
        {cv_text}
        
        Provide detailed analysis covering structure, content quality, strengths, 
        weaknesses, and specific improvement recommendations.
        """,
        agent=cv_analyst_agent,
        expected_output="Detailed CV analysis with specific improvement recommendations"
    )
    
    research_task = Task(
        description=f"""
        Research current trends and requirements for {target_role} positions 
        in the {industry} industry. Focus on in-demand skills, technologies, 
        and market requirements that should be reflected in the CV.
        """,
        agent=industry_researcher_agent,
        expected_output="Industry trends and requirements analysis"
    )
    
    optimization_task = Task(
        description=f"""
        Based on the CV analysis and industry research, optimize the CV for 
        ATS systems and {target_role} positions. Focus on keyword optimization, 
        skill highlighting, and content structure.
        
        Original CV:
        {cv_text}
        """,
        agent=cv_optimizer_agent,
        expected_output="ATS-optimized CV recommendations"
    )
    
    writing_task = Task(
        description=f"""
        Create an improved version of the CV incorporating all analysis, 
        research insights, and optimization recommendations. The improved CV should:
        1. Address all identified weaknesses
        2. Include relevant industry keywords
        3. Be ATS-friendly
        4. Maintain professional formatting
        5. Highlight achievements effectively
        
        Target role: {target_role}
        Industry: {industry}
        """,
        agent=cv_writer_agent,
        expected_output="Complete improved CV version"
    )
    
    return analysis_task, research_task, optimization_task, writing_task

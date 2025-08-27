import requests
from crewai.tools import tool
from config.settings import PERPLEXITY_BASE_URL, SONAR_MODEL, TOOL_CONFIG

@tool
def analyze_cv_content(cv_text: str, api_key: str = None) -> str:
    """
    Analyze CV content for strengths, weaknesses, and improvement opportunities
    """
    if not api_key:
        return "Please provide a Perplexity API key to analyze CV."
    
    url = f"{PERPLEXITY_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Analyze this CV/Resume and provide detailed feedback:
    
    CV Content:
    {cv_text}
    
    Please analyze:
    1. Overall structure and formatting
    2. Content quality and relevance
    3. Missing sections or information
    4. Strengths and achievements
    5. Areas for improvement
    6. ATS (Applicant Tracking System) compatibility
    7. Industry-specific recommendations
    
    Provide specific, actionable feedback.
    """
    
    payload = {
        "model": SONAR_MODEL,
        "messages": [
            {
                "role": "system", 
                "content": "You are an expert HR professional and career counselor specializing in CV/Resume analysis and improvement."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        **TOOL_CONFIG
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error analyzing CV: {str(e)}"

@tool
def research_industry_trends(industry: str, api_key: str = None) -> str:
    """
    Research current industry trends and required skills
    """
    if not api_key:
        return "Please provide a Perplexity API key to research trends."
    
    url = f"{PERPLEXITY_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Research current trends for {industry} industry in 2025:
    
    Please provide:
    1. Most in-demand skills and technologies
    2. Current salary trends
    3. Popular job titles and roles
    4. Emerging technologies and trends
    5. Certification and education requirements
    6. Key companies hiring in this field
    
    Focus on actionable insights for CV improvement.
    """
    
    payload = {
        "model": SONAR_MODEL,
        "messages": [
            {
                "role": "system", 
                "content": "You are an industry research specialist providing current market insights."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "max_tokens": 1500,
        "temperature": 0.2
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error researching industry trends: {str(e)}"

@tool
def optimize_cv_keywords(cv_text: str, target_role: str, api_key: str = None) -> str:
    """
    Optimize CV with relevant keywords for ATS systems
    """
    if not api_key:
        return "Please provide a Perplexity API key to optimize keywords."
    
    url = f"{PERPLEXITY_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Optimize this CV for the role: {target_role}
    
    Current CV:
    {cv_text}
    
    Please provide:
    1. Key ATS-friendly keywords to include
    2. Industry-specific terms and technologies
    3. Action verbs and achievement-focused language
    4. Skills section optimization
    5. Job description alignment suggestions
    
    Focus on maximizing ATS compatibility while maintaining readability.
    """
    
    payload = {
        "model": SONAR_MODEL,
        "messages": [
            {
                "role": "system", 
                "content": "You are an ATS optimization specialist helping improve CV keyword density and relevance."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "max_tokens": 1500,
        "temperature": 0.2
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error optimizing keywords: {str(e)}"

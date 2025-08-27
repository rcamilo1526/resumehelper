# Page configuration
PAGE_CONFIG = {
    "page_title": "CV Enhancement Multi-Agent System",
    "page_icon": "💼",
    "layout": "wide"
}

# API Configuration
PERPLEXITY_BASE_URL = "https://api.perplexity.ai"
SONAR_MODEL = "sonar"

# App Configuration
SUPPORTED_FILE_TYPES = ['pdf']
MAX_FILE_SIZE = 10  # MB

# Industry Options
INDUSTRY_OPTIONS = [
    "Technology", "Finance", "Healthcare", "Marketing", 
    "Education", "Manufacturing", "Consulting", "Retail", "Other"
]

# Agent Configuration
AGENT_CONFIG = {
    "max_iter": 3,
    "verbose": True,
    "allow_delegation": False
}

# Tool Configuration  
TOOL_CONFIG = {
    "max_tokens": 2000,
    "temperature": 0.3,
    "top_p": 0.9
}

# 📄 CV Enhancement Multi-Agent System

AI-powered CV optimization using CrewAI and Perplexity Sonar API.

## ✨ Features

- **4 AI Agents**: Analyst, Researcher, Optimizer, Writer
- **PDF/Text Upload**: Multiple input formats
- **Real-time Analysis**: Industry trends & ATS optimization
- **Professional Output**: Improved CV ready for download

## 🚀 Quick Start
```bash
git clone
cd resumehelper
pip install -r requirements.txt
streamlit run main.py
```
## 🔑 Setup

1. Get [Perplexity API key](https://www.perplexity.ai/settings/api)
2. Enter API key in the app sidebar
3. Upload CV and specify target role
4. Get your improved CV!

## 📁 Structure
```bash
resumehelper/
├── main.py              # Streamlit app
├── config/settings.py   # Configuration
├── config/agents.py     # AI agents
├── config/tools.py      # Custom tools
├── config/tasks.py      # Task definitions
└── utils/               # Utilities    
```

## 🛠️ Tech Stack

- **Streamlit** - Web interface
- **CrewAI** - Multi-agent framework
- **Perplexity Sonar** - Real-time AI analysis
- **PyPDF2** - PDF processing

---
**Transform your career, one CV at a time** 🚀
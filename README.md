# WebMaintX: AI-Powered Webpage Maintenance Agent

## Project Overview
WebMaintX is an autonomous AI agent designed to automate webpage maintenance tasks using Large Language Models (LLMs). This intelligent system independently analyzes webpages, identifies issues, and executes maintenance tasks with minimal human intervention, making it ideal for large-scale deployment across dynamic websites.

## Core Capabilities
- **Content Updates**: Automatically detects outdated information and updates it using data from connected APIs or databases.
- **SEO Optimization**: Enhances webpage metadata, keywords, and structure to improve search engine rankings.
- **Error Fixing**: Identifies and repairs broken links, incorrect formatting, and other technical issues.
- **Content Generation**: Creates missing sections or suggests improvements for existing content.
- **Performance Monitoring**: Regularly analyzes webpage performance metrics and suggests actionable improvements.

## Technical Architecture
- **LLM Foundation**: Utilizes open-source models (Meta Llama 3.3, DeepSeek-R1) for reasoning and analysis.
- **Cyclical Reasoning**: Implements LangGraph for iterative analysis-plan-execute-verify workflows.
- **MCP Integration**: Uses Model Context Protocol for secure API and database interactions.
- **Web Analysis Tools**: Combines Selenium and BeautifulSoup for comprehensive webpage analysis.
- **Page Object Model**: Adapts the Page Object pattern for structured webpage element manipulation.

## Key Features
- **Semantic Understanding**: Comprehends webpage content context rather than relying on simple pattern matching.
- **Recursive Updates**: Changes to one element trigger evaluation of related elements for consistency.
- **Multi-LLM Architecture**: Employs specialized model variants optimized for different maintenance tasks.
- **Human-in-the-Loop Integration**: Optional verification workflows for sensitive content updates.
- **Adaptive Learning**: Improves maintenance decisions through reinforcement learning from past changes.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/webmaintx.git
   ```
2. Navigate to the project directory:
   ```bash
   cd webmaintx
   ```
3. Create a virtual environment and activate it:
   ```bash
   python -m venv webagent-env
   source webagent-env/bin/activate  # On Windows: webagent-env\Scripts\activate
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Configure your settings in `config.yaml`:
   ```bash
   cp config.example.yaml config.yaml
   nano config.yaml  # Edit with your settings
   ```
2. Run the agent:
   ```bash
   python main.py --url https://example.com
   ```
3. For batch processing multiple pages:
   ```bash
   python batch_processor.py --sitemap https://example.com/sitemap.xml
   ```

## Testing
- A dummy website is included in the `test_website/` directory for testing purposes.
- Run the test suite:
  ```bash
  python -m pytest tests/
  ```
- Test on the dummy website:
  ```bash
  python test_agent.py --website test_website/
  ```

## Project Structure
```
webmaintx/
├── main.py                    # Main entry point
├── config.yaml                # Configuration file
├── requirements.txt           # Dependencies
├── README.md                  # Documentation
├── agent/                     # Agent core components
│   ├── __init__.py
│   ├── llm_provider.py        # LLM integration
│   ├── workflow.py            # LangGraph workflow
│   └── mcp_adapters.py        # MCP protocol adapters
├── analysis/                  # Webpage analysis tools
│   ├── __init__.py
│   ├── scraper.py             # Web scraping utilities
│   ├── seo_analyzer.py        # SEO analysis tools
│   └── content_analyzer.py    # Content analysis tools
├── actions/                   # Maintenance actions
│   ├── __init__.py
│   ├── content_updater.py     # Content update logic
│   ├── link_fixer.py          # Link repair utilities
│   └── performance_monitor.py # Performance monitoring
└── test_website/              # Dummy website for testing
```

## Contributing
Contributions are welcome! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- This project was developed for the Agent-X competition at Cognizance, IIT Roorkee.
- Special thanks to the open-source communities behind LangChain, LangGraph, and other tools used in this project.

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/12141938/a1aee48e-edf3-4de5-8cd8-28333f9c3379/Agent-X-25.docx-1.pdf

---

## Setup

1. Create a virtual environment:
```bash
python -m venv webagent-env
source webagent-env/bin/activate  # On Windows: webagent-env\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following variables:
```
LLM_MODEL_ID=meta-llama/Llama-3
API_KEY=your_api_key
```

## Usage

Run the agent:
```bash
python main.py
```

## Testing

Run tests:
```bash
python -m pytest tests/
```

## Monitoring

Access the Prometheus metrics at `http://localhost:8000/metrics`
View Grafana dashboard at `http://localhost:3000`

## License

MIT License 
# Web Crawler + Research Assistant 🌐

An intelligent research assistant powered by CrewAI that combines web scraping, internet research, and automated report generation to help users gather and analyze information efficiently.

<img width="743" alt="Screenshot 2025-04-28 at 10 14 01 PM" src="https://github.com/user-attachments/assets/b64b076c-a7c1-4dc9-b2ac-cbeeafb07331" />

## Features 🚀

- **Web Scraping**: Extracts content from any specified website URL
- **Smart Internet Research**: Performs targeted searches using the Brave Search API
- **Automated Report Generation**: Combines findings into well-structured reports
- **User-Friendly Interface**: Built with Streamlit for easy interaction
- **Downloadable Results**: Export reports in text format

## Technology Stack 🛠️

- **CrewAI**: For orchestrating AI agents
- **Streamlit**: Web interface framework
- **Python 3.x**: Core programming language
- **Brave Search API**: For internet research
- **GPT-3.5 Turbo**: Language model for content processing

## Installation 📦

1. Clone the repository:
```bash
git clone https://github.com/yourusername/web-crawler-research-assistant.git
cd web-crawler-research-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure API keys:
Create `.streamlit/secrets.toml` file (not tracked in git) with your API keys:
```toml
# API Keys Configuration
BRAVE_API_KEY = "your_brave_api_key"
OPENAI_API_KEY = "your_openai_api_key"
```

> **Note**: The `.streamlit/secrets.toml` file is automatically excluded from git to protect your API keys. Never commit sensitive credentials to version control.

## Usage 💻

1. Start the application:
```bash
streamlit run crewai.py
```

2. Access the web interface at `http://localhost:8501`

3. Enter:
   - Website URL to scrape
   - Research question to investigate

4. Click "Generate Report" and wait for the results

## How It Works 🔄

1. **Web Scraping Agent**
   - Crawls the specified website
   - Extracts relevant content
   - Summarizes key findings

2. **Research Agent**
   - Performs Brave searches
   - Analyzes top 5 results
   - Synthesizes information

3. **Writer Agent**
   - Combines scraped and researched data
   - Generates structured report
   - Saves output to file

## Project Structure 📁

```
.
├── crewai.py          # Main application file
├── requirements.txt    # Project dependencies
├── .streamlit               # Environment variables
    └── secrets.toml
└── outputs/           # Generated reports directory
    └── final_report.txt
```

## Configuration ⚙️

- **Brave Search**: Limited to top 5 US-based results
- **Report Format**: Plain text (.txt)
- **Process Flow**: Sequential execution of tasks
- **Language Model**: GPT-3.5 Turbo

## Limitations 🚧

- Currently only supports text-based reports
- Limited to single URL scraping per session
- Requires active internet connection
- API rate limits may apply

## Contributing 🤝

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 👏

- CrewAI team for the framework
- Brave Search for the API
- OpenAI for GPT-3.5 Turbo
- Streamlit for the UI framework

## Support 🆘

For support, please open an issue in the GitHub repository or contact the maintainers.

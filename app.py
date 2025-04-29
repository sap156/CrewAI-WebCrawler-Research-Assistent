import os
import streamlit as st
from dotenv import load_dotenv
from app import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool, BraveSearchTool, FileWriterTool

# Initialize environment variables for API keys and configurations
load_dotenv()

# Initialize core tools with default settings
# Brave Search tool configured for US-based results with limited output
brave_search_tool = BraveSearchTool(
    country="US",
    n_results=5,  # Limit to top 5 results for conciseness
    save_file=False  # Don't save intermediate search results
)

# Tool for writing the final report to disk
file_writer_tool = FileWriterTool()

def create_dynamic_crewai_setup(website_url, research_question):
    """
    Creates a dynamic CrewAI workflow setup based on user inputs.
    
    Args:
        website_url (str): The target URL for web scraping
        research_question (str): The research topic to investigate
        
    Returns:
        Crew: Configured CrewAI instance with agents and tasks
    """
    # Initialize web scraper with user-provided URL
    scraper_tool = ScrapeWebsiteTool(website_url=website_url)

    # Define specialized AI agents
    scraper_agent = Agent(
        role="Web Scraper",
        goal="Scrape the provided website and extract key readable content.",
        backstory="Expert in crawling websites and extracting valuable information.",
        tools=[scraper_tool],
        verbose=True,  # Enable detailed logging
        allow_delegation=False,  # Agent works independently
        LLM="gpt-3.5-turbo"
    )

    search_agent = Agent(
        role="Internet Researcher",
        goal="Search for updated information related to the user's research question.",
        backstory="Expert at finding current data through web search.",
        tools=[brave_search_tool],
        verbose=True,
        allow_delegation=False,
        LLM="gpt-3.5-turbo"
    )

    writer_agent = Agent(
        role="Report Writer",
        goal="Organize the scraped and searched information into a clean report and save it.",
        backstory="Professional at writing neat, structured reports for business and technical users.",
        tools=[file_writer_tool],
        verbose=True,
        allow_delegation=False,
        LLM="gpt-3.5-turbo"
    )

    # Define sequential tasks for the workflow
    scrape_task = Task(
        description="Scrape the given website and summarize the key findings.",
        expected_output="Summary of important content extracted from the website.",
        agent=scraper_agent,
        LLM="gpt-3.5-turbo"
    )

    search_task = Task(
        description=f"Search for '{research_question}' on the internet using Brave and summarize the top 5 results.",
        expected_output="Summary of latest web information related to the research question.",
        agent=search_agent,
        LLM="gpt-3.5-turbo"
    )

    write_task = Task(
        description=f"""Combine the outputs from the website scraping and Brave search into a single report.
Save it as 'outputs/final_report.txt'.""",
        expected_output="Confirmation that 'final_report.txt' has been successfully saved.",
        agent=writer_agent,
        LLM="gpt-3.5-turbo"
    )

    # Create and configure the CrewAI workflow
    crew = Crew(
        agents=[scraper_agent, search_agent, writer_agent],
        tasks=[scrape_task, search_task, write_task],
        process=Process.sequential,  # Execute tasks in order
        verbose=True,  # Enable detailed logging
        LLM="gpt-3.5-turbo"
    )

    return crew

# Streamlit UI Configuration and Layout
st.set_page_config(
    page_title="🌐 Web Crawler + Research Assistant",
    layout="centered" 
)

st.title("🌐 Web Crawler + Research Assistant")

# Application description and instructions
st.markdown("""
This app scrapes any website you provide, searches related information on the internet using Brave,  
and generates a final report for you! 📄
""")

# User input form with default values
with st.form("scrape_search_form"):
    website_url = st.text_input(
        "🔗 Enter Website URL to Scrape:",
        value="https://techcrunch.com/startups/"  # Default URL for demonstration
    )
    research_question = st.text_input(
        "❓ Enter a Research Question:",
        value="Latest startup funding news"  # Default research topic
    )
    submitted = st.form_submit_button("Generate Report 🚀")

# Main execution logic
if submitted:
    # Input validation
    if not website_url or not research_question:
        st.error("Please provide both Website URL and Research Question!")
    else:
        # Progress indicator
        st.info("🚀 Running Web Scraping + Brave Search... Please wait...")

        # Initialize and execute CrewAI workflow
        dynamic_crew = create_dynamic_crewai_setup(website_url, research_question)
        result = dynamic_crew.kickoff()

        st.success("✅ Report generated successfully!")

        # Display execution results
        st.header("📋 Crew Execution Output:")
        st.write(result)

        # Load and display the generated report
        try:
            with open("outputs/final_report.txt", "r", encoding="utf-8") as f:
                report_content = f.read()

            st.header("📄 Final Report Content:")
            # Display report in scrollable text area
            st.text_area("Final Report", value=report_content, height=400)

            # Add download functionality for the report
            st.download_button(
                label="📥 Download Report",
                data=report_content,
                file_name="final_report.md",
                mime="text/plain"
            )
        except FileNotFoundError:
            st.error("Report file not found!")


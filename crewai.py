# app.py

import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool, BraveSearchTool, FileWriterTool

# ✅ Load environment variables
load_dotenv()

# ✅ Initialize Tools (but scraper will be re-created dynamically based on user input)
brave_search_tool = BraveSearchTool(
    country="US",
    n_results=5,
    save_file=False
)

file_writer_tool = FileWriterTool()

# ✅ Function to dynamically create Crew based on user input
def create_dynamic_crewai_setup(website_url, research_question):
    # Create a fresh Scrape tool based on user URL
    scraper_tool = ScrapeWebsiteTool(website_url=website_url)

    # Agents
    scraper_agent = Agent(
        role="Web Scraper",
        goal="Scrape the provided website and extract key readable content.",
        backstory="Expert in crawling websites and extracting valuable information.",
        tools=[scraper_tool],
        verbose=True,
        allow_delegation=False,
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

    # Tasks
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

    # Create Crew
    crew = Crew(
        agents=[scraper_agent, search_agent, writer_agent],
        tasks=[scrape_task, search_task, write_task],
        process=Process.sequential,
        verbose=True,
        LLM="gpt-3.5-turbo"
    )

    return crew

# ✅ Streamlit App

st.set_page_config(page_title="🌐 Web Crawler + Research Assistant", layout="centered")

st.title("🌐 Web Crawler + Research Assistant")

st.markdown("""
This app scrapes any website you provide, searches related information on the internet using Brave,  
and generates a final report for you! 📄
""")

with st.form("scrape_search_form"):
    website_url = st.text_input("🔗 Enter Website URL to Scrape:", value="https://techcrunch.com/startups/")
    research_question = st.text_input("❓ Enter a Research Question:", value="Latest startup funding news")
    submitted = st.form_submit_button("Generate Report 🚀")

if submitted:
    if not website_url or not research_question:
        st.error("Please provide both Website URL and Research Question!")
    else:
        st.info("🚀 Running Web Scraping + Brave Search... Please wait...")

        # Create crew dynamically
        dynamic_crew = create_dynamic_crewai_setup(website_url, research_question)

        # Run Crew
        result = dynamic_crew.kickoff()

        st.success("✅ Report generated successfully!")

        # Show result
        st.header("📋 Crew Execution Output:")
        st.write(result)


        # Read and display the saved report
        try:
            with open("outputs/final_report.txt", "r", encoding="utf-8") as f:
                report_content = f.read()

            st.header("📄 Final Report Content:")
            st.text_area("Final Report", value=report_content, height=400)

            # Download button
            st.download_button(
                label="📥 Download Report",
                data=report_content,
                file_name="final_report.txt",
                mime="text/plain"
            )
        except FileNotFoundError:
            st.error("Report file not found!")


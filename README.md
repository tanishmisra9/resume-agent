# Resume Agent

**Resume Agent** is a Python tool that automates resume parsing, job posting analysis, and AI-driven tailoring suggestions.  
It uses LangChain and OpenAI's GPT-5-mini model to provide line-specific and big-picture feedback that helps candidates optimize their resumes for specific job postings.

---

## Features

- **Resume Parsing**: Extracts and cleans text from PDF resumes.  
- **Job Posting Scraper**: Scrapes URLs and uses **zero-shot classification** with the **Facebook BART-Large-MNLI** model to filter complex HTML job data into relevant content.  
  This reduces irrelevant text and **minimizes AI token usage by up to 80%** — compressing 600+ lines of HTML into roughly 100 lines of meaningful job text.  
- **Resume Tailoring**: Generates actionable, line-specific, and big-picture resume edits aligned with the job description.  
- **Command-Line Interface**: Run all components seamlessly from the terminal.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tanishmisra9/resume-agent.git
   cd resume-agent

2. Create and activate a virtual environment:
    '''bash
    python3 -m venv venv
    source venv/bin/activate

3. Install dependencies
    '''bash
    pip install -r requirements.txt

4. Add your OpenAI API key to a .env file:
    '''bash
    OPENAI_API_KEY=your_api_key_here

## Tech Stack

- **Python 3.12.2+**
- **LangChain** – Framework for orchestrating LLM workflows  
- **LangGraph** – Lightweight graph-based runtime for LangChain agents  
- **OpenAI GPT-5-mini** – Core LLM for generating tailored resume suggestions  
- **Transformers (Facebook BART-Large-MNLI)** – Used for zero-shot classification to filter job posting text  
- **BeautifulSoup4** – Cleans and parses raw HTML from job pages  
- **PyPDF** – Extracts and processes text from resume PDFs  
- **dotenv** – Manages environment variables securely  
- **Requests** – Handles HTTP requests for scraping job data  
- **Regex** – For text cleanup and sentence segmentation
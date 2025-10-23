"""
interactive_resume_agent.py

Interactive terminal workflow:
1. Parse a resume PDF.
2. Fetch and filter a job posting.
3. Tailor the resume with GPT-5 mini suggestions using LangChain.
"""

import subprocess
import time
from pathlib import Path
from resume_tailor import tailor_resume

# Paths
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
PARSED_RESUME_PATH = DATA_DIR / "parsed_resume.txt"
FILTERED_JOB_PATH = DATA_DIR / "filtered.txt"
SUGGESTIONS_PATH = DATA_DIR / "resume_suggestions.txt"


def main():
    # Step 1: Resume parsing
    resume_file = input("Enter the name of your resume PDF file in 'data/' (e.g., test.pdf): ").strip()

    try:
        subprocess.run(
            ["python3", "src/resume_parser.py", resume_file],
            check=True
        )
        print(f"Parsed resume saved to: {PARSED_RESUME_PATH}")
    except subprocess.CalledProcessError as e:
        print("Error parsing resume:", e)
        return

    # Step 2: Job posting fetch & filter
    job_url = input("Enter the job posting URL: ").strip()

    try:
        subprocess.run(
            ["python3", "src/job_fetcher.py", job_url],
            check=True
        )
        print(f"Job posting fetched and filtered: {FILTERED_JOB_PATH}")
    except subprocess.CalledProcessError as e:
        print("Error fetching job posting:", e)
        return

    # Step 3: Call resume_tailor with timer
    with open(PARSED_RESUME_PATH, "r", encoding="utf-8") as f:
        resume_text = f.read()

    with open(FILTERED_JOB_PATH, "r", encoding="utf-8") as f:
        job_text = f.read()

    print("Contacting GPT-5 mini for tailoring suggestions...")
    start_time = time.time()
    suggestions = tailor_resume(resume_text, job_text)
    elapsed = time.time() - start_time
    print(f"Agent request completed in {elapsed:.2f} seconds.")

    if not suggestions.strip():
        print("Warning: Tailoring suggestions returned empty. Please check your API key and network.")
    else:
        # Save suggestions
        with open(SUGGESTIONS_PATH, "w", encoding="utf-8") as f:
            f.write(suggestions)
        print(f"Tailoring suggestions saved to {SUGGESTIONS_PATH}")

    print("Workflow complete! Review the suggestions and update your resume accordingly.")


if __name__ == "__main__":
    main()

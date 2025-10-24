"""
job_fetcher.py

Scrape a job posting URL, extract all visible text (no empty lines),
classify and filter relevant sentences, and save the output to data/filtered.txt.
"""

import warnings
import requests
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup
from time import time
from transformers import pipeline

# ---- Suppress warnings globally ----
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("torch").setLevel(logging.ERROR)

# ---- Directories ----
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# ---- Classifier setup ----
# Using a stable zero-shot classification model
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

def scrape_posting(url: str) -> str:
    """Scrape HTML text from a job posting and clean whitespace."""
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text(separator="\n")
    text = re.sub(r"[ \t]+", " ", text)

    # lines = [line.strip() for line in text.splitlines() if line.strip()]
    lines = [line.strip() for line in text.splitlines() if line.strip() and len(line.strip().split()) > 2]
    
    cleaned_text = "\n".join(lines)
    return cleaned_text

def filter_job_text(text: str) -> str:
    """Use zero-shot classification to filter for relevant internship or job content across industries."""
    candidate_labels = [
        "internship description",
        "job description",
        "company hiring information",
        "recruitment posting",
        "career opportunity",
        "unrelated text"
    ]

    sentences = re.split(r"(?<=[.!?])\s+", text)
    filtered_sentences = []

    for sent in sentences:
        if len(sent.split()) < 5:
            continue
        result = classifier(sent, candidate_labels)
        top_label = result["labels"][0]
        if top_label != "unrelated text" and result["scores"][0] > 0.3:
            filtered_sentences.append(sent.strip())

    return "\n".join(filtered_sentences)

# ---- Main execution ----
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 src/job_fetcher.py <job_posting_url>")
        sys.exit(1)

    url = sys.argv[1]
    start_time = time()

    try:
        print("Scraping your URL...")
        cleaned_text = scrape_posting(url)
        print("Filtering HTML text...")
        filtered_text = filter_job_text(cleaned_text)
    except Exception as e:
        print("Error scraping or classifying job posting:", e)
        sys.exit(1)

    output_file = DATA_DIR / "filtered.txt"
    output_file.write_text(filtered_text, encoding="utf-8")

    elapsed = time() - start_time
    print(f"Filtered job posting saved to: {output_file}")
    print(f"Time elapsed: {elapsed:.2f} seconds")
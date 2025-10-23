"""
resume_parser.py

Extracts and cleans text from PDF resumes. Can be extended for additional file types later.
Provides a command-line interface for specifying which resume PDF to parse.
"""

import logging
from pathlib import Path
from pypdf import PdfReader
import argparse
import re

# suppress pypdf warnings for malformed objects
logging.getLogger("pypdf").setLevel(logging.ERROR)

def clean_text(raw_text: str) -> str:
    """
    Cleans resume text, stripping extra whitespaces and
    removing multiple consecutive blank lines.
    
    Args:
        raw_text (str): Raw text extracted from PDF.

    Returns:
        str: Cleaned, normalized text.
    """
    # remove leading / trailing whitespace
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    
    # replace 2 or more consecutive spaces with a single tab
    # {2,} means “2 or more” of the whitespace character
    lines = [re.sub(r' {2,}', '\t', line) for line in lines]

    # join lines and replace multiple consecutive newlines
    cleaned_text = "\n".join(lines)
    
    cleaned_text = re.sub(r'\n{2,}', '\n', cleaned_text) 
    
    return cleaned_text

def parse_resume(file_path: str) -> str:
    """
    Extracts text from a PDF resume and returns cleaned text.

    Args:
        file_path (str): Path to the PDF resume file.

    Returns:
        str: The cleaned text of the resume.
    """
    reader = PdfReader(file_path)
    all_text = []

    for page in reader.pages:
        raw_text = page.extract_text()
        if raw_text:
            all_text.append(raw_text)

    combined_text = "\n".join(all_text)

    reader.close()

    return clean_text(combined_text)

# CLI for running from terminal
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse and clean a resume PDF.")
    parser.add_argument("filename", type=str, help="Name of the PDF file in the data/ directory")
    args = parser.parse_args()

    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    pdf_path = DATA_DIR / args.filename

    if not pdf_path.exists():
        print(f"Error: File {args.filename} not found in {DATA_DIR}")
        exit(1)

    resume_text = parse_resume(pdf_path)

    output_file = DATA_DIR / "parsed_resume.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(resume_text)

    print("Parsed resume saved to:", output_file)
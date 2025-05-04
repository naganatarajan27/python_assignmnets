import sys
import re
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_chapter_questions(text, chapter_name):
    # Normalize chapter name for regex
    chapter_pattern = re.escape(chapter_name.strip())
    chapter_regex = rf"(Chapter \d+: {chapter_pattern})(.*?)(?=Chapter \d+:|\Z)"  # Match until next chapter or end
    match = re.search(chapter_regex, text, re.DOTALL | re.IGNORECASE)
    
    if not match:
        return None

    chapter_content = match.group(2)

    # Extract questions (starting with number. e.g., 1. What...)
    question_regex = r"\d+\.\s.*?(?=\n\d+\.|\Z)"
    questions = re.findall(question_regex, chapter_content, re.DOTALL)
    return [q.strip() for q in questions]

def main():
    if len(sys.argv) < 2:
        print("❌ Error: Chapter name must be provided as a command line argument.")
        return

    chapter_name = sys.argv[1].strip()
    if not chapter_name:
        print("❌ Error: Chapter name cannot be empty.")
        return

    pdf_path = "/Users/naganatarajan/Desktop/GEN_AI_Tasks/my_python_tasks/content/Chemistry Questions.pdf"
    try:
        text = extract_text_from_pdf(pdf_path)
        questions = extract_chapter_questions(text, chapter_name)

        if not questions:
            print(f"❌ No questions found for chapter: '{chapter_name}'")
        else:
            print(f"✅ Questions from '{chapter_name}':\n")
            for q in questions:
                print(q + "\n")

    except Exception as e:
        print(f"❌ Error reading PDF: {e}")

if __name__ == "__main__":
    main()
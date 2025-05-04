import os
import pandas as pd
import re
import json
from sqlalchemy import create_engine
from PyPDF2 import PdfReader

# ---------- CONFIG ----------
folder = "/Users/naganatarajan/Desktop/GEN_AI_Tasks/my_python_tasks/content/" 
config_path = os.path.join(folder, "config.json")
PDF_PATH = os.path.join(folder,"Chemistry Questions.pdf")
MYSQL_URI = "mysql+pymysql://root:admin1234@localhost:3306/natarajan_main"  # Update credentials

# ---------- LOAD CONFIG ----------
def load_config(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f" Failed to load config: {e}")
        return {}


# ---------- PDF TO TEXT ----------
def extract_text(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

# ---------- PARSE QUESTIONS ----------
def extract_questions(text, pattern):
    questions = []
    chapters = re.split(r"(Chapter\s+\d+:\s+.*?)\n", text)
    subject = "Chemistry"

    for i in range(1, len(chapters), 2):
        chapter = chapters[i].strip()
        body = chapters[i + 1]

        for match in re.finditer(pattern, body, re.DOTALL):
            block = match.group(1).strip()
            lines = block.split("\n")
            question_text = lines[0].strip()
            options = {l[0]: l[3:].strip() for l in lines[1:5] if len(l) > 3}
            #correct_letter = re.search(r"Answer:\s+([A-D])", block).group(1)
            #correct_text = options.get(correct_letter, "")

            questions.append({
                "Subject_Name": subject,
                "Chapter_Name": chapter,
                "Question_Text": question_text,
                "Answer_option_A": options.get('A', ''),
                "Answer_option_B": options.get('B', ''),
                "Answer_option_C": options.get('C', ''),
                "Answer_option_D": options.get('D', '')
                #"correct_answer": correct_text
            })

    return pd.DataFrame(questions)

# ---------- WRITE TO MYSQL ----------
def write_to_db(df):
    try:
        engine = create_engine(MYSQL_URI)
        with engine.connect() as conn:
            df.to_sql(name='Questions_Table', con=conn, if_exists='append', index=False)
        print(f" {len(df)} questions inserted into MySQL.")
    except Exception as e:
        print(f" Error writing to DB: {e}")

# ---------- MAIN ----------
def main():
    config = load_config(config_path)
    text = extract_text(PDF_PATH)
    df = extract_questions(text, config["question_regex"])
    print(df.head())  # Preview first few rows
    write_to_db(df)

if __name__ == "__main__":
    main()
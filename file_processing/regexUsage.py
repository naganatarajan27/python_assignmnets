import os
import json
import re
import PyPDF2

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config.get("regex", "")

def extract_matching_text_from_pdf(pdf_path, pattern):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            matches = []
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    found = re.findall(pattern, page_text)
                    matches.extend(found)
            return "\n".join(matches)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

def process_folder_with_regex(folder_path, regex_pattern):
    output = ""
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            matched_text = extract_matching_text_from_pdf(pdf_path, regex_pattern)
            if matched_text:
                output += f"From {filename}:\n{matched_text}\n\n"
    if output:
        output_path = os.path.join(folder_path, "output.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✔ Matched content written to {output_path}")

def get_all_subfolders(main_folder):
    return [os.path.join(root, d)
            for root, dirs, _ in os.walk(main_folder)
            for d in dirs]
def main():

    folder = "/Users/naganatarajan/Desktop/GEN_AI_Tasks/my_python_tasks/content/" 
    config_path = os.path.join(folder, "config.json")
    regex_pattern = load_config(config_path)

    print(f"🔍 Using regex: {regex_pattern}")

    subfolders = get_all_subfolders(folder)
    for folder in subfolders:
        process_folder_with_regex(folder, regex_pattern)
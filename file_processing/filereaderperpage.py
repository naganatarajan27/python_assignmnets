import os
import PyPDF2

def read_pdf_from_folder_based_page_number(folder_path, filename, pagenumber):
    file_path = os.path.join(folder_path, filename)

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num, page in enumerate(reader.pages):
            if page_num + 1 == pagenumber:
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page.extract_text() or "[No text found]"
        return text
    
## ----- Write content to a text file ----- ##
def write_to_text_file(text, output_file, output_folder):
    ## ----- Store this file under the “/content” folder ----- ##
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, output_file)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)
        ## ----- Take care of case where the output.txt file is not available ----- ##
        if not os.path.exists(output_path):
            print(f"Failed !!! File not found: {output_path}")
            return
        else:
             print(f"Success !!! Content written to {output_path}")

def main():
    folder = "/Users/naganatarajan/Desktop/GEN_AI_Tasks/my_python_tasks/content/"  # Change this to your folder path
    pdf_file = "Chemistry Questions.pdf"        # Change this to your PDF file name
    output_file="output.txt"
    output_folder = "/Users/naganatarajan/Desktop/GEN_AI_Tasks/my_python_tasks/content/Project_3_output"  # Change this to your output folder path
    pagenumber = 1
    content = read_pdf_from_folder_based_page_number(folder, pdf_file,pagenumber)
    if content:
        write_to_text_file(content,output_file,output_folder)
    else:
        print(f"Failed !!! No Content Found: {content}")

if __name__ == "__main__":
    main()
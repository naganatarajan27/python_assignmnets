import os
import pandas as pd
import re
import json
from sqlalchemy import create_engine
from PyPDF2 import PdfReader

# ---------- CONFIG ----------
MYSQL_URI = "mysql+pymysql://root:admin1234@localhost:3306/natarajan_main"  # Update credentials



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
    subject_name = input("Enter the Subject Name: ")
    chapter_name = input("Enter the Chapter Name: ")
    question = input("Enter the Question: ")
    answer_option_a = input("Enter Answer Option A: ")
    answer_option_b = input("Enter Answer Option B: ")
    answer_option_c = input("Enter Answer Option C: ")
    answer_option_d = input("Enter Answer Option D: ")
    df = pd.DataFrame({
        "Question_Text": [question],
        "Answer_option_A": [answer_option_a],
        "Answer_option_B": [answer_option_b],
        "Answer_option_C": [answer_option_c],
        "Answer_option_D": [answer_option_d]
    })
    df['Chapter_Name'] = chapter_name
    df['Subject_Name'] = subject_name
    print(df.head())  # Preview first few rows
    write_to_db(df)

if __name__ == "__main__":
    main()
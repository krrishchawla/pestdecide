from tenacity import retry, stop_after_attempt, wait_random_exponential
from llm import GPT4QAModel
from PyPDF2 import PdfReader
from prompt import get_prompt
import numpy as np
import os
import json
from json.decoder import JSONDecodeError
from tqdm import tqdm
from PyPDF2.errors import PdfReadError


def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()
    return pdf_text


def make_summary_from_pdf(pdf_file):
    model = GPT4QAModel()
    pdf = extract_text_from_pdf(pdf_file)
    seed = get_prompt(pdf_text=pdf)
    response = model.answer_question(seed)
    return response


def populate_summaries():
    list_of_files = os.listdir('./pdfs')

    for file in tqdm(list_of_files, desc="Processing files"):
        if file == '.DS_Store':
            continue

        output_path = f'./summaries/{file.replace(".pdf", ".json")}'
        # Skip processing if the output file already exists
        # if os.path.exists(output_path):
        #     continue
        out_file = file.replace('.pdf', '.json')

        if out_file in os.listdir('./summaries'):
            continue

        pdf_path = f'./pdfs/{file}'

        try:
            llm_response = make_summary_from_pdf(pdf_path)
            print(llm_response)
            if llm_response is not None:
                try:
                    data = json.loads(llm_response)
                    with open(output_path, 'w') as f:
                        json.dump(data, f)
                except JSONDecodeError as e:
                    print(f"JSONDecodeError for file {file}: {e}")
        except PdfReadError as e:
            print(f"PdfReadError for file {file}: {e}")


def list_pests_with_banned_regions():
    files_with_ban_info = []

    for file in os.listdir('./summaries'):
        if file.endswith('.json'):
            file_path = os.path.join('./summaries', file)

            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    # Check if the key exists and is not an empty string
                    if data.get("Is this product banned in any region?", "") != "":
                        files_with_ban_info.append(file)
            except json.JSONDecodeError as e:
                print(f"Error reading JSON from file {file}: {e}")

    print(files_with_ban_info)


def main():
    # model = GPT4QAModel()
    # pdf = extract_text_from_pdf('./pdfs/121-34.pdf')
    # seed = get_prompt(pdf_text=pdf)
    # response = model.answer_question(seed)
    # print(response)
    # populate_summaries()
    lst = os.listdir('./summaries')
    for ls in lst:
        print(ls.replace('.json', ''))

    

if __name__ == "__main__":
    main()

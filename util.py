from tenacity import retry, stop_after_attempt, wait_random_exponential
from llm import GPT4QAModel
from PyPDF2 import PdfReader


def generate_cover(resume, job_description):
    # Your email generation logic here
    model = GPT4QAModel()
    prompt = get_prompt(resume, job_description)
    response = model.answer_question(prompt)
    return response


def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()
    return pdf_text


def main():
    model = GPT4QAModel()
    prompt = "hello world"
    response = model.answer_question(prompt)
    print(response)

if __name__ == "__main__":
    main()

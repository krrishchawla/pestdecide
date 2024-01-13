import openai
from tenacity import retry, stop_after_attempt, wait_random_exponential
import os

GPT3 = "gpt-3.5-turbo"
GPT4 = "gpt-4"
GPT4_turbo = 'gpt-4-1106-preview'

class GPT4QAModel():
    def __init__(self, model=GPT4):
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        self.model = model

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def _attempt_answer_question(self, question, max_tokens=2000, stop_sequence=None):
        response = openai.ChatCompletion.create(
          model=self.model,
          messages=[
                {"role": "system", "content": "You are Question Answering Portal"},
                {"role": "user", "content": question}
            ],
          temperature=0
        )
        
        return response["choices"][0]['message']['content'].strip()


    @retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(6))
    def answer_question(self, question, max_tokens=3000, stop_sequence=None):

        try:
            return self. _attempt_answer_question(question, max_tokens=max_tokens, stop_sequence=stop_sequence)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    pass
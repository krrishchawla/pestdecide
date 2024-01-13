def question_list():
    lst = [
        "What crops is this useful for?",
        "First aid information?",
        "What special restrictions are placed on this product to protect the environment?",
        "What PPE should I wear?",
        "How, where, and on what crop should I use the product? How much is okay?",
        "How does the product have to be stored or disposed?",
        "Is this product banned in any region?"
        ]
    
    
    return lst


def get_prompt(pdf_text):
    lst = question_list()
    seed = f'''
        You are an assistant that is summarizing information about the pesticide provided below. 
        The text has several details about the pesticide use.

        I am providing you with a list of questions. I need answers for each of those questions within 100 words.

        I want you to output a JSON file, with the questions I provide as keys, and the answers you find as values to those keys.

        If no relevant answer exists, add an empty string for that question key.

        Do not hallucinate, only answer based on the text I provide. Please be accurate, this is very important. 

        Here is the list of questions: {lst}

        Here is the information you need to find answers in:
        {pdf_text}
        '''
    return seed
    




def get_prompt(pdf_text):
    table = output_table()
    seed = f'''
        You are an assitant to summarize and collect information.
        I have some text with information from which I need to filter out specific details from.
        The details are stores as keys in the following python dictionary, I want you to populate 
        the dictionary with values that you find in the text for the specific key. Format it as a python
        dictionary.

        Here is the output format dictionary: {table}

        Here is the information:
        {pdf_text}
        '''
    
def output_table():
    table = {'': None,
             
             
            }
    return table

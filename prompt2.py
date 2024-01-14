import json

def question_list():
    lst = [
        "Pros",
        "Cons",
        "Valid Crop",
        "Valid Location"
        ]
    return lst


def add_summary(user_inputted_pest, topK):
    info = {}
    # Load data from epa_regno_info.json
    with open('epa_regno_info.json', 'r') as file:
        epa_regno_info = json.load(file)

    eparegno_shortlist = [item["eparegno"] for item in epa_regno_info if any(pest.get("pest", "").lower() == user_inputted_pest.lower() for pest in item.get("pests", []))]

    for eparegno in eparegno_shortlist[:topK]:
        # Create the summary file path
        summary_file_path = f"summaries/{eparegno}.json"

        try:
            # Load the summary data from the file
            with open(summary_file_path, 'r') as file:
                summary_data = json.load(file)

            # Find corresponding entry in epa_regno_info.json
            epa_info = next((item for item in epa_regno_info if item['eparegno'] == eparegno), None)

            if epa_info:
                # Add only selected details from epa_regno_info.json to the summary_data
                selected_keys = ['signal_word', 'active_ingredients', 'types']
                for key in selected_keys:
                    if key in epa_info:
                        summary_data[key] = epa_info[key]

                # Add the summary data to the global variable info
                info[eparegno] = summary_data
            else:
                print(f"Details not found for Eparegno: {eparegno}")

        except FileNotFoundError:
            print(f"Summary file not found for Eparegno: {eparegno}")
    
    return info



def get_prompt2(crop, location, pest, topK):
    lst = question_list()
    details = add_summary(pest, topK)
    seed = f'''
        You are an assistant that is summarizing information about the pesticide provided below. 
        The JSON I provide below, called "info.json", has several details about each pesticide use.
        I will also provide a list with information on the crop and geographical location the pesticide will be used in.

        Using just this info, I need the pros, cons, and whether it can be used on the specified crop and location for each pesticide within 100 words.

        I want you to output a JSON file, with the "eparegnos" I provide as keys for each pesticide with this structure: pros, cons, bool if it can work with specified crop (assume true unless noted otherwise), and bool if it can work in a specific geographical region (assume true unless noted otherwise).

        If no relevant pros or cons exist, add an empty string for that key. Assume true for the crop and location fields. 

        Do not hallucinate, only answer based on the text I provide. Please be accurate, this is very important. 

        Here is the list of pros and cons: {lst}

        Here is the "info.json" you need to find answers in (the keys are the names of the pesticides.)
        {details}

        Here is the crop and location data [{crop},{location}]

        '''
    return seed


if __name__ == '__main__':
    pass
    
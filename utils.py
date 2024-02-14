import re
import json

def decode_to_json(text):
    # Pattern to match content within "<>"
    pattern = r'<(.*?)>'
    matches = re.findall(pattern, text)

    # Initialize the structure of the JSON
    result = {"questions": []}
    question = None

    for match in matches:
        # Check if the current match is a question
        if match.endswith('?'):
            question = {"question": match, "options": []}
            result["questions"].append(question)
        else:
            # Check if the current match contains an option (e.g., "R1 = 2.6MΩ")
            option_match = re.search(r'R1\s*=\s*([\d.]+[MKΩ]+)', match)
            if option_match:
                # Found an R1 option, create a new option entry
                option_text = "R1 = " + option_match.group(1)
                option = {"option": option_text, "correct": True, "tip": match}
                if question:
                    question["options"].append(option)
            elif question and question["options"]:
                # If there's already an option, append the current match as additional information to the last option's tip
                question["options"][-1]['tip'] += " " + match

    return json.dumps(result, indent=2)
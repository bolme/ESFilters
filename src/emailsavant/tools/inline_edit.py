#! python3

import os
import json
import time
from datetime import datetime
import emailsavant
import ollama

LOGGING = False # Good for debugging purposes.  Save the logs to ~/.email_savant/logs/inline_edit/request_[timestamp].json

def request_text_generation(prompt,seed=None):
    '''
    This function takes a prompt as input and sends it to the text-generation-webui
    service. The generated text is then returned to the user.

    Args:
    prompt (str): The prompt to be sent to the text-generation-webui service.

    Returns:
    str: The generated text.
    '''
    # Use ollama.generate with the mistral model
    response = ollama.generate(
        model="mistral",
        prompt=prompt,
        stream=False
    )
    
    # Parse the response
    generated_text = response['response']
    response_count = response['eval_count']
    prompt_count = response['prompt_eval_count']
    
    #print(response)

    return generated_text, prompt_count, response_count

    
def prepare_prompt(prompt_label, input_text):
    """
    Prepare a prompt by filling in a template with some input text.

    Parameters:
    prompt_label (str): The name of the prompt template file (without the extension).
    input_text (str): The text that will be inserted into the template.

    Returns:
    str: The prepared prompt.
    """

    # Construct the absolute path to the template file.
    template_path = os.path.join(os.path.dirname(os.path.abspath(emailsavant.__file__)), 'prompts', prompt_label + '.prompt')

    # Open the template file in read mode.
    with open(template_path, 'r') as file:
        # Read the entire content of the file into a string.
        prompt_template = file.read()
    
    # Format the prompt template by replacing `{input}` with the input text.
    prompt = prompt_template.format(input = input_text)

    # Return the prepared prompt.
    return prompt


def text_diff_highlight(original, edited, color=True):
    '''
    This function takes an original text and an edited text as input and returns
    the differences between the two texts where modified words in the edited version
    are placed in square brackets.

    Args:
    original (str): The original text.
    edited (str): The edited text.

    Returns:
    str: The differences between the two texts as a highlighted string.
    '''
    import difflib

    # Split the original and edited text into words
    original_words = original.split()
    edited_words = edited.split()

    # Get the differences between the two texts
    diff = difflib.ndiff(original_words, edited_words)

    # Highlight the differences
    highlighted_diff = ''
    
    if color:
        for word in diff:
            if word[0] == ' ':
                highlighted_diff += word[2:] + ' '
            elif word[0] == '+':
                if highlighted_diff.endswith('] '):
                    highlighted_diff = highlighted_diff[:-2] + ' \033[92m' + word[2:] + '\033[0m] '
                else:
                    highlighted_diff += '\033[92m' + word[2:] + '\033[0m '
    else:
        # Highlight difference with << and >>
        for word in diff:
            if word[0] == ' ':
                highlighted_diff += word[2:] + ' '
            elif word[0] == '+':
                if highlighted_diff.endswith('>> '):
                    highlighted_diff = highlighted_diff[:-3] + ' ' + word[2:] + '>> '
                else:
                    highlighted_diff += '<< ' + word[2:] + '>> '

    return highlighted_diff



# Run as command-line script
# Example: echo "helo human Eye  hav Reall prob lems wit typing.." | python -m emailsavant.tools.inline_edit proofread
# Result: Hello human, I have real problems with typing.
if __name__ == '__main__':
    import sys

    # Check if prompt_label was passed as a command-line argument
    if len(sys.argv) < 2:
        print("Please provide the prompt label as a command-line argument.")
        sys.exit(1)

    # Get the prompt_label from the command-line arguments
    prompt_label = sys.argv[1]

    # Read all of stdin into a string
    input_text = sys.stdin.read().strip()

    start_time = time.time()

    prompt = prepare_prompt(prompt_label,input_text)

    generated_text, input_tokens, generated_tokens = request_text_generation(prompt)

    end_time = time.time()

    print(generated_text.strip())

    if LOGGING:
        # Save the highlighted difference to a proofreading log in json format.
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        highlighted_diff = text_diff_highlight(input_text, generated_text, color=False)
        log_data = {
            'datetime': current_datetime, 
            'prompt_label': prompt_label,  # Add this line
            'input': input_text, 
            'output': generated_text, 
            'highlighted_diff': highlighted_diff, 
            'time_taken': end_time - start_time,
            'input_tokens': input_tokens,
            'generated_tokens': generated_tokens
        }
        
        # store the log in a hidden directory in the user's home directory for .email_savant/logs/proofreading/request_[timestamp].json
        log_path = os.path.expanduser('~') + '/.email_savant/logs/inline_edit/request_' + prompt_label + '_' + timestamp + '.json'
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'w') as file:
            json.dump(log_data, file, indent=4)
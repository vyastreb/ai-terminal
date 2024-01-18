"""
MistralTerminal.py
This script is a terminal interface for MistralAI.
It is a simple script that allows you to ask questions to MistralAI directly in terminal and get (relatively) short answers.
V.A. Yastrebov, CNRS, MINES Paris - PSL, France, Jan 2024.
License: BSD 3 clause
"""

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
import sys
import re

# Handle arguments
# --help/-h:                writes help
# --temp/-T:                sets temperature
# --tokens/-t:              sets number of tokens
# --model/-m:               sets the model
# --verbatim/-v:            prints the question verbatim
# : Text of the question:   after ":" the question goes

# Default values
# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
ANSWER_COLOR = BLUE
CODE_COLOR = RED

model = "mistral-tiny"
T0 = 0.2
TokenMax = 2
PrintQuestion = False
max_length = 80

def answer_question(my_question,temperature=T0, max_tokens=TokenMax):
    messages = [
        ChatMessage(role="user", content=my_question,temperature=temperature, max_tokens=max_tokens),
    ]
    chat_response = client.chat(
        model=model,
        messages=messages,
    )
    bot_response = chat_response.choices[0].message.content
    return bot_response

def strip_ansi_codes(text):
    # Regular expression to match ANSI escape codes
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def print_in_box(text, color_code):
    text = re.sub(r'\n+', '\n', text).strip()
    RESET = ANSWER_COLOR
    lines = text.split('\n')
    # Calculate max length considering the visible characters only
    max_length = max(len(strip_ansi_codes(line)) for line in lines)
    header = " AI REPLY "
    upper_border = '+' + '--' + header + "-" * (max_length - len(header) - 2) + '--' + '+'
    lower_border = '+' + '-' * (max_length + 2) + '+'

    bold_pattern = re.compile(r'\*\*(.*?)\*\*')
    italic_pattern = re.compile(r'\*(.*?)\*')

    print(color_code + upper_border)
    for line in lines:
        print('| ' + line + ' ' * (max_length - len(strip_ansi_codes(line))) + ' |')
    print(lower_border + '\033[0m')  # Reset to default color at the end

def split_long_lines(input_string, max_line_length):
    words = input_string.split()
    new_string = ""
    current_line = ""

    for word in words:
        # Check if adding the next word exceeds the max line length
        if len(current_line) + len(word) + 1 > max_line_length:
            # Add the current line to the new string and start a new line
            new_string += current_line.rstrip() + "\n"
            current_line = word + " "
        else:
            current_line += word + " "

    # Add the last line to the new string
    new_string += current_line.rstrip()
    return new_string

def split_long_lines_preserving_breaks(input_string, max_line_length):
    lines = input_string.split('\n')
    new_lines = []

    for line in lines:
        words = line.split()
        current_line = ""

        for word in words:
            # Check if adding the next word exceeds the max line length
            if len(current_line) + len(word) + 1 > max_line_length:
                # Add the current line to the new lines and start a new line
                new_lines.append(current_line.rstrip())
                current_line = word + " "
            else:
                current_line += word + " "

        # Add the last line to the new lines
        new_lines.append(current_line.rstrip())

    # Reconstruct the text with the original line breaks
    return '\n'.join(new_lines)

def colorize_text(text):    
    # Define ANSI background color codes
    RESET = ANSWER_COLOR  # Reset to default

    bold_pattern = re.compile(r'\*\*(.*?)\*\*')
    italic_pattern = re.compile(r'\*(.*?)\*')
    colored_text = bold_pattern.sub(lambda m: '\033[1m' + m.group(1) + '\033[0m' + RESET, text)  # Make **bold**
    colored_text = italic_pattern.sub(lambda m: '\033[3m' + m.group(1) + '\033[0m' + RESET, colored_text)  # Make *italic*

    # Regex patterns for single and triple backticks
    pattern_inline = re.compile(r'`(.*?)`')  # Single backtick
    pattern_block = re.compile(r'```(.*?)```', re.DOTALL)  # Triple backtick

    # Replace patterns with colored text and add extra spaces on the ends
    colored_text = pattern_block.sub(lambda m: CODE_COLOR + m.group(1)+ RESET, colored_text)
    colored_text = pattern_inline.sub(lambda m: CODE_COLOR + m.group(1) + RESET, colored_text)

    return colored_text


# Parse arguments
for i in range(len(sys.argv)):
    if sys.argv[i] == "--help" or sys.argv[i] == "-h":
        print("Usage: python3 MistralTerminal.py\n \
            --model/-m:  sets the model\n \
            --temp/-T:   sets temperature\n \
            --tokens/-t: sets number of tokens\n \
            --help/-h:   writes help")
        print("Example: python3 MistralTerminal.py --model mistral-tiny --temp 0.2 --tokens 5")
        print("Default values:\n   model=mistral-tiny\n   temperature=0.2\n   number_of_tokens=2")
        exit()
    elif sys.argv[i] == "--model" or sys.argv[i] == "-m":
        model = sys.argv[i+1]
    elif sys.argv[i] == "--verbatim" or sys.argv[i] == "-v":
        PrintQuestion = True
    elif sys.argv[i] == "--temp" or sys.argv[i] == "-T":
        T0 = float(sys.argv[i+1])
    elif sys.argv[i] == "--tokens" or sys.argv[i] == "-t":
        TokenMax = int(sys.argv[i+1])        
    else:
        if i == 0:
            continue
        if sys.argv[i] == ":":
            # Concatenate everything after ":" into a single string including all types of quotes, primes, etc.
            my_question = " ".join(sys.argv[i+1:])
            break

if PrintQuestion:
    print("<"+my_question+">")


# Retrieve API key
api_key = os.environ["MISTRAL_API_KEY"]

# Request to MistralAI
client = MistralClient(api_key=api_key)

answer = answer_question(my_question)
adjusted_text = split_long_lines_preserving_breaks(answer,max_length)
print_in_box(colorize_text(adjusted_text), ANSWER_COLOR)

"""
MistralTerminal.py
This script is a terminal interface for MistralAI.
It is a simple script that allows you to ask questions to MistralAI directly in terminal and get (relatively) short answers.
V.A. Yastrebov, CNRS, MINES Paris - PSL, France, Jan 2024.
License: BSD 3 clause

Handle arguments:
--help/-h:                writes help
--temp/-T:                sets temperature
--tokens/-t:              sets number of tokens
--model/-m:               sets the model
--verbose/-v:             prints the question
--not-chat/-n:            switchs off chat mode, does not keep previous answers
       :                  text of the question - after ":" the question goes

It stores the history of previous answers in a file in home directory `.mistralai/history.txt`
The configuration file `.mistralai/config.json` is used to store the parameters.
"""

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os, sys, re, time, json
from collections import deque

########################################
#     Global parameters
########################################

CONFIG_PATH  = os.path.expanduser("~/.mistralai/config.json")
HISTORY_PATH = os.path.expanduser("~/.mistralai/history.txt")

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
# Answers (code blocks) will be printed in ANSWER_COLOR (CODE_COLOR), choose the one which is visible on your terminal in both light and dark mode
ANSWER_COLOR = BLUE
CODE_COLOR = RED
# Activate emoji support
EMOJI = True
# Default MistralAI parameters: temperature T0, maximal number of used tokens TokenMax, and model
T0          = 0.3
TokenMax    = 100
model       = "mistral-tiny"

########################################
#     MistralAI client
########################################

# Retrieve API key
try:
    api_key = os.environ["MISTRAL_API_KEY"]
except KeyError:
    print("Error: MISTRAL_API_KEY environment variable is not set.")
    exit()

# create MistralAI client
client = MistralClient(api_key=api_key)

########################################
#     Functions
########################################

def Role(i, size):
        if i % 2 == 0:
            return "user"
        else:
            return "assistant"

def follow_chat(chat_history : deque, temperature=T0, max_tokens=TokenMax):
    if len(chat_history) == 1:
        return answer_question(chat_history[0],temperature=temperature, max_tokens=max_tokens)
    else:
        messages = []
        for i in range(len(chat_history)):
            messages.append(ChatMessage(role=Role(i,len(chat_history)), content=chat_history[i],temperature=temperature, max_tokens=max_tokens))
        # print("\n\n == MESSAGES == \n\n", messages )
        try:
            chat_response = client.chat(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            bot_response = chat_response.choices[0].message.content
        except Exception as e:
            print("An error occurred:", e)
            bot_response = "ERROR: An error occurred, please try again"
        return bot_response

def answer_question(my_question,temperature=T0, max_tokens=TokenMax):
        messages = [
            ChatMessage(role="user", content=my_question,temperature=temperature, max_tokens=max_tokens),
        ]
        chat_response = client.chat(
            model=model,
            messages=messages,
            temperature=temperature, 
            max_tokens=max_tokens,
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
    max_line_length = max(len(strip_ansi_codes(line)) for line in lines)

    if EMOJI:
        header = " < 🤖 > "
        upper_border = '+' + '--' + header + "-" * (max_line_length - len(header) - 3) + '--' + '+'
    else:
        header = " AI REPLY "
        upper_border = '+' + '--' + header + "-" * (max_line_length - len(header) - 2) + '--' + '+'
    lower_border = '+' + '-' * (max_line_length + 2) + '+'

    # bold_pattern = re.compile(r'\*\*(.*?)\*\*')
    # italic_pattern = re.compile(r'\*(.*?)\*')

    print(color_code + upper_border)
    for line in lines:
        print('  ' + line + ' ' * (max_line_length - len(strip_ansi_codes(line))) + '  ')
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

########################################
#     Main
########################################

def main():    
    global T0, TokenMax, model
    # Local parameters: chat and output parameters
    Chat = True
    verbose = False
    max_memory = 31 # Maximum number of previous answers to keep in memory in chat mode, should be odd
    waitingTime = 180 # Time in seconds after which the history is erased
    max_line_length = 80      

    # Checks whether config file exists: if yes, read parameters from there, otherwise use default values
    ArgumentsProvenance = "Default values"
    if os.path.isfile(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as file:
                ArgumentsProvenance = "Configuration file"
                config = json.load(file)
                model = config["model"]
                max_memory = config["max_memory"]
                T0 = config["temperature"]
                TokenMax = config["max_tokens"]
                waitingTime = config["waitingTime"]
                max_line_length = config["max_line_length"]
        except json.JSONDecodeError as e:
            print(f"Error reading JSON file: {e}")
        except KeyError as e:
            print(f"Missing key in JSON file: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


    # Parse arguments
    for i in range(len(sys.argv)):
        if sys.argv[i] == "--help" or sys.argv[i] == "-h":
            print("Usage: python3 MistralTerminal.py\n \
                --model/-m:     sets the model\n \
                --temp/-T:      sets temperature\n \
                --tokens/-t:    sets number of tokens\n \
                --not-chat/-n:  switchs off chat mode, does not keep previous answers\n \
                --help/-h:      writes help")
            print("Example: python3 MistralTerminal.py --model mistral-tiny --temp 0.2 --tokens 50")
            print("Default values:\n   model={}\n   temperature={}\n   number_of_tokens={}".format(model,T0,TokenMax))
            exit()
        elif sys.argv[i] == "--model" or sys.argv[i] == "-m":
            ArgumentsProvenance = "Command line"
            model = sys.argv[i+1]
        elif sys.argv[i] == "--verbose" or sys.argv[i] == "-v":
            verbose = True
        elif sys.argv[i] == "--temp" or sys.argv[i] == "-T":
            ArgumentsProvenance = "Command line"
            T0 = float(sys.argv[i+1])
        elif sys.argv[i] == "--tokens" or sys.argv[i] == "-t":
            ArgumentsProvenance = "Command line"
            TokenMax = int(sys.argv[i+1])        
        elif sys.argv[i] == "--not-chat" or sys.argv[i] == "-n":
            Chat = False
        else:
            if i == 0:
                continue
            if sys.argv[i] == ":":
                # Concatenate everything after ":" into a single string.
                my_question = " ".join(sys.argv[i+1:])
                break

    if verbose:
        if ArgumentsProvenance == "Default values":
            print("No configuration file found, using default parameters:")
        elif ArgumentsProvenance == "Command line":
            print("Using parameters from command line:")
        elif ArgumentsProvenance == "Configuration file":            
            print("Configuration file found, using parameters from there:")
        else:
            print("Warning: unknown provenance of parameters, using default values.")
        print(" \nmodel: {} \
                \nmax_memory: {} \
                \ntemperature: {} \
                \nmax_tokens: {} \
                \nwaitingTime: {} \
                \nmax_line_length: {}".format(model,max_memory,T0,TokenMax,waitingTime,max_line_length))

    # Previous answers are kept in HISTORY_PATH, check that it exists, and if it exists and not older than 1 minute, read it, otherwise erase it and create a new one
    if Chat:
        try:
            if os.path.isfile(HISTORY_PATH):
                if os.path.getmtime(HISTORY_PATH) > time.time() - waitingTime:
                    with open(HISTORY_PATH, 'r') as f:
                        chat_history = deque(f.read().split('$$##'), maxlen=max_memory)
                    with open(HISTORY_PATH, 'a') as f:
                        f.write('$$##' + my_question)
                    chat_history.append(my_question)
                else:
                    chat_history = deque([my_question], maxlen=max_memory)
                    with open(HISTORY_PATH, 'w') as f:
                        f.write(my_question)
            else:
                chat_history = deque([my_question], maxlen=max_memory)
                with open(HISTORY_PATH, 'w') as f:
                    f.write(my_question)
        except Exception as e:
            print("An error occurred:", e)


    if verbose:
        print("Question: <"+my_question+">")
        if Chat:
            for i in range(len(chat_history)):
                message = chat_history[i].replace('\n\n',' ').replace('\n',' ').replace('\r',' ').replace('\t',' ')
                print("Previous messages #{}: <{}>".format(i,message))

    if Chat:
        answer = follow_chat(chat_history,temperature=T0, max_tokens=TokenMax)
    else:
        answer = answer_question(my_question,temperature=T0, max_tokens=TokenMax)   
    if Chat:
        chat_history.append(answer)
        with open(os.path.expanduser("~/.mistralai/history.txt"), 'w') as f:
            f.write('\n$$##\n'.join(chat_history))
    adjusted_text = split_long_lines_preserving_breaks(answer,max_line_length)
    print_in_box(colorize_text(adjusted_text), ANSWER_COLOR)
if __name__ == "__main__":
    main()
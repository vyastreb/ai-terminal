"""
MistralTerminal.py
This script is a terminal interface for MistralAI.
This script allows to interact with MistralAI's chatbot directly in the terminal and get well formated answers.

Author: Vladislav A. Yastrebov 
Affiliation: CNRS, MINES Paris - PSL, France, Jan 2024.
License: BSD 3 clause
Repository: https://github.com/vyastreb/ai-terminal

Handle arguments:
--help/-h:                writes help
--temp/-T:                sets temperature
--tokens/-t:              sets number of tokens
--model/-m:               sets the model
--verbose/-v:             prints the question
--not-chat/-n:            switchs off chat mode, does not keep previous answers
--unit-test/-u:           unit tests

It stores the history of previous answers in a file in home directory `.mistralai/history.txt`
The configuration file `.mistralai/config.json` is used to store the parameters.
"""

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os, sys, re, time, json, contextlib, readline, subprocess
from collections import deque

########################################
#     Global parameters
########################################

CONFIG_PATH     = os.path.expanduser("~/.mistralai/config.json")
HISTORY_PATH    = os.path.expanduser("~/.mistralai/history.txt")
QUESTIONS_PATH  = os.path.expanduser("~/.mistralai/questions.txt")

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
    print("Error: MISTRAL_API_KEY environment variable is not set.\nObtain you API key from https://mistral.ai")
    exit()

# create MistralAI client
client = MistralClient(api_key=api_key)

########################################
#     Functions
########################################

def load_history():
    if os.path.exists(QUESTIONS_PATH):
        readline.read_history_file(QUESTIONS_PATH)

def save_history():
    readline.write_history_file(QUESTIONS_PATH)

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
            messages.append(ChatMessage(role=Role(i,len(chat_history)), content=chat_history[i]))
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
            ChatMessage(role="user", content=my_question),
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

def replace_code_tag(line):
    TAGS = ["bash","python","yaml","json","html","css","javascript","typescript","c","cpp","java","kotlin","scala","swift","php","ruby","perl","shell","powershell","sql","r","matlab","latex","markdown"]
    changed = False
    for tag in TAGS:
        if tag in line:
            line = line.replace(tag,"")
            changed = True
    return changed, line

def split_long_lines_preserving_breaks(input_string, max_line_length):
    lines = input_string.split('\n')
    new_lines = []
    code_blocks = []
    block_id = 1
    start_block = False
    one_block = ""

    for line in lines:
        current_line = ""
        if start_block and "```" in line:
            start_block = False
        elif "```" in line and not start_block:
            print("Start>> ",line   )
            start_block = True
            # find first occurence of "```" in line
            i = line.find("```")
            # print("in line <"+line+">, code block starts at ",i)
            one_block = line.replace("```","")
            replaced, one_block = replace_code_tag(one_block)
            print("one_block: ",one_block)
            if replaced:
                line = line[:i] + "```[" + str(block_id) + "] "+line[i+3:]
        if start_block and "```" not in line:
            one_block += line + "\n"
        if not start_block and one_block != "":
            code_blocks.append(one_block)
            one_block = ""
            block_id += 1

        words = line.split()

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
    return '\n'.join(new_lines), code_blocks

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
# Functions for copying to clipboard
########################################

# Function to copy text to the clipboard
def copy_to_clipboard(text):
    try:
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(text.encode('utf-8'))
    except FileNotFoundError:
        # pbcopy might not be available on Linux, trying xclip instead
        process = subprocess.Popen(['xclip', '-selection', 'c'], stdin=subprocess.PIPE)
        process.communicate(input=text.encode('utf-8'))

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
                --model/-m:     sets the model (mistral-tiny, mistral-small or mistral-medium)\n \
                --temp/-T:      sets temperature (0.0 <= T <= 1.0)\n \
                --tokens/-t:    sets number of tokens (integer, 1 sentence ~ 50)\n \
                --verbose/-v:   verbose output\n \
                --not-chat/-n:  switchs off chat mode, does not keep previous answers\n \
                --help/-h:      writes help")
            print("Example: python3 MistralTerminal.py --model mistral-tiny --temp 0.2 --tokens 50")
            print("To know current values, execute with --verbose")
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
            continue                

    load_history()
    my_question = input("> ")
    save_history()

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
                if True: #os.path.getmtime(HISTORY_PATH) > time.time() - waitingTime:
                    with open(HISTORY_PATH, 'r') as f:
                        chat_history = deque(f.read().split('$$##'), maxlen=max_memory)
                    with open(HISTORY_PATH, 'a') as f:
                        f.write('$$##' + my_question)
                    chat_history.append(my_question)
                # else:
                #     chat_history = deque([my_question], maxlen=max_memory)
                #     with open(HISTORY_PATH, 'w') as f:
                #         f.write(my_question)
                #     with open(QUESTIONS_PATH, 'w') as f:
                #         f.write(my_question)
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

    try:
        if Chat:
            answer = follow_chat(chat_history,temperature=T0, max_tokens=TokenMax)
        else:
            answer = answer_question(my_question,temperature=T0, max_tokens=TokenMax)   
    except Exception as e:
        print("An error occurred:", e)
        answer = "ERROR: An error occurred, please try again"
    if Chat:
        chat_history.append(answer)
        with open(os.path.expanduser("~/.mistralai/history.txt"), 'w') as f:
            f.write('\n$$##\n'.join(chat_history))

    # FIXME add code blocks here
    adjusted_text,code_blocks = split_long_lines_preserving_breaks(answer,max_line_length)
    print_in_box(colorize_text(adjusted_text), ANSWER_COLOR)

    # If there are code blocks, prompt the user to choose one to copy
    if code_blocks:
        while True:  # Keep asking until the user inputs a valid option
            try:
                block_selection = input(CODE_COLOR + ">>> Select [code block] to copy to the clipboard: " + "\033[0m")
                selection = int(block_selection)
                if 1 <= selection <= len(code_blocks):
                    copy_to_clipboard(code_blocks[selection - 1])
                    # print(f"Code block [{selection}] has been copied to the clipboard.")
                    break
                else:   # Do nothing
                    break
            except ValueError: # Do nothing
                break

if __name__ == "__main__":
    with contextlib.suppress(TypeError):
        main()


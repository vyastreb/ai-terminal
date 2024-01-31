# MistralTerminal - chatbot in your Linux terminal

## Overview

MistralTerminal is a command-line interface for interacting with MistralAI. It allows users to send questions directly from the terminal and receive concise answers from MistralAI. This script is designed for simplicity and ease of use. It keeps the conversation in a local file, so you can continue interact with it without giving the context every time. It also supports colored output for enhanced readability.

## Author

V.A. Yastrebov, CNRS, MINES Paris - PSL, France, Jan 2024.
License: BSD 3 clause

## Requirements

- Python 3
- mistralai Python package `pip install mistralai`
- An API key for MistralAI, check on [mistral.ai](https://mistral.ai)

## Installation

Ensure Python 3 and the necessary packages are installed. Set your MistralAI API key in your environment:

```bash
export MISTRAL_API_KEY='your_api_key_here'
```
You can also set-up an alias `ai` to run the script from anywhere in your terminal (for `bash` add in your `.bashrc`):

```bash
alias ai="python3 /path/to/script/MistralTerminal.py 2>/dev/null "
```


### Options

- `--model/-m`: Sets the MistralAI model to be used. Default is 'mistral-tiny'.
- `--temp/-T`: Sets the temperature for the AI's responses. Default is 0.2.
- `--tokens/-t`: Sets the maximum number of tokens in the response. Default is 2.
- `--verbose/-v`: If set, prints the question or the whole history.
- `--no-chat/-n`: If set, does not keep the discussion in memory.
- `--help/-h`: Displays the help message and usage instructions.

The default model is 'mistral-tiny', which is a smaller model that is faster to load and run. The default temperature is 0.2, which is a good value for most questions. The default token count is 2, which is a good value for most questions. The verbose option is useful for checking whether your question was correctly parsed by the script. For example, if you have `#` or `"` in your question, you need to put it with `\#`, `\"`, the same with brackets.

### Configuration file

All parameters could be defined in the script or in the config file `~/.mistralai/config.json`. 
If config file is not found, the script will use default parameters.
If config file exists, it will use parameters from the file, and will ignore parameters defined in the script.
But if you prescribe options in the command line, they will be used instead of the config file.

*Example of config file:*
```
{
 "model": "mistral-tiny",
 "max_memory": 31,
 "max_tokens": 1000,
 "waitingTime": 180,
 "max_line_length": 80,
 "temperature": 0.5
}
``` 

### Usage

The script can be run from the command line with various options. Enter your question preceded by `:` and the script will process and display the AI's response.

```bash
python3 MistralTerminal.py [options] : your question
```
or if you set-up an alias:
```bash
ai [options] : your question
```
Examples:
```bash
ai : How to convert jpg to png in linux?
```
```bash
ai --temp 0.5 : What is the meaning of life?
```
```bash
ai --model mistral-tiny --temp 0.2 --tokens 5 : What is best cheese in France?
```

### Features

- Can be run from anywhere in the terminal
- Keeps the history of conversation in a local file for some time
- Colored output for enhanced readability
- Adjustable parameters for model, temperature, and token count
- Supports multi-line responses with automatic line wrapping

### Notes

- Ensure your terminal supports ANSI color codes for the best experience.
- The history of last messages (31 by default) is stored in `~/.mistralai/history.txt` for 3 minutes by default. You can change the number of stored messages and the time in the script of in config file: `max_memory` and `waitingTime`.


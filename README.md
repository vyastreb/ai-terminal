# MistralTerminal - chatbot in your Linux terminal

## Overview
MistralTerminal is a command-line interface for interacting with MistralAI. It allows users to send questions directly from the terminal and receive concise answers from MistralAI. This script is designed for simplicity and ease of use.

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
- `--verbatim/-v`: If set, prints the question verbatim.
- `--help/-h`: Displays the help message and usage instructions.

The default model is 'mistral-tiny', which is a smaller model that is faster to load and run. The default temperature is 0.2, which is a good value for most questions. The default token count is 2, which is a good value for most questions. The verbatim option is useful for checking whether your question was correctly parsed by the script. For example, if you have `#` in your question, you need to put it with `\#`.

## Usage
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

## Features
- Colored output for enhanced readability
- Adjustable parameters for model, temperature, and token count
- Supports multiline responses with automatic line wrapping

## Notes
- Ensure your terminal supports ANSI color codes for the best experience.
- The script dynamically adjusts the line length to fit the terminal window.



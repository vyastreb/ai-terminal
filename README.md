# MistralTerminal - chatbot in your Linux terminal

## Overview

MistralTerminal is a command-line interface for interacting with MistralAI. It allows users to send questions directly from the terminal and receive concise answers from MistralAI. This script is designed for simplicity and ease of use. It keeps the conversation history, so you can continue interact with it without giving the context every time. The input can be multiline. If the script suggest code blocks, you can easily copy them in the clipboard. It also supports colored output for enhanced readability.

## License

License: BSD 3 clause

## Author

V.A. Yastrebov, CNRS, MINES Paris - PSL, France, Jan 2024.

## External Contributors

- [Basile Marchand](https://github.com/basileMarchand)

## Requirements

- An API key for MistralAI, check on [mistral.ai](https://mistral.ai)

## Installation

Set your MistralAI API key in your environment:

```bash
export MISTRAL_API_KEY='your_api_key_here'
```

### From Github sources

```bash
git clone https://github.com/vyastreb/ai-terminal.git
cd ai-terminal
```

Install required dependencies and the `ai` command using :

```bash
pip install .
```

### From PyPi

**Comming Soon**

## Options

- `--model/-m`: Sets the MistralAI model to be used (mistral-tiny, mistral-small or mistral-medium). Default is 'mistral-tiny'.
- `--temp/-T`: Sets the temperature for the AI's responses. Default is 0.2.
- `--tokens/-t`: Sets the maximum number of tokens in the response. Default is 2.
- `--verbose/-v`: If set, prints the question or the whole history.
- `--no-chat/-n`: If set, does not keep the discussion in memory.
- `--unit-test/-u`: Unit tests.
- `--help/-h`: Displays the help message and usage instructions.

The default model is 'mistral-tiny', which is a smaller model that is faster to load and run. The default temperature is 0.5, which is a good value for most questions. The default token count is 350, which is a reasonable length for most answers. The verbose option is useful for checking whether your questions and history were correctly parsed by the script.

### Configuration file

All parameters could be defined in the script or in the config file `~/.mistralai/config.json`.
If config file is not found, the script will use default parameters.
If config file exists, it will use parameters from the file, and will ignore parameters defined in the script.
But if you prescribe options in the command line, they will be used instead of the config file.

_Example of config file:_

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

## Usage

```bash
ai [options]
```

These commands will start a new line `>  ` where your question could be written.

**Examples:**

```bash
ai
> How to convert jpg to png in linux?
```

```bash
ai --temp 0.0
> What is the meaning of life?
```

```bash
ai --model mistral-tiny --temp 0.8 --tokens 5000
> What is the best (according to parisian) cheese in France?
```

```bash
ai -m mistral-small -T 0.8 -t 500 -v
> What is the visible EM spectrum?
```

### Features

- Can be run from anywhere in the terminal
- Supports multi-line input
- Remembers past questions
- If one code block is shown, it automatically stores it in the clipboard
- If several code blocks are shown, it suggests to store the one you want in the clipboard
- Keeps the history of conversation in a local file for some (user defined) time
- Colored output for enhanced readability
- Adjustable parameters for model, temperature, and token count
- Supports multi-line responses with automatic line wrapping

### Notes

- Ensure your terminal supports ANSI color codes for the best experience.
- The history of last messages (31 by default) is stored in `~/.mistralai/history.txt` for 3 minutes by default. You can change the number of stored messages and the time in the script of in config file: `max_memory` and `waitingTime`.


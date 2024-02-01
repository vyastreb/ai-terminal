
# TODO

+ [ ] Make code in \`xxx\` and code in blocks \`\`\`xxx\`\`\` selectable.

# Done

January 31, 2024

+ [x] Handles proper input with tracking of history of questions.

January 30, 2024

+ [x] Keeps dialog history.

January 19, 2024

+ [x] Add possibility to make a dialog by keeping recent messages in the memory. *Fixed on Jan 30, 2024.*
+ [x] Script does not handle \#, \' and probably \" in the text of the question,  solve it. *FIXED on Jan 31, 2024"

3. Syntaxis with \`xxx\` does not work well, see example:

+-- < 🤖 > -----------------------------------------------------------------------+
| Yes, you can set up your environment to use Python 3.10 as your default version |
| when you type python or pip in your terminal or command prompt. This            |
| process is called setting up a Python environment variable. Here's a            |
| step-by-step guide for different operating systems:                             |
| For macOS:                                                                      |
| 1. Install Homebrew (if you haven't already) by running this command in your    |
| terminal: `/usr/bin/ruby -e "$(curl -fsSL                                       |
| https://raw.githubusercontent.com/Homebrew/install/master/install)"`            |
| 2. Install Python 3.10 using Homebrew: brew install python@3.10                 |
| 3. Add the Python 3.10 binary to your PATH: `echo 'export                       |
| PATH="/usr/local/opt/python@3.10/bin:$PATH"' >> ~/.zshrc` (for Zsh users) or    |
| echo 'export PATH="/usr/local/opt/python@3.10/bin:$PATH"' >> ~/.bash_profile    |
| (for Bash users)                                                                |
| 4. Install pip for Python 3.10: `curl https://bootstrap.pypa.io/get-pip.py |    |
| sudo python3.10`                                                                |
| 5. Make sure pip is linked to Python 3.10: `sudo ln -s                          |
| /usr/local/opt/python@3.10/lib/python3.10/site-packages/pip /usr/local/bin/pip` |
| 6. Test your setup: python --version and pip --version should display           |
| Python 3.10 as the active version.                                              |
| For Windows:                                                                    |
| 1. Download Python 3.10 from the official website, specifically the installer   |
| for Windows, and run it. Make sure to check the box "Add Python 3.10 to PATH"   |
| during the installation process.                                                |
| 2. Install pip for Python 3.10: Open your Command Prompt, type python and       |
| press Enter. In the new Python window, type pip install pip and press Enter.    |
| Close the Python window.                                                        |
| 3. Test your setup: Open a new Command Prompt window and type `python           |
| --version and pip --version` to check that Python 3.10 is indeed the active     |
| version.                                                                        |
| For Linux (non-macOS):                                                          |
| 1. Install Python 3.10 using your package manager. For example, if you're using |
| Ubuntu, type sudo apt install python3.10.                                       |
| 2. Make sure Python 3.10 is the default version: `sudo update-alternatives      |
| --config python`. Choose Python 3.10 as the preferred version.                  |
| 3. Install pip for Python 3.10: `sudo apt install python3.10-venv               |
| python3.10-distutils python3.10-dev and then sudo update-alternatives           |
| --install /usr/bin/pip pip /usr/bin/pip3.10 2`.                                 |
| 4. Test your setup: Open a new terminal window and type python --version and    |
| pip --version to check that Python 3.10 is indeed the active version.           |
+---------------------------------------------------------------------------------+

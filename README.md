# Introduction to ES Filters

Embrace AI on your Mac with ES Filters! This versatile tool offers a range of filters for text enhancement within macOS. The suite includes tools for proofreading, clarifying text, converting to professional voice, and even transforming text into PowerPoint bullet points.

Originally developed as test prompts for the ambitious email processing tool, Email Savant, these filters have stood alone as an independent, user-friendly solution. You can easily apply them to any text written on your MacOS machine.

ES Filters utilize local AI models through Ollama. For optimal performance, we recommend an M2 or better processor with at least 6GB of free memory. Please note that this is research software and requires some software development experience for installation.

# Instructions
  1. Choose text.
  2. Right click on it.
  3. Select "Services" at the bottom of the menu.
  4. Pick a filter to apply to the text.

Filters usually take a few seconds to execute based on the length of the text. The generated text replaces the selected in the document.

# Installation

**Install ollama:** Download and install the binary from here: https://ollama.com/download

Once ollama is installed and running you should be prompted to install the commandline tools. Currently and prompts are configured for ```mistral``` because it does better following directions and generating parsable json outputs.  Have llama pull that model (approx. 4GB).

```bash
ollama pull mistral
```

Test ollama with a chat window...

```bash
ollama run mistral
```

**Note:** Smaller models are now available, which may be more performant on slower machines like phi3.5 or gemma2:2b. These may necessitate simple code adjustments to utilize these other models.

**Install Miniconda and Python**

https://docs.anaconda.com/miniconda/#miniconda-latest-installer-links

From the main directory of the emailsavant package, execute the subsequent commands. (Please note: python 3.11 is necessary for open-webui, which is an excellent enhancement to the environment):

```bash
conda create -n emailsavant python=3.11
conda activate emailsavant
git clone https://github.com/bolme/EmailSavant.git
cd EmailSavant
pip install -e .
```

**Optional Install OpenWebUI:** OpenWebUI is a user-friendly graphical chat interface for ollama models, providing you with a local AI chat interface!

```bash
conda activate emailsavant
pip install open-webui
```

Test it with this command:
```bash
open-webui serve --host 127.0.0.1 --port 8888
```


**Install Inline Editing Tools**

These are command line tools that translate a stdin to stdout through a filter.

Test the inline_edit.py script by running the following command:

```bash
echo "Herre is sosomme bad spellinggs." | ${HOME}/miniconda3/envs/emailsavant/bin/python -m emailsavant.tools.inline_edit proofread
```

The output should look something like this...
```
Here is some bad spelling.
```

**Install MacOS Automator Tasks**

On MacOS the inline editing tools can be installed as services.   **Note:** This assumes that you are using python installed here through miniconda `${HOME}/miniconda3/envs/emailsavant/bin/python`.


To install configured services run the following commands.

```bash
cd EmailSavant
cp -r Quick_Actions/*.workflow ${HOME}/Library/Services/
```

To use them select text to process and then right click and use the "Services" menu to apply a filter..

# Create custom prompts:

Prompts can be added in the src/emailsavant/prompts directory by duplicating and modifying one of the existing prompts.  A custom automator task can be added to the services menu using the following instructions:

 1. Open Automator and create a new Quick Action.
 2. Select "Output replaces selected text."
 3. Add a "Run Shell Script" action.
 4. Set the shell to "/bin/bash" and the input to "stdin".
 5. Paste the following code into the script: ```${HOME}/miniconda3/envs/emailsavant/bin/python -m emailsavant.tools.inline_edit proofread```
    * If needed use command  `which python` to find the path to the emailsavant python executable.
 6. Save the Quick Action with the name "ES Proofread".
 7. Repeat the process with other prompts: bullets, clarify, personal, preview, prefessional, reduce, summary, or your own custom prompts.




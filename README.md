# LLM-Powered Notes App

## Overview

This is a Tkinter-based note-taking application enhanced with LLM (Large Language Model) capabilities, allowing users to receive autocompletion suggestions based on their inputs. The app allows users to write notes, save files, open existing files, and undo changes. Users can also select from different LLM models to provide note suggestions, such as completing sentences, adding more information, or filling in placeholders.

## Features

- **Autocomplete Notes**: Press `Ctrl + Enter` to get autocomplete suggestions powered by the selected LLM model.
- **Save/Save As**: Save the current note (`Ctrl + S`) or save it as a new file (`Ctrl + Shift + S`).
- **Open File**: Open existing `.txt` files (`Ctrl + O`).
- **Undo Changes**: Revert to previous edits using the undo stack (`Ctrl + Z`).
- **Model Selection**: Choose between different LLM models for autocompletion.
- **File Management**: Easily open and save notes using the file menu or hotkeys.

## Requirements

- Python 3.x
- `ollama` library for LLM-based autocompletion
- `tkinter` for the GUI

- `Ollama` application download

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/llm-powered-notes-app.git
   cd llm-powered-notes-app
   ```

2. Install the required dependencies:
   ```bash
   pip install ollama
   ```
3. [Install Ollama](https://ollama.com/download)

4. Run the application:
   ```bash
   python app.py
   ```

## How to Use

1. **Start Writing**: Use the main text area to write your notes.
2. **Autocomplete**: Press `Ctrl + Enter` to receive autocompletion suggestions from the LLM based on your notes.
3. **Save Files**: 
   - Press `Ctrl + S` to save your work.
   - Use `Ctrl + Shift + S` to save as a new file.
4. **Open Files**: Use `Ctrl + O` to open an existing text file.
5. **Undo Changes**: Press `Ctrl + Z` to undo the last significant change.
6. **Model Selection**: From the `Model` menu, select the desired LLM model for generating suggestions.

## Hotkeys

| Function      | Shortcut             |
|---------------|----------------------|
| Autocomplete  | `Ctrl + Enter`        |
| Save          | `Ctrl + S`            |
| Save As       | `Ctrl + Shift + S`    |
| Open File     | `Ctrl + O`            |
| Undo          | `Ctrl + Z`            |

## Customization

You can customize the available models by updating the `model_options` list in the code. The app defaults to the first model in the list.  

By default, Meta AI's llama3.2:3b model is used.

import ollama
import tkinter as tk
from tkinter import font, filedialog, Menu, messagebox

# Initialize undo stack
undo_stack = []
change_threshold = 3  # Threshold to determine significant changes
last_change_length = 0  # Length of the last change
current_file_path = None  # Store the currently opened file's path

# List of possible model options
model_options = ['llama3.2:3b','llama3.2:1b']
selected_model = model_options[0]  # Default model

# Function to update the selected model
def update_model(model):
    global selected_model
    selected_model = model

# Function to get autocomplete suggestions and display them in the suggestion bar
def autocomplete_input(user_input):
    prompt = "You are a note-taking assistant. Either complete the user's notes, add more information, or fill in the placeholders marked with '{?}' where the '?' may include helpful information."
    
    stream = ollama.chat(
        model=selected_model,
        messages=[
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': user_input}
        ],
        stream=True,
    )

    suggestion_text_widget.config(state="normal")
    suggestion_text_widget.delete("1.0", tk.END)  # Clear previous content

    for chunk in stream:
        suggestion_text_widget.insert(tk.END, chunk['message']['content'])
        suggestion_text_widget.see(tk.END)  # Scroll to the end of the text box
        suggestion_text_widget.update()  # Refresh the widget

# Function to save text to a file
def save_to_file():
    global current_file_path
    text = text_widget.get("1.0", tk.END)
    if current_file_path:  # If a file is already opened, save to that file
        with open(current_file_path, 'w') as file:
            file.write(text)
    else:  # If no file is opened, follow the save as procedure
        save_as()

# Function to open a text file and load it into the text widget
def open_file():
    global current_file_path
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        try:
            current_file_path = file_path  # Update the current file path
            with open(file_path, 'r') as file:
                content = file.read()
                text_widget.delete("1.0", tk.END)  # Clear current content
                text_widget.insert(tk.END, content)  # Load content from file
            root.title("LLM-Powered Notes App - " + file_path)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening the file: {e}")

# Function to invoke Save As dialog
def save_as():
    global current_file_path
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        current_file_path = file_path  # Update the current file path
        with open(file_path, 'w') as file:
            text = text_widget.get("1.0", tk.END)
            file.write(text)

    root.title("LLM-Powered Notes App - " + file_path)


# Function to save current text to undo stack and update it on changes
def save_to_undo_stack():
    global last_change_length
    current_text = text_widget.get("1.0", tk.END)[:-1]  # Remove trailing newline
    change_length = len(current_text) - last_change_length
    
    if abs(change_length) >= change_threshold:
        undo_stack.append(current_text)  # Save significant change to undo stack
        if len(undo_stack) > 10:  # Limit the size of the stack
            undo_stack.pop(0)
        last_change_length = len(current_text)

# Function to revert the last edit (Ctrl-Z)
def revert_edit():
    if undo_stack:
        last_edit = undo_stack.pop()  # Pop the last change from undo stack
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, last_edit)
        global last_change_length
        last_change_length = len(last_edit)

# Hotkey to trigger autocomplete on Ctrl+Enter
def on_ctrl_enter(event):
    # get document content
    user_input = text_widget.get("1.0", tk.END)
    autocomplete_input(user_input)

# Hotkey to save to file on Ctrl+S
def on_ctrl_s(event):
    save_to_file()

# Hotkey to save as on Ctrl+Shift+S
def on_ctrl_shift_s(event):
    save_as()

# Hotkey to revert edit on Ctrl-Z
def on_ctrl_z(event):
    revert_edit()

# Hotkey to open file on Ctrl-O
def on_ctrl_o(event):
    open_file()

# Function to monitor changes in the text widget
def on_text_change(event):
    save_to_undo_stack()

# Create the main window and set it to a specific size (windowed, taking up the whole screen)
root = tk.Tk()
root.title("LLM-Powered Notes App")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")  # Set the window size to the screen dimensions
root.configure(bg="#f0f0f0")  # Set a light gray background for the window

# Create a Frame to contain the text widget and center it
frame = tk.Frame(root, bg="white", bd=2, relief=tk.GROOVE)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=screen_width * 0.7, height=screen_height * 0.8)

# Create a large font for the text widget
big_font = font.Font(family="Helvetica", size=18)

# Create a Text widget for input with larger size and font
text_widget = tk.Text(frame, height=30, width=100, font=big_font, wrap="word", bg="white", bd=0)
text_widget.pack(side=tk.LEFT, fill="both", expand=True, padx=20, pady=20)

# Add a vertical scrollbar to the text widget
text_scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_widget.config(yscrollcommand=text_scrollbar.set)

# Create a Frame for the autocomplete suggestion bar on the right
suggestion_frame = tk.Frame(root, bg="lightgray", bd=2, relief=tk.GROOVE)
suggestion_frame.place(relx=0.85, rely=0.5, anchor=tk.CENTER, width=screen_width * 0.25, height=screen_height * 0.8)

# Create a Text widget for showing autocomplete suggestions
suggestion_text_widget = tk.Text(suggestion_frame, height=30, width=30, font=big_font, wrap="word", fg="black", bg="lightgray", bd=0)
suggestion_text_widget.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)

# Add a vertical scrollbar to the suggestion text widget
suggestion_scrollbar = tk.Scrollbar(suggestion_frame, command=suggestion_text_widget.yview)
suggestion_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
suggestion_text_widget.config(yscrollcommand=suggestion_scrollbar.set)

# Ensure the autocomplete suggestion widget is just for display
suggestion_text_widget.config(state="disabled")  # Make it non-editable

# Create a menu bar for Save, Open, and Model options
menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Save", command=save_to_file)  # Add Save option
file_menu.add_command(label="Save As", command=save_as)  # Add Save As option
file_menu.add_command(label="Open", command=open_file)  # Add Open option
menu_bar.add_cascade(label="File", menu=file_menu)

# Create a Model menu
model_menu = Menu(menu_bar, tearoff=0)
for model in model_options:
    model_menu.add_radiobutton(label=model, command=lambda m=model: update_model(m))
menu_bar.add_cascade(label="Model", menu=model_menu)

root.config(menu=menu_bar)  # Set the menu bar

# Bind hotkeys for saving, opening, and undo
text_widget.bind("<Control-Return>", on_ctrl_enter)
text_widget.bind("<Control-s>", on_ctrl_s)
text_widget.bind("<Control-Shift-s>", on_ctrl_shift_s)
text_widget.bind("<Control-z>", on_ctrl_z)
text_widget.bind("<Control-o>", on_ctrl_o)

# Monitor changes in the text widget
text_widget.bind("<KeyRelease>", on_text_change)

# Make sure the text widget keeps focus
text_widget.focus_set()

root.mainloop()
import os
import string
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import gui

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        gui.path_input.delete(0, tk.END)
        gui.path_input.insert(0, directory)

def filter_files(files):
    if not gui.is_filtered.get():
        return files

    type_filter = gui.type_filter_input.get().lower()
    include_filter = gui.include_filter_input.get().lower()

    filtered = []
    for file in files:
        _, ext = os.path.splitext(file)
        if (not type_filter or ext.lstrip(".") == type_filter) and (not include_filter or include_filter in file.lower()):
            filtered.append(file)
    return filtered

def rename():
    directory = gui.path_input.get()
    rename_option = gui.rename_var.get()

    if not directory:
        messagebox.showwarning("Warning", "Please select a directory.")
        return

    entries = [e for e in gui.rename_fields_frame.winfo_children() if isinstance(e, ttk.Entry)]

    if rename_option == "Remove":
        if not any([gui.remove_letters.get(), gui.remove_numbers.get(), gui.remove_special.get(), gui.specific_text_entry.get().strip()]):
            messagebox.showwarning("Warning", "Please select at least one checkbox or fill in the Specific Text field.")
            return
    else:
        if not all(e.get().strip() for e in entries):
            messagebox.showwarning("Warning", "Please fill in all required fields.")
            return

    files = os.listdir(directory)
    filtered_files = filter_files(files)

    renames = []  # to check for duplicates
    for i, file in enumerate(filtered_files):
        old_path = os.path.join(directory, file)
        root_name, ext = os.path.splitext(file)

        if rename_option == "Rename":
            new_name = f"{entries[0].get().strip()}{f'_{i+1}' if len(filtered_files) > 1 else ''}{ext}"
        elif rename_option == "Replace":
            old_value = entries[0].get().strip()
            new_value = entries[1].get().strip()
            if not any(old_value in f.lower() for f in filtered_files):
                messagebox.showwarning("Warning", f"Value '{old_value}' not found in any filenames.")
                return
            new_name = f"{root_name.lower().replace(old_value.lower(), new_value, 1)}{ext}" 
        elif rename_option == "Add":
            value_to_add = entries[0].get().strip()
            position = gui.position_var.get()
            new_name = f"{value_to_add}{root_name}{ext}" if position == "Start" else f"{root_name}{value_to_add}{ext}"
        elif rename_option == "Remove":
            chars_to_remove = ""
            if gui.remove_letters.get():
                chars_to_remove += string.ascii_letters
            if gui.remove_numbers.get():
                chars_to_remove += string.digits
            if gui.remove_special.get():
                chars_to_remove += string.punctuation.replace("_", "")  # exclude underscores
            
            new_name = root_name.translate(str.maketrans('', '', chars_to_remove))
            if gui.specific_text_entry.get().strip():  # check if input is entered
                new_name = new_name.replace(gui.specific_text_entry.get().strip(), '', 1)  # remove input (once)

            # check if filename would be empty
            if not new_name:
                messagebox.showwarning("Warning", f"Removing these characters would result in an empty filename for '{file}'.")
                continue

            new_name += ext

        new_path = os.path.join(directory, new_name)

        # check for duplicates before renaming
        if new_name in renames:
            messagebox.showwarning("Warning", f"Duplicate name '{new_name}' detected. Renaming aborted.")
            return
        renames.append(new_name)

        try:
            os.rename(old_path, new_path)
        except OSError as e:
            messagebox.showerror("Error", f"An error occurred while renaming: {e}")
            return

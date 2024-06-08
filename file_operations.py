import os
import string
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import gui

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        gui.path_entry.delete(0, tk.END)
        gui.path_entry.insert(0, directory)
        update_file_list()

def filter_files(files):
    type_filter = gui.type_filter_entry.get().lower().split(';') if gui.type_filter_var.get() else []
    include_filter = gui.include_filter_entry.get().lower()

    if not type_filter and not include_filter:
        return files

    return [file for file in files
        if (not type_filter or any(os.path.splitext(file)[1].lstrip(".") == f.strip() for f in type_filter)) and (not include_filter or include_filter in file.lower())]

def rename():
    directory = gui.path_entry.get()
    rename_option = gui.current_tab
    current_tab_frame = gui.rename_tabs[rename_option]

    if not directory:
        messagebox.showwarning("Warning", "Please select a directory.")
        return

    entries = []

    for widget in current_tab_frame.winfo_children():
        if isinstance(widget, ttk.Entry):
            entries.append(widget)
        elif isinstance(widget, ttk.Checkbutton) and rename_option == "Remove":
            if widget.instate(["selected"]): 
                entries.append(widget)

    if rename_option == "Remove":
        if (
            not any(entry.get().strip() for entry in entries if isinstance(entry, ttk.Entry)) and 
            not any(entry.instate(["selected"]) for entry in entries if isinstance(entry, ttk.Checkbutton))
        ):
            messagebox.showwarning("Warning", "Please select at least one checkbox or fill in the Specific Text field.")
            return
    else:
        if not all(e.get().strip() for e in entries):
            messagebox.showwarning("Warning", "Please fill in all required fields.")
            return

    files = os.listdir(directory)
    filtered_files = filter_files(files)

    # confirmation on >18 file changes
    if len(filtered_files) > 18:
        confirm = messagebox.askyesno(
            "Confirmation",
            f"{len(filtered_files)} files are going to be changed.\n\nDo you want to proceed?"
        )
        if not confirm:
            return

    renames = []  # to check for duplicates
    for i, file in enumerate(filtered_files):
        old_path = os.path.join(directory, file)

        # check if file (not directory)
        if not os.path.isfile(old_path):
            continue

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
            if gui.remove_specials.get():
                chars_to_remove += string.punctuation.replace("_", "")  # exclude underscores
            
            new_name = root_name.translate(str.maketrans('', '', chars_to_remove))
            if gui.remove_entry.get().strip():  # check if input is entered
                new_name = new_name.replace(gui.remove_entry.get().strip(), '', 1)  # remove input (once)

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
    update_file_list()

def update_file_list():
    directory = gui.path_entry.get()
    gui.file_list.config(state="normal")
    gui.file_list.delete("1.0", tk.END)

    if not directory or not os.path.isdir(directory):
        gui.file_list.insert(tk.END, "\n\n\n\n\n\n\n\nPlease select a path", "center")
        gui.file_list.config(state="disabled")
        return

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))] # filter out directories
    filtered_files = filter_files(files)

    rename_option = gui.current_tab
    rename_tab_frame = gui.rename_tabs[rename_option]

    entries = []
    for widget in rename_tab_frame.winfo_children():
        if isinstance(widget, ttk.Entry):
            entries.append(widget)
        elif isinstance(widget, ttk.Checkbutton) and rename_option == "Remove":
            if widget.instate(["selected"]):
                entries.append(widget)

    seen_files = set()
    if filtered_files:
        for i, file in enumerate(filtered_files):
            root_name, ext = os.path.splitext(file)
            new_name = preview_name(root_name, ext, entries, i, filtered_files)

            before_label = tk.Label(gui.file_list, image=gui.file_icon, text=f"  {file}  ", compound="left", foreground="black", background="white")
            gui.file_list.window_create(tk.END, window=before_label)

            if new_name and new_name != file and all(hasattr(e, 'get') and e.get().strip() for e in entries):
                error_occurred = (not new_name or new_name.lower() in seen_files)

                after_label_color = "red" if error_occurred else "blue"
                after_label_text = f" ->   {new_name}" if new_name else " ->   error"
                after_label = tk.Label(gui.file_list, text=after_label_text, foreground=after_label_color, background="white")
                gui.file_list.window_create(tk.END, window=after_label)

            gui.file_list.insert(tk.END, "\n", "line")

            if new_name:
                seen_files.add(new_name.lower())
    else:
        gui.file_list.insert(tk.END, "\n\n\n\n\n\n\n\nNo files found", "center")

    gui.file_list.config(state="disabled")

def preview_name(root_name, ext, entries, i, filtered_files):
    rename_option = gui.current_tab

    if rename_option == "Rename":
        return f"{entries[0].get().strip()}{f'_{i+1}' if len(filtered_files) > 1 else ''}{ext}"

    elif rename_option == "Replace":
        old_value = entries[0].get().strip()
        new_value = entries[1].get().strip()
        if not any(old_value in f.lower() for f in filtered_files):
            return None  # no change if old_value is not found
        return f"{root_name.lower().replace(old_value.lower(), new_value, 1)}{ext}"

    elif rename_option == "Add":
        value_to_add = entries[0].get().strip()
        position = gui.position_var.get()
        return f"{value_to_add}{root_name}{ext}" if position == "Start" else f"{root_name}{value_to_add}{ext}"

    elif rename_option == "Remove":
        chars_to_remove = ""
        if gui.remove_letters.get():
            chars_to_remove += string.ascii_letters
        if gui.remove_numbers.get():
            chars_to_remove += string.digits
        if gui.remove_specials.get():
            chars_to_remove += string.punctuation.replace("_", "") 

        new_name = root_name.translate(str.maketrans('', '', chars_to_remove))
        if gui.remove_entry.get().strip():
            new_name = new_name.replace(gui.remove_entry.get().strip(), '', 1)

        # handle empty
        if not new_name:
            return None
        return new_name + ext

    else:
        return None

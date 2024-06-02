import tkinter as tk
from tkinter import ttk
import file_operations

def create_main_window(root):
    root.resizable(False, False)
    root.config(borderwidth=10)

    create_path_section(root)
    create_filter_section(root)
    create_rename_section(root)

    # submit
    rename_button = ttk.Button(root, text="Submit", command=file_operations.rename)
    rename_button.grid(row=5, columnspan=3, pady=15)

def create_path_section(root):
    global path_input

    ttk.Label(root, text="Path:").grid(row=0, column=0, padx=5, pady=15, sticky="w")
    path_input = ttk.Entry(root, width=40)
    path_input.grid(row=0, column=1, padx=5, sticky="we")
    ttk.Button(root, text="Browse", command=file_operations.browse_directory).grid(row=0, column=2, padx=7, sticky="w")

def toggle_filter_fields():
    state = "normal" if is_filtered.get() else "disabled"
    type_filter_input.config(state=state)
    include_filter_input.config(state=state)

def create_filter_section(root):
    global type_filter_input, include_filter_input, is_filtered

    ttk.Label(root, text="Filter").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    is_filtered = tk.BooleanVar()
    ttk.Checkbutton(root, variable=is_filtered, command=toggle_filter_fields).grid(row=1, column=1, padx=5, sticky="w")
    ttk.Label(root, text="Type:").grid(row=2, column=0, padx=5, sticky="w")
    type_filter_input = ttk.Entry(root, width=30, state="disabled")
    type_filter_input.grid(row=2, column=1, padx=5, sticky="w")
    ttk.Label(root, text="Includes:").grid(row=2, column=1, padx=5, sticky="e")
    include_filter_input = ttk.Entry(root, width=30, state="disabled")
    include_filter_input.grid(row=2, column=2, padx=5, sticky="w")

def create_rename_section(root):
    global rename_var, rename_fields_frame

    ttk.Label(root, text="Option:").grid(row=3, column=0, padx=5, pady=20, sticky="w")
    rename_var = tk.StringVar(value="Rename")
    rename_options = ["Rename", "Replace", "Add", "Remove"]
    rename_dropdown = ttk.Combobox(root, textvariable=rename_var, values=rename_options, state="readonly", width=27)
    rename_dropdown.grid(row=3, column=1, padx=5, sticky="w")
    rename_dropdown.bind("<<ComboboxSelected>>", lambda event: handle_rename_fields())

    rename_fields_frame = ttk.Frame(root)
    rename_fields_frame.grid(row=4, column=0, columnspan=3, sticky="w")

def create_input_field(label_text, width=30, row=0, column=0):
    ttk.Label(rename_fields_frame, text=label_text).grid(row=row, column=column, padx=5, sticky="w")
    entry = ttk.Entry(rename_fields_frame, width=width)
    entry.grid(row=row, column=column + 1, padx=5, sticky="w")
    return entry

def handle_rename_fields():
    global position_var, remove_letters, remove_numbers, remove_special, specific_text_entry

    for widget in rename_fields_frame.winfo_children():
        widget.destroy()

    option = rename_var.get()
    if option == "Rename":
        create_input_field("Name: ")
    elif option == "Replace":
        create_input_field("Replace:")
        create_input_field("With:", column=2)
    elif option == "Add":
        create_input_field("Name: ")
        ttk.Label(rename_fields_frame, text="At:").grid(row=0, column=2, padx=5, sticky="w")
        position_var = tk.StringVar(value="Start")
        ttk.Combobox(rename_fields_frame, textvariable=position_var, values=["Start", "End"], state="readonly", width=27).grid(row=0, column=3, padx=5, sticky="w")
    elif option == "Remove":
        specific_text_entry = create_input_field("Remove:", row=0)
        remove_letters = tk.BooleanVar(value=False)
        ttk.Checkbutton(rename_fields_frame, text="Letters (all)", variable=remove_letters).grid(row=0, column=3, sticky="w")
        remove_numbers = tk.BooleanVar(value=False)
        ttk.Checkbutton(rename_fields_frame, text="Numbers (all)", variable=remove_numbers).grid(row=1, column=3, sticky="w")
        remove_special = tk.BooleanVar(value=False)
        ttk.Checkbutton(rename_fields_frame, text="Special Characters (all)", variable=remove_special).grid(row=2, column=3, sticky="w")

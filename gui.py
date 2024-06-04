import tkinter as tk
from tkinter import ttk
import file_operations

def create_window(root):
    root.resizable(False, False)
    root.config(borderwidth=10)

    create_sidebar(root)
    create_main(root)

def create_sidebar(root):
    sidebar_frame = ttk.Frame(root)
    sidebar_frame.grid(row=0, rowspan=12, column=0, columnspan=3, sticky="w")

    create_rename_section(sidebar_frame)

    # submit
    rename_button = ttk.Button(root, text="Submit", command=file_operations.rename)
    rename_button.grid(row=12, pady=15)

def create_main(root):
    main_frame = ttk.Frame(root)
    main_frame.grid(row=0, rowspan=12, column=5, columnspan=6, sticky="w")

    create_path_section(main_frame)
    create_filter_section(main_frame)

def create_entry_field(label_text, width=30, row=0, column=0):
    ttk.Label(rename_fields_frame, text=label_text).grid(row=row, column=column, padx=5, sticky="w")
    entry = ttk.Entry(rename_fields_frame, width=width)
    entry.grid(row=row, column=column + 1, padx=5, sticky="w")
    return entry

def handle_rename_fields():
    global position_var, remove_letters, remove_numbers, remove_specials, remove_entry

    for widget in rename_fields_frame.winfo_children():
        widget.destroy()

    option = rename_var.get()
    if option == "Rename":
        create_entry_field("Name: ")
    elif option == "Replace":
        create_entry_field("Replace:")
        create_entry_field("With:", column=2)
    elif option == "Add":
        create_entry_field("Name: ")
        ttk.Label(rename_fields_frame, text="At:").grid(row=0, column=2, padx=5, sticky="w")
        position_var = tk.StringVar(value="Start")
        ttk.Combobox(rename_fields_frame, textvariable=position_var, values=["Start", "End"], state="readonly", width=27).grid(row=0, column=3, padx=5, sticky="w")
    elif option == "Remove":
        remove_entry = create_entry_field("Remove:", row=0)
        remove_letters = tk.BooleanVar(value=False)
        ttk.Checkbutton(rename_fields_frame, text="Letters (all)", variable=remove_letters).grid(row=0, column=3, sticky="w")
        remove_numbers = tk.BooleanVar(value=False)
        ttk.Checkbutton(rename_fields_frame, text="Numbers (all)", variable=remove_numbers).grid(row=1, column=3, sticky="w")
        remove_specials = tk.BooleanVar(value=False)
        ttk.Checkbutton(rename_fields_frame, text="Special Characters (all)", variable=remove_specials).grid(row=2, column=3, sticky="w")

def toggle_filter():
    state = "normal" if is_filtered.get() else "disabled"
    type_filter_entry.config(state=state)
    include_filter_entry.config(state=state)

def create_path_section(root):
    global path_entry

    ttk.Label(root, text="Path:").grid(row=0, column=0, padx=5, pady=15, sticky="w")
    path_entry = ttk.Entry(root, width=40)
    path_entry.grid(row=0, column=1, padx=5, sticky="we")
    ttk.Button(root, text="Browse", command=file_operations.browse_directory).grid(row=0, column=2, padx=7, sticky="w")

def create_filter_section(root):
    global type_filter_entry, include_filter_entry, is_filtered

    ttk.Label(root, text="Filter").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    is_filtered = tk.BooleanVar()
    ttk.Checkbutton(root, variable=is_filtered, command=toggle_filter).grid(row=1, column=1, padx=5, sticky="w")
    ttk.Label(root, text="Type:").grid(row=2, column=0, padx=5, sticky="w")
    type_filter_entry = ttk.Entry(root, width=30, state="disabled")
    type_filter_entry.grid(row=2, column=1, padx=5, sticky="w")
    ttk.Label(root, text="Includes:").grid(row=2, column=1, padx=5, sticky="e")
    include_filter_entry = ttk.Entry(root, width=30, state="disabled")
    include_filter_entry.grid(row=2, column=2, padx=5, sticky="w")

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

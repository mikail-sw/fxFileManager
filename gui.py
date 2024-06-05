import tkinter as tk
from tkinter import ttk
import file_operations

def create_window(root):
    root.geometry("900x450")
    root.resizable(False, False)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=2)
    root.grid_columnconfigure(1, weight=6)

    create_sidebar(root)
    create_main(root)

def create_sidebar(root):
    global rename_tabs, rename_options

    sidebar_frame = ttk.Frame(root)
    sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
    sidebar_frame.grid_rowconfigure(4, weight=1)

    style = ttk.Style()
    style.configure("Main.TFrame", background="grey")
    style.layout("TNotebook", [("Notebook.tab", {"sticky": "nswe"})])
    style.configure("TNotebook.Tab", padding=5)
    style.configure("Custom.TCheckbutton", background="grey")

    # tabs
    notebook = ttk.Notebook(sidebar_frame, style="TNotebook")
    notebook.grid(row=0, column=0, sticky="nsew")
    rename_tabs = {}  
    rename_options = ["Rename", "Replace", "Add", "Remove"]
    for option in rename_options:
        tab_frame = ttk.Frame(notebook, padding=(15, 35, 0, 0))
        notebook.add(tab_frame, text=option)
        rename_tabs[option] = tab_frame

    notebook.bind("<<NotebookTabChanged>>", on_tab_change)

    # submit button
    rename_button = ttk.Button(sidebar_frame, text="Submit", command=file_operations.rename)
    rename_button.grid(row=6, column=0, columnspan=2, pady=20, sticky="s")

def create_main(root):
    global file_list

    main_frame = ttk.Frame(root, style="Main.TFrame")
    main_frame.grid(row=0, column=1, sticky="nsew")

    create_path_section(main_frame)
    create_filter_section(main_frame)

    # overview
    file_list = tk.Text(main_frame, wrap="word", padx=10, pady=10)
    file_list.grid(row=2, column=0, columnspan=7, padx=(10, 30), pady=10, sticky="w")
    file_list.tag_configure("center", justify="center")
    file_list.tag_configure("line", spacing3=5)
    main_frame.grid_rowconfigure(2, weight=1)

    file_operations.update_file_list()

def create_entry_field(parent_frame, label_text, width=30, row=0, column=0):
    ttk.Label(parent_frame, text=label_text).grid(row=row, column=column, pady=(15, 0), sticky="w")
    entry = ttk.Entry(parent_frame, width=width)
    entry.grid(row=row + 1, column=column, pady=5, sticky="w")
    return entry

def toggle_filter():
    state = "normal" if is_filtered.get() else "disabled"
    type_filter_entry.config(state=state)
    include_filter_entry.config(state=state)

def on_tab_change(event):
    global current_tab, position_var, remove_letters, remove_numbers, remove_specials, remove_entry

    current_tab = event.widget.tab(event.widget.select(), "text") if event else rename_options[0]

    # Clear existing fields in the current tab
    for widget in rename_tabs[current_tab].winfo_children():
        widget.destroy()

    # Create the appropriate fields based on the selected tab
    if current_tab == "Rename":
        create_entry_field(rename_tabs[current_tab], "Name:")
    elif current_tab == "Replace":
        create_entry_field(rename_tabs[current_tab], "Replace:")
        create_entry_field(rename_tabs[current_tab], "With:", row=2,)
    elif current_tab == "Add":
        create_entry_field(rename_tabs[current_tab], "Name:")
        ttk.Label(rename_tabs[current_tab], text="At:").grid(row=2, column=0, pady=(15, 0), sticky="w")
        position_var = tk.StringVar(value="Start")
        ttk.Combobox(rename_tabs[current_tab], textvariable=position_var, values=["Start", "End"], state="readonly", width=27).grid(row=3, column=0, pady=5, sticky="w")
    elif current_tab == "Remove":
        remove_entry = create_entry_field(rename_tabs[current_tab], "Remove:")
        remove_letters = tk.BooleanVar(value=False)
        ttk.Checkbutton(rename_tabs[current_tab], text="Letters (all)", variable=remove_letters).grid(row=2, column=0, pady=(15, 3), sticky="w")
        remove_numbers = tk.BooleanVar(value=False)
        ttk.Checkbutton(rename_tabs[current_tab], text="Numbers (all)", variable=remove_numbers).grid(row=3, column=0, pady=3, sticky="w")
        remove_specials = tk.BooleanVar(value=False)
        ttk.Checkbutton(rename_tabs[current_tab], text="Special Characters (all)", variable=remove_specials).grid(row=4, column=0, pady=3, sticky="w")

def create_path_section(root):
    global path_entry

    ttk.Label(root, text="Path:", background="grey", foreground="white").grid(row=0, column=0, padx=(10,5), pady=7, sticky="w")
    path_entry = ttk.Entry(root)
    path_entry.grid(row=0, column=1, columnspan=5, pady=7, sticky="we")
    ttk.Button(root, text="Browse", command=file_operations.browse_directory, style="Custom.TButton").grid(row=0, column=6,padx=(10,20), pady=7, sticky="w")

def create_filter_section(root):
    global type_filter_entry, include_filter_entry, is_filtered

    ttk.Label(root, text="Filter", background="grey", foreground="white").grid(row=1, column=0, padx=(10,5), pady=5, sticky="w")
    is_filtered = tk.BooleanVar()
    ttk.Checkbutton(root, variable=is_filtered, command=toggle_filter, style="Custom.TCheckbutton").grid(row=1, column=1, padx=5, sticky="w")
    ttk.Label(root, text="Type:", background="grey", foreground="white").grid(row=1, column=2, padx=5, sticky="w")
    type_filter_entry = ttk.Entry(root, width=15, state="disabled")
    type_filter_entry.grid(row=1, column=3, padx=5, sticky="w")
    ttk.Label(root, text="Includes:", background="grey", foreground="white").grid(row=1, column=4, padx=5, sticky="w")
    include_filter_entry = ttk.Entry(root, width=30, state="disabled")
    include_filter_entry.grid(row=1, column=5, padx=5, sticky="w")

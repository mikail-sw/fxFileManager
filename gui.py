import tkinter as tk
from tkinter import ttk
import file_operations

def create_window(root):
    root.resizable(False, False)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=2)
    root.grid_columnconfigure(1, weight=6)

    style_config()

    create_sidebar(root)
    create_main(root)

def create_sidebar(root):
    sidebar_frame = ttk.Frame(root, style="Main.TFrame")
    sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
    sidebar_frame.grid_rowconfigure(4, weight=1)

    create_tabs(sidebar_frame)

    # submit
    rename_button = ttk.Button(sidebar_frame, text="submit", command=file_operations.rename)
    rename_button.grid(row=6, column=0, columnspan=2, pady=20, sticky="s")

def create_main(root):
    main_frame = ttk.Frame(root, style="Main.TFrame")
    main_frame.grid(row=0, column=1, sticky="nsew")

    create_path_section(main_frame)
    create_filter_section(main_frame)
    create_overview_section(main_frame)

    file_operations.update_file_list()

def create_entry_field(parent_frame, label_text, width=30, row=0, column=0):
    ttk.Label(parent_frame, text=label_text).grid(row=row, column=column, pady=(15, 0), sticky="w")
    entry = ttk.Entry(parent_frame, width=width)
    entry.grid(row=row + 1, column=column, pady=5, sticky="w")

    entry.bind("<KeyRelease>", lambda event: file_operations.update_file_list()) 

    return entry

def on_tab_change(event):
    global current_tab, position_var, remove_letters, remove_numbers, remove_specials, remove_entry

    current_tab = event.widget.tab(event.widget.select(), "text") if event else rename_options[0]

    for widget in rename_tabs[current_tab].winfo_children():
        widget.destroy()

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
        
        position_var.trace_add("write", lambda *args: file_operations.update_file_list())

    elif current_tab == "Remove":
        remove_entry = create_entry_field(rename_tabs[current_tab], "Remove:")
        remove_letters = tk.BooleanVar(value=False)
        ttk.Checkbutton(rename_tabs[current_tab], text="Letters (all)", variable=remove_letters).grid(row=2, column=0, pady=(15, 3), sticky="w")
        remove_numbers = tk.BooleanVar(value=False)
        ttk.Checkbutton(rename_tabs[current_tab], text="Numbers (all)", variable=remove_numbers).grid(row=3, column=0, pady=3, sticky="w")
        remove_specials = tk.BooleanVar(value=False)
        ttk.Checkbutton(rename_tabs[current_tab], text="Special Characters (all)", variable=remove_specials).grid(row=4, column=0, pady=3, sticky="w")

        for var in [remove_letters, remove_numbers, remove_specials]:
            var.trace_add("write", lambda *args: file_operations.update_file_list())

    file_operations.update_file_list()

def create_tabs(root):
    global rename_tabs, rename_options
    
    notebook = ttk.Notebook(root, style="TNotebook")
    notebook.grid(row=0, column=0, sticky="nsew")
    
    rename_tabs = {}  
    rename_options = ["Rename", "Replace", "Add", "Remove"]
    for option in rename_options:
        tab_frame = ttk.Frame(notebook, padding=(15, 35, 0, 0))
        notebook.add(tab_frame, text=option)
        rename_tabs[option] = tab_frame

    notebook.bind("<<NotebookTabChanged>>", on_tab_change)

def create_path_section(root):
    global path_entry

    ttk.Label(root, text="Path:", background="grey", foreground="white").grid(row=0, column=0, padx=(10,5), pady=7, sticky="w")
    path_entry = ttk.Entry(root)
    path_entry.grid(row=0, column=1, columnspan=5, pady=7, sticky="we")
    ttk.Button(root, text="search", command=file_operations.browse_directory, style="Custom.TButton").grid(row=0, column=6,padx=(10,20), pady=7, sticky="w")

def create_filter_section(root):
    global type_filter_entry, include_filter_entry, type_filter_var, include_filter_var

    ttk.Label(root, image=filter_icon, background="grey").grid(row=1, column=0, padx=(10,0), pady=5, sticky="w")

    type_filter_var = tk.StringVar()
    type_filter_var.trace_add("write", lambda *args: file_operations.update_file_list())

    ttk.Label(root, text="Type:", background="grey", foreground="white").grid(row=1, column=1, sticky="w")
    type_filter_entry = ttk.Entry(root, width=20, textvariable=type_filter_var)
    type_filter_entry.grid(row=1, column=2, sticky="w")

    include_filter_var = tk.StringVar()
    include_filter_var.trace_add("write", lambda *args: file_operations.update_file_list())

    ttk.Label(root, text="Includes:", background="grey", foreground="white").grid(row=1, column=3, sticky="w")
    include_filter_entry = ttk.Entry(root, width=30, textvariable=include_filter_var)
    include_filter_entry.grid(row=1, column=4, sticky="w")

def create_overview_section(root):
    global file_list

    file_list = tk.Text(root, wrap="word", padx=10, pady=10, background="white", foreground="black")
    file_list.grid(row=2, column=0, columnspan=7, padx=10, pady=10, sticky="nswe")
    file_list.tag_configure("center", justify="center")
    file_list.tag_configure("line", spacing3=5)
    root.grid_rowconfigure(2, weight=1)

def style_config():
    global filter_icon, folder_icon, file_icon, arrow_icon

    style = ttk.Style()
    style.configure("Main.TFrame", background="grey")
    style.layout("TNotebook", [("Notebook.tab", {"sticky": "nswe"})])
    style.configure("TNotebook.Tab", padding=5)
    style.configure("Custom.TCheckbutton", background="grey")

    filter_icon = tk.PhotoImage(file="./assets/filter.png").subsample(2, 2)
    file_icon = tk.PhotoImage(file="./assets/file.png").subsample(2, 2)

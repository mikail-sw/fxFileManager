# fxFileManager: A File Management Tool for Production Workflows

A simple yet powerful file managment tool built with Python and Tkinter, specifically designed to simplify the often complex conventions and workflows in VFX and production.

## Introduction

Tired of manually managing files one by one? `fxFileManager` automates this tedious task, offering a user-friendly interface for various renaming operations and filtering capabilities to precisely target the files you want to modify.

## Features

- **Directory Selection:**
    - Browse and select the target directory using a file dialog or manually enter the path.
- **Filtering Options:**
    - Narrow down your selection by the file type (e.g., `.txt`, `.jpg`, `.mp3`)
    - Refine further by specifying text that must be included in the filenames.
- **Rename Options:**
    - **Rename:** Replace the entire filename with a new one, with an optional incrementing counter for multiple files (e.g., "document_1", "document_2").
    - **Replace:** Find and replace specific text within filenames.
    - **Add:** Insert text at the beginning (prefix) or end (suffix) of filenames.
    - **Remove:** Eliminate unwanted elements from filenames:
        - Letters (all)
        - Numbers (all)
        - Special characters (excluding underscores)
        - A specific text string

## How to Use

1. **Prerequisites:**
   - Python 3.x installed
   - This repository cloned or downloaded
   
2. **Running the Application:**
   - **Open a terminal or command prompt.**
   - **Navigate to the project directory:**
     ```bash
     cd path/to/fxFileManager
     ```
   - **Run the main script:**
     ```bash
     python main.py
     ```

3. **Using the Interface:**

   - **Path Selection:**
     - Click the "Browse" button to choose a directory.
     - Alternatively, type the directory path directly into the entry field.
   - **Filtering (Optional):**
     - Enable filtering by checking the "Filter" checkbox.
     - Specify the desired file type in the "Type" field (e.g., "txt").
     - Enter text to match in the "Includes" field.
   - **Rename Options:**
     - Select the desired action ("Rename", "Replace", "Add", or "Remove") from the dropdown.
     - Fill in the required fields based on your chosen action:
       - **Rename:** Enter the new base name.
       - **Replace:** Enter the text to replace and the replacement text.
       - **Add:** Enter the text to add and choose "Start" or "End".
       - **Remove:** Select the removal options (checkboxes and/or "Specific Text" field).
   - **Submit:**
     - Click the "Submit" button to apply the renaming changes.

## Examples
- Rename files to "document_1", "document_2", etc.:
  - Choose "Rename".
  - Enter "document" in the "New Name" field.
- Replace all instances of "old_" with "new_" in filenames:
  - Choose "Replace".
  - Enter "old_" in the "Replace" field and "new_" in the "With" field.
- Add the prefix "prefix_" to all filenames:
  - Choose "Add".
  - Enter "prefix_" in the "Value to Add" field and select "Start".
- Remove all numbers from filenames:
  - Choose "Remove".
  - Check the "Numbers" checkbox.

## Error Handling

The tool includes checks for:
- Empty or invalid input fields.
- Replace value not found in filenames.
- Renaming that would result in empty filenames.
- Duplicate filenames after renaming.

You'll receive a message box if any of these errors occur.

## Future Enhancements

- Packaging and Distribution:
  - Create an easy-to-use installer or executable.
- User Interface:
  - Add tooltips or help text to guide users.
- File Renamer:
  - Support for regular expressions in filtering and replacing.
  - Undo/redo functionality.
  - Batch processing of multiple directories.
  - Additional renaming actions:
    - Case conversion (e.g., lowercase, UPPERCASE, Title Case)
    - Date/time insertion or modification
    - Number formatting (e.g., leading zeros)
    - Customizable renaming templates
- Advanced File Management:
  - File/folder sorting and organizing tools.
  - Bulk file moving and copying.
  - Duplicate file detection and removal.
  - Integration with cloud storage services (e.g., Dropbox, Google Drive).
  - File/folder tagging and categorization.
- **VFX-Specific Enhancements:**
  - Render Layer and AOV Naming: Support for standardized naming conventions for render layers and AOVs.
  - Slate/Burn-in Integration: Automate the extraction of information from slates or burn-ins to use in file renaming.
  - Frame Padding: Add options for padding frame numbers with zeros.
  - Integration with Shot Management: Link renaming actions to shot information in project management software.

## Contributing
At this stage, the project is not yet open to contributions. However, I welcome feedback and suggestions for future enhancements. You can open an issue or reach out to me directly to share your ideas.

## License
This project is currently not released under an open-source license. The code is available for reference and learning purposes.

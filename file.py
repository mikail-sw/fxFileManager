import os

class File:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.root_name, self.ext = os.path.splitext(self.name)
        self.preview_name = None

    def get_renamed_name(self, rename_option, rename_params):
        new_root_name = self.root_name

        if rename_option == "Rename":
            new_root_name = rename_params["new_name"]
            new_root_name += (
                f"_{rename_params['file_index'] + 1}"
                if rename_params.get("append_number")
                else ""
            )
        elif rename_option == "Replace":
            old_value, new_value = rename_params["old_value"], rename_params["new_value"]
            new_root_name = self.root_name.replace(old_value, new_value, 1)
        elif rename_option == "Add":
            value_to_add, position = rename_params["value_to_add"], rename_params["position"]
            new_root_name = (
                f"{value_to_add}{self.root_name}"
                if position == "Start"
                else f"{self.root_name}{value_to_add}"
            )
        elif rename_option == "Remove":
            chars_to_remove = "".join(
                c
                for c, remove in rename_params.items()
                if remove and c in ["letters", "numbers", "specials"]
            )
            if chars_to_remove:  # check if any characters are to be removed
                new_root_name = self.root_name.translate(str.maketrans("", "", chars_to_remove))
            specific_text = rename_params.get("specific_text")
            if specific_text:
                new_root_name = new_root_name.replace(specific_text, "", 1)

        # check empty
        new_root_name = new_root_name if new_root_name else self.root_name 

        return f"{new_root_name}{self.ext}"

import re
import argparse

from typing import Dict, Any


def input_file_to_str(path: str) -> str:
    """Reads the content of a file from the given path and returns it as a string."""
    with open(path, 'r', encoding="utf-8") as f:
        return f.read()


def delete_comments(input_data: str) -> str:
    """Removes single-line and multi-line comments from the provided input data."""
    filter_single_comments = re.sub(
        r'^\".*$', '', input_data, flags=re.MULTILINE)
    filter_multi_comments = re.sub(
        r'\(\*\s*.*?\s*\*\)', '', filter_single_comments, flags=re.DOTALL)
    return filter_multi_comments


def parse_globals(input_data: str) -> Dict[str, Any]:
    """Parses global constants from the input data string and returns them as a dictionary."""
    globals = {}
    matches = re.findall(
        r'\s+([a-zA-Z][_a-zA-Z0-9]*)\s*:=\s*("[^"]*"|\d+|true|false)', input_data)
    for name, value in matches:
        if value.isdigit():
            globals[name] = int(value)
        elif value == "true":
            globals[name] = True
        elif value == "false":
            globals[name] = False
        else:
            globals[name] = value.strip('"')
    return globals


def parse_dict(input_data: str, globals_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Converts a configuration language string into a dictionary."""
    output = {}

    sections = re.findall(r'(\w+)\s*=\s*{([^}]*)}', input_data)

    for section_key, section_content in sections:
        items = {}

        for item in re.findall(r'([a-zA-Z][_a-zA-Z0-9]*)\s*=\s*(?:(?:"([^"]*)")|(?:\.([^.]*)\.)|(\d+)|(\w+));', section_content):
            item_key = item[0]
            item_value = None

            if item[1]:    # String value
                item_value = item[1]
            elif item[2]:  # Globals const
                global_key = item[2]
                item_value = globals_dict.get(global_key, None)
            elif item[3]:  # Number
                item_value = int(item[3])
            elif item[4]:  # Boolean
                if item[4].lower() == "true":
                    item_value = True
                elif item[4].lower() == "false":
                    item_value = False

            items[item_key] = item_value

        output[section_key] = items

    return output


def dict_to_toml(data: Dict[str, Any], depth: int = 0) -> str:
    toml_str = ""
    indent = "  " * depth

    for key, value in data.items():
        if isinstance(value, dict):
            toml_str += f"\n{indent}[{key}]\n"
            toml_str += dict_to_toml(value, depth + 1)
        elif isinstance(value, str):
            toml_str += f'{indent}{key} = "{value}"\n'
        elif isinstance(value, bool):
            toml_str += f"{indent}{key} = {'true' if value else 'false'}\n"
        elif isinstance(value, (int, float)):
            toml_str += f"{indent}{key} = {value}\n"
        else:
            raise ValueError(f"Unsupported type for TOML: {type(value)}")

    return toml_str


def main():
    parser = argparse.ArgumentParser(description="EduConfigParser")
    parser.add_argument("path", help="Path to the input file")
    path = parser.parse_args().path
    
    input = input_file_to_str(path)
    input_without_comments = delete_comments(input)
    globals = parse_globals(input_without_comments)
    dict = parse_dict(input_without_comments, globals)
    toml_str = dict_to_toml(dict)
    print(toml_str)


if __name__ == "__main__":
    main()

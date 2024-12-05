import re

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


def main():
    path = "example.txt"
    input = input_file_to_str(path)
    output = delete_comments(input)
    print(output)


if __name__ == "__main__":
    main()

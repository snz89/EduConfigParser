import re


def input_file_to_str(path: str) -> str:
    with open(path, 'r', encoding="utf-8") as f:
        return f.read()


def delete_comments(input_data: str) -> str:
    filter_single_comments = re.sub(
        r'^\".*$', '', input_data, flags=re.MULTILINE)
    filter_multi_comments = re.sub(
        r'\(\*\s*.*?\s*\*\)', '', filter_single_comments, flags=re.DOTALL)
    return filter_multi_comments


def main():
    path = "example.txt"
    input = input_file_to_str(path)
    output = delete_comments(input)
    print(output)


if __name__ == "__main__":
    main()

# EduConfigParser
 
Сommand-line tool that processes a custom configuration language and converts it into the TOML format. The tool removes comments, parses constants and dictionaries, resolves global constants, and generates valid TOML output.

## Features

- **Comment Removal:** Supports single-line `(")` and multi-line `((* ... *))` comments.
- **Global Constants:** Parses and resolves constants declared using the := operator.
- **Nested Dictionaries:** Processes nested configuration dictionaries and converts them into TOML sections.

## Installation

1. Clone the repository:

```
git clone https://github.com/snz89/EduConfigParser.git
cd EduConfigParser
```

2. Run the script:

```
python -m src.main example.txt
```

## Usage

1. Create an input file, for example, `example.txt`:

```
(*
This is a comment
*)
db_name := "test_db"

{
    database_config = {
        host = "127.0.0.1";
        port = 5432;
        db_name = .db_name.;
    }
}
```

2. Run the script:

```
python -m src.main example.txt
```

3. Example output:

```toml
[database_config]
  host = "127.0.0.1"
  port = 5432
  db_name = "test_db"
```

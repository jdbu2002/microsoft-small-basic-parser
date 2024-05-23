# Microsoft Small Basic Parser

This is the repository used for the lexer and parser of the Microsoft Small Basic language.
This project is part of the first deliveries of the Programming Languages Course at the Universidad Nacional de Colombia.

## Technologies Used

| Type       | Technology                                       |
| ---------- | ------------------------------------------------ |
| Language   | [Python](https://www.python.org/) 🐍             |
| Formatting | [Flake8](https://flake8.pycqa.org/en/latest/) 🧹 |

## Execute the code

To execute the code, you need to have Python installed on your computer. You can download it from the [official website](https://www.python.org/).

To run the code, you need to execute the following command:

```bash
python src/main.py
```

Also, there are two folders in the repository, `in` and `out`. The first one must contain the grammar file (`grammar.txt`) and a test file (`test.txt`) to check if the test is syntactically correct; the second one will contain the output of the parser.

You can customize the outputs in the `parser.py` file changing the boolean flags in the `main` function with the `prints` function parameters.

You can also change the empty string and end of file tokens in the `parser.py` file.
And define the main rule in the `parser.py` file. (`START`)

## Grammar

The grammar should have the following format:

```
# This creates a non-terminal definition
<non-terminal> -> <production>

# This creates two definitions of a same non-terminal
<non-terminalA> -> <production>
<non-terminalA> -> <production>

# Tokens must be in UPPERCASE
<non-terminal> -> TOKEN

# The empty string is '' (can be customized by changing the code)
<non-terminal> -> ''

# The end of the file is represented by the token $ (can be customized by changing the code)
<non-terminal> -> $
```

The grammar must be LL(1) to work. I made a checker to verify if the grammar is LL(1) or not.
It worked for me, but perhaps it has its limitations. If you find a false-positive or false-negative, please let me know.

import re

from syn_token import Token

sym = {
    "=": "equals",
    ".": "period",
    ",": "comma",
    ":": "colon",
    "[": "left_brac",
    "]": "right_brac",
    "(": "left_paren",
    ")": "right_paren",
    "+": "plus",
    "-": "minus",
    "*": "times",
    "/": "div",
    "<>": "diff",
    "<": "less",
    "<=": "leq",
    ">": "greater",
    ">=": "geq",
}
keywords = {
    "For",
    "EndFor",
    "To",
    "Step",
    "If",
    "Then",
    "Else",
    "ElseIf",
    "EndIf",
    "Goto",
    "Sub",
    "EndSub",
    "While",
    "EndWhile",
    "And",
    "Or",
    "TextWindow",
    "Array",
    "Stack",
    "Program",
}

text = '(?P<Text>"[^"]*")'
comment = "(?P<Comment>'.*)"
ident = "(?P<Id>[a-zA-ZÀ-ÿ]\w*)"
number = "(?P<Number>\d+(\.\d*)?)"
diff = "(?P<Diff>(<(>|=)?|>(=)?))"
special = "(?P<Special>\S)"

tokens = []


def throw_lexical_error(row, col):
    print(f">>> Error lexico (Linea: {str(row)}, Posicion: {str(col)})")


def lexer(row, line):
    final_pattern = "|".join([comment, text, number, diff, ident, special])
    for tkn in re.finditer(final_pattern, line):
        if tkn.lastgroup == "Comment":
            continue
        elif tkn.lastgroup == "Text":
            value = tkn.group()
            if value.lower() == '"true"':
                token = Token(row, tkn.start() + 1, "Null", "True")
            elif value.lower() == '"false"':
                token = Token(row, tkn.start() + 1, "Null", "False")
            else:
                value = value[1:-1]
                token = Token(row, tkn.start() + 1, value, "tkn_text")
        elif tkn.lastgroup == "Number":
            token = Token(row, tkn.start() + 1, tkn.group(), "tkn_number")
        elif tkn.lastgroup == "Id":
            if tkn.group() in keywords:
                token = Token(row, tkn.start() + 1, "Null", tkn.group())
            else:
                token = Token(row, tkn.start() + 1, tkn.group(), "id")
        elif tkn.lastgroup == "Diff" or tkn.group() in sym.keys():
            tkn_type = "tkn_" + sym[tkn.group()]
            token = Token(row, tkn.start() + 1, "Null", tkn_type)
        else:
            throw_lexical_error(row, tkn.start() + 1)
            return "Error"
        tokens.append(token)


def main():
    with open("./out/test.txt", "r") as f:
        row = 0

        for line in f:
            row += 1
            lexon = lexer(row, line)
            if lexon == "Error":
                break

    with open("./out/tokens.txt", "w") as f:
        for token in tokens:
            f.write(f"{token}\n")

    return tokens

from syn_token import Token

grammar: dict[str, list[str]] = {}
first_sets: dict[str, set[str]] = {}
follow_sets: dict[str, set[str]] = {}
prediction_sets: dict[str, list[set[str]]] = {}
tokens = []

stack_updates = []

EMPTY = "''"
START = "inicio"


def print_stacks():
    with open("./out/stack_updates.txt", "w") as f:
        for stack_update in stack_updates:
            f.write(f"{stack_update}\n")


def set_grammar():
    with open("./in/grammar.txt", "r") as f:
        for line in f:
            line = line.strip()

            if line == "":
                continue

            rule, phrase = line.split("->")
            rule = rule.strip()
            phrase = phrase.strip()

            if rule in grammar:
                grammar[rule].append(phrase)
            else:
                grammar[rule] = [phrase]


def set_sets():
    for rule in grammar:
        first_sets[rule] = set()
        follow_sets[rule] = set()


def generate_first_set(rule: str):
    if len(first_sets[rule]) > 0:
        return

    first_set: set[str] = set()

    for phrase in grammar[rule]:
        first_set = first_set.union(generate_first(phrase))

    first_sets[rule] = first_set


def generate_first(phrase: str):
    part = phrase.split(" ")[0]

    if part.islower():
        generate_first_set(part)
        check_set = first_sets[part].copy()

        if EMPTY in check_set and len(check_set) != 1:
            cutted = phrase.split(" ", 1)[1]
            cut_phrase = cutted if len(phrase.split(" ")) > 1 else EMPTY
            second_set = generate_first(cut_phrase)
            check_set.remove(EMPTY)
            check_set = check_set.union(second_set)

        return check_set

    return {part}


def generate_follow_set(rule: str, rule_list: list[str] = []):
    if rule in rule_list:
        return
    if len(follow_sets[rule]) > 0:
        return
    if rule == START:
        follow_sets[rule] = {"$"}

    follow_set: set[str] = set()

    for some_rule, phrases in grammar.items():
        for phrase in phrases:
            word_list = phrase.split(" ")

            while rule in word_list:
                index = word_list.index(rule)
                word_list = word_list[index + 1 :]

                part = " ".join(word_list)
                check_set: set[str] = set()

                if part != "":
                    check_set = generate_first(part)
                    follow_set = follow_set.union(check_set)

                if part == "" or EMPTY in check_set:

                    if EMPTY in follow_set:
                        follow_set.remove(EMPTY)

                    generate_follow_set(some_rule, rule_list + [rule])
                    follow_set = follow_set.union(follow_sets[some_rule])

    follow_sets[rule] = follow_set


def generate_prediction_sets():
    for rule, phrases in grammar.items():
        prediction_sets[rule] = []

        for phrase in phrases:
            prediction_sets[rule].append(generate_first(phrase))

            if EMPTY in prediction_sets[rule][-1]:
                prediction_sets[rule][-1].remove(EMPTY)
                prediction_sets[rule][-1] = prediction_sets[rule][-1].union(
                    follow_sets[rule]
                )


def printer(filename: str, data):
    with open(filename, "w") as f:
        for x, v in data.items():
            f.write(f"{x}:\n")
            for y in v:
                f.write(f"\t{y}\n")


def printers(first=False, follow=False, prediction=False):
    if first:
        printer("./out/first_sets.txt", first_sets)

    if follow:
        printer("./out/follow_sets.txt", follow_sets)

    if prediction:
        printer("./out/prediction_sets.txt", prediction_sets)


def ll1_checker():
    for _, prediction_set_list in prediction_sets.items():
        test_set = set()

        for prediction_set in prediction_set_list:
            test_set = test_set.intersection(prediction_set)

        if len(test_set) != 0:
            raise TypeError("Grammar is not LL1")


def get_tokens():
    with open("./out/tokens.txt", "r") as f:
        return [token.strip() for token in f]


def get_symbol(token_type: str):
    token_type = token_type.upper()
    SYMBOLS = {
        "ID": "Identificador",
        "TKN_EQUALS": "=",
        "TKN_PERIOD": ".",
        "TKN_COMMA": ",",
        "TKN_COLON": ":",
        "TKN_LEFT_BRAC": "[",
        "TKN_RIGHT_BRAC": "]",
        "TKN_LEFT_PAREN": "(",
        "TKN_RIGHT_PAREN": ")",
        "TKN_PLUS": "+",
        "TKN_MINUS": "-",
        "TKN_TIMES": "*",
        "TKN_DIV": "/",
        "TKN_DIFF": "<>",
        "TKN_LESS": "<",
        "TKN_LEQ": "<=",
        "TKN_GREATER": ">",
        "TKN_GEQ": ">=",
        "TRUE": "Verdadero",
        "FALSE": "Falso",
        "TKN_NUMBER": "Numero",
        "TKN_TEXT": "Texto",
        "FOR": "For",
        "ENDFOR": "EndFor",
        "TO": "To",
        "STEP": "Step",
        "IF": "If",
        "THEN": "Then",
        "ELSE": "Else",
        "ELSEIF": "ElseIf",
        "ENDIF": "EndIf",
        "GOTO": "Goto",
        "SUB": "Sub",
        "ENDSUB": "EndSub",
        "WHILE": "While",
        "ENDWHILE": "EndWhile",
        "AND": "And",
        "OR": "Or",
        "TEXTWINDOW": "TextWindow",
        "ARRAY": "Array",
        "STACK": "Stack",
        "PROGRAM": "Program",
        "$": "EOF",
    }

    return f"'{SYMBOLS[token_type]}'"


def update_stack(rule: str, phrase: str):
    if phrase == EMPTY:
        phrase = ""

    global stack

    stack = stack.replace(rule, phrase, 1).strip()
    stack_updates.append(stack)


def throw_syntax_error(token: Token, expected_set: set[str]):
    lexeme = ""

    if token.lexeme != "Null":
        if token.type == "$":
            lexeme = " el final del archivo"
        else:
            lexeme = f": '{token.lexeme}'"
    else:
        lexeme = f": {get_symbol(token.type)}"

    expected_list = list(expected_set)
    expected_list = list(map(get_symbol, expected_list))
    expected_list.sort()
    expected = ", ".join(expected_list)

    print(
        f"[{token.row}:{token.column}] Error sintactico: Se encontro{lexeme};"
        f"se esperaba: {expected}."
    )
    print_stacks()
    exit()


def find_rule_phrase(rule: str):
    global current_token
    global stack
    expected_set: set[str] = set()
    see_follow = False

    for index, phrase in enumerate(grammar[rule]):
        prediction_set = prediction_sets[rule][index]

        see_follow = see_follow or phrase == EMPTY

        if phrase != EMPTY:
            expected_set = expected_set.union(prediction_set)

        if current_token.type.upper() in prediction_set:
            return (rule, phrase)

    if see_follow:
        update_stack(rule, "")
        expected_set = expected_set.union(generate_first(stack))

    throw_syntax_error(current_token, expected_set)

    return ("None", "None")


def match_phrase(phrase: str):
    global current_token
    global tokens
    global stack
    word_list = phrase.split(" ")

    for word in word_list:
        if word.islower():
            rule_phrase = find_rule_phrase(word)
            update_stack(word, rule_phrase[1])
            match_phrase(rule_phrase[1])
            continue

        if word == EMPTY:
            continue

        if current_token.type.upper() != word:
            throw_syntax_error(current_token, {word})
            return

        if len(tokens) == 0:
            if word == "$":
                return

            throw_syntax_error(current_token, {word})
            return

        current_token = tokens.pop(0)
        update_stack(word, "")


def parser():
    global current_token
    global tokens
    global stack

    current_token = tokens.pop(0)
    stack = f"{START} $"

    rule_phrase = find_rule_phrase(START)
    update_stack(START, rule_phrase[1])
    match_phrase(rule_phrase[1])

    print("El analisis sintactico ha finalizado exitosamente.")


def add_eof():
    global tokens
    final_token: Token = tokens[-1]
    tokens.append(Token(final_token.row + 1, 1, "EOF", "$"))


def main(tokens2: list[Token]):
    set_grammar()
    set_sets()

    for rule in grammar:
        generate_first_set(rule)

    for rule in grammar:
        generate_follow_set(rule)

    generate_prediction_sets()

    printers(True, True, True)

    ll1_checker()

    global tokens
    tokens = tokens2

    add_eof()

    parser()

    print_stacks()

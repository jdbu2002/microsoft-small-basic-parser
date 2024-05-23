from lexer import main as lexer
from syn_parser import main as parser


def main():
    tokens = lexer()
    parser(tokens)


if __name__ == "__main__":
    main()

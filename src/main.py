from src.forth_ast import AbstractSyntaxTree
from src.forth_lexer import ForthLex
from src.forth_parser import ForthParser


def main():
    lexer = ForthLex().build()
    parser = ForthParser(lexer)

    while True:
        try:
            s = input("forth >> ")
        except (EOFError, KeyboardInterrupt):
            break
        if not s:
            continue

        result: AbstractSyntaxTree = parser.parse(s)
        if result:
            print(result.evaluate())


if __name__ == "__main__":
    main()

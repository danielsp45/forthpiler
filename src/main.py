from src.forthparser import ForthParser
from src.forthlex import ForthLex


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
        result = parser.parse(s)
        if result:
            print(result)


if __name__ == "__main__":
    main()

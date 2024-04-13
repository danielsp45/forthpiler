import ply.yacc as yacc
from forthlex import ForthLex
from forthparser import ForthParser


def main():
    # Usage example:
    if __name__ == "__main__":
        from forthlex import ForthLex  # Make sure to have your Forth lexer available.

        lexer = ForthLex()
        lexer.build()  # Build the lexer
        parser = ForthParser(lexer)  # Instantiate the parser with lexer

        while True:
            try:
                s = input("forth >> ")
            except EOFError:
                break
            if not s:
                continue
            result = parser.parse(s)
            if result:
                print(result)


if __name__ == "__main__":
    main()

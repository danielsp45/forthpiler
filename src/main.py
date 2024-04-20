from forth_ast import AbstractSyntaxTree, Translator
from forth_lexer import ForthLex
from forth_parser import ForthParser
from ewvm_translator import EWVMTranslator


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
        translator: Translator = EWVMTranslator()
        if result:
            print('\n'.join(result.evaluate(translator)))


if __name__ == "__main__":
    main()

from enum import Enum

from ewvmapi.ewvm_api import run_code
from forthpiler.syntax import AbstractSyntaxTree
from forthpiler.ewvm_translator import EWVMTranslator
from forthpiler.lexer import ForthLex
from forthpiler.parser import ForthParser


class InterpretingMode(Enum):
    PARSE = ("parse >> ", lambda result: print(result.__repr__()))
    TRANSLATE = (
        "translate >> ",
        lambda result: print("\n".join(result.evaluate(EWVMTranslator()))),
    )
    RUN = (
        "run >> ",
        lambda result: print(run_code("\n".join(result.evaluate(EWVMTranslator())))),
    )

    def __init__(self, prefix, action):
        self.prefix = prefix
        self.action = action


def main():
    lexer = ForthLex().build()
    parser = ForthParser(lexer)
    commands = ("/parse", "/run", "/translate")
    mode = InterpretingMode.TRANSLATE
    print(f"Starting in {mode.name}.")
    print(f"Change to other interpreter modes with {', '.join(commands)}")

    while True:
        try:
            s = input(mode.prefix)
        except (EOFError, KeyboardInterrupt):
            break
        if not s:
            continue

        if s in commands:
            mode = InterpretingMode[s[1:].upper()]
            print(f"Mode changed to {mode.name}")
            continue

        result: AbstractSyntaxTree = parser.parse(s)
        if result:
            mode.action(result)


if __name__ == "__main__":
    main()

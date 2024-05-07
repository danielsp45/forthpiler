from enum import Enum

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit import print_formatted_text, ANSI

from ewvmapi.ewvm_api import run_code
from forthpiler.ewvm_translator import EWVMTranslator
from forthpiler.lexer import ForthLex
from forthpiler.parser import ForthParser
from forthpiler.syntax import AbstractSyntaxTree
import forthpiler.syntax as ast
from forthpiler.visualizer import visualize


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
    VISUALIZE = (
        "visualize >> ",
        lambda result: visualize(result),
    )

    def __init__(self, prefix, action):
        self.prefix = prefix
        self.action = action


def main():
    lexer = ForthLex().build()
    parser = ForthParser(lexer)

    commands = ("/parse", "/run", "/translate", "/visualize")
    mode = InterpretingMode.TRANSLATE
    print(f"Starting in {mode.name}.")
    print(f"Change to other interpreter modes with {', '.join(commands)}")

    session = PromptSession()
    with patch_stdout():
        while True:
            try:
                s = session.prompt(mode.prefix)
            except (EOFError, KeyboardInterrupt):
                break

            if s in commands:
                mode = InterpretingMode[s[1:].upper()]
                print(f"Mode changed to {mode.name}")
                continue

            result: AbstractSyntaxTree = parser.parse(s)

            if result:
                try:
                    mode.action(result)
                except ast.TranslationError as e:
                    print_formatted_text(ANSI(f"\x1b[31m{str(e)}"))
                    continue


if __name__ == "__main__":
    main()

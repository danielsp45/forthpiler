from enum import Enum

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit import print_formatted_text, ANSI

from ewvmapi.ewvm_api import run_code
from forthpiler.ewvm_translator import EWVMTranslator
from forthpiler.lexer import ForthLex
from forthpiler.parser import ForthParser
from forthpiler.visualizer import visualize

import forthpiler.syntax as ast


def print_red(text: str) -> None:
    print_formatted_text(ANSI(f"\x1b[31m{text}"))


class InterpretingMode(Enum):
    PARSE, TRANSLATE, RUN, VISUALIZE = range(4)

    def get_prefix(self):
        match self:
            case InterpretingMode.PARSE:
                return "parse >> "
            case InterpretingMode.TRANSLATE:
                return "translate >> "
            case InterpretingMode.RUN:
                return "run >> "
            case InterpretingMode.VISUALIZE:
                return "visualize >> "

    def run_action(self, result, standard_lib_functions: list[ast.Function]):
        match self:
            case InterpretingMode.PARSE:
                print(result.__repr__())
            case InterpretingMode.TRANSLATE:
                print("\n".join(result.evaluate(EWVMTranslator(standard_lib_functions))))
            case InterpretingMode.RUN:
                print(f"'{run_code("\n".join(result.evaluate(EWVMTranslator(standard_lib_functions))))}'")
            case InterpretingMode.VISUALIZE:
                visualize(result)


def main():
    lexer = ForthLex().build()
    parser = ForthParser(lexer)

    commands = ("/parse", "/run", "/translate", "/visualize")
    mode = InterpretingMode.TRANSLATE
    print(f"Starting in {mode.name}.")
    print(f"Change to other interpreter modes with {', '.join(commands)}")

    standard_lib_functions = [('spaces', '0 DO SPACE LOOP ')]
    standard_lib_functions = [ast.Function(name, parser.parse(f)) for (name, f) in standard_lib_functions]

    session = PromptSession()
    with patch_stdout():
        while True:
            try:
                s = session.prompt(mode.get_prefix())
            except (EOFError, KeyboardInterrupt):
                break

            if s in commands:
                mode = InterpretingMode[s[1:].upper()]
                print(f"Mode changed to {mode.name}")
                continue

            result: AbstractSyntaxTree = parser.parse(s)

            if result:
                try:
                    mode.run_action(result, standard_lib_functions)
                except Exception as e:
                    print_red(str(e))
                    continue


if __name__ == "__main__":
    main()

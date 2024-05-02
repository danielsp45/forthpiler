from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

from ewvmapi.ewvm_api import run_code
from forthpiler.ewvm_translator import EWVMTranslator
from forthpiler.lexer import ForthLex
from forthpiler.parser import ForthParser
from forthpiler.syntax import AbstractSyntaxTree


class InterpretingMode:
    def __init__(self):
        self.name = ""
        self.prefix = ""
        self.action = None

    def set_mode(self, mode: str):
        if mode == "run":
            self.name = "RUN"
            self.prefix = "run >> "
            self.action = lambda result: print(self.run(result))
        elif mode == "parse":
            self.name = "PARSE"
            self.prefix = "parse >> "
            self.action = lambda result: print(self.parse(result))
        elif mode == "translate":
            self.name = "TRANSLATE"
            self.prefix = "translate >> "
            self.action = lambda result: print(self.translate(result))
        else:
            raise ValueError("Invalid mode")

    def parse(self, result):
        return result.__repr__()

    def translate(self, result):
        return "\n".join(self._prepend_code(result))

    def run(self, result):
        return run_code("\n".join(self._prepend_code(result)))

    def _prepend_code(self, result):
        translator = EWVMTranslator()
        code = result.evaluate(translator)

        code.insert(0, f"start")
        for _ in range(len(translator.user_declared_variables)):
            code.insert(0, f"pushi 0")

        return code


def main():
    lexer = ForthLex().build()
    parser = ForthParser(lexer)

    commands = ("/parse", "/run", "/translate")
    interpreting_mode = InterpretingMode()
    interpreting_mode.set_mode("translate")
    print(f"Starting in {interpreting_mode.name}.")
    print(f"Change to other interpreter modes with {', '.join(commands)}")

    session = PromptSession()
    with patch_stdout():
        while True:
            try:
                s = session.prompt(interpreting_mode.prefix)
            except (EOFError, KeyboardInterrupt):
                break

            if s in commands:
                interpreting_mode.set_mode(s[1:])
                print(f"Mode changed to {interpreting_mode.name}")
                continue

            result: AbstractSyntaxTree = parser.parse(s)

            if result and interpreting_mode.action:
                interpreting_mode.action(result)


if __name__ == "__main__":
    main()

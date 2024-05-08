from prompt_toolkit import print_formatted_text, ANSI


def print_red(text: str) -> None:
    print_formatted_text(ANSI(f"\x1b[31m{text}"))

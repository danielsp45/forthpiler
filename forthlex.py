import ply.lex as lex


class ForthLex(object):
    tokens = (
        "NUMBER",
        "STRING",
        # Arithmetic operators
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE",
        # Comparison operators
        "IS_GREATER",
        "IS_LESS",
        "IS_EQUAL",
        "IS_GREATER_EQUAL",
        "IS_LESS_EQUAL",
        # Control flow
        "IF",
        "ELSE",
        "THEN",
        # Punctuation
        "DOT",
        "COLON",
        "SEMICOLON",
        # Other tokens
        "PRINT_STRING",
        "WORD",
    )

    # Regular expression rules for simple tokens
    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_TIMES = r"\*"
    t_DIVIDE = r"/"
    t_COLON = r":"
    t_SEMICOLON = r";"
    t_DOT = r"\."
    t_IS_GREATER = r">"
    t_IS_LESS = r"<"
    t_IS_EQUAL = r"="
    t_IS_GREATER_EQUAL = r">="
    t_IS_LESS_EQUAL = r"<="
    t_WORD = r"[a-zA-Z_][a-zA-Z0-9_]*"

    def t_STRING(self, t):
        r"\".*\" "
        t.value = t.value[1:-1]
        return t

    def t_IF(self, t):
        r"[iI][fF]"
        return t

    def t_ELSE(self, t):
        r"[eE][lL][sS][eE]"
        return t

    def t_THEN(self, t):
        r"[tT][hH][eE][nN]"
        return t

    def t_NUMBER(self, t):
        r"\d+"
        t.value = int(t.value)
        return t

    def t_PRINT_STRING(self, t):
        r"\.\".*\" "
        t.value = t.value[3:-1]
        return t

    def t_COMMENT(self, t):
        r"\(.*\)"
        pass

    # Define a rule for comments in the form \ comment \n
    def t_COMMENT_LINE(self, t):
        r"\\.*\n"
        t.lexer.lineno += 1
        pass

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = " \t"

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


if __name__ == "__main__":
    # Build the lexer and try it out
    m = ForthLex()
    m.build()  # Build the lexer
    test_string = input(">> ")
    m.test(test_string)  # Test it

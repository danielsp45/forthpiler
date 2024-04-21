import ply.lex as lex


class ForthLex(object):
    def __init__(self):
        self.lexer = None

    tokens = (
        "NUMBER",
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE",
        "EXP",
        "MOD",
        "SLASH_MOD",
        "COLON",
        "SEMICOLON",
        "LITERAL",
        "PRINT_STRING",
    )

    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_TIMES = r"\*"
    t_DIVIDE = r"/"
    t_EXP = r"\*\*"
    t_SLASH_MOD = r"\/MOD"
    t_COLON = r":"
    t_SEMICOLON = r";"

    # Ignore comments anywhere
    def t_comment(self, t):
        r"\(.*\)"
        pass

    def t_NUMBER(self, t):
        r"[+-]?\d+"
        t.value = int(t.value)
        return t

    def t_PRINT_STRING(self, t):
        r"\.\"\s.*\" "
        t.value = t.value[3:-2]
        return t

    # This MOD needs to be here because of conflicts with LITERAL.
    # Check https://stackoverflow.com/questions/2910338/python-yacc-lexer-token-priority
    def t_MOD(self, t):
        r"""MOD"""
        return t

    # Words cannot be started by numbers in our implementation
    def t_LITERAL(self, t):
        r"""[\.a-zA-Z][\.a-zA-Z\d]*"""
        return t

    def t_newline(self, t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)

    t_ignore = " \t"

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self

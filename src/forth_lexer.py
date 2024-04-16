import ply.lex as lex


class ForthLex(object):
    def __init__(self):
        self.lexer = None

    tokens = ("NUMBER", "PLUS", "MINUS", "TIMES", "DIVIDE", "EXP", "MOD", "SLASH_MOD")

    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_TIMES = r"\*"
    t_DIVIDE = r"/"
    t_EXP = r"\*\*"
    t_MOD = r"MOD"
    t_SLASH_MOD = r"\/MOD"

    def t_NUMBER(self, t):
        r"[+-]?\d+"
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    t_ignore = " \t"

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self

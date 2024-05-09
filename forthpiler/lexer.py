import ply.lex as lex


class ForthLex(object):
    def __init__(self):
        self.lexer = None

    reserved = {
        "if": "IF",
        "else": "ELSE",
        "then": "THEN",
        "do": "DO",
        "loop": "LOOP",
        "+loop": "PLUS_LOOP",
        "begin": "BEGIN",
        "until": "UNTIL",
        "variable": "VARIABLE_DECLARATION",
        "!": "STORE",
        "@": "FETCH",
    }

    tokens = [
        "NUMBER",
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE",
        "EXP",
        "MOD",
        "SLASH_MOD",
        "EQUALS",
        "NOT_EQUALS",
        "LESS_THAN",
        "LESS_THAN_OR_EQUAL_TO",
        "GREATER_THAN",
        "GREATER_THAN_OR_EQUAL_TO",
        "ZERO_EQUALS",
        "ZERO_LESS_THAN",
        "ZERO_LESS_THAN_OR_EQUAL_TO",
        "ZERO_GREATER_THAN",
        "ZERO_GREATER_THAN_OR_EQUAL_TO",
        "COLON",
        "SEMI_COLON",
        "LITERAL",
        "PRINT_STRING",
        "CHAR_FUNC",
    ] + list(reserved.values())

    # Literals are not defined with the built-in `literals` definition
    # because some of them have more than one character.

    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_TIMES = r"\*"
    t_DIVIDE = r"/"
    t_EXP = r"\*\*"
    t_SLASH_MOD = r"\/MOD"

    t_EQUALS = r"="
    t_NOT_EQUALS = r"<>"
    t_LESS_THAN = r"<"
    t_GREATER_THAN = r">"

    def t_LESS_THAN_OR_EQUAL_TO(self, t):
        r"<="
        return t

    def t_GREATER_THAN_OR_EQUAL_TO(self, t):
        r">="
        return t

    def t_ZERO_EQUALS(self, t):
        r"0="
        return t

    def t_ZERO_LESS_THAN_OR_EQUAL_TO(self, t):
        r"0<="
        return t

    def t_ZERO_LESS_THAN(self, t):
        r"0<"
        return t

    def t_ZERO_GREATER_THAN_OR_EQUAL_TO(self, t):
        r"0>="
        return t

    def t_ZERO_GREATER_THAN(self, t):
        r"0>"
        return t

    t_COLON = r":"
    t_SEMI_COLON = r";"

    # Ignore comments anywhere
    def t_comment(self, t):
        r"""\\.*|(\(.*\))"""
        pass

    def t_PRINT_STRING(self, t):
        r"\.\"\s.*?\" "
        t.value = t.value[3:-1]
        return t

    # This MOD needs to be here because of conflicts with LITERAL
    # Check https://stackoverflow.com/questions/2910338/python-yacc-lexer-token-priority
    def t_MOD(self, t):
        r"""MOD"""
        return t

    def t_CHAR_FUNC(self, t):
        r"""[cC][hH][aA][rR]\s."""
        t.value = t.value[-1]
        return t

    # This is defined as a single rule, in order to avoid conflicts
    # with the operator PLUS
    def t_PLUS_LOOP(self, t):
        r"\+[lL][oO][oO][pP]"
        t.type = self.reserved.get(t.value.lower(), "PLUS_LOOP")
        return t

    def t_LITERAL(self, t):
        r"""[\.a-zA-Z\d\?\!\@][-\.a-zA-Z\d]*"""
        if t.value.isdigit():
            t.type = "NUMBER"
            t.value = int(t.value)
            return t

        # Check if the value is a reserved word and if it is, change the type, otherwise, it is a LITERAL
        t.type = self.reserved.get(t.value.lower(), "LITERAL")
        return t

    def t_NUMBER(self, t):
        r"[+-]?\d+"
        t.value = int(t.value)
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

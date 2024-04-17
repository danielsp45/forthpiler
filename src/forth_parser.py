import ply.yacc as yacc

from src.forth_ast import AbstractSyntaxTree, Number, Operator, OperatorType


class ForthParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self)

    def p_ast(self, p):
        "ast : grammar"
        p[0] = AbstractSyntaxTree(p[1])

    def p_grammar_empty(self, p):
        "grammar :"
        p[0] = []

    def p_grammar_expression(self, p):
        "grammar : expression grammar"
        p[0] = [p[1]] + p[2]

    def p_expression_number(self, p):
        "expression : NUMBER"
        p[0] = Number(p[1])

    def p_expression_operator(self, p):
        "expression : operator"
        p[0] = p[1]

    def p_operator(self, p):
        """operator : PLUS
        | MINUS
        | TIMES
        | DIVIDE
        | EXP
        | MOD
        | SLASH_MOD"""
        match p[1]:
            case "+":
                p[0] = Operator(OperatorType.PLUS)
            case "-":
                p[0] = Operator(OperatorType.MINUS)
            case "*":
                p[0] = Operator(OperatorType.TIMES)
            case "/":
                p[0] = Operator(OperatorType.DIVIDE)
            case "**":
                p[0] = Operator(OperatorType.EXP)
            case "MOD":
                p[0] = Operator(OperatorType.MOD)
            case "/MOD":
                p[0] = Operator(OperatorType.SLASH_MOD)

    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Syntax error at EOF")

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)

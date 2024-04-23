import ply.yacc as yacc

import forthpiler.syntax as ast


class ForthParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self)

    def p_ast(self, p):
        """ast : grammar"""
        p[0] = ast.AbstractSyntaxTree(p[1])

    def p_grammar_empty(self, p):
        """grammar :"""
        p[0] = []

    def p_grammar_expression(self, p):
        """grammar : expression grammar"""
        p[0] = [p[1]] + p[2]

    def p_expression_number(self, p):
        """expression : NUMBER"""
        p[0] = ast.Number(p[1])

    def p_expression_operator(self, p):
        """expression : operator"""
        p[0] = p[1]

    def p_expression_function(self, p):
        """expression : function"""
        p[0] = p[1]

    def p_expression_literal(self, p):
        """expression : LITERAL"""
        p[0] = ast.Literal(p[1])

    def p_expression_print_string(self, p):
        """expression : PRINT_STRING"""
        p[0] = ast.PrintString(p[1])

    def p_expression_char_function(self, p):
        """expression : CHAR_FUNC"""
        p[0] = ast.CharFunction(p[1])

    def p_operator_plus(self, p):
        """operator : PLUS"""
        p[0] = ast.Operator(ast.OperatorType.PLUS)

    def p_operator_minus(self, p):
        """operator : MINUS"""
        p[0] = ast.Operator(ast.OperatorType.MINUS)

    def p_operator_times(self, p):
        """operator : TIMES"""
        p[0] = ast.Operator(ast.OperatorType.TIMES)

    def p_operator_divide(self, p):
        """operator : DIVIDE"""
        p[0] = ast.Operator(ast.OperatorType.DIVIDE)

    def p_operator_exp(self, p):
        """operator : EXP"""
        p[0] = ast.Operator(ast.OperatorType.EXP)

    def p_operator_mod(self, p):
        """operator : MOD"""
        p[0] = ast.Operator(ast.OperatorType.MOD)

    def p_operator_slash_mod(self, p):
        """operator : SLASH_MOD"""
        p[0] = ast.Operator(ast.OperatorType.SLASH_MOD)

    def p_function(self, p):
        """function : COLON LITERAL ast SEMICOLON"""
        p[0] = ast.Function(p[2], p[3])

    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Syntax error at EOF")

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)

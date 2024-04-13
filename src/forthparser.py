import ply.yacc as yacc
from forthlex import ForthLex
from ast_node import ASTNode


class ForthParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self)

    def p_program(self, p):
        "program : statements"
        p[0] = ASTNode(type="program", children=[p[1]])

    def p_statements(self, p):
        """statements : statements statement
        | statement
        """
        if len(p) == 3:
            p[0] = ASTNode(type="statements", children=[p[1], p[2]])
        elif len(p) == 2:
            p[0] = ASTNode(type="statements", children=[p[1]])

    def p_statement(self, p):
        "statement : expression"
        p[0] = p[1]

    def p_literal_expression(self, p):
        """expression : NUMBER
        | STRING
        """
        p[0] = ASTNode(type="literal_expression", leaf=p[1])

    def p_operator_expression(self, p):
        "expression : arithmetic_op"
        p[0] = p[1]

    def p_arithmetic_op(self, p):
        """arithmetic_op : expression expression PLUS
        | expression expression MINUS
        | expression expression TIMES
        | expression expression DIVIDE"""
        left = p[1]
        right = p[2]
        operator = p[3]  # Adjusted according to the correct position of the operator
        p[0] = ASTNode(type="arithmetic_op", children=[left, right], leaf=operator)

    def p_empty(self, p):
        "empty :"
        pass

    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Syntax error at EOF")

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)

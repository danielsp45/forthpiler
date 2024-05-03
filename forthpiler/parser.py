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

    def p_expression_comparison_operator(self, p):
        """expression : comparison_operator"""
        p[0] = p[1]

    def p_expression_function(self, p):
        """expression : function"""
        p[0] = p[1]

    def p_expression_if_statement(self, p):
        """expression : if_statement"""
        p[0] = p[1]

    def p_expression_variable_declaration(self, p):
        """expression : VARIABLE_DECLARATION LITERAL"""
        p[0] = ast.VariableDeclaration(p[2])

    def p_expression_store(self, p):
        """expression : LITERAL STORE"""
        p[0] = ast.StoreVariable(p[1])

    def p_expression_fetch(self, p):
        """expression : LITERAL FETCH"""
        p[0] = ast.FetchVariable(p[1])

    def p_expression_loop_statement(self, p):
        """expression : loop_statement"""
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

    def p_comparison_operator_equals(self, p):
        """comparison_operator : EQUALS"""
        p[0] = ast.ComparisonOperator(ast.ComparisonOperatorType.EQUALS)

    def p_comparison_operator_not_equals(self, p):
        """comparison_operator : NOT_EQUALS"""
        p[0] = ast.ComparisonOperator(ast.ComparisonOperatorType.NOT_EQUALS)

    def p_comparison_operator_less_than(self, p):
        """comparison_operator : LESS_THAN"""
        p[0] = ast.ComparisonOperator(ast.ComparisonOperatorType.LESS_THAN)

    def p_comparison_operator_less_than_or_equal_to(self, p):
        """comparison_operator : LESS_THAN_OR_EQUAL_TO"""
        p[0] = ast.ComparisonOperator(ast.ComparisonOperatorType.LESS_THAN_OR_EQUAL_TO)

    def p_comparison_operator_greater_than(self, p):
        """comparison_operator : GREATER_THAN"""
        p[0] = ast.ComparisonOperator(ast.ComparisonOperatorType.GREATER_THAN)

    def p_comparison_operator_greater_than_or_equal_to(self, p):
        """comparison_operator : GREATER_THAN_OR_EQUAL_TO"""
        p[0] = ast.ComparisonOperator(
            ast.ComparisonOperatorType.GREATER_THAN_OR_EQUAL_TO
        )

    def p_comparison_operator_zero_equals(self, p):
        """comparison_operator : ZERO_EQUALS"""
        p[0] = ast.ComparisonOperator(ast.ComparisonOperatorType.ZERO_EQUALS)

    def p_comparison_operator_zero_less_than(self, p):
        """comparison_operator : ZERO_LESS_THAN"""
        p[0] = ast.ComparisonOperator(ast.ComparisonOperatorType.ZERO_LESS_THAN)

    def p_comparison_operator_zero_less_than_or_equal_to(self, p):
        """comparison_operator : ZERO_LESS_THAN_OR_EQUAL_TO"""
        p[0] = ast.ComparisonOperator(
            ast.ComparisonOperatorType.ZERO_LESS_THAN_OR_EQUAL_TO
        )

    def p_comparison_operator_zero_greater_than(self, p):
        """comparison_operator : ZERO_GREATER_THAN"""
        p[0] = ast.ComparisonOperator(ast.ComparisonOperatorType.ZERO_GREATER_THAN)

    def p_comparison_operator_zero_greater_than_or_equal_to(self, p):
        """comparison_operator : ZERO_GREATER_THAN_OR_EQUAL_TO"""
        p[0] = ast.ComparisonOperator(
            ast.ComparisonOperatorType.ZERO_GREATER_THAN_OR_EQUAL_TO
        )

    def p_function(self, p):
        """function : COLON LITERAL ast SEMI_COLON"""
        p[0] = ast.Function(p[2], p[3])

    def p_if_statement_without_else(self, p):
        """if_statement : IF ast THEN"""
        p[0] = ast.IfStatement(p[2], None)

    def p_if_statement_with_else(self, p):
        """if_statement : IF ast ELSE ast THEN"""
        p[0] = ast.IfStatement(p[2], p[4])

    def p_do_statement_normal(self, p):
        """loop_statement : DO ast LOOP"""
        p[0] = ast.DoLoopStatement(p[2])

    def p_do_statement_plus(self, p):
        """loop_statement : DO ast PLUS_LOOP"""
        p[0] = ast.DoPlusLoopStatement(p[2])

    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Syntax error at EOF")

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)

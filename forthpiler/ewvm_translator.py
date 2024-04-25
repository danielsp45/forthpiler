from typing import Dict, List

import forthpiler.syntax as ast


class EWVMTranslator(ast.Translator):
    def __init__(self):
        self.predefined_functions: Dict[str, List[str]] = {
            ".": ["writei"],
            "emit": ["writechr"],
            "space": ["pushi 32", "writechr"],  # 32 is ASCII code for space
            "cr": ["pushi 10", "writechr"],  # 10 is ASCII code for newline,
            "swap": ["swap"],
            "dup": ["dup 1"],
            "2dup": ["pushsp", "load -1"] * 2,
        }
        self.user_defined_functions: Dict[str, ast.AbstractSyntaxTree] = {}

        self.if_counter = 1  # Counter for if statements

    def visit_number(self, number: ast.Number) -> List[str]:
        return [f"pushi {number.number}"]

    def visit_operator(self, operator: ast.Operator) -> List[str]:
        match operator.operator_type:
            case ast.OperatorType.PLUS:
                return ["add"]
            case ast.OperatorType.MINUS:
                return ["sub"]
            case ast.OperatorType.TIMES:
                return ["mul"]
            case ast.OperatorType.DIVIDE:
                return ["div"]
            case ast.OperatorType.EXP:
                raise NotImplementedError
            case ast.OperatorType.MOD:
                return ["mod"]
            case ast.OperatorType.SLASH_MOD:
                raise NotImplementedError

    def visit_comparison_operator(
        self, comparison_operator: ast.ComparisonOperator
    ) -> List[str]:
        match comparison_operator.comparison_operator_type:
            case ast.ComparisonOperatorType.EQUALS:
                return ["equal"]
            case ast.ComparisonOperatorType.NOT_EQUALS:
                return ["equal", "not"]
            case ast.ComparisonOperatorType.LESS_THAN:
                return ["inf"]
            case ast.ComparisonOperatorType.LESS_THAN_OR_EQUAL_TO:
                return ["infeq"]
            case ast.ComparisonOperatorType.GREATER_THAN:
                return ["sup"]
            case ast.ComparisonOperatorType.GREATER_THAN_OR_EQUAL_TO:
                return ["supeq"]
            case ast.ComparisonOperatorType.ZERO_EQUALS:
                return ["not"]
            case ast.ComparisonOperatorType.ZERO_LESS_THAN:
                return ["pushi 0", "inf"]
            case ast.ComparisonOperatorType.ZERO_LESS_THAN_OR_EQUAL_TO:
                return ["pushi 0", "infeq"]
            case ast.ComparisonOperatorType.ZERO_GREATER_THAN:
                return ["pushi 0", "sup"]
            case ast.ComparisonOperatorType.ZERO_GREATER_THAN_OR_EQUAL_TO:
                return ["pushi 0", "supeq"]

    def visit_function(self, function: ast.Function) -> List[str]:
        if function.name in self.user_defined_functions:
            raise ast.TranslationError(f"Function {function.name} already defined")

        self.user_defined_functions[function.name] = function.ast
        return []

    def visit_if_statement(self, if_statement: ast.IfStatement) -> List[str]:
        result: List[str] = []
        if if_statement.with_else:
            result = self._visit_if_statement_with_else(if_statement)
        else:
            result = self._visit_if_statement_without_else(if_statement)

        self.if_counter += 1
        return result

    def _visit_if_statement_with_else(self, if_statement: ast.IfStatement) -> List[str]:
        return [
            f"jz else{self.if_counter}",
            *if_statement.if_true.evaluate(self),
            f"jump endif{self.if_counter}",
            f"else{self.if_counter}:",
            *if_statement.if_false.evaluate(self),
            f"endif{self.if_counter}:",
        ]

    def _visit_if_statement_without_else(
        self, if_statement: ast.IfStatement
    ) -> List[str]:
        return [
            f"jz endif{self.if_counter}",
            *if_statement.if_true.evaluate(self),
            f"endif{self.if_counter}:",
        ]

    def visit_literal(self, literal: ast.Literal) -> List[str]:
        value = literal.content

        if value in self.user_defined_functions:
            return self.user_defined_functions[value].evaluate(self)

        if value in self.predefined_functions:
            return self.predefined_functions[value]

        raise ast.TranslationError(f"Literal {value} not found")

    def visit_print_string(self, print_string: ast.PrintString) -> List[str]:
        return [f'pushs "{print_string.content}"\nwrites']

    def visit_char_function(self, char_function: ast.CharFunction) -> List[str]:
        return [f'pushs "{char_function.content}"\nchrcode']

    def translate(self, ast: ast.AbstractSyntaxTree) -> List[str]:
        return [res for expr in ast.expressions for res in expr.evaluate(self)]

from typing import Dict, List

from forthpiler import syntax
from forthpiler.syntax import *


class SemanticError(Exception):
    pass


class SemanticAnalyzer(syntax.Translator[str]):
    def __init__(self):
        self._variables = []
        self._functions = []
        self._loop_depth = 0
        self._predefined_functions: Dict[str, List[str]] = {
            ".": ["writei"],
            "emit": ["writechr"],
            "space": ["pushi 32", "writechr"],  # 32 is ASCII code for space
            "cr": ["pushi 10", "writechr"],  # 10 is ASCII code for newline,
            "swap": ["swap"],
            "dup": ["dup 1"],
            "2dup": ["pushsp", "load -1"] * 2,
            "drop": ["pop 1"],
            "i": ["i"],
            "j": ["j"],
        }

    def visit_number(self, number: Number):
        pass

    def visit_operator(self, operator: Operator):
        pass

    def visit_comparison_operator(self, comparison_operator: ComparisonOperator):
        pass

    def visit_function(self, function: Function):
        self._functions.append(function.name)
        function.ast.evaluate(self)

    def visit_do_loop_statement(self, do_loop: DoLoopStatement):
        self._loop_depth += 1
        do_loop.body.evaluate(self)
        self._loop_depth -= 1

    def visit_do_plus_loop_statement(self, do_loop: DoPlusLoopStatement):
        self._loop_depth += 1
        do_loop.body.evaluate(self)
        self._loop_depth -= 1

    def visit_if_statement(self, if_statement: IfStatement):
        pass

    def visit_variable_declaration(self, variable_declaration: VariableDeclaration):
        self._variables.append(variable_declaration.name)

    def visit_store_variable(self, store_variable: StoreVariable):
        if store_variable.name not in self._variables:
            raise SemanticError(f"Variable {store_variable.name} not declared")

    def visit_fetch_variable(self, fetch_variable: FetchVariable):
        if fetch_variable.name not in self._variables:
            raise SemanticError(f"Variable {fetch_variable.name} not declared")

    def visit_literal(self, literal: Literal):
        if literal.content == "j" and self._loop_depth < 2:
            raise SemanticError("j is only allowed inside a nested loop")

        if (
            literal.content not in self._variables
            and literal.content not in self._functions
            and literal.content not in self._predefined_functions
        ):
            raise SemanticError(f"Unknown variable or function {literal.content}")

    def visit_print_string(self, print_string: PrintString):
        pass

    def visit_char_function(self, char_function: CharFunction):
        pass

    def translate(self, ast: AbstractSyntaxTree):
        for expr in ast.expressions:
            expr.evaluate(self)

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
            "drop": ["pop 1"],
            "i": ["i"],
        }
        self.user_defined_functions: Dict[str, ast.AbstractSyntaxTree] = {}
        self.user_declared_variables: List[str] = []
        self.if_counter = 0
        self.while_counter = 0

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

    def visit_do_loop_statement(self, do_loop: ast.DoLoopStatement) -> List[str]:
        current_while_counter = self.while_counter
        self.while_counter += 1
        body = do_loop.body.evaluate(self)

        initialization = self._generate_loop_initialization(current_while_counter)

        loop_condition = self._generate_loop_condition(current_while_counter)

        loop_body = self._generate_loop_body(body, current_while_counter)

        loop_end = self._generate_loop_end(current_while_counter)

        return initialization + loop_condition + loop_body + loop_end

    def visit_do_plus_loop_statement(
        self, do_loop: ast.DoPlusLoopStatement
    ) -> List[str]:
        current_while_counter = self.while_counter
        self.while_counter += 1
        body = do_loop.body.evaluate(self)

        initialization = self._generate_plus_loop_initialization(current_while_counter)

        loop_condition = self._generate_plus_loop_condition(current_while_counter)

        loop_body = self._generate_loop_body(body, current_while_counter)

        loop_end = self._generate_plus_loop_end(current_while_counter)

        return initialization + loop_condition + loop_body + loop_end

    def visit_if_statement(self, if_statement: ast.IfStatement) -> List[str]:
        if if_statement.with_else:
            return self._visit_if_statement_with_else(if_statement)
        else:
            return self._visit_if_statement_without_else(if_statement)

    def _visit_if_statement_with_else(self, if_statement: ast.IfStatement) -> List[str]:
        current_if_counter = self.if_counter
        self.if_counter += 1

        return [
            f"jz else{current_if_counter}",
            *if_statement.if_true.evaluate(self),
            f"jump endif{current_if_counter}",
            f"else{current_if_counter}:",
            *if_statement.if_false.evaluate(self),
            f"endif{current_if_counter}:",
            *if_statement.always.evaluate(self),
        ]

    def _visit_if_statement_without_else(
        self, if_statement: ast.IfStatement
    ) -> List[str]:
        current_if_counter = self.if_counter
        self.if_counter += 1

        return [
            f"jz endif{current_if_counter}",
            *if_statement.if_true.evaluate(self),
            f"endif{current_if_counter}:",
            *if_statement.always.evaluate(self),
        ]

    def visit_variable_declaration(
        self, variable_declaration: ast.VariableDeclaration
    ) -> List[str]:
        self.user_declared_variables.append(variable_declaration.name)

        return []

    def visit_store_variable(self, store_variable: ast.StoreVariable) -> List[str]:
        if store_variable.name not in self.user_declared_variables:
            raise ast.TranslationError(f"Variable {store_variable.name} not declared")

        variable_index = self.user_declared_variables.index(store_variable.name)

        return [
            f"storeg {variable_index}",
        ]

    def visit_fetch_variable(self, fetch_variable: ast.FetchVariable) -> List[str]:
        if fetch_variable.name not in self.user_declared_variables:
            raise ast.TranslationError(f"Variable {fetch_variable.name} not declared")

        variable_index = self.user_declared_variables.index(fetch_variable.name)

        return [
            f"pushg {variable_index}",
        ]

    def visit_literal(self, literal: ast.Literal) -> List[str]:
        value = literal.content.lower()

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

    def _generate_loop_initialization(self, current_while_counter: int) -> List[str]:
        return [
            "alloc 2",
            "swap",
            "store 1",
            f"pushst {current_while_counter}",
            "swap",
            "store 0",
        ]

    def _generate_plus_loop_initialization(
        self, current_while_counter: int
    ) -> List[str]:
        return [
            "dup 1",
            "alloc 3",
            "swap",
            "store 1",
            f"pushst {current_while_counter}",
            "swap",
            "store 2",
            f"pushst {current_while_counter}",
            "swap",
            "store 0",
        ]

    def _generate_plus_loop_condition(self, current_while_counter: int) -> List[str]:
        return [
            f"startwhile{current_while_counter}:",
            f"pushst {current_while_counter}",
            "load 0",
            "dup 1",
            f"pushst {current_while_counter}",
            "load 2",
            "sup",
            f"jz ifreverseloop{current_while_counter}",
            f"pushst {current_while_counter}",
            "load 1",
            "sup",
            f"jump elsereverseloop{current_while_counter}",
            f"ifreverseloop{current_while_counter}:",
            f"pushst {current_while_counter}",
            "load 1",
            "inf",
            f"elsereverseloop{current_while_counter}:",
            f"jz endwhile{current_while_counter}",
        ]

    def _generate_loop_condition(self, current_while_counter: int) -> List[str]:
        return [
            f"startwhile{current_while_counter}:",
            f"pushst {current_while_counter}",
            "load 0",
            f"pushst {current_while_counter}",
            "load 1",
            "sup",
            f"jz endwhile{current_while_counter}",
        ]

    def _generate_loop_body(
        self, body: List[str], current_while_counter: int
    ) -> List[str]:
        for index, line in enumerate(body):
            if line == "i":
                body[index] = f"pushst {current_while_counter}\nload 1"

        return body

    def _generate_loop_end(self, current_while_counter: int) -> List[str]:
        return [
            f"pushst {current_while_counter}",
            "load 1",
            "pushi 1",
            "add",
            f"pushst {current_while_counter}",
            "swap",
            "store 1",
            f"jump startwhile{current_while_counter}",
            f"endwhile{current_while_counter}:",
            "popst",
        ]

    def _generate_plus_loop_end(self, current_while_counter: int) -> List[str]:
        return [
            f"pushst {current_while_counter}",
            "load 1",
            "add",
            f"pushst {current_while_counter}",
            "swap",
            "store 1",
            f"jump startwhile{current_while_counter}",
            f"endwhile{current_while_counter}:",
            "popst",
        ]

from typing import Dict, List

import forthpiler.syntax as ast


class EWVMTranslator(ast.Translator[List[str]]):
    def __init__(self, standard_lib_functions: List[ast.Word]):
        self.predefined_words: Dict[str, List[str]] = {
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
        self.user_defined_words: Dict[str, ast.AbstractSyntaxTree] = {}

        self.declared_entities_counter = 0
        self.user_declared_variables: Dict[str, int] = {}
        self.user_declared_constants: Dict[str, int] = {}

        self.if_counter = 0
        self.loop_counter = 0
        self.loop_depth = 0
        self.heap_counter = 0

        self.started = False

        for standard_lib_function in standard_lib_functions:
            self.predefined_words[standard_lib_function.name] = self.visit_word(
                standard_lib_function
            )

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
                raise NotImplementedError("Operator `exp` not implemented")
            case ast.OperatorType.MOD:
                return ["mod"]
            case ast.OperatorType.SLASH_MOD:
                raise NotImplementedError("Operator `slashmod` not implemented")

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

    def visit_word(self, word: ast.Word) -> List[str]:
        if word.name in self.user_defined_words:
            raise ast.TranslationError(f"Function '{word.name}' already defined")

        self.user_defined_words[word.name] = word.ast.evaluate(self)
        return []

    def visit_do_loop_statement(self, do_loop: ast.DoLoopStatement) -> List[str]:
        self.loop_depth += 1
        current_loop_counter = self.loop_counter
        self.loop_counter += 1

        current_heap_counter = self.heap_counter
        self.heap_counter += 1

        body = do_loop.body.evaluate(self)
        initialization = self._generate_loop_initialization(current_heap_counter)
        loop_condition = self._generate_loop_condition(
            current_loop_counter, current_heap_counter
        )
        loop_body = self._generate_loop_body(body, current_heap_counter)
        loop_end = self._generate_loop_end(current_loop_counter, current_heap_counter)
        self.loop_depth -= 1

        return initialization + loop_condition + loop_body + loop_end

    def visit_do_plus_loop_statement(
        self, do_loop: ast.DoPlusLoopStatement
    ) -> List[str]:
        self.loop_depth += 1
        current_loop_counter = self.loop_counter
        self.loop_counter += 1

        current_heap_counter = self.heap_counter
        self.heap_counter += 1

        body = do_loop.body.evaluate(self)
        initialization = self._generate_plus_loop_initialization(current_heap_counter)
        loop_condition = self._generate_plus_loop_condition(
            current_loop_counter, current_heap_counter
        )
        loop_body = self._generate_loop_body(body, current_heap_counter)
        loop_end = self._generate_plus_loop_end(
            current_loop_counter, current_heap_counter
        )
        self.loop_depth -= 1

        return initialization + loop_condition + loop_body + loop_end

    def visit_begin_until_statement(
        self, begin_until: ast.BeginUntilStatement
    ) -> List[str]:
        current_loop_counter = self.loop_counter
        self.loop_counter += 1

        body = begin_until.body.evaluate(self)

        return [
            f"startloop{current_loop_counter}:",
            *body,
            f"jz startloop{current_loop_counter}",
        ]

    def visit_begin_again_statement(
        self, begin_until: ast.BeginUntilStatement
    ) -> List[str]:
        current_loop_counter = self.loop_counter
        self.loop_counter += 1

        body = begin_until.body.evaluate(self)

        return [
            f"startloop{current_loop_counter}:",
            *body,
            f"jump startloop{current_loop_counter}",
        ]

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
        ]

    def visit_variable_declaration(
        self, variable_declaration: ast.VariableDeclaration
    ) -> List[str]:
        self.user_declared_variables[
            variable_declaration.name
        ] = self.declared_entities_counter
        self.declared_entities_counter += 1

        return []

    def visit_store_variable(self, store_variable: ast.StoreVariable) -> List[str]:
        if store_variable.name in self.user_declared_constants:
            raise ast.TranslationError(
                f"Cannot reassign a value to constant '{store_variable.name}'"
            )
        if store_variable.name not in self.user_declared_variables:
            raise ast.TranslationError(f"Variable '{store_variable.name}' not declared")

        variable_index = self.user_declared_variables[store_variable.name]

        return [f"storeg {variable_index}"]

    def visit_fetch_variable(self, fetch_variable: ast.FetchVariable) -> List[str]:
        if fetch_variable.name not in self.user_declared_variables:
            raise ast.TranslationError(f"Variable '{fetch_variable.name}' not declared")

        variable_index = self.user_declared_variables[fetch_variable.name]

        return [f"pushg {variable_index}"]

    def visit_constant_declaration(
        self, constant_declaration: ast.ConstantDeclaration
    ) -> List[str]:
        variable_index = self.declared_entities_counter
        self.declared_entities_counter += 1

        self.user_declared_constants[constant_declaration.name] = variable_index

        return [f"storeg {variable_index}"]

    def visit_literal(self, literal: ast.Literal) -> List[str]:
        value = literal.content.lower()

        if value == "j" and self.loop_depth < 2:
            raise ast.TranslationError("'j' is only allowed inside a nested loop")

        if value in self.user_defined_words:
            return self.user_defined_words[value].evaluate(self)

        if value in self.predefined_words:
            return self.predefined_words[value]

        if value in self.user_declared_constants:
            variable_index = self.user_declared_constants[value]
            return [f"pushg {variable_index}"]

        if value in self.user_declared_variables:
            raise ast.TranslationError(f"Bad use of variable '{value}'")

        raise ast.TranslationError(f"Literal '{value}' not found")

    def visit_print_string(self, print_string: ast.PrintString) -> List[str]:
        return [f'pushs "{print_string.content}"', "writes"]

    def visit_char_function(self, char_function: ast.CharFunction) -> List[str]:
        return [f'pushs "{char_function.content}"', "chrcode"]

    def translate(self, ast: ast.AbstractSyntaxTree) -> List[str]:
        if not self.started:
            self.started = True
            code = [res for expr in ast.expressions for res in expr.evaluate(self)]

            code.insert(0, f"start")
            total_variables = len(self.user_declared_variables) + len(
                self.user_declared_constants
            )
            for _ in range(total_variables):
                code.insert(0, f"pushi 0")
            code.append("stop")
        else:
            code = [res for expr in ast.expressions for res in expr.evaluate(self)]

        return code

    def _generate_loop_initialization(self, current_heap_counter: int) -> List[str]:
        return [
            "alloc 2",
            "swap",
            "store 1",
            f"pushst {current_heap_counter}",
            "swap",
            "store 0",
        ]

    def _generate_plus_loop_initialization(
        self, current_heap_counter: int
    ) -> List[str]:
        return [
            "dup 1",
            "alloc 3",
            "swap",
            "store 1",
            f"pushst {current_heap_counter}",
            "swap",
            "store 2",
            f"pushst {current_heap_counter}",
            "swap",
            "store 0",
        ]

    def _generate_plus_loop_condition(
        self, current_loop_counter: int, current_heap_counter: int
    ) -> List[str]:
        return [
            f"startloop{current_loop_counter}:",
            f"pushst {current_heap_counter}",
            "load 0",
            "dup 1",
            f"pushst {current_heap_counter}",
            "load 2",
            "sup",
            f"jz ifreverseloop{current_loop_counter}",
            f"pushst {current_heap_counter}",
            "load 1",
            "sup",
            f"jump elsereverseloop{current_loop_counter}",
            f"ifreverseloop{current_loop_counter}:",
            f"pushst {current_heap_counter}",
            "load 1",
            "inf",
            f"elsereverseloop{current_loop_counter}:",
            f"jz endloop{current_loop_counter}",
        ]

    def _generate_loop_condition(
        self, current_loop_counter: int, current_heap_counter: int
    ) -> List[str]:
        return [
            f"startloop{current_loop_counter}:",
            f"pushst {current_heap_counter}",
            "load 0",
            f"pushst {current_heap_counter}",
            "load 1",
            "sup",
            f"jz endloop{current_loop_counter}",
        ]

    def _generate_loop_body(
        self, body: List[str], current_heap_counter: int
    ) -> List[str]:
        for index, line in enumerate(body):
            if line == "i":
                body[index] = f"pushst {current_heap_counter}\nload 1"

            if line == "j":
                body[index] = f"pushst {current_heap_counter - 1}\nload 1"

        return body

    def _generate_loop_end(
        self, current_loop_counter: int, current_heap_counter: int
    ) -> List[str]:
        self.heap_counter -= 1

        return [
            f"pushst {current_heap_counter}",
            "load 1",
            "pushi 1",
            "add",
            f"pushst {current_heap_counter}",
            "swap",
            "store 1",
            f"jump startloop{current_loop_counter}",
            f"endloop{current_loop_counter}:",
            "popst",
        ]

    def _generate_plus_loop_end(
        self, current_loop_counter: int, current_heap_counter: int
    ) -> List[str]:
        self.heap_counter -= 1

        return [
            f"pushst {current_heap_counter}",
            "load 1",
            "add",
            f"pushst {current_heap_counter}",
            "swap",
            "store 1",
            f"jump startloop{current_loop_counter}",
            f"endloop{current_loop_counter}:",
            "popst",
        ]

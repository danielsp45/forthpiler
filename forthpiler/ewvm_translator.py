import forthpiler.syntax as ast


class EWVMTranslator(ast.Translator):
    def __init__(self):
        self.predefined_functions = {".": ["writei"], "emit": ["writechr"]}
        self.user_defined_functions = {}

    def visit_number(self, number: ast.Number) -> list[str]:
        return [f"pushi {number.number}"]

    def visit_operator(self, operator: ast.Operator) -> list[str]:
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

    def visit_function(self, function: ast.Function) -> list[str]:
        if function.name in self.user_defined_functions:
            raise ast.TranslationError(f"Function {function.name} already defined")
        self.user_defined_functions[function.name] = function.ast
        return []

    def visit_literal(self, literal: ast.Literal) -> list[str]:
        value = literal.content
        if value in self.user_defined_functions:
            return self.user_defined_functions[value].evaluate(self)
        if value in self.predefined_functions:
            return self.predefined_functions[value]
        raise ast.TranslationError(f"Literal {value} not found")

    def visit_print_string(self, print_string: ast.PrintString) -> list[str]:
        return [f'pushs "{print_string.content}"\nwrites']

    def visit_char_function(self, char_function: ast.CharFunction) -> list[str]:
        return [f'pushs "{char_function.content}"\nchrcode']

    def translate(self, ast: ast.AbstractSyntaxTree) -> list[str]:
        return [res for expr in ast.expressions for res in expr.evaluate(self)]

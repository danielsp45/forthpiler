import forth_ast


class EWVMTranslator(forth_ast.Translator):
    def __init__(self):
        self.predefined_functions = {
            ".": ["writei"]
        }
        self.user_defined_functions = {}

    def visit_number(self, number: forth_ast.Number) -> list[str]:
        return [f"pushi {number.number}"]

    def visit_operator(self, operator: forth_ast.Operator) -> list[str]:
        match operator.operator_type:
            case forth_ast.OperatorType.PLUS:
                return ["add"]
            case forth_ast.OperatorType.MINUS:
                return ["sub"]
            case forth_ast.OperatorType.TIMES:
                return ["mul"]
            case forth_ast.OperatorType.DIVIDE:
                return ["div"]
            case forth_ast.OperatorType.EXP:
                raise NotImplementedError
            case forth_ast.OperatorType.MOD:
                return ["mod"]
            case forth_ast.OperatorType.SLASH_MOD:
                raise NotImplementedError

    def visit_function(self, function: forth_ast.Function) -> list[str]:
        if function.name in self.user_defined_functions:
            raise forth_ast.TranslationError(f"Function {function.name} already defined")
        self.user_defined_functions[function.name] = function.ast
        return []

    def visit_literal(self, literal: forth_ast.Literal) -> list[str]:
        value = literal.content
        if value in self.user_defined_functions:
            return self.user_defined_functions[value].evaluate(self)
        if value in self.predefined_functions:
            return self.predefined_functions[value]
        raise forth_ast.TranslationError(f"Literal {value} not found")

    def translate(self, ast: forth_ast.AbstractSyntaxTree) -> list[str]:
        return [res for expr in ast.expressions for res in expr.evaluate(self)]

import forth_ast


class EWVMTranslator(forth_ast.Translator):
    predefined_functions = {
        ".": ["writei"]
    }

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
        raise NotImplementedError

    def visit_literal(self, literal: forth_ast.Literal) -> list[str]:
        value = literal.content
        if value not in self.predefined_functions:
            raise forth_ast.TranslationError(f"Literal {value} not found")
        return self.predefined_functions[value]

    def translate(self, ast: forth_ast.AbstractSyntaxTree) -> list[str]:
        return [res for expr in ast.expressions for res in expr.evaluate(self)]

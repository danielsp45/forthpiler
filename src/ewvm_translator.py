import forth_ast


class EWVMTranslator(forth_ast.Translator):
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

    def translate(self, ast: forth_ast.AbstractSyntaxTree) -> list[str]:
        return [res for expr in ast.expressions for res in expr.evaluate(self)]

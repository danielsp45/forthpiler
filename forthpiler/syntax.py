from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import override


class Translator(ABC):
    @abstractmethod
    def visit_number(self, number: Number) -> list[str]:
        pass

    @abstractmethod
    def visit_operator(self, operator: Operator) -> list[str]:
        pass

    @abstractmethod
    def visit_comparison_operator(
        self, comparison_operator: ComparisonOperator
    ) -> list[str]:
        pass

    @abstractmethod
    def visit_function(self, function: Function) -> list[str]:
        pass

    @abstractmethod
    def visit_if_statement(self, if_statement: IfStatement) -> list[str]:
        pass

    @abstractmethod
    def visit_literal(self, literal: Literal) -> list[str]:
        pass

    @abstractmethod
    def visit_print_string(self, print_string: PrintString) -> list[str]:
        pass

    @abstractmethod
    def visit_char_function(self, char_function: CharFunction) -> list[str]:
        pass

    @abstractmethod
    def translate(self, ast: AbstractSyntaxTree) -> list[str]:
        pass


class TranslationError(Exception):
    pass


class Expression(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def evaluate(self, translator: Translator):
        pass


class Number(Expression):
    def __init__(self, number: int):
        super().__init__()
        self.number = number

    @override
    def __repr__(self):
        return f"Number({self.number})"

    @override
    def __eq__(self, other):
        return self.number == other.number

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_number(self)


class OperatorType(Enum):
    PLUS = 1
    MINUS = 2
    TIMES = 3
    DIVIDE = 4
    EXP = 5
    MOD = 6
    SLASH_MOD = 7

    def __eq__(self, other):
        return self.value == other.value


class Operator(Expression):
    def __init__(self, operator_type: OperatorType):
        super().__init__()
        self.operator_type = operator_type

    @override
    def __repr__(self):
        return f"Operator({self.operator_type})"

    @override
    def __eq__(self, other):
        return self.operator_type == other.operator_type

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_operator(self)


class ComparisonOperatorType(Enum):
    EQUALS = 1
    NOT_EQUALS = 2
    LESS_THAN = 3
    LESS_THAN_OR_EQUAL_TO = 4
    GREATER_THAN = 5
    GREATER_THAN_OR_EQUAL_TO = 6
    ZERO_EQUALS = 7
    ZERO_LESS_THAN = 8
    ZERO_LESS_THAN_OR_EQUAL_TO = 9
    ZERO_GREATER_THAN = 10
    ZERO_GREATER_THAN_OR_EQUAL_TO = 11

    def __eq__(self, other):
        return self.value == other.value


class ComparisonOperator(Expression):
    def __init__(self, comparison_operator_type: ComparisonOperatorType):
        super().__init__()
        self.comparison_operator_type = comparison_operator_type

    def __repr__(self):
        return f"ComparisonOperator({self.comparison_operator_type})"

    def __eq__(self, other):
        return self.comparison_operator_type == other.comparison_operator_type

    def evaluate(self, translator: Translator):
        return translator.visit_comparison_operator(self)


class Literal(Expression):
    def __init__(self, content: str):
        super().__init__()
        self.content = content

    @override
    def __repr__(self):
        return f"Literal({self.content})"

    @override
    def __eq__(self, other):
        return self.content == other.content

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_literal(self)


class Function(Expression):
    def __init__(self, name: str, ast: AbstractSyntaxTree):
        super().__init__()
        self.name = name
        self.ast = ast

    def __repr__(self):
        return f"Function(name={self.name}, ast={self.ast})"

    def __eq__(self, other: Function):
        return self.name == other.name and self.ast == other.ast

    def evaluate(self, translator: Translator):
        return translator.visit_function(self)


class IfStatement(Expression):
    def __init__(
        self,
        if_true: AbstractSyntaxTree,
        if_false: AbstractSyntaxTree,
        always: AbstractSyntaxTree,
    ):
        super().__init__()
        self.if_true = if_true
        self.if_false = if_false
        self.always = always

        self.with_else = if_false is not None

    def __repr__(self):
        return f"IfStatement(if_true={self.if_true}, if_false={self.if_false}, always={self.always})"

    def __eq__(self, other):
        return (
            self.if_true == other.if_true
            and self.if_false == other.if_false
            and self.always == other.always
        )

    def evaluate(self, translator: Translator):
        return translator.visit_if_statement(self)


class PrintString(Expression):
    def __init__(self, content: str):
        super().__init__()
        self.content = content

    def __repr__(self):
        return f"PrintString('{self.content}')"

    def __eq__(self, other):
        return self.content == other.content

    def evaluate(self, translator: Translator):
        return translator.visit_print_string(self)


class CharFunction(Expression):
    def __init__(self, content: str):
        super().__init__()
        self.content = content

    def __repr__(self):
        return f"CharFunction('{self.content}')"

    def __eq__(self, other):
        return self.content == other.content

    def evaluate(self, translator: Translator):
        return translator.visit_char_function(self)


class AbstractSyntaxTree:
    def __init__(self, expressions: list[Expression]):
        self.expressions = expressions

    def __repr__(self):
        expressions_repr = ", ".join([str(expr) for expr in self.expressions])
        return f"AST(expressions=[{expressions_repr}])"

    def __eq__(self, other):
        return self.expressions == other.expressions

    def evaluate(self, translator: Translator):
        return translator.translate(self)

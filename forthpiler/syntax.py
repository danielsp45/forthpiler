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
    def visit_function(self, function: Function) -> list[str]:
        pass

    @abstractmethod
    def visit_literal(self, literal: Literal) -> list[str]:
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

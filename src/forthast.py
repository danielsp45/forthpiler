from abc import ABC, abstractmethod
from enum import Enum
from typing import override


class Expression(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass


class Number(Expression):
    def __init__(self, number: int):
        super().__init__()
        self.number = number

    @override
    def __repr__(self):
        return str(self.number)

    @override
    def __eq__(self, other):
        return self.number == other.number


class OperatorType(Enum):
    PLUS = 1
    MINUS = 2
    TIMES = 3
    DIVIDE = 4
    EXP = 5
    MOD = 6
    SLASH_MOD = 7


class Operator(Expression):
    def __init__(self, operator_type: OperatorType):
        super().__init__()
        self.operator_type = operator_type

    @override
    def __repr__(self):
        return str(self.operator_type)

    @override
    def __eq__(self, other):
        return self.operator_type == other.operator_type


class AbstractSyntaxTree:
    def __init__(self, expressions: list[Expression]):
        self.expressions = expressions

    def __repr__(self):
        expressions_repr = ', '.join([str(expr) for expr in self.expressions])
        return f"AST(expressions=[{expressions_repr}])"

    def __eq__(self, other):
        return self.expressions == other.expressions

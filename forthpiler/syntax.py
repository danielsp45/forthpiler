from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Generic, List, Optional, TypeVar, override

T = TypeVar("T", bound="Translator")


class Translator(ABC, Generic[T]):
    @abstractmethod
    def visit_number(self, number: Number) -> T:
        pass

    @abstractmethod
    def visit_operator(self, operator: Operator) -> T:
        pass

    @abstractmethod
    def visit_comparison_operator(self, comparison_operator: ComparisonOperator) -> T:
        pass

    @abstractmethod
    def visit_word(self, function: Word) -> T:
        pass

    @abstractmethod
    def visit_do_loop_statement(self, do_loop: DoLoopStatement) -> T:
        pass

    @abstractmethod
    def visit_do_plus_loop_statement(self, do_loop: DoPlusLoopStatement) -> T:
        pass

    @abstractmethod
    def visit_begin_until_statement(self, begin_until: BeginUntilStatement) -> T:
        pass

    @abstractmethod
    def visit_begin_again_statement(self, begin_again: BeginAgainStatement) -> T:
        pass

    @abstractmethod
    def visit_if_statement(self, if_statement: IfStatement) -> T:
        pass

    @abstractmethod
    def visit_variable_declaration(
            self, variable_declaration: VariableDeclaration
    ) -> T:
        pass

    @abstractmethod
    def visit_constant_declaration(
            self, constant_declaration: ConstantDeclaration
    ) -> T:
        pass

    @abstractmethod
    def visit_store_variable(self, store_variable: StoreVariable) -> T:
        pass

    @abstractmethod
    def visit_fetch_variable(self, fetch_variable: FetchVariable) -> T:
        pass

    @abstractmethod
    def visit_literal(self, literal: Literal) -> T:
        pass

    @abstractmethod
    def visit_print_string(self, print_string: PrintString) -> T:
        pass

    @abstractmethod
    def visit_char_function(self, char_function: CharFunction) -> T:
        pass

    @abstractmethod
    def translate(self, ast: AbstractSyntaxTree) -> T:
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

    def __repr__(self):
        return self.name


class Operator(Expression):
    def __init__(self, operator_type: OperatorType):
        super().__init__()
        self.operator_type = operator_type

    @override
    def __repr__(self):
        return f"Operator({self.operator_type.__repr__()})"

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

    def __repr__(self):
        return self.name


class ComparisonOperator(Expression):
    def __init__(self, comparison_operator_type: ComparisonOperatorType):
        super().__init__()
        self.comparison_operator_type = comparison_operator_type

    @override
    def __repr__(self):
        return f"ComparisonOperator({self.comparison_operator_type.__repr__()})"

    @override
    def __eq__(self, other):
        return self.comparison_operator_type == other.comparison_operator_type

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_comparison_operator(self)


class Literal(Expression):
    def __init__(self, content: str):
        super().__init__()
        self.content = content.lower()

    @override
    def __repr__(self):
        return f"Literal('{self.content}')"

    @override
    def __eq__(self, other):
        return self.content == other.content

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_literal(self)


class Word(Expression):
    def __init__(self, name: str, ast: AbstractSyntaxTree):
        super().__init__()
        self.name = name.lower()
        self.ast = ast

    @override
    def __repr__(self):
        return f"Word(name={self.name}, ast={self.ast})"

    @override
    def __eq__(self, other: Word):
        return self.name == other.name and self.ast == other.ast

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_word(self)


class DoLoopStatement(Expression):
    def __init__(self, ast: AbstractSyntaxTree):
        super().__init__()
        self.body = ast

    @override
    def __repr__(self):
        return f"DoLoopStatement(body={self.body})"

    @override
    def __eq__(self, other: DoLoopStatement):
        return self.body == other.body

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_do_loop_statement(self)


class DoPlusLoopStatement(Expression):
    def __init__(self, ast: AbstractSyntaxTree):
        super().__init__()
        self.body = ast

    @override
    def __repr__(self):
        return f"DoPlusLoopStatement(body={self.body})"

    @override
    def __eq__(self, other: DoPlusLoopStatement):
        return self.body == other.body

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_do_plus_loop_statement(self)


class BeginUntilStatement(Expression):
    def __init__(self, ast: AbstractSyntaxTree):
        super().__init__()
        self.body = ast

    @override
    def __repr__(self):
        return f"BeginUntilStatement(body={self.body})"

    @override
    def __eq__(self, other: BeginUntilStatement):
        return self.body == other.body

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_begin_until_statement(self)


class BeginAgainStatement(Expression):
    def __init__(self, ast: AbstractSyntaxTree):
        super().__init__()
        self.body = ast

    @override
    def __repr__(self):
        return f"BeginAgainStatement(body={self.body})"

    @override
    def __eq__(self, other: BeginUntilStatement):
        return self.body == other.body

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_begin_again_statement(self)


class IfStatement(Expression):
    def __init__(
            self, if_true: AbstractSyntaxTree, if_false: Optional[AbstractSyntaxTree]
    ):
        super().__init__()
        self.if_true = if_true
        self.if_false = if_false

        self.with_else = if_false is not None

    @override
    def __repr__(self):
        return f"IfStatement(if_true={self.if_true}, if_false={self.if_false}"

    @override
    def __eq__(self, other):
        return self.if_true == other.if_true and self.if_false == other.if_false

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_if_statement(self)


class VariableDeclaration(Expression):
    def __init__(self, name: str):
        super().__init__()
        self.name = name.lower()

    @override
    def __repr__(self):
        return f"VariableDeclaration(name={self.name})"

    @override
    def __eq__(self, other):
        return self.name == other.name

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_variable_declaration(self)


class ConstantDeclaration(Expression):
    def __init__(self, name: str):
        super().__init__()
        self.name = name.lower()

    @override
    def __repr__(self):
        return f"ConstantDeclaration(name={self.name})"

    @override
    def __eq__(self, other):
        return self.name == other.name

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_constant_declaration(self)


class StoreVariable(Expression):
    def __init__(self, name: str):
        super().__init__()
        self.name = name.lower()

    @override
    def __repr__(self):
        return f"StoreVariable(name={self.name})"

    @override
    def __eq__(self, other):
        return self.name == other.name

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_store_variable(self)


class FetchVariable(Expression):
    def __init__(self, name: str):
        super().__init__()
        self.name = name.lower()

    @override
    def __repr__(self):
        return f"FetchVariable(name={self.name})"

    @override
    def __eq__(self, other):
        return self.name == other.name

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_fetch_variable(self)


class PrintString(Expression):
    def __init__(self, content: str):
        super().__init__()
        self.content = content

    @override
    def __repr__(self):
        return f"PrintString('{self.content}')"

    @override
    def __eq__(self, other):
        return self.content == other.content

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_print_string(self)


class CharFunction(Expression):
    def __init__(self, char_code: int):
        super().__init__()
        self.char_code = char_code

    @override
    def __repr__(self):
        return f"CharFunction('{self.char_code}')"

    @override
    def __eq__(self, other):
        return self.char_code == other.char_code

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_char_function(self)


class AbstractSyntaxTree:
    def __init__(self, expressions: List[Expression]):
        self.expressions = expressions

    def __repr__(self):
        expressions_repr = ", ".join([str(expr) for expr in self.expressions])
        return f"AST(expressions=[{expressions_repr}])"

    def __eq__(self, other):
        return self.expressions == other.expressions

    def evaluate(self, translator: Translator):
        return translator.translate(self)

from forthpiler.syntax import (
    AbstractSyntaxTree,
    Function,
    Literal,
    Number,
    Operator,
    OperatorType,
)
from forthpiler.lexer import ForthLex
from forthpiler.parser import ForthParser

lexer = ForthLex().build()
parser = ForthParser(lexer)


def test_simple_add():
    code = """1 2 +"""
    assert parser.parse(code) == AbstractSyntaxTree(
        [Number(1), Number(2), Operator(OperatorType.PLUS)]
    )


def test_complex_arithmetic():
    code = """1 2 + 3 *"""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            Number(1),
            Number(2),
            Operator(OperatorType.PLUS),
            Number(3),
            Operator(OperatorType.TIMES),
        ]
    )


def test_all_operators():
    code = """1 2 2 ** + 3 - 4 * 5 / 6 MOD 7 /MOD"""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            Number(1),
            Number(2),
            Number(2),
            Operator(OperatorType.EXP),
            Operator(OperatorType.PLUS),
            Number(3),
            Operator(OperatorType.MINUS),
            Number(4),
            Operator(OperatorType.TIMES),
            Number(5),
            Operator(OperatorType.DIVIDE),
            Number(6),
            Operator(OperatorType.MOD),
            Number(7),
            Operator(OperatorType.SLASH_MOD),
        ]
    )


def test_literal():
    code = """Boas Pessoal .  3 2 +"""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            Literal("Boas"),
            Literal("Pessoal"),
            Literal("."),
            Number(3),
            Number(2),
            Operator(OperatorType.PLUS),
        ]
    )


def test_function():
    code = """: add 3 4 + ; add"""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            Function(
                "add",
                AbstractSyntaxTree([Number(3), Number(4), Operator(OperatorType.PLUS)]),
            ),
            Literal("add"),
        ]
    )

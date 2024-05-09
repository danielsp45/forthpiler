from forthpiler.lexer import ForthLex
from forthpiler.parser import ForthParser
from forthpiler.syntax import (
    AbstractSyntaxTree,
    ComparisonOperator,
    ComparisonOperatorType,
    DoLoopStatement,
    FetchVariable,
    Function,
    IfStatement,
    Literal,
    Number,
    Operator,
    OperatorType,
    PrintString,
    StoreVariable,
    VariableDeclaration,
)

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


def test_simple_function():
    code = """: two 2 ; two"""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            Function(
                "two",
                AbstractSyntaxTree([Number(2)]),
            ),
            Literal("two"),
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


def test_comparison_operators():
    code = """1 2 = 3 <> 4 < 5 0<= 5 <= 6 > 7 >= 8 0 = 9 0< 10 0> <= 11 0 > 12 0 >="""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            Number(1),
            Number(2),
            ComparisonOperator(ComparisonOperatorType.EQUALS),
            Number(3),
            ComparisonOperator(ComparisonOperatorType.NOT_EQUALS),
            Number(4),
            ComparisonOperator(ComparisonOperatorType.LESS_THAN),
            Number(5),
            ComparisonOperator(ComparisonOperatorType.ZERO_LESS_THAN_OR_EQUAL_TO),
            Number(5),
            ComparisonOperator(ComparisonOperatorType.LESS_THAN_OR_EQUAL_TO),
            Number(6),
            ComparisonOperator(ComparisonOperatorType.GREATER_THAN),
            Number(7),
            ComparisonOperator(ComparisonOperatorType.GREATER_THAN_OR_EQUAL_TO),
            Number(8),
            Number(0),
            ComparisonOperator(ComparisonOperatorType.EQUALS),
            Number(9),
            ComparisonOperator(ComparisonOperatorType.ZERO_LESS_THAN),
            Number(10),
            ComparisonOperator(ComparisonOperatorType.ZERO_GREATER_THAN),
            ComparisonOperator(ComparisonOperatorType.LESS_THAN_OR_EQUAL_TO),
            Number(11),
            Number(0),
            ComparisonOperator(ComparisonOperatorType.GREATER_THAN),
            Number(12),
            Number(0),
            ComparisonOperator(ComparisonOperatorType.GREATER_THAN_OR_EQUAL_TO),
        ]
    )


def test_do_loop_outside_function():
    code = """10 0 DO I . LOOP"""
    assert parser.parse(code) == AbstractSyntaxTree([])


def test_do_loop_inside_function():
    code = """: iter 10 0 do i . loop ; iter"""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            Function(
                "iter",
                AbstractSyntaxTree(
                    [
                        Number(10),
                        Number(0),
                        DoLoopStatement(
                            AbstractSyntaxTree(
                                [
                                    Literal("I"),
                                    Literal("."),
                                ]
                            )
                        ),
                    ]
                ),
            ),
            Literal("iter"),
        ]
    )


def test_nested_do_loop_outside_function():
    code = """10 0 DO ." LINE: " 2 0 DO I . LOOP CR LOOP"""
    assert parser.parse(code) == AbstractSyntaxTree([])


def test_nested_do_loop():
    code = """: nested 10 0 DO ." LINE: " 2 0 DO I . LOOP CR LOOP ; nested"""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            Function(
                "nested",
                AbstractSyntaxTree(
                    [
                        Number(10),
                        Number(0),
                        DoLoopStatement(
                            AbstractSyntaxTree(
                                [
                                    PrintString("LINE: "),
                                    Number(2),
                                    Number(0),
                                    DoLoopStatement(
                                        AbstractSyntaxTree(
                                            [
                                                Literal("I"),
                                                Literal("."),
                                            ]
                                        )
                                    ),
                                    Literal("CR"),
                                ]
                            )
                        ),
                    ]
                ),
            ),
            Literal("nested"),
        ]
    )


def test_do_plus_loop():
    code = """: doplus 10 0 DO I . 1 +LOOP ; doplus"""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            Function(
                "doplus",
                AbstractSyntaxTree(
                    [
                        Number(10),
                        Number(0),
                        DoLoopStatement(
                            AbstractSyntaxTree(
                                [
                                    Literal("I"),
                                    Literal("."),
                                    Number(1),
                                ]
                            )
                        ),
                    ]
                ),
            ),
            Literal("doplus"),
        ]
    )


def test_variable_assignment():
    code = """variable x 10 x ! x @ ."""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            VariableDeclaration("x"),
            Number(10),
            StoreVariable("x"),
            FetchVariable("x"),
            Literal("."),
        ]
    )


def test_complex_variable_operations():
    code = """VARIABLE DATE   VARIABLE MONTH   VARIABLE YEAR : STOREDATE  YEAR !  DATE !  MONTH ! ; 7 31 03 STOREDATE"""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            VariableDeclaration("DATE"),
            VariableDeclaration("MONTH"),
            VariableDeclaration("YEAR"),
            Function(
                "STOREDATE",
                AbstractSyntaxTree(
                    [
                        StoreVariable("YEAR"),
                        StoreVariable("DATE"),
                        StoreVariable("MONTH"),
                    ]
                ),
            ),
            Number(7),
            Number(31),
            Number(3),
            Literal("STOREDATE"),
        ]
    )


def test_if_statement_outside_function():
    code = """1 2 = IF 3 ELSE 4 THEN"""
    assert parser.parse(code) == AbstractSyntaxTree([])


def test_if_statement_inside_function():
    code = """: test 1 2 = if 3 else 4 then ; test"""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            Function(
                "test",
                AbstractSyntaxTree(
                    [
                        Number(1),
                        Number(2),
                        ComparisonOperator(ComparisonOperatorType.EQUALS),
                        IfStatement(
                            AbstractSyntaxTree(
                                [
                                    Number(3),
                                ]
                            ),
                            AbstractSyntaxTree(
                                [
                                    Number(4),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            Literal("test"),
        ]
    )

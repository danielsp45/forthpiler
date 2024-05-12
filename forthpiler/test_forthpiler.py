from forthpiler.lexer import ForthLex
from forthpiler.parser import ForthParser
from forthpiler.syntax import *

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
    code = """1 2 2 * + 3 - 4 * 5 / 6 MOD 7 /MOD"""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            Number(1),
            Number(2),
            Number(2),
            Operator(OperatorType.TIMES),
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


def test_word():
    code = """: AVERAGE ( a b -- avg ) + 2/ ; 10 20 AVERAGE ."""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            Word(
                "average",
                AbstractSyntaxTree(
                    [
                        Operator(OperatorType.PLUS),
                        Number(2),
                        Operator(OperatorType.DIVIDE),
                    ]
                ),
            ),
            Number(10),
            Number(20),
            Literal("average"),
            Literal("."),
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


def test_do_loop():
    code = """10 0 DO I . LOOP"""
    assert parser.parse(code) == AbstractSyntaxTree(
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
    )


def test_nested_do_loop():
    code = """10 0 DO ." LINE: " 2 0 DO I . LOOP CR LOOP"""
    assert parser.parse(code) == AbstractSyntaxTree(
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
    )


def test_nested_do_loop_in_word():
    code = """: nested 10 0 DO ." LINE: " 2 0 DO I . LOOP CR LOOP ; nested"""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            Word(
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
    code = """10 0 DO I . 1 +LOOP"""
    assert parser.parse(code) == AbstractSyntaxTree(
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
    )


def test_if_statement():
    code = """1 2 = if 3 then"""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            Number(1),
            Number(2),
            ComparisonOperator(ComparisonOperatorType.EQUALS),
            IfStatement(AbstractSyntaxTree([Number(3)]), None),
        ]
    )


def test_simple_if_else_statement():
    code = """1 2 = if 3 else 4 then"""
    assert parser.parse(code) == AbstractSyntaxTree(
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
    )


def test_if_else_statement_inside_word():
    code = """: test 1 2 = if 3 else 4 then ; test"""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            Word(
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
            Word(
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


def test_begin_until():
    code = """10 BEGIN 1 + DUP . 20 < UNTIL"""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            Number(10),
            BeginUntilStatement(
                AbstractSyntaxTree(
                    [
                        Number(1),
                        Operator(OperatorType.PLUS),
                        Literal("DUP"),
                        Literal("."),
                        Number(20),
                        ComparisonOperator(ComparisonOperatorType.LESS_THAN),
                    ]
                )
            ),
        ]
    )


def test_begin_again():
    code = """BEGIN ." Hello World" AGAIN"""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            BeginUntilStatement(
                AbstractSyntaxTree(
                    [
                        PrintString("Hello World"),
                    ]
                )
            ),
        ]
    )


def test_constant_definition():
    code = """220 CONSTANT LIMIT 10 LIMIT + ."""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            Number(220),
            ConstantDeclaration("LIMIT"),
            Number(10),
            Literal("LIMIT"),
            Operator(OperatorType.PLUS),
            Literal("."),
        ]
    )


def test_char():
    code = """CHAR H 72 CHAR ."""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            CharWord(ord("H")),
            Number(72),
            CharWord(ord(".")),
        ]
    )


def test_char_string():
    code = """CHAR BOAS 34"""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            CharWord(ord("B")),
            Number(34),
        ]
    )


def test_char_quotes():
    code = """CHAR " """
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            CharWord(ord('"')),
        ]
    )


def test_char_char():
    code = """CHAR CHAR"""
    assert parser.parse(code) == AbstractSyntaxTree(
        [
            CharWord(ord("C")),
        ]
    )

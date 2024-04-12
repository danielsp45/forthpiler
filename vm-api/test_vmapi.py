import vmapi


def test_simple_add():
    code = """
pushi 2
pushi 3
add
writei
"""
    assert vmapi.run_code(code) == '5'


def test_swap():
    code = """
pushi 2
pushi 3
swap
writei
"""
    assert vmapi.run_code(code) == '2'

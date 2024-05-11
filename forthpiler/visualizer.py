import graphviz

from forthpiler import syntax
from forthpiler.syntax import *


class GraphvizTranslator(syntax.Translator[str]):
    def __init__(self):
        self.current_id = 0
        self.graph = graphviz.Digraph(comment="Visualize AST")

    def get_new_id(self):
        self.current_id += 1
        return str(self.current_id)

    def visit_number(self, number: Number) -> str:
        e_id = self.get_new_id()
        self.graph.node(e_id, str(number), shape="box")
        return e_id

    def visit_operator(self, operator: Operator) -> str:
        e_id = self.get_new_id()
        self.graph.node(e_id, str(operator), shape="box")
        return e_id

    def visit_comparison_operator(self, comparison_operator: ComparisonOperator) -> str:
        e_id = self.get_new_id()
        self.graph.node(e_id, str(comparison_operator), shape="box")
        return e_id

    def visit_function(self, word: Word) -> str:
        e_id = self.get_new_id()
        self.graph.node(e_id, f"Word(name={word.name})")
        ast_id = self.translate(word.ast)
        self.graph.edge(e_id, ast_id)
        return e_id

    def visit_do_loop_statement(self, do_loop: DoLoopStatement) -> str:
        e_id = self.get_new_id()
        self.graph.node(e_id, f"DoLoopStatement")
        ast_id = self.translate(do_loop.body)
        self.graph.edge(e_id, ast_id)
        return e_id

    def visit_do_plus_loop_statement(self, do_loop: DoPlusLoopStatement) -> str:
        e_id = self.get_new_id()
        self.graph.node(e_id, f"DoPlusLoopStatement")
        ast_id = self.translate(do_loop.body)
        self.graph.edge(e_id, ast_id)
        return e_id

    def visit_begin_until_statement(self, begin_until_loop: BeginUntilStatement) -> str:
        e_id = self.get_new_id()
        self.graph.node(e_id, f"BeginUntilStatement")
        ast_id = self.translate(begin_until_loop.body)
        self.graph.edge(e_id, ast_id)
        return e_id

    def visit_begin_again_statement(self, begin_again_loop: BeginAgainStatement) -> str:
        e_id = self.get_new_id()
        self.graph.node(e_id, f"BeginAgainStatement")
        ast_id = self.translate(begin_again_loop.body)
        self.graph.edge(e_id, ast_id)
        return e_id

    def visit_if_statement(self, if_statement: IfStatement) -> str:
        e_id = self.get_new_id()
        self.graph.node(e_id, f"IfStatement")
        if_true_id = self.get_new_id()

        self.graph.node(if_true_id, f"IfTrue")
        if_true_ast_id = self.translate(if_statement.if_true)
        self.graph.edge(e_id, if_true_id)
        self.graph.edge(if_true_id, if_true_ast_id)

        if if_statement.if_false is not None:
            if_false_id = self.get_new_id()
            self.graph.node(if_false_id, f"IfFalse")
            if_false_ast_id = self.translate(if_statement.if_false)
            self.graph.edge(e_id, if_false_id)
            self.graph.edge(if_false_id, if_false_ast_id)

        return e_id

    def visit_variable_declaration(
        self, variable_declaration: VariableDeclaration
    ) -> str:
        e_id = self.get_new_id()
        self.graph.node(e_id, str(variable_declaration), shape="box")
        return e_id

    def visit_store_variable(self, store_variable: StoreVariable) -> str:
        e_id = self.get_new_id()
        self.graph.node(e_id, str(store_variable), shape="box")
        return e_id

    def visit_fetch_variable(self, fetch_variable: FetchVariable) -> str:
        e_id = self.get_new_id()
        self.graph.node(e_id, str(fetch_variable), shape="box")
        return e_id

    def visit_literal(self, literal: Literal) -> str:
        e_id = self.get_new_id()
        self.graph.node(e_id, str(literal), shape="box")
        return e_id

    def visit_print_string(self, print_string: PrintString) -> str:
        e_id = self.get_new_id()
        self.graph.node(e_id, str(print_string), shape="box")
        return e_id

    def visit_char_function(self, char_function: CharFunction) -> str:
        e_id = self.get_new_id()
        self.graph.node(e_id, str(char_function), shape="box")
        return e_id

    def translate(self, ast: AbstractSyntaxTree) -> str:
        e_id = self.get_new_id()
        self.graph.node(e_id, f"AST(len={len(ast.expressions)})")
        for expression in ast.expressions:
            expression_id = expression.evaluate(self)
            self.graph.edge(e_id, expression_id)
        return e_id


def visualize(ast: syntax.AbstractSyntaxTree):
    translator = GraphvizTranslator()
    translator.translate(ast)

    translator.graph.render("visualize/result", view=True)

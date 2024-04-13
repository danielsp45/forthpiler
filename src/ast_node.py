class ASTNode:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children is None:
            children = []
        self.children = children
        self.leaf = leaf

    def __repr__(self):
        return f"ASTNode(type={self.type}, children={self.children}, leaf={self.leaf})"

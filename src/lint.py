import ast
from collections import defaultdict


class Scope:
    def __init__(self, name):
        self.name = name
        self.load = set()
        self.store = dict()


class Linter(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.stack = []

    def visit_Module(self, node):
        self.stack.append(Scope('global'))
        self.generic_visit(node)
        scope = self.stack.pop()
        self.check(scope)

    def visit_Import(self, node):
        for item in node.names:
            self.stack[-1].store[item.name] = node.lineno
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for item in node.names:
            self.stack[-1].store[item.name] = node.lineno
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if self.stack[-1].name != 'class':
            self.stack[-1].store[node.name] = node.lineno
        else:
            if node.name == '__init__':
                seen = defaultdict(int)
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        seen[item.targets[0].attr] += 1 # noqa

                if problems := {k for (k, v) in seen.items() if v > 1}:
                    msg = ", ".join(p for p in problems)
                    print(f"duplicate attrs   : {msg} ({node.lineno})\n")

        scope = Scope(node.name)
        if node.args.args:
            for arg in node.args.args:
                scope.store[arg.arg] = arg.lineno
        if node.args.kwarg:
            scope.store[node.args.kwarg.arg] = node.args.kwarg.lineno

        self.stack.append(scope)
        self.generic_visit(node)
        scope = self.stack.pop()
        self.check(scope)

    @staticmethod
    def check(scope):
        if unused := set(scope.store).difference(scope.load):
            if 'self' in unused:
                print(f"method '{scope.name}' can be static\n")
                unused.remove('self')
                if not unused:
                    return

            result = sorted([(name, scope.store[name]) for name in unused], key=lambda t: t[1])
            names = f",\n{" " * 20}".join(f"{name} ({lineno})" for name, lineno in result)
            print(f"{scope.name:<18}: {names}\n")

    def visit_ClassDef(self, node):
        self.stack[-1].store[node.name] = node.lineno
        self.stack.append(Scope('class'))
        self.generic_visit(node)
        scope = self.stack.pop()
        self.check(scope)

    def visit_Dict(self, node):
        seen = defaultdict(int)
        for key in node.keys:
            if isinstance(key, ast.Constant):
                seen[key.value] += 1

        if problems := {k for (k, v) in seen.items() if v > 1}:
            msg = ", ".join(p for p in problems)
            print(f"duplicate keys    : {msg} ({node.lineno})\n")
            self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.stack[-1].load.add(node.id)
        elif isinstance(node.ctx, ast.Store):
            self.stack[-1].store[node.id] = node.lineno
        else:
            raise TypeError("Unknown context")
        self.generic_visit(node)


if __name__ == "__main__":
    with open("../resources/test_file.py", "r") as reader:
        source = reader.read()
    tree = ast.parse(source)
    # print(ast.dump(tree, indent=4))
    linter = Linter()
    linter.visit(tree)


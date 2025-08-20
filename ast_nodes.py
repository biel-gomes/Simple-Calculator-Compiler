class Node:
    pass

# Representa um número
class NumNode(Node):
    def __init__(self, valor):
        self.valor = valor

# Representa uma string
class StringNode(Node):
    def __init__(self, valor):
        self.valor = valor

# Representa uma variável
class VarNode(Node):
    def __init__(self, nome):
        self.nome = nome

# Representa uma operação binária, como 2 + 3
class BinOpNode(Node):
    def __init__(self, no_esquerdo, op_token, no_direito):
        self.no_esquerdo = no_esquerdo
        self.op_token = op_token
        self.no_direito = no_direito

# Representa uma atribuição
class AssignNode(Node):
    def __init__(self, var_node, expr_node):
        self.var_node = var_node
        self.expr_node = expr_node

# Representa um comando, como leia(x) ou escreva("Total:")
class CommandNode(Node):
    def __init__(self, cmd_token, child_node):
        self.cmd_token = cmd_token
        self.child_node = child_node
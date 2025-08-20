from tokens import T_SOMA, T_SUBTRACAO, T_MULT, T_DIV, T_LEIA, T_ESCREVA
from ast_nodes import NumNode, StringNode, VarNode, BinOpNode, AssignNode, CommandNode

class Interpreter:
    def __init__(self, tabela_simbolos):
        self.tabela_simbolos = tabela_simbolos

    def visitar(self, no):
        if isinstance(no, NumNode):
            return no.valor
        elif isinstance(no, StringNode):
            return no.valor
        elif isinstance(no, VarNode):
            return self.visitar_VarNode(no)
        elif isinstance(no, BinOpNode):
            return self.visitar_BinOpNode(no)
        elif isinstance(no, AssignNode):
            return self.visitar_AssignNode(no)
        elif isinstance(no, CommandNode):
            return self.visitar_CommandNode(no)
        else:
            raise Exception(f"Tipo desconhecido: {type(no)}")

    def visitar_VarNode(self, no):
        valor = self.tabela_simbolos.get(no.nome)
        if valor is None:
            raise NameError(f"ERRO: A variável '{no.nome}' não foi definida.")
        return valor

    def visitar_BinOpNode(self, no):
        valor_esq = self.visitar(no.no_esquerdo)
        valor_dir = self.visitar(no.no_direito)
        
        op = no.op_token.tipo
        if op == T_SOMA: return valor_esq + valor_dir
        if op == T_SUBTRACAO: return valor_esq - valor_dir
        if op == T_MULT: return valor_esq * valor_dir
        if op == T_DIV:
            if valor_dir == 0: raise ZeroDivisionError("ERRO: Divisão por zero.")
            return valor_esq / valor_dir

    def visitar_AssignNode(self, no):
        valor_expr = self.visitar(no.expr_node)
        self.tabela_simbolos[no.var_node.nome] = valor_expr
        return None
    
    def visitar_CommandNode(self, no):
        tipo_cmd = no.cmd_token.tipo
        if tipo_cmd == T_LEIA:
            var_nome = no.child_node.nome
            while True:
                try:
                    entrada = input()
                    self.tabela_simbolos[var_nome] = float(entrada)
                    break
                except ValueError:
                    print("Entrada inválida. Por favor, digite um número.")
                    print(">> ", end='')
        elif tipo_cmd == T_ESCREVA:
            valor = self.visitar(no.child_node)
            print(valor, end='')
        
        return None
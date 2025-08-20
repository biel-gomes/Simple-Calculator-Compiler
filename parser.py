from tokens import T_NUMERO, T_ID, T_STRING, T_ATRIBUICAO, T_SOMA, T_SUBTRACAO, T_MULT, T_DIV, T_PAREN_E, T_PAREN_D, T_LEIA, T_ESCREVA, T_EOF
from ast_nodes import NumNode, VarNode, StringNode, BinOpNode, AssignNode, CommandNode

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_atual = self.lexer.proximo_token()
        
    def espiar(self):
        # Olha o próximo token sem consumir a entrada
        pos_backup = self.lexer.pos
        char_backup = self.lexer.char_atual
        
        proximo_token = self.lexer.proximo_token()
        
        self.lexer.pos = pos_backup
        self.lexer.char_atual = char_backup
        
        return proximo_token

    def consumir(self, tipo_token):
        if self.token_atual.tipo == tipo_token:
            self.token_atual = self.lexer.proximo_token()
        else:
            raise Exception(f'Erro de Sintaxe: esperado {tipo_token}, encontrado {self.token_atual.tipo}')

    # fator: NUMERO | ID | ( expressao )
    def fator(self):
        token = self.token_atual
        if token.tipo == T_NUMERO:
            self.consumir(T_NUMERO)
            return NumNode(token.valor)
        elif token.tipo == T_ID:
            self.consumir(T_ID)
            return VarNode(token.valor)
        elif token.tipo == T_PAREN_E:
            self.consumir(T_PAREN_E)
            no = self.expressao()
            self.consumir(T_PAREN_D)
            return no
        raise SyntaxError(f"Erro de Sintaxe: Expressão incompleta. Esperado um número, variável ou parêntese, mas encontrou '{token.tipo}'.")

    # termo: fator ((MULT | DIV) fator)*
    def termo(self):
        no = self.fator()
        while self.token_atual.tipo in (T_MULT, T_DIV):
            op_token = self.token_atual
            self.consumir(op_token.tipo)
            no = BinOpNode(no_esquerdo=no, op_token=op_token, no_direito=self.fator())
        return no

    # expressao: termo ((SOMA | SUBTRACAO) termo)*
    def expressao(self):
        no = self.termo()
        while self.token_atual.tipo in (T_SOMA, T_SUBTRACAO):
            op_token = self.token_atual
            self.consumir(op_token.tipo)
            no = BinOpNode(no_esquerdo=no, op_token=op_token, no_direito=self.termo())
        return no

    def parse(self):
        if self.token_atual.tipo in (T_LEIA, T_ESCREVA):
            no_da_arvore = self.parse_comando()
        
        elif self.token_atual.tipo == T_ID and self.espiar().tipo == T_ATRIBUICAO:
            no_da_arvore = self.parse_atribuicao()
        
        else:
            no_da_arvore = self.expressao()

        if self.token_atual.tipo != T_EOF:
            valor = self.token_atual.valor if self.token_atual.valor is not None else self.token_atual.tipo
            raise SyntaxError(f"Erro de Sintaxe: Token inesperado '{valor}' após uma expressão válida.")

        return no_da_arvore
    
    def parse_comando(self):
        cmd_token = self.token_atual
        self.consumir(cmd_token.tipo)
        self.consumir(T_PAREN_E)
        
        if self.token_atual.tipo == T_ID:
            child_node = VarNode(self.token_atual.valor)
            self.consumir(T_ID)
        elif self.token_atual.tipo == T_STRING:
            child_node = StringNode(self.token_atual.valor)
            self.consumir(T_STRING)
        else:
            raise SyntaxError(f"Argumento inválido para comando {cmd_token.tipo}")
        
        self.consumir(T_PAREN_D)
        return CommandNode(cmd_token, child_node)

    def parse_atribuicao(self):
        var_node = VarNode(self.token_atual.valor)
        self.consumir(T_ID)
        self.consumir(T_ATRIBUICAO)
        expr_node = self.expressao()
        return AssignNode(var_node, expr_node)
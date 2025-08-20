T_NUMERO      = 'NUMERO'
T_SOMA        = 'SOMA'
T_SUBTRACAO   = 'SUBTRACAO'
T_MULT        = 'MULT'
T_DIV         = 'DIV'
T_PAREN_E     = 'PAREN_E'
T_PAREN_D     = 'PAREN_D'
T_ID          = 'ID'
T_ATRIBUICAO  = 'ATRIBUICAO'
T_STRING      = 'STRING'
T_LEIA        = 'LEIA'
T_ESCREVA     = 'ESCREVA'
T_EOF         = 'EOF' 


class Token:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"Token({self.tipo}, {repr(self.valor)})"

PALAVRAS_RESERVADAS = {
    'leia': Token(T_LEIA),
    'escreva': Token(T_ESCREVA)
}
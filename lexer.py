from tokens import Token, T_NUMERO, T_ID, T_STRING, T_ATRIBUICAO, T_SOMA, T_SUBTRACAO, T_MULT, T_DIV, T_PAREN_E, T_PAREN_D, T_EOF, PALAVRAS_RESERVADAS

class Lexer:
    def __init__(self, texto):
        self.texto = texto
        self.pos = 0
        self.char_atual = self.texto[self.pos] if self.pos < len(self.texto) else None

    def avancar(self):
        self.pos += 1
        self.char_atual = self.texto[self.pos] if self.pos < len(self.texto) else None

    def pular_espacos(self):
        while self.char_atual is not None and self.char_atual.isspace():
            self.avancar()
    
    def numero(self):
        resultado = ''
        while self.char_atual is not None and (self.char_atual.isdigit() or self.char_atual == '.'):
            resultado += self.char_atual
            self.avancar()
        return float(resultado)

    def string_literal(self):
        resultado = ''
        self.avancar()
        while self.char_atual is not None and self.char_atual != '"':
            resultado += self.char_atual
            self.avancar()
        self.avancar()
        return resultado

    def identificador(self):
        resultado = ''
        while self.char_atual is not None and (self.char_atual.isalnum() or self.char_atual == '_'):
            resultado += self.char_atual
            self.avancar()
        token = PALAVRAS_RESERVADAS.get(resultado.lower(), Token(T_ID, resultado))
        return token

    def proximo_token(self):
        while self.char_atual is not None:
            if self.char_atual.isspace():
                self.pular_espacos()
                continue
            if self.char_atual.isdigit():
                return Token(T_NUMERO, self.numero())
            if self.char_atual.isalpha():
                return self.identificador()
            if self.char_atual == '"':
                return Token(T_STRING, self.string_literal())
            if self.char_atual == ':' and self.pos + 1 < len(self.texto) and self.texto[self.pos + 1] == '=':
                self.avancar()
                self.avancar()
                return Token(T_ATRIBUICAO)
            
            op_map = {'+': T_SOMA, '-': T_SUBTRACAO, '*': T_MULT, '/': T_DIV, '(': T_PAREN_E, ')': T_PAREN_D}
            if self.char_atual in op_map:
                tipo = op_map[self.char_atual]
                self.avancar()
                return Token(tipo)

            raise Exception(f'Caractere inválido: {self.char_atual}')

        return Token(T_EOF)
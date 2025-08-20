from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def main():
    print("Faça seu cálculo ou digite 'sair' para fechar.")
    
    variaveis = {}

    while True:
        try:
            linha = input('>> ')
            if not linha:
                continue
            if linha.lower() == 'sair':
                break
            
            lexer = Lexer(linha)
            
            parser = Parser(lexer)
            arvore = parser.parse()
            
            interpretador = Interpreter(variaveis)
            resultado = interpretador.visitar(arvore)
            
            if resultado is not None:
                print(resultado)

        except (Exception, NameError, ZeroDivisionError) as e:
            print(e)
        except EOFError:
            break
            
    print("\nFinalizando.")

if __name__ == "__main__":
    main()
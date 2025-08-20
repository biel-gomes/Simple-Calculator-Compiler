import sys
from io import StringIO

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def carregar_testes(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    testes_brutos = conteudo.strip().split('====')
    casos_de_teste = []

    for teste_str in testes_brutos:
        if not teste_str.strip():
            continue
        
        linhas = teste_str.strip().split('\n')
        nome_teste = linhas[0].strip()
        
        partes = teste_str.split('--')
        entradas_str = partes[0]
        saida_esperada = partes[1].strip()

        entradas_calculadora = [ln.replace('>> ', '').strip() for ln in entradas_str.split('\n') if ln.startswith('>> ')]
        entradas_leia = [ln.replace('<< ', '').strip() for ln in entradas_str.split('\n') if ln.startswith('<< ')]
        
        casos_de_teste.append({
            'nome': nome_teste,
            'entradas': entradas_calculadora,
            'entradas_leia': entradas_leia,
            'saida_esperada': saida_esperada
        })
    return casos_de_teste

def executar_testes(casos_de_teste):
    """Executa todos os casos de teste e reporta os resultados."""
    sucessos = 0
    falhas = 0
    detalhes_falhas = []

    print("Iniciando execução dos testes...\n")

    for i, teste in enumerate(casos_de_teste):
        print(f"Executando Teste {i+1}: {teste['nome']}")

        # Para cada teste, a tabela de símbolos (memória) é reiniciada
        tabela_de_simbolos = {}
        interpretador = Interpreter(tabela_de_simbolos)
        
        # Redireciona a entrada e saída padrão para capturar os resultados
        stdout_original = sys.stdout
        stdin_original = sys.stdin
        sys.stdout = saida_capturada = StringIO()
        sys.stdin = StringIO('\n'.join(teste['entradas_leia']))

        try:
            # Executa cada linha de entrada do teste
            for linha in teste['entradas']:
                lexer = Lexer(linha)
                parser = Parser(lexer)
                arvore = parser.parse()
                resultado = interpretador.visitar(arvore)
                if resultado is not None:
                    print(resultado)
            
            # Compara o resultado obtido com o esperado
            saida_obtida = saida_capturada.getvalue().strip()
            if saida_obtida == teste['saida_esperada']:
                print("  -> [PASSOU]\n")
                sucessos += 1
            else:
                print(f"  -> [FALHOU]\n")
                falhas += 1
                detalhes_falhas.append({
                    'nome': teste['nome'],
                    'esperado': teste['saida_esperada'],
                    'obtido': saida_obtida
                })

        except (Exception, NameError, ZeroDivisionError, SyntaxError) as e:
            # Se um erro ocorreu durante a execução
            saida_obtida = str(e)
            if saida_obtida == teste['saida_esperada']:
                print("  -> [PASSOU] (Erro esperado foi capturado corretamente)\n")
                sucessos += 1
            else:
                print(f"  -> [FALHOU] (Erro inesperado)\n")
                falhas += 1
                detalhes_falhas.append({
                    'nome': f"{teste['nome']} (Erro Inesperado)",
                    'esperado': teste['saida_esperada'],
                    'obtido': saida_obtida
                })

        finally:
            # Restaura a entrada e saída padrão
            sys.stdout = stdout_original
            sys.stdin = stdin_original

    return sucessos, falhas, detalhes_falhas

def imprimir_relatorio(sucessos, falhas, detalhes_falhas):
    """Imprime um resumo final dos resultados dos testes."""
    total = sucessos + falhas
    print("\n" + "="*30)
    print("      RELATÓRIO FINAL DE TESTES")
    print("="*30)
    print(f"Total de Testes: {total}")
    print(f"Sucessos: {sucessos}")
    print(f"Falhas: {falhas}")
    print("="*30)

    if falhas > 0:
        print("\nDetalhes das Falhas:\n")
        for falha in detalhes_falhas:
            print(f"--- FALHA EM: {falha['nome']} ---")
            print(f"  Esperado : '{falha['esperado']}'")
            print(f"  Obtido   : '{falha['obtido']}'")
            print("-"*(len(falha['nome']) + 16) + "\n")

if __name__ == "__main__":
    casos = carregar_testes('testes.txt')
    s, f, d = executar_testes(casos)
    imprimir_relatorio(s, f, d)
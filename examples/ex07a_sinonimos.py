try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "7A",
    "title": 'Escolha lexical binária',
    "chapter": '7 — Linguagem',
    "summary": 'Codifique bits escolhendo entre duas palavras equivalentes (ex.: \'erro\' = 0, \'problema\' = 1).',
    "algorithm": 'Cada posição do texto tem um par de alternativas pré-definido. Para o bit 0 usa-se a primeira palavra; para o bit 1, a segunda. O receptor, conhecendo os pares, lê qual foi usada. A dificuldade é que sinônimos raramente funcionam em todos os contextos.',
    "references": [6],
}
pares={'rápido':('rápido','veloz'),'erro':('erro','problema')}

def escolher(palavra,bit): return pares[palavra][int(bit)]

def run():
    palavra='erro'
    return result([
        step("1. Par lexical", "Definimos duas alternativas para a mesma posição.", pares[palavra], "json"),
        step("2. Bit 0", "Escolhemos a primeira alternativa.", escolher(palavra,'0')),
        step("3. Bit 1", "Escolhemos a segunda alternativa.", escolher(palavra,'1')),
        step("4. Limitação", "Sinônimos raramente são equivalentes em todos os contextos.", "qualidade semântica precisa ser validada"),
    ], final="O canal usa escolha de palavra, não caracteres invisíveis.")
if __name__ == '__main__': cli_main(run)

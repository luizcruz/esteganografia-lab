try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "2D",
    "title": 'Lendo um acróstico',
    "chapter": '2 — Texto estrutural',
    "summary": 'Extraia uma mensagem escondida nas iniciais de cada linha de um texto comum.',
    "algorithm": 'O texto é dividido em linhas e o algoritmo pega o primeiro caractere de cada uma. Concatenadas, essas letras formam a mensagem. O segredo está na regra posicional combinada entre emissor e receptor, não em caracteres especiais.',
    "references": [],
}
def run():
    texto = 'Sempre revise o código.\nEvite suposições escondidas.\nGaranta testes simples.'
    linhas=texto.splitlines()
    letras=[linha[0] for linha in linhas]
    segredo=''.join(letras)
    return result([
        step("1. Texto", "Leia normalmente: nada precisa parecer estranho.", texto),
        step("2. Regra compartilhada", "Pegue a primeira letra de cada linha.", letras, "json"),
        step("3. Mensagem", "As letras formam o canal posicional.", segredo),
    ], final=segredo)
if __name__ == '__main__': cli_main(run)

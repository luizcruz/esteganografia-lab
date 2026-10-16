try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "9A",
    "title": 'Canal semântico de brinquedo',
    "chapter": '9 — Canais semânticos',
    "summary": 'Canal semântico: o bit decide qual fato verdadeiro e opcional entra no texto.',
    "algorithm": 'Uma frase-base é sempre mantida; para o bit 0 acrescenta-se o fato A e para o bit 1, o fato B — ambos verdadeiros e plausíveis. O sinal está no conteúdo escolhido, não na forma, por isso sobrevive a paráfrases e reformatações.',
    "references": [15],
}
def resumo(bit):
    base='O projeto foi concluído no prazo.'
    if bit=='0': return base+' A equipe utilizou Python.'
    return base+' O sistema passou por testes automatizados.'

def run():
    r0=resumo('0'); r1=resumo('1')
    return result([
        step("1. Base", "A afirmação central é idêntica.", 'O projeto foi concluído no prazo.'),
        step("2. Bit 0", "Inclui um fato opcional A.", r0),
        step("3. Bit 1", "Inclui um fato opcional B.", r1),
        step("4. Diferença", "O sinal está no conteúdo selecionado, não em Unicode ou pontuação.", "o que foi dito"),
    ], final="Canal semântico = significado/seleção de fatos como portador.")
if __name__ == '__main__': cli_main(run)

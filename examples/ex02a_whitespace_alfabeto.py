try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "2A",
    "title": 'Whitespace como alfabeto binário',
    "chapter": '2 — Texto estrutural',
    "summary": 'Use caracteres de espaçamento como alfabeto binário: espaço = 0 e TAB = 1.',
    "algorithm": 'Cada bit da mensagem é trocado por um símbolo de espaçamento — espaço para 0, TAB para 1. Como ambos são invisíveis na maioria das telas, o script usa repr() e marcadores [ESP]/[TAB] para mostrar o que realmente foi gravado.',
    "references": [18],
}
def run():
    ZERO = ' '
    UM = '\t'
    bits = '0101'
    marcas = ''.join(ZERO if b == '0' else UM for b in bits)
    visivel = marcas.replace(' ', '[ESP]').replace('\t', '[TAB]')
    return result([
        step("1. Definir o alfabeto", "Espaço representa 0; TAB representa 1.", {"0":"[ESP]","1":"[TAB]"}, "json"),
        step("2. Codificar 0101", "Trocamos cada bit pela marca correspondente.", visivel),
        step("3. Ver o conteúdo real", "repr() torna TAB e espaços mais fáceis de inspecionar.", repr(marcas)),
    ], final=visivel)
if __name__ == '__main__': cli_main(run)

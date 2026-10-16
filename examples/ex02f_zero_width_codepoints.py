try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "2F",
    "title": 'Enxergando zero-width por code point',
    "chapter": '2 — Texto estrutural',
    "summary": 'Revele caracteres invisíveis (zero-width) inspecionando os code points Unicode.',
    "algorithm": 'Uma string que aparenta ser \'ABC\' recebe U+200B e U+200C entre as letras. O script compara o comprimento (5, não 3) e lista cada caractere como U+XXXX com ord(), tornando visível o que a renderização esconde.',
    "references": [19],
}
def mostrar_codepoints(texto):
    return [f'U+{ord(c):04X}' for c in texto]

def run():
    ZERO='\u200b'; UM='\u200c'
    s='A'+ZERO+'B'+UM+'C'
    return result([
        step("1. String", "Na tela ela parece quase apenas ABC.", s),
        step("2. Comprimento", "Há cinco code points, não três.", len(s)),
        step("3. Code points", "U+200B e U+200C revelam os caracteres extras.", mostrar_codepoints(s), "json"),
    ], final="O que os olhos não mostram, o computador ainda armazena.")
if __name__ == '__main__': cli_main(run)

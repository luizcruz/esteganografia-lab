try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "7C",
    "title": 'Ativa versus passiva',
    "chapter": '7 — Linguagem',
    "summary": 'Codifique bits pela estrutura da frase: voz ativa = 0, voz passiva = 1.',
    "algorithm": 'Para o bit 0 a frase é gerada na voz ativa; para o bit 1, na passiva. O conteúdo é o mesmo, mudando só a sintaxe. O receptor identifica a construção usada para recuperar o bit.',
    "references": [15],
}
def frase(bit):
    if bit=='0': return 'A equipe aprovou o plano.'
    return 'O plano foi aprovado pela equipe.'

def run():
    f0=frase('0'); f1=frase('1')
    return result([
        step("1. Bit 0", "Voz ativa.", f0),
        step("2. Bit 1", "Voz passiva.", f1),
        step("3. Comparação", "A proposição central é semelhante, mas foco e estilo mudam.", {"ativa":f0,"passiva":f1}, "json"),
    ], final="Isso é codificação sintática; não é DCT.")
if __name__ == '__main__': cli_main(run)

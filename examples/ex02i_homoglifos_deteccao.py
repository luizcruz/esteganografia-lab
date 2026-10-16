try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "2I",
    "title": 'Detectando um homóglifo específico',
    "chapter": '2 — Texto estrutural',
    "summary": 'Construa um detector simples que encontra um homóglifo cirílico escondido no texto.',
    "algorithm": 'O algoritmo percorre o texto caractere por caractere e registra a posição de cada ocorrência do \'а\' cirílico (U+0430). É uma defesa mínima: um detector real verificaria o script Unicode de cada caractere e sinalizaria mistura de alfabetos.',
    "references": [],
}
def detectar_scripts_simplificado(texto):
    suspeitos=[]
    for i,c in enumerate(texto):
        if c=='а':
            suspeitos.append((i,'U+0430'))
    return suspeitos

def run():
    texto='Casа'
    suspeitos=detectar_scripts_simplificado(texto)
    return result([
        step("1. Texto recebido", "Parece 'Casa', mas a última letra não é latina.", texto),
        step("2. Varredura", "Procuramos o code point cirílico usado nesta demonstração.", suspeitos, "json"),
        step("3. Interpretação", "Uma defesa real verificaria scripts Unicode de forma geral, não apenas um caractere.", "detector didático"),
    ], final=f"Ocorrências suspeitas: {len(suspeitos)}")
if __name__ == '__main__': cli_main(run)

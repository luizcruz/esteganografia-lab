try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "13B",
    "title": 'Steganographic gap simplificado',
    "chapter": '13 — LLM steganalysis',
    "summary": 'Steganographic gap: meça quanto o receptor ganha a mais que um observador sem a chave.',
    "algorithm": 'O gap é a utilidade obtida pelo receptor (que conhece o esquema) menos a de um sentinel com capacidade semelhante, mas sem conhecê-lo. Um gap grande indica que existe informação útil oculta, acessível apenas a quem tem o segredo.',
    "references": [15],
}
def steg_gap(utilidade_receptor,utilidade_sentinel): return utilidade_receptor-utilidade_sentinel

def run():
    receptor=.85; sentinel=.15; gap=steg_gap(receptor,sentinel)
    return result([
        step("1. Receptor", "Conhece o esquema e consegue aproveitar a informação oculta.", receptor),
        step("2. Sentinel", "Tem capacidades semelhantes, mas não conhece o esquema.", sentinel),
        step("3. Diferença", "A assimetria de utilidade é a intuição do gap.", gap),
    ], final=f"Δsteg = {gap:.2f}", note="A formalização do paper é mais rica; este exemplo mostra apenas a diferença intuitiva.")
if __name__ == '__main__': cli_main(run)

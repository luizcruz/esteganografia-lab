try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "13A",
    "title": 'Perplexidade simplificada',
    "chapter": '13 — LLM steganalysis',
    "summary": 'Calcule a perplexidade de um texto: a \'surpresa\' média do modelo diante dos tokens.',
    "algorithm": 'Toma-se o logaritmo da probabilidade de cada token, calcula-se a média e aplica-se exp(−média) — equivalente ao inverso da média geométrica das probabilidades. Tokens prováveis dão perplexidade baixa; improváveis, alta. Pode indicar manipulação, mas sozinha não prova esteganografia.',
    "references": [14],
}
import math

def perplexidade(probabilidades):
    logp=sum(math.log(p) for p in probabilidades)/len(probabilidades)
    return math.exp(-logp)

def run():
    a=[0.5,0.4,0.6]; b=[0.2,0.3,0.1]
    pa=perplexidade(a); pb=perplexidade(b)
    return result([
        step("1. Sequência A", "Tokens relativamente prováveis.", a, "json"),
        step("2. Perplexidade A", "Menor surpresa média.", round(pa,3)),
        step("3. Sequência B", "Tokens menos prováveis.", b, "json"),
        step("4. Perplexidade B", "Maior surpresa média.", round(pb,3)),
        step("5. Limite", "Perplexidade alta ou baixa, sozinha, não prova esteganografia.", "métrica ≠ prova"),
    ], final=f"A={pa:.3f}; B={pb:.3f}")
if __name__ == '__main__': cli_main(run)

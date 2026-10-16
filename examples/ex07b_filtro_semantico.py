try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "7B",
    "title": 'Filtro de similaridade semântica',
    "chapter": '7 — Linguagem',
    "summary": 'Filtre substituições de palavras: aceite só as que mantêm o sentido acima de um limiar.',
    "algorithm": 'Cada substituição candidata tem uma pontuação de similaridade semântica; o algoritmo aceita apenas as que atingem o limiar (0,90). Em um sistema real, essa pontuação viria de embeddings de um modelo de linguagem.',
    "references": [],
}
def aceitar_substituicao(similaridade,limiar=0.90): return similaridade>=limiar

def run():
    testes=[0.94,0.81,0.90]
    dados=[{"similaridade":s,"aceita":aceitar_substituicao(s)} for s in testes]
    return result([
        step("1. Limiar", "Neste exemplo exigimos pelo menos 0,90.", 0.90),
        step("2. Avaliar candidatos", "Pontuações maiores passam pelo filtro.", dados, "json"),
        step("3. Interpretação", "Um embedding real produziria a similaridade; aqui usamos números fornecidos.", "filtro didático"),
    ], final="0,94 passa; 0,81 é rejeitado.")
if __name__ == '__main__': cli_main(run)

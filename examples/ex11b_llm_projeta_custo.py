try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "11B",
    "title": 'LLM como projetista de custo — simulação',
    "chapter": '11 — Deep learning',
    "summary": 'Simule o ciclo em que um LLM propõe funções de custo e as melhores são selecionadas.',
    "algorithm": 'A cada rodada geram-se 5 funções candidatas (com complexidade e artefato aleatórios). Cada uma recebe um score fictício que premia complexidade e penaliza artefatos; as duas melhores viram feedback para a rodada seguinte. Reproduz a estrutura de busca evolutiva do paper, não seus resultados.',
    "references": [13],
}
import random

def candidatos(rodada):
    rng=random.Random(rodada)
    return [{"nome":f'f{rodada}_{i}',"complexidade":rng.uniform(.1,1.0),"artefato":rng.uniform(.1,1.0)} for i in range(5)]

def avaliar(c):
    # score maior = melhor, apenas para a simulação
    return 1.2*c['complexidade']-0.8*c['artefato']

def run():
    historico=[]; feedback=None
    for rodada in range(3):
        cs=candidatos(rodada)
        pont=[{**c,"score":round(avaliar(c),3)} for c in cs]
        pont.sort(key=lambda x:x['score'],reverse=True)
        feedback=pont[:2]
        historico.append({"rodada":rodada+1,"top2":feedback})
    return result([
        step("1. Gerar candidatos", "Simulamos programas de função de custo.", "5 por rodada"),
        step("2. Avaliar", "Uma função de avaliação fictícia substitui o steganalyzer real.", historico, "json"),
        step("3. Selecionar", "Os melhores seriam usados como feedback para a próxima rodada.", feedback, "json"),
    ], final=f"Melhor candidato final: {feedback[0]['nome']}", note="O script executa a estrutura do ciclo, não reproduz o método experimental do paper.")
if __name__ == '__main__': cli_main(run)

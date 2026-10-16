try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "5B",
    "title": 'Escolher posições de menor custo',
    "chapter": '5 — Minimum distortion',
    "summary": 'Escolha onde esconder os bits: selecione as posições do cover com menor custo.',
    "algorithm": 'O algoritmo associa cada posição ao seu custo, ordena do menor para o maior e pega as k primeiras. É uma estratégia gulosa; métodos reais como STC (Syndrome-Trellis Codes) resolvem o problema completo de transportar a mensagem minimizando a soma dos custos.',
    "references": [1],
}
def escolher_posicoes(custos,quantidade):
    pares=sorted(enumerate(custos),key=lambda x:x[1])
    return [indice for indice,_ in pares[:quantidade]],pares

def run():
    custos=[10.0,0.7,5.2,0.4,3.0]
    escolhidas,ordenadas=escolher_posicoes(custos,2)
    return result([
        step("1. Custos", "Cada unidade do cover recebeu um risco estimado.", custos, "json"),
        step("2. Ordenar", "Visualize índice e custo do menor para o maior.", ordenadas, "json"),
        step("3. Selecionar", "Pegamos as duas posições mais baratas.", escolhidas, "json"),
    ], final="Escolhidas: [3, 1]", note="STC resolve um problema mais completo: transportar a mensagem obedecendo custos.")
if __name__ == '__main__': cli_main(run)

try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "4C",
    "title": 'PVD: capacidade pelo contraste',
    "chapter": '4 — Frequência e codificação',
    "summary": 'PVD (Pixel-Value Differencing): regiões com mais contraste podem guardar mais bits.',
    "algorithm": 'Para cada par de pixels vizinhos, o algoritmo calcula a diferença absoluta e a enquadra em faixas (<8, <16, <32, ≥32), atribuindo de 1 a 4 bits de capacidade. Bordas toleram mudanças maiores sem serem percebidas. Versão simplificada do método de Wu e Tsai.',
    "references": [22],
}
def capacidade_pvd_simplificada(a,b):
    d=abs(a-b)
    if d<8:return 1
    if d<16:return 2
    if d<32:return 3
    return 4

def run():
    pares=[(120,122),(120,131),(120,151),(20,100)]
    dados=[{"par":p,"diferenca":abs(p[0]-p[1]),"capacidade":capacidade_pvd_simplificada(*p)} for p in pares]
    return result([
        step("1. Calcular diferenças", "Pares suaves produzem diferenças pequenas; bordas produzem maiores.", dados, "json"),
        step("2. Interpretar", "Nesta simplificação, diferenças maiores recebem maior capacidade.", "mais contraste → mais bits"),
    ], final="Este script ensina a intuição, não o PVD completo de Wu e Tsai.")
if __name__ == '__main__': cli_main(run)

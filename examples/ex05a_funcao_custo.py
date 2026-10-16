try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "5A",
    "title": 'Função de custo de brinquedo',
    "chapter": '5 — Minimum distortion',
    "summary": 'Uma função de custo de brinquedo: alterar regiões complexas é mais barato que alterar regiões lisas.',
    "algorithm": 'Para cada posição, o custo é 1 / variação local. Regiões suaves (pouca variação) ficam caras de modificar; regiões texturizadas ficam baratas, pois são difíceis de modelar e escondem melhor as mudanças. É a ideia por trás de métodos de distorção mínima como HUGO, WOW e S-UNIWARD.',
    "references": [1],
}
def custo(local_variacao):
    return 1.0/(local_variacao+1e-6)

def run():
    variacoes=[0.1,1,5,20]
    dados=[{"variacao":v,"custo":round(custo(v),3)} for v in variacoes]
    return result([
        step("1. Variação local", "Valores baixos representam regiões mais suaves.", variacoes, "json"),
        step("2. Custo", "Nesta função didática, maior variação significa menor custo.", dados, "json"),
        step("3. Intuição", "Modificar regiões difíceis de modelar tende a deixar menos rastro.", "complexidade ↑ → custo ↓"),
    ], final="A função real em métodos modernos é muito mais sofisticada.")
if __name__ == '__main__': cli_main(run)

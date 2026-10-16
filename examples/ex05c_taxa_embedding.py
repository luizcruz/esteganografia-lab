try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "5C",
    "title": 'Taxa de incorporação',
    "chapter": '5 — Minimum distortion',
    "summary": 'Calcule a taxa de incorporação: quantos bits de payload por unidade de cover.',
    "algorithm": 'taxa = bits do payload / unidades disponíveis no cover (pixels, coeficientes etc.). O script compara três cenários: quanto maior a taxa, mais alterações e, em geral, maior o risco de detecção.',
    "references": [1],
}
def taxa(payload_bits,unidades_cover): return payload_bits/unidades_cover

def run():
    casos=[(1000,100000),(5000,100000),(10000,100000)]
    dados=[{"payload_bits":p,"unidades":u,"taxa":taxa(p,u)} for p,u in casos]
    return result([
        step("1. Fórmula", "taxa = bits do payload / unidades disponíveis", "p/u"),
        step("2. Exemplos", "Aumentar o payload aumenta a taxa e normalmente também o rastro.", dados, "json"),
    ], final="1000 / 100000 = 0,01 bit por unidade")
if __name__ == '__main__': cli_main(run)

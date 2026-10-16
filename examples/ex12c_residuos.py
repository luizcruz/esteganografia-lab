try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "12C",
    "title": 'Resíduo 1D',
    "chapter": '12 — Esteganálise',
    "summary": 'Calcule resíduos: as diferenças entre valores vizinhos, base de muitos steganalyzers.',
    "algorithm": 'Para cada posição, subtrai-se o valor atual do seguinte, obtendo a sequência de resíduos. Isso remove o conteúdo \'liso\' do sinal e destaca o ruído fino, onde as alterações esteganográficas ficam mais aparentes.',
    "references": [1],
}
def run():
    valores=[10,11,10,10,13,12]
    residuos=[valores[i+1]-valores[i] for i in range(len(valores)-1)]
    pares=[{"de":valores[i],"para":valores[i+1],"residuo":residuos[i]} for i in range(len(residuos))]
    return result([
        step("1. Sinal", "Sequência numérica simples.", valores, "json"),
        step("2. Diferenças locais", "Subtraímos cada valor de seu vizinho seguinte.", pares, "json"),
        step("3. Resíduos", "Modelos de esteganálise trabalham com ideias muito mais ricas desse tipo.", residuos, "json"),
    ], final=str(residuos))
if __name__ == '__main__': cli_main(run)

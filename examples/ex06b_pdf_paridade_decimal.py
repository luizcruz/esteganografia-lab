try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "6B",
    "title": 'Paridade decimal conceitual',
    "chapter": '6 — PDF',
    "summary": 'Esconda um bit na última casa decimal de um número em um stream PDF.',
    "algorithm": 'O valor é multiplicado por 1000 para levar a 3ª casa decimal ao domínio inteiro; o LSB desse inteiro é forçado para o bit da mensagem e o resultado é dividido de volta por 1000. A mudança máxima é 0,001 — invisível na renderização.',
    "references": [7],
}
def codificar_decimal(valor,bit,casas=3):
    escala=10**casas
    inteiro=round(valor*escala)
    inteiro=(inteiro & ~1)|int(bit)
    return inteiro/escala

def run():
    valor=12.000; bit='1'; saida=codificar_decimal(valor,bit)
    return result([
        step("1. Valor", "Imagine um operando de ponto flutuante em um stream PDF.", valor),
        step("2. Escalar", "Multiplicar por 1000 leva a última casa ao domínio inteiro.", int(round(valor*1000))),
        step("3. Forçar paridade", "Definimos o LSB do inteiro conforme o bit.", int(round(saida*1000))),
        step("4. Voltar a decimal", "Dividimos novamente pela escala.", saida),
    ], final=f"{valor:.3f} → {saida:.3f}", note="Demonstração conceitual; editar PDF real exige parser e validação estrutural.")
if __name__ == '__main__': cli_main(run)

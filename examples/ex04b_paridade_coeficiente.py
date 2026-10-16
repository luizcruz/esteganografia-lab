try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "4B",
    "title": 'Paridade de coeficiente',
    "chapter": '4 — Frequência e codificação',
    "summary": 'Esconda um bit na paridade de um coeficiente de frequência arredondado.',
    "algorithm": 'O coeficiente é arredondado para inteiro; se sua paridade (par = 0, ímpar = 1) não corresponde ao bit, soma-se 1. Ex.: 12,2 → 12 → 13 para transportar o bit 1. É apenas a intuição de embedding em coeficientes, sem quantização nem codec JPEG reais.',
    "references": [24],
}
def esconder_bit_na_paridade(valor,bit):
    inteiro=int(round(valor))
    if (inteiro&1)!=int(bit): inteiro+=1
    return inteiro

def run():
    valor=12.2; bit='1'; arred=int(round(valor)); saida=esconder_bit_na_paridade(valor,bit)
    return result([
        step("1. Coeficiente", "Valor de brinquedo vindo de uma transformada.", valor),
        step("2. Arredondar", "Trabalhamos com um inteiro para observar paridade.", arred),
        step("3. Ajustar", "Se a paridade não representa o bit, somamos 1.", saida),
        step("4. LSB final", "13 é ímpar, portanto representa 1 neste esquema simples.", saida&1),
    ], final="12.2 → 13 para transportar o bit 1", note="Não é um JPEG stego completo; quantização e codec reais exigem muito mais cuidado.")
if __name__ == '__main__': cli_main(run)

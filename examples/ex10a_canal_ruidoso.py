try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "10A",
    "title": 'Canal ruidoso',
    "chapter": '10 — Robustez',
    "summary": 'Simule um canal ruidoso que inverte bits aleatoriamente durante o transporte.',
    "algorithm": 'Para cada bit enviado sorteia-se um número; se ele for menor que a probabilidade de erro (25%), o bit é invertido. O resultado modela de forma abstrata recompressão, edição ou sanitização sofridas pelo stego-object.',
    "references": [9],
}
import random

def canal_ruidoso(bits,prob_erro=0.1,rng=None):
    rng=rng or random; saida=[]; eventos=[]
    for i,b in enumerate(bits):
        errou=rng.random()<prob_erro
        novo=('1' if b=='0' else '0') if errou else b
        saida.append(novo); eventos.append({"i":i,"antes":b,"depois":novo,"erro":errou})
    return ''.join(saida),eventos

def run():
    bits='10101010'; saida,eventos=canal_ruidoso(bits,0.25,random.Random(2))
    return result([
        step("1. Bits enviados", "Mensagem binária antes do canal.", bits),
        step("2. Eventos", "Cada posição tem chance de ser invertida.", eventos, "json"),
        step("3. Bits recebidos", "Erros representam edições, recompressões ou outras transformações de forma abstrata.", saida),
    ], final=f"Erros: {sum(e['erro'] for e in eventos)}")
if __name__ == '__main__': cli_main(run)

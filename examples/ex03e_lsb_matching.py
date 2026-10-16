try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "3E",
    "title": 'LSB matching (±1)',
    "chapter": '3 — Imagens e LSB',
    "summary": 'LSB matching: ajuste a paridade somando ou subtraindo 1 ao acaso, em vez de substituir o bit.',
    "algorithm": 'Se o LSB do valor já é igual ao bit, nada muda. Caso contrário, o algoritmo soma +1 ou −1 aleatoriamente (respeitando os limites 0 e 255). O receptor lê o LSB do mesmo jeito, mas a alteração aleatória evita o padrão estatístico de pares que denuncia o LSB replacement.',
    "references": [1, 5],
}
import random

def lsb_matching(valor,bit,rng):
    if (valor&1)==int(bit): return valor
    if valor==0: return 1
    if valor==255: return 254
    return valor+rng.choice([-1,1])

def run():
    rng=random.Random(7)
    entradas=[120,121,0,255,122]
    bits=['1','1','1','0','1']
    linhas=[]
    for v,b in zip(entradas,bits):
        s=lsb_matching(v,b,rng)
        linhas.append({"valor":v,"bit":b,"saida":s,"delta":s-v,"lsb_final":s&1})
    return result([
        step("1. Regra", "Se a paridade já corresponde ao bit, não mudamos nada.", "(valor & 1) == bit"),
        step("2. Caso contrário", "Escolhemos +1 ou -1, respeitando os limites 0 e 255.", linhas, "json"),
    ], final="O objetivo continua sendo controlar a paridade, mas sem substituição determinística.")
if __name__ == '__main__': cli_main(run)

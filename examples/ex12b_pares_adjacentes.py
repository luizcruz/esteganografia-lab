try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "12B",
    "title": 'Regularidade em pares adjacentes',
    "chapter": '12 — Esteganálise',
    "summary": 'Detecte LSB pela regularidade entre frequências de pares vizinhos (2k, 2k+1).',
    "algorithm": 'O algoritmo agrupa o histograma em pares de valores (100/101, 102/103…) e soma as diferenças absolutas de frequência em cada par. O LSB replacement tende a igualar essas frequências, então uma soma muito baixa é suspeita. É a intuição do ataque qui-quadrado.',
    "references": [17],
}
def diferenca_pares(hist):
    soma=0; detalhes=[]
    for v in range(0,254,2):
        a,b=hist.get(v,0),hist.get(v+1,0)
        if a or b:
            detalhes.append({"par":[v,v+1],"freq":[a,b],"delta":abs(a-b)})
        soma+=abs(a-b)
    return soma,detalhes

def run():
    h1={100:80,101:20}; h2={100:51,101:49}
    s1,d1=diferenca_pares(h1); s2,d2=diferenca_pares(h2)
    return result([
        step("1. Histograma A", "Frequências bem desequilibradas.", d1, "json"),
        step("2. Histograma B", "Frequências quase iguais.", d2, "json"),
        step("3. Métrica simples", "Somamos diferenças absolutas entre pares.", {"A":s1,"B":s2}, "json"),
    ], final="É apenas uma intuição; não é o teste chi-square completo.")
if __name__ == '__main__': cli_main(run)

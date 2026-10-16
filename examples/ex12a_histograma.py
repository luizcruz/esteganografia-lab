try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "12A",
    "title": 'Histograma mínimo',
    "chapter": '12 — Esteganálise',
    "summary": 'Monte um histograma: conte quantas vezes cada valor de pixel aparece.',
    "algorithm": 'Counter percorre a lista de valores e conta as ocorrências de cada um, gerando uma tabela valor → frequência. Esteganálise estatística parte daí: certos embeddings alteram essas frequências de forma detectável.',
    "references": [17],
}
from collections import Counter

def run():
    valores=[100,100,100,101,101,102,102,102,102]
    h=Counter(valores)
    tabela=[{"valor":v,"frequencia":h[v]} for v in sorted(h)]
    return result([
        step("1. Amostras", "Pense nesses números como intensidades ou valores de pixels.", valores, "json"),
        step("2. Contar", "Counter calcula a frequência de cada valor.", tabela, "json"),
        step("3. Por que importa", "Alguns embeddings alteram relações de frequência entre valores vizinhos.", "estatística pode revelar mudanças invisíveis"),
    ], final=str(dict(h)))
if __name__ == '__main__': cli_main(run)

try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "8B",
    "title": 'Particionando tokens aceitáveis',
    "chapter": '8 — LLMs',
    "summary": 'Divida os tokens plausíveis em dois grupos e use o grupo escolhido para transmitir um bit.',
    "algorithm": 'Primeiro descartam-se tokens com probabilidade abaixo do limiar. Os restantes são divididos por posição: índices pares formam o grupo do bit 0 e ímpares o do bit 1. Para enviar um bit, o gerador só pode escolher dentro do grupo correspondente — o que distorce a distribuição original.',
    "references": [6],
}
def grupo(bit,candidatos,limiar=0.10):
    validos=[t for t,p in candidatos if p>=limiar]
    return validos[::2] if bit=='0' else validos[1::2]

def run():
    candidatos=[('azul',0.45),('limpo',0.30),('nublado',0.15),('escuro',0.10)]
    g0=grupo('0',candidatos); g1=grupo('1',candidatos)
    return result([
        step("1. Filtrar", "Descartamos candidatos abaixo do limiar.", [t for t,p in candidatos if p>=0.10], "json"),
        step("2. Grupo 0", "Índices pares da lista válida.", g0, "json"),
        step("3. Grupo 1", "Índices ímpares da lista válida.", g1, "json"),
        step("4. Consequência", "Forçar um grupo pode impedir o token originalmente mais provável.", "plausível ≠ estatisticamente invisível"),
    ], final=f"0 → {g0}; 1 → {g1}")
if __name__ == '__main__': cli_main(run)

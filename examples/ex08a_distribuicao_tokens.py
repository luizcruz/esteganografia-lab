try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "8A",
    "title": 'Distribuição de tokens de brinquedo',
    "chapter": '8 — LLMs',
    "summary": 'Visualize como um modelo de linguagem distribui probabilidades entre os próximos tokens.',
    "algorithm": 'Uma lista de tokens candidatos com probabilidades (somando 1) é exibida junto da probabilidade acumulada, que mostra como um sorteio escolheria cada token. Essa liberdade entre opções plausíveis é o espaço que a esteganografia com LLMs explora.',
    "references": [6],
}
def run():
    candidatos=[('azul',0.45),('limpo',0.30),('nublado',0.15),('escuro',0.10)]
    acumulado=0; linhas=[]
    for token,p in candidatos:
        acumulado+=p; linhas.append({"token":token,"p":p,"acumulado":round(acumulado,2)})
    return result([
        step("1. Próximos tokens", "Um modelo distribui probabilidade entre alternativas.", candidatos, "json"),
        step("2. Soma", "As probabilidades deste exemplo somam 1.", sum(p for _,p in candidatos)),
        step("3. Acumulada", "Ajuda a visualizar como uma amostragem poderia escolher tokens.", linhas, "json"),
    ], final="A liberdade entre alternativas plausíveis pode ser usada como canal.")
if __name__ == '__main__': cli_main(run)

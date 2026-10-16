try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "2E",
    "title": 'Gerando um acróstico',
    "chapter": '2 — Texto estrutural',
    "summary": 'Gere um acróstico: construa linhas cujas iniciais soletram a palavra secreta.',
    "algorithm": 'Para cada letra do segredo, o algoritmo junta a letra a uma continuação de frase fornecida, formando uma linha. As linhas são unidas com quebras de linha e, para verificar, as iniciais são lidas de volta. Exige exatamente uma continuação por letra.',
    "references": [],
}
def criar_acrostico(segredo, continuacoes):
    if len(segredo) != len(continuacoes):
        raise ValueError('uma continuação por letra')
    return '\n'.join(letra + resto for letra, resto in zip(segredo, continuacoes))

def run():
    segredo='SOL'
    continuacoes=['istemas devem ser testados.','bserve a saída com atenção.','eia os resultados antes de concluir.']
    texto=criar_acrostico(segredo,continuacoes)
    recuperado=''.join(l[0] for l in texto.splitlines())
    return result([
        step("1. Segredo", "Cada letra precisa iniciar uma linha.", segredo),
        step("2. Completar as linhas", "As continuações dão aparência de texto comum.", continuacoes, "json"),
        step("3. Cover gerado", "O resultado carrega o acróstico.", texto),
        step("4. Verificação", "Ler as iniciais recupera a palavra.", recuperado),
    ], final=recuperado)
if __name__ == '__main__': cli_main(run)

try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "0C",
    "title": 'Cover, payload e stego-object',
    "chapter": '0 — Fundamentos',
    "summary": 'Separe os três papéis de todo sistema: cover (cobertura), payload (segredo) e stego-object (resultado).',
    "algorithm": 'Não há incorporação ainda: o script apenas declara um cover (lista de números), um payload (bits) e mostra que o stego-object só passa a existir depois que um algoritmo de embedding combina os dois. É o vocabulário usado em todas as aulas seguintes.',
    "references": [1, 2, 4],
}
def run():
    cover = [100, 101, 102, 103]
    payload = '10'
    stego_object = None
    return result([
        step("1. Cover", "É o objeto aparentemente comum que servirá de cobertura.", cover, "json"),
        step("2. Payload", "É a mensagem que desejamos transportar de forma oculta.", payload),
        step("3. Stego-object", "Só existirá depois que algum algoritmo incorporar o payload ao cover.", stego_object, "json"),
    ], final="Primeiro identifique os papéis; só depois escolha um algoritmo.")
if __name__ == '__main__': cli_main(run)

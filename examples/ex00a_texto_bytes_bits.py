try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "0A",
    "title": 'Texto → bytes → bits',
    "chapter": '0 — Fundamentos',
    "summary": 'Veja como uma mensagem de texto vira bytes, números de 0 a 255 e, por fim, bits.',
    "algorithm": 'O texto é codificado em UTF-8, gerando uma sequência de bytes. Cada byte é exibido como inteiro decimal e depois formatado com 8 dígitos binários. É essa sequência de bits que qualquer técnica esteganográfica vai esconder.',
    "references": [],
}
def run():
    texto = "OI"
    dados = texto.encode("utf-8")
    numeros = list(dados)
    bits = [f"{b:08b}" for b in dados]
    return result([
        step("1. Texto original", "Começamos com dois caracteres legíveis.", texto),
        step("2. UTF-8", "encode('utf-8') transforma o texto em bytes.", repr(dados)),
        step("3. Valores decimais", "Cada byte também pode ser visto como um inteiro de 0 a 255.", numeros, "json"),
        step("4. Representação binária", "Cada byte ocupa 8 bits neste exemplo.", bits, "json"),
    ], final="OI → [79, 73] → 01001111 01001001")
if __name__ == '__main__': cli_main(run)

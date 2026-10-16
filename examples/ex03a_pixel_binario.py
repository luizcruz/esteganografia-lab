try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "3A",
    "title": 'Um pixel como números e bits',
    "chapter": '3 — Imagens e LSB',
    "summary": 'Veja um pixel RGB como três números de 0 a 255 e como seus 8 bits.',
    "algorithm": 'Cada canal (R, G, B) do pixel é convertido em binário de 8 bits. Comparando 120 e 121, nota-se que somar 1 altera apenas o bit menos significativo (LSB) — uma mudança de cor imperceptível, que é exatamente o espaço explorado pela esteganografia LSB.',
    "references": [],
}
def run():
    pixel=(120,200,33)
    bits=[f'{canal:08b}' for canal in pixel]
    return result([
        step("1. Pixel RGB", "Cada canal é um inteiro entre 0 e 255.", pixel, "json"),
        step("2. Binário", "Os mesmos canais podem ser vistos como oito bits.", bits, "json"),
        step("3. Comparar 120 e 121", "Uma mudança de uma unidade altera o último bit.", {"120":f'{120:08b}',"121":f'{121:08b}'}, "json"),
    ], final="LSB explora justamente essa pequena diferença numérica.")
if __name__ == '__main__': cli_main(run)

try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "2B",
    "title": 'Incorporar e extrair whitespace',
    "chapter": '2 — Texto estrutural',
    "summary": 'Esconda um bit no final de cada linha e recupere a mensagem lendo esses finais.',
    "algorithm": 'Na incorporação, cada linha do cover recebe um espaço (bit 0) ou um TAB (bit 1) no final; é preciso ter pelo menos uma linha por bit. Na extração, o algoritmo percorre as linhas e verifica com endswith() qual símbolo aparece no fim, reconstruindo a sequência de bits.',
    "references": [18],
}
def esconder_no_fim_das_linhas(linhas, bits):
    if len(bits) > len(linhas):
        raise ValueError('faltam linhas para todos os bits')
    saida = []
    for linha, bit in zip(linhas, bits):
        marca = ' ' if bit == '0' else '\t'
        saida.append(linha + marca)
    return '\n'.join(saida)

def extrair_do_fim_das_linhas(texto):
    bits = []
    for linha in texto.splitlines():
        if linha.endswith('\t'):
            bits.append('1')
        elif linha.endswith(' '):
            bits.append('0')
    return ''.join(bits)

def run():
    cover = ['Primeira linha', 'Segunda linha', 'Terceira linha', 'Quarta linha']
    bits = '0101'
    stego = esconder_no_fim_das_linhas(cover, bits)
    visual = stego.replace(' ', '·').replace('\t', '→TAB')
    extraidos = extrair_do_fim_das_linhas(stego)
    return result([
        step("1. Cover", "Quatro linhas oferecem quatro posições.", cover, "json"),
        step("2. Bits", "Precisamos esconder um bit por linha.", bits),
        step("3. Incorporar", "Cada linha recebe ESP ou TAB no fim.", visual),
        step("4. Extrair", "Lemos somente a última marca de cada linha.", extraidos),
    ], final=f"Recuperação correta? {extraidos == bits}")
if __name__ == '__main__': cli_main(run)

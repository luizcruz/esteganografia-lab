try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "10B",
    "title": 'Correção por repetição',
    "chapter": '10 — Robustez',
    "summary": 'Proteja a mensagem contra ruído repetindo cada bit 3 vezes e decidindo por voto majoritário.',
    "algorithm": 'Na codificação, cada bit vira um bloco de três cópias. Depois que o canal corrompe algumas posições, a decodificação olha cada bloco e escolhe o símbolo mais frequente. Corrige até um erro por bloco, ao custo de triplicar o tamanho.',
    "references": [9],
}
def repetir(bits,n=3): return ''.join(b*n for b in bits)

def voto_majoritario(bits,n=3):
    saida=[]
    for i in range(0,len(bits),n):
        bloco=bits[i:i+n]
        saida.append('1' if bloco.count('1')>bloco.count('0') else '0')
    return ''.join(saida)

def run():
    original='1010'; codificado=repetir(original)
    corrompido=list(codificado); corrompido[1]='0'; corrompido[7]='0' if corrompido[7]=='1' else '1'; corrompido=''.join(corrompido)
    recuperado=voto_majoritario(corrompido)
    return result([
        step("1. Original", "Quatro bits úteis.", original),
        step("2. Repetir 3×", "Cada bit vira um bloco de três.", codificado),
        step("3. Introduzir erros", "Alteramos algumas posições para simular ruído.", corrompido),
        step("4. Voto majoritário", "Cada bloco decide pelo símbolo que aparece mais vezes.", recuperado),
    ], final=f"Recuperação correta? {recuperado==original}")
if __name__ == '__main__': cli_main(run)

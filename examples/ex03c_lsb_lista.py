try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "3C",
    "title": 'LSB em uma lista de canais',
    "chapter": '3 — Imagens e LSB',
    "summary": 'Esconda uma sequência de bits nos LSBs de uma lista de valores e recupere-a.',
    "algorithm": 'Na incorporação, o i-ésimo bit da mensagem é gravado no LSB do i-ésimo valor do cover usando a máscara da aula 3B. Na extração, lê-se valor & 1 das primeiras n posições. Cada valor muda no máximo ±1 e o cover precisa ter ao menos uma posição por bit.',
    "references": [5],
}
def forcar_lsb(valor,bit): return (valor & 0b11111110)|int(bit)

def esconder_bits_em_valores(valores,bits):
    if len(bits)>len(valores): raise ValueError('cover pequeno demais')
    saida=list(valores)
    for i,bit in enumerate(bits): saida[i]=forcar_lsb(saida[i],bit)
    return saida

def extrair_bits_de_valores(valores,n):
    return ''.join(str(v&1) for v in valores[:n])

def run():
    cover=[120,200,33,77,154,9]; bits='101011'
    stego=esconder_bits_em_valores(cover,bits)
    mudancas=[{"i":i,"cover":a,"stego":b,"delta":b-a} for i,(a,b) in enumerate(zip(cover,stego))]
    extraidos=extrair_bits_de_valores(stego,len(bits))
    return result([
        step("1. Cover", "Imagine que cada número seja um canal de pixel.", cover, "json"),
        step("2. Payload", "Um bit por valor.", bits),
        step("3. Alterações", "Cada posição muda no máximo uma unidade.", mudancas, "json"),
        step("4. Extração", "Lemos o LSB de cada posição.", extraidos),
    ], final=f"Recuperação correta? {extraidos==bits}")
if __name__ == '__main__': cli_main(run)

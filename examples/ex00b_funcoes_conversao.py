try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "0B",
    "title": 'Funções texto ↔ bits',
    "chapter": '0 — Fundamentos',
    "summary": 'Crie funções reutilizáveis para converter texto em bits e bits de volta em texto.',
    "algorithm": 'texto_para_bits codifica o texto em UTF-8 e concatena cada byte em 8 bits. bits_para_texto faz o caminho inverso: fatia a string de 8 em 8, converte cada grupo em inteiro, monta os bytes e decodifica em UTF-8. Ao final, o script confere se a ida e volta preserva o texto original.',
    "references": [],
}
def texto_para_bits(texto):
    return ''.join(f'{b:08b}' for b in texto.encode('utf-8'))

def bits_para_texto(bits):
    if len(bits) % 8:
        raise ValueError('a quantidade de bits precisa ser múltipla de 8')
    valores = [int(bits[i:i+8], 2) for i in range(0, len(bits), 8)]
    return bytes(valores).decode('utf-8')

def run():
    texto = 'OI'
    bits = texto_para_bits(texto)
    volta = bits_para_texto(bits)
    return result([
        step("1. Codificar", "Cada byte do UTF-8 é formatado com 8 bits.", bits),
        step("2. Agrupar de 8 em 8", "Os grupos voltam a números decimais.", [int(bits[i:i+8],2) for i in range(0,len(bits),8)], "json"),
        step("3. Decodificar", "bytes(...).decode('utf-8') recupera o texto.", volta),
    ], final=f"Ida e volta preservou o texto? {volta == texto}")
if __name__ == '__main__': cli_main(run)

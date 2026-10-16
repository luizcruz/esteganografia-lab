try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "3B",
    "title": 'Forçando o LSB',
    "chapter": '3 — Imagens e LSB',
    "summary": 'Use máscaras binárias para gravar o bit desejado no LSB de um valor.',
    "algorithm": 'O valor passa por um AND com 11111110, que zera o último bit, e depois por um OR com o bit da mensagem, que o define como 0 ou 1. O resultado difere do original em no máximo uma unidade.',
    "references": [],
}
def forcar_lsb(valor,bit):
    return (valor & 0b11111110) | int(bit)

def run():
    entradas=[120,121,122]
    saidas=[forcar_lsb(v,'1') for v in entradas]
    pares=[{"antes":v,"antes_bin":f'{v:08b}',"depois":s,"depois_bin":f'{s:08b}'} for v,s in zip(entradas,saidas)]
    return result([
        step("1. Máscara", "AND com 11111110 zera somente o último bit.", 'valor & 11111110'),
        step("2. Inserção", "OR com 0 ou 1 define o bit desejado.", '| bit'),
        step("3. Exemplos", "Observe que a mudança numérica é 0 ou 1.", pares, "json"),
    ], final=str(saidas))
if __name__ == '__main__': cli_main(run)

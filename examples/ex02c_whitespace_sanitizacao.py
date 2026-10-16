try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "2C",
    "title": 'Sanitização destrói whitespace',
    "chapter": '2 — Texto estrutural',
    "summary": 'Veja como uma limpeza automática de espaços finais apaga completamente o canal de whitespace.',
    "algorithm": 'Os bits são escondidos no fim das linhas (como na 2B) e extraídos com sucesso. Em seguida, uma sanitização aplica rstrip() em cada linha — algo que editores e sistemas fazem sozinhos — e a nova extração não encontra nenhum bit. Mostra o trade-off entre invisibilidade e robustez.',
    "references": [18],
}
def esconder(linhas, bits):
    return '\n'.join(l + (' ' if b == '0' else '\t') for l,b in zip(linhas,bits))

def extrair(texto):
    out=[]
    for l in texto.splitlines():
        if l.endswith('\t'): out.append('1')
        elif l.endswith(' '): out.append('0')
    return ''.join(out)

def sanitizar(texto):
    return '\n'.join(linha.rstrip() for linha in texto.splitlines())

def run():
    bits='0101'; cover=['A','B','C','D']
    stego=esconder(cover,bits)
    antes=extrair(stego)
    limpo=sanitizar(stego)
    depois=extrair(limpo)
    return result([
        step("1. Antes da sanitização", "O canal ainda contém as marcas finais.", antes),
        step("2. rstrip()", "Um editor pode remover espaços e TABs finais automaticamente.", repr(limpo)),
        step("3. Depois", "O extrator já não encontra os símbolos.", depois or '(nenhum bit)'),
    ], final="Alta fidelidade visual, baixa robustez.")
if __name__ == '__main__': cli_main(run)

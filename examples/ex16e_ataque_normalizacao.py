try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "16E",
    "title": 'Sanitização quebra o pipeline',
    "chapter": '16 — Laboratório',
    "summary": 'Ataque por sanitização: remova os caracteres invisíveis e veja a extração falhar.',
    "algorithm": 'Um sanitizador apaga todos os U+200B e U+200C do stego. O extrator, que precisa de pelo menos 48 bits para ler o cabeçalho, não encontra nada e falha. O CRC detecta corrupção, mas não traz robustez: sem redundância ou outro canal, a mensagem se perde.',
    "references": [],
}
import zlib
ZERO,UM='\u200b','\u200c'

def preparar(texto):
    d=texto.encode(); return len(d).to_bytes(2,'big')+zlib.crc32(d).to_bytes(4,'big')+d

def bits(d): return ''.join(f'{b:08b}' for b in d)
def embed(c,b): return c+''.join(ZERO if x=='0' else UM for x in b)
def remover_format_chars(texto): return texto.replace(ZERO,'').replace(UM,'')

def tentar_extrair(stego):
    b=''.join('0' if c==ZERO else '1' for c in stego if c in (ZERO,UM))
    if len(b)<48: raise ValueError('cabeçalho desapareceu')
    return b

def run():
    stego=embed('Relatório concluído.',bits(preparar('OI')))
    antes=len(stego); sanitizado=remover_format_chars(stego); depois=len(sanitizado)
    try:
        tentar_extrair(sanitizado); status='inesperadamente recuperável'
    except Exception as e:
        status=f'falhou como esperado: {e}'
    return result([
        step("1. Stego", "O texto contém caracteres de formato invisíveis.", {"comprimento":antes}, "json"),
        step("2. Sanitizar", "Removemos U+200B e U+200C.", {"comprimento":depois}, "json"),
        step("3. Extrair", "Sem as marcas, não existe cabeçalho suficiente.", status),
    ], final="O checksum não cria robustez; ele apenas ajuda a perceber corrupção.")
if __name__ == '__main__': cli_main(run)

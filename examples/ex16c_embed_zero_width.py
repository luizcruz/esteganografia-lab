try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "16C",
    "title": 'Payload em zero-width',
    "chapter": '16 — Laboratório',
    "summary": 'Esconda o payload completo em um texto usando caracteres zero-width.',
    "algorithm": 'Os bits do payload são mapeados para U+200B (0) e U+200C (1) e anexados ao final do cover. O texto continua com a mesma aparência, mas ganha 64 code points invisíveis.',
    "references": [],
}
import zlib
ZERO,UM='\u200b','\u200c'

def preparar_payload(texto):
    d=texto.encode(); return len(d).to_bytes(2,'big')+zlib.crc32(d).to_bytes(4,'big')+d

def bytes_para_bits(dados): return ''.join(f'{b:08b}' for b in dados)
def embed_zero_width(cover,bits): return cover+''.join(ZERO if b=='0' else UM for b in bits)

def run():
    cover='Relatório concluído.'; bits=bytes_para_bits(preparar_payload('OI')); stego=embed_zero_width(cover,bits)
    return result([
        step("1. Cover", "Texto visível.", cover),
        step("2. Bits", "Payload completo já convertido.", bits),
        step("3. Incorporar", "0→U+200B e 1→U+200C.", {"bits":len(bits),"novos_codepoints":len(stego)-len(cover)}, "json"),
        step("4. Stego", "A renderização pouco muda, mas o comprimento aumenta.", stego),
    ], final=f"Comprimento: {len(cover)} → {len(stego)} code points")
if __name__ == '__main__': cli_main(run)

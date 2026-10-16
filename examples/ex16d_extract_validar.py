try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "16D",
    "title": 'Extração e validação ponta a ponta',
    "chapter": '16 — Laboratório',
    "summary": 'Extraia e valide a mensagem: leia o cabeçalho, confira o CRC32 e decodifique.',
    "algorithm": 'O extrator filtra apenas os caracteres zero-width e os converte em bits e bytes. Lê os 2 primeiros bytes (tamanho), os 4 seguintes (CRC esperado) e a mensagem. Recalcula o CRC32 sobre a mensagem: se bater, decodifica o UTF-8; senão, sinaliza corrupção.',
    "references": [],
}
import zlib
ZERO,UM='\u200b','\u200c'

def preparar_payload(texto):
    d=texto.encode(); return len(d).to_bytes(2,'big')+zlib.crc32(d).to_bytes(4,'big')+d

def bytes_para_bits(d): return ''.join(f'{b:08b}' for b in d)
def bits_para_bytes(bits): return bytes(int(bits[i:i+8],2) for i in range(0,len(bits),8) if len(bits[i:i+8])==8)
def embed(cover,bits): return cover+''.join(ZERO if b=='0' else UM for b in bits)

def extract_zero_width(stego):
    bits=''.join('0' if c==ZERO else '1' for c in stego if c in (ZERO,UM))
    dados=bits_para_bytes(bits)
    if len(dados)<6: raise ValueError('payload curto demais')
    tamanho=int.from_bytes(dados[:2],'big')
    esperado=int.from_bytes(dados[2:6],'big')
    msg=dados[6:6+tamanho]
    calculado=zlib.crc32(msg)
    if calculado!=esperado: raise ValueError('payload corrompido')
    return msg.decode(),bits,tamanho,esperado,calculado

def run():
    cover='Relatório concluído.'; bits=bytes_para_bits(preparar_payload('OI')); stego=embed(cover,bits)
    msg,bits2,tam,esp,calc=extract_zero_width(stego)
    return result([
        step("1. Filtrar marcas", "Lemos apenas os dois caracteres zero-width.", bits2),
        step("2. Cabeçalho", "Os dois primeiros bytes informam o tamanho.", tam),
        step("3. Checksum esperado", "Vem gravado no payload.", f"0x{esp:08X}"),
        step("4. Checksum calculado", "Recalculamos sobre a mensagem extraída.", f"0x{calc:08X}"),
        step("5. Mensagem", "Como os CRCs batem, decodificamos UTF-8.", msg),
    ], final=f"Mensagem recuperada: {msg}")
if __name__ == '__main__': cli_main(run)

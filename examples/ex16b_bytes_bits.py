try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "16B",
    "title": 'Payload bytes → bits',
    "chapter": '16 — Laboratório',
    "summary": 'Converta o payload preparado em uma sequência de bits pronta para o canal.',
    "algorithm": 'Cada byte do payload (cabeçalho + CRC + mensagem) é formatado em 8 bits e tudo é concatenado. \'OI\' gera 8 bytes, ou seja, 64 bits.',
    "references": [],
}
import zlib

def preparar_payload(texto):
    d=texto.encode(); return len(d).to_bytes(2,'big')+zlib.crc32(d).to_bytes(4,'big')+d

def bytes_para_bits(dados): return ''.join(f'{b:08b}' for b in dados)

def run():
    payload=preparar_payload('OI'); bits=bytes_para_bits(payload)
    grupos=[bits[i:i+8] for i in range(0,len(bits),8)]
    return result([
        step("1. Payload", "Bytes preparados pelo exemplo anterior.", list(payload), "json"),
        step("2. Converter", "Cada byte vira oito caracteres 0/1.", grupos, "json"),
        step("3. Sequência final", "Essa sequência pode ser mapeada para símbolos do canal.", bits),
    ], final=f"{len(payload)} bytes → {len(bits)} bits")
if __name__ == '__main__': cli_main(run)

try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "16A",
    "title": 'Payload com tamanho e CRC32',
    "chapter": '16 — Laboratório',
    "summary": 'Prepare o payload com cabeçalho: 2 bytes de tamanho + 4 bytes de CRC32 + mensagem.',
    "algorithm": 'A mensagem é codificada em UTF-8; seu comprimento vira 2 bytes (big-endian) e o CRC32 dos dados vira mais 4. Os três são concatenados. O tamanho diz ao receptor onde parar; o CRC permite detectar se algo foi corrompido.',
    "references": [],
}
import zlib

def preparar_payload(texto):
    dados=texto.encode('utf-8')
    tamanho=len(dados).to_bytes(2,'big')
    checksum=zlib.crc32(dados).to_bytes(4,'big')
    return tamanho+checksum+dados

def run():
    texto='OI'; dados=texto.encode(); tamanho=len(dados).to_bytes(2,'big'); crc=zlib.crc32(dados); payload=preparar_payload(texto)
    return result([
        step("1. Dados", "Mensagem em UTF-8.", list(dados), "json"),
        step("2. Tamanho", "Dois bytes armazenam o comprimento.", list(tamanho), "json"),
        step("3. CRC32", "Quatro bytes permitem detectar corrupção acidental.", f"0x{crc:08X}"),
        step("4. Payload", "Cabeçalho + checksum + conteúdo.", list(payload), "json"),
    ], final=f"{len(payload)} bytes no total")
if __name__ == '__main__': cli_main(run)

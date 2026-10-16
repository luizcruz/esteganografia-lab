try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "3D",
    "title": 'LSB real com Pillow',
    "chapter": '3 — Imagens e LSB',
    "summary": 'Aplique LSB em uma imagem PNG real com Pillow, alterando o canal vermelho do primeiro pixel.',
    "algorithm": 'O script gera uma imagem 64×64 em gradiente, lê o pixel (0,0) e grava o bit 1 no LSB do canal R com a máscara binária. Antes e depois são exibidos como imagens. PNG não tem compressão com perdas, então o bit sobrevive; em JPEG ele seria destruído.',
    "references": [],
}
import base64, io
from PIL import Image

def data_url(img):
    b=io.BytesIO(); img.save(b,format='PNG')
    return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()

def run():
    img=Image.new('RGB',(64,64))
    px=img.load()
    for y in range(64):
        for x in range(64): px[x,y]=(120+x,120+y,80)
    r,g,b=px[0,0]
    bit='1'; r2=(r & 0b11111110)|int(bit)
    cover_url=data_url(img.copy())
    px[0,0]=(r2,g,b)
    stego_url=data_url(img)
    return result([
        step("1. Criar cover", "Geramos uma pequena PNG sem compressão com perdas.", cover_url, "image"),
        step("2. Primeiro pixel", "Lemos RGB em (0,0).", {"R":r,"G":g,"B":b}, "json"),
        step("3. Forçar bit 1", "Somente o LSB do canal R é controlado.", {"antes":f'{r:08b}',"depois":f'{r2:08b}'}, "json"),
        step("4. Stego", "A mudança é praticamente invisível neste exemplo.", stego_url, "image"),
    ], final=f"R mudou de {r} para {r2}", note="Em JPEG, a recompressão pode destruir esse LSB simples.")
if __name__ == '__main__': cli_main(run)

try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "4A",
    "title": 'DCT e DCT inversa',
    "chapter": '4 — Frequência e codificação',
    "summary": 'Transforme um bloco de pixels para o domínio da frequência (DCT) e reconstrua-o (IDCT).',
    "algorithm": 'Um bloco 4×4 passa pela DCT 2D ortonormal, que o representa como coeficientes de frequência (o canto superior esquerdo é a média; os demais, detalhes). A IDCT reconstrói o bloco e np.allclose confirma que nada se perdeu. JPEG e vários métodos esteganográficos operam nesse domínio.',
    "references": [21],
}
import numpy as np
from scipy.fft import dctn,idctn

def run():
    bloco=np.array([[10,10,10,10],[10,12,12,10],[10,12,12,10],[10,10,10,10]],dtype=float)
    coef=dctn(bloco,norm='ortho')
    rec=idctn(coef,norm='ortho')
    return result([
        step("1. Bloco espacial", "Começamos com valores semelhantes a intensidades de pixels.", np.round(bloco,2).tolist(), "table"),
        step("2. DCT", "A transformada reorganiza a informação em coeficientes de frequência.", np.round(coef,2).tolist(), "table"),
        step("3. IDCT", "A inversa reconstrói o bloco.", np.round(rec,2).tolist(), "table"),
        step("4. Conferência", "np.allclose verifica erro numérico muito pequeno.", bool(np.allclose(bloco,rec)), "json"),
    ], final="A DCT não é esteganografia; ela cria outro domínio onde algoritmos podem operar.")
if __name__ == '__main__': cli_main(run)

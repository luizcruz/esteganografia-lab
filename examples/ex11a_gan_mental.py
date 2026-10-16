try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "11A",
    "title": 'GAN mental em três papéis',
    "chapter": '11 — Deep learning',
    "summary": 'Entenda a arquitetura de esteganografia com GANs: um gerador contra dois críticos.',
    "algorithm": 'O gerador cria uma imagem a partir de ruído; o discriminador avalia se ela parece real e o steganalyzer estima a probabilidade de conter dados ocultos. No treino, o gerador é ajustado para maximizar o realismo e minimizar a suspeita. Aqui as funções são simuladas.',
    "references": [5],
}
def gerador(z): return f'imagem_sintetica({z})'
def discriminador(imagem): return {'entrada':imagem,'score_realismo':0.86}
def steganalyzer(imagem): return {'entrada':imagem,'prob_stego':0.22}

def run():
    imagem=gerador('ruido_01'); real=discriminador(imagem); steg=steganalyzer(imagem)
    return result([
        step("1. Gerador", "Cria uma amostra a partir de um vetor/ruído latente.", imagem),
        step("2. Discriminador", "Pergunta se a imagem parece pertencer à distribuição real.", real, "json"),
        step("3. Steganalyzer", "Pergunta se a imagem parece um carrier manipulado.", steg, "json"),
        step("4. Objetivo conjunto", "O gerador recebe pressão para parecer real e pouco suspeito.", "realismo alto + prob_stego baixa"),
    ], final="Arquitetura didática: dois críticos pressionam o gerador.")
if __name__ == '__main__': cli_main(run)

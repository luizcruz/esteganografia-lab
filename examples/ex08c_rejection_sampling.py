try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "8C",
    "title": 'Rejection sampling simples',
    "chapter": '8 — LLMs',
    "summary": 'Rejection sampling: sorteie candidatos até achar um que codifique o bit desejado.',
    "algorithm": 'O algoritmo sorteia uma opção, classifica-a como 0 ou 1 e, se a classe não for a do bit desejado, descarta e sorteia de novo (até um limite de tentativas). A primeira compatível é aceita. Como as opções vêm do próprio sorteio, o texto preserva melhor a naturalidade.',
    "references": [6],
}
import random

def rejection_sample(opcoes,bit,classificar,max_tentativas=100,rng=None):
    rng=rng or random
    historico=[]
    for _ in range(max_tentativas):
        candidato=rng.choice(opcoes)
        classe=classificar(candidato)
        historico.append((candidato,classe))
        if classe==bit: return candidato,historico
    raise RuntimeError('não encontrou candidato')

def run():
    opcoes=['azul','limpo','nublado','escuro']
    classes={'azul':'0','limpo':'1','nublado':'0','escuro':'1'}
    candidato,hist=rejection_sample(opcoes,'1',classes.get,rng=random.Random(4))
    return result([
        step("1. Objetivo", "Precisamos de uma opção classificada como bit 1.", '1'),
        step("2. Tentativas", "Candidatos incompatíveis são rejeitados.", hist, "json"),
        step("3. Aceito", "A primeira opção da classe correta encerra a busca.", candidato),
    ], final=candidato, note="É a forma genérica da ideia, sem depender de um LLM específico.")
if __name__ == '__main__': cli_main(run)

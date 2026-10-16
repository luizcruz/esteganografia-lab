try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "1A",
    "title": 'Alice–Warden–Bob',
    "chapter": '1 — Modelo mental',
    "summary": 'Simule o modelo dos prisioneiros: Alice esconde, Wendy (warden) vigia e Bob extrai com a chave.',
    "algorithm": 'embedir(cover, mensagem, chave) devolve um objeto que mantém a aparência do cover e guarda a mensagem internamente. extrair(stego, chave) só devolve a mensagem se a chave conferir. A implementação é abstrata de propósito: o foco é a interface E/D e o papel do observador, não a técnica de ocultação.',
    "references": [1],
}
def embedir(cover, mensagem, chave=None):
    # Demonstração reversível: anexamos um marcador interno.
    # Não representa um método furtivo real.
    return {"aparencia": cover, "interno": mensagem, "chave": chave}

def extrair(stego, chave=None):
    if stego.get("chave") != chave:
        raise ValueError("chave incorreta")
    return stego["interno"]

def run():
    cover = "Relatório comum"
    mensagem = "OI"
    chave = "aula"
    stego = embedir(cover, mensagem, chave)
    recuperada = extrair(stego, chave)
    return result([
        step("1. Alice escolhe o cover", "O observador deveria enxergar apenas o objeto comum.", cover),
        step("2. Alice incorpora", "Aqui usamos uma simulação estrutural para mostrar a interface E(cover,mensagem,chave).", stego, "json"),
        step("3. Wendy observa", "Ela pode tentar decidir se houve manipulação, mesmo sem conhecer a mensagem.", "cover ou stego?"),
        step("4. Bob extrai", "Com a regra correta e a chave, Bob recupera o payload.", recuperada),
    ], final=f"extrair(embedir(...)) == mensagem → {recuperada == mensagem}", note="A implementação é propositalmente abstrata; o objetivo é aprender o fluxo.")
if __name__ == '__main__': cli_main(run)

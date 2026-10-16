try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "2H",
    "title": 'Homóglifos: aparência ≠ código',
    "chapter": '2 — Texto estrutural',
    "summary": 'Compare letras visualmente idênticas que têm códigos Unicode diferentes (a latino × а cirílico).',
    "algorithm": 'O script coloca lado a lado o \'a\' latino (U+0061) e o \'а\' cirílico (U+0430), testa a igualdade em Python (False) e mostra o code point de cada um. Trocar um pelo outro em posições escolhidas é a base dos canais por homóglifos.',
    "references": [],
}
def run():
    latino='a'; cirilico='а'
    return result([
        step("1. Aparência", "Os dois caracteres parecem muito semelhantes.", f"{latino} / {cirilico}"),
        step("2. Igualdade", "Para Python, são caracteres diferentes.", latino==cirilico, "json"),
        step("3. Unicode latino", "a latino é U+0061.", f"U+{ord(latino):04X}"),
        step("4. Unicode cirílico", "а cirílico é U+0430.", f"U+{ord(cirilico):04X}"),
    ], final="Mesma aparência pode esconder representações diferentes.")
if __name__ == '__main__': cli_main(run)

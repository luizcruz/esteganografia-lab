try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "2G",
    "title": 'Canal binário zero-width',
    "chapter": '2 — Texto estrutural',
    "summary": 'Monte um canal binário com caracteres de largura zero: U+200B = 0 e U+200C = 1.',
    "algorithm": 'Na incorporação, cada bit vira um caractere invisível (U+200B para 0, U+200C para 1) e a sequência é anexada ao fim do cover. Na extração, o algoritmo descarta tudo que não for um desses dois caracteres e converte os restantes de volta em bits. O texto parece igual, mas fica mais longo.',
    "references": [19],
}
ZERO, UM='\u200b','\u200c'

def ocultar_zero_width(cover,bits):
    marcas=''.join(ZERO if b=='0' else UM for b in bits)
    return cover+marcas

def extrair_zero_width(stego):
    return ''.join('0' if c==ZERO else '1' for c in stego if c in (ZERO,UM))

def run():
    cover='Relatório aprovado.'; bits='10110'
    stego=ocultar_zero_width(cover,bits)
    extraidos=extrair_zero_width(stego)
    return result([
        step("1. Cover", "Texto normal de cobertura.", cover),
        step("2. Bits", "Mensagem binária de brinquedo.", bits),
        step("3. Stego", "Visualmente o texto permanece quase igual.", stego),
        step("4. Tamanho", "Os code points invisíveis aumentam o comprimento.", {"cover":len(cover),"stego":len(stego)}, "json"),
        step("5. Extração", "Filtrar apenas U+200B/U+200C reconstrói os bits.", extraidos),
    ], final=f"Recuperação correta? {extraidos==bits}")
if __name__ == '__main__': cli_main(run)

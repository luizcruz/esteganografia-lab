try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "6A",
    "title": 'Anatomia mínima de um stream PDF',
    "chapter": '6 — PDF',
    "summary": 'Conheça os operadores de um content stream PDF que posicionam e desenham texto.',
    "algorithm": 'O script decompõe um stream mínimo: BT inicia o texto, Tf escolhe fonte e tamanho, Td move a posição, Tj desenha a string e ET encerra. Os operandos numéricos (tamanhos, coordenadas) são os candidatos a portar bits ocultos.',
    "references": [7],
}
def run():
    stream='BT\n/F1 12 Tf\n288 720 Td\n(ABC) Tj\nET'
    operadores=[
        {"linha":"BT","papel":"início do objeto de texto"},
        {"linha":"/F1 12 Tf","papel":"fonte F1 em tamanho 12"},
        {"linha":"288 720 Td","papel":"deslocamento de posição"},
        {"linha":"(ABC) Tj","papel":"desenhar texto"},
        {"linha":"ET","papel":"fim do objeto de texto"},
    ]
    return result([
        step("1. Stream", "PDF guarda comandos, não apenas texto corrido.", stream),
        step("2. Interpretar", "Cada operador controla uma parte da renderização.", operadores, "json"),
    ], final="Valores numéricos de certos operadores podem ser canais de estudo.")
if __name__ == '__main__': cli_main(run)

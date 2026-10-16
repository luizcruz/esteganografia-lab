try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "15A",
    "title": 'Pipeline multimodal — simulação',
    "chapter": '15 — Multimodalidade',
    "summary": 'Simule um pipeline multimodal: vídeo → texto → incorporação → vídeo sintetizado.',
    "algorithm": 'O vídeo é convertido em descrição textual; a incorporação acontece nesse domínio linguístico (com as técnicas das aulas 7–9); e uma etapa de síntese recriaria o áudio/vídeo a partir do texto modificado. Cada etapa é uma função simulada.',
    "references": [8],
}
def transcrever_e_descrever(video): return f'texto extraído de {video}: pessoa explica um projeto.'
def incorporar_no_texto(texto): return texto+' [variante semântica controlada]'
def sintetizar_video(stego_texto): return {'video_sintetico':'saida.mp4','base_textual':stego_texto}

def pipeline_multimodal(video):
    texto=transcrever_e_descrever(video)
    stego_texto=incorporar_no_texto(texto)
    video_saida=sintetizar_video(stego_texto)
    return texto,stego_texto,video_saida

def run():
    texto,stego,saida=pipeline_multimodal('aula.mp4')
    return result([
        step("1. Decompor", "Conteúdo audiovisual é representado linguisticamente.", texto),
        step("2. Incorporar no domínio linguístico", "A simulação marca que houve uma escolha controlada.", stego),
        step("3. Reconstruir", "Uma etapa de síntese produziria novamente áudio/vídeo.", saida, "json"),
    ], final="O domínio do canal mudou: espaço-tempo → linguagem → espaço-tempo.", note="Simulação conceitual; não implementa modelos de voz ou vídeo.")
if __name__ == '__main__': cli_main(run)

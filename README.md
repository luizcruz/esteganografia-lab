# EsteganoLab — laboratório didático de esteganografia

Interface web local baseada nos exemplos Python do **Guia Didático — Esteganografia do zero aos LLMs**.

## O que foi implementado

- **49 scripts Python executáveis**, um para cada exemplo do guia (0A a 16E, incluindo os exemplos conceituais transformados em simulações executáveis).
- Interface web com **código à esquerda** e **resultado passo a passo à direita**.
- Botão **▶ Executar** em cada exemplo.
- Navegação por capítulo, busca e progresso salvo no navegador.
- Saídas estruturadas com números, matrizes, imagens e observações didáticas.
- Exemplo de LSB com uma PNG sintética gerada em memória.
- Exemplos que o guia chama de *conceituais* continuam identificados como simulações; eles não são apresentados como reprodução integral dos papers.

## Instalação

Requer Python 3.10+.

### Windows

Abra a pasta no Prompt/PowerShell e execute:

```bat
start_windows.bat
```

Ou manualmente:

```bat
python -m pip install -r requirements.txt
python app.py
```

### Linux / macOS

```bash
./start_linux_mac.sh
```

Ou:

```bash
python3 -m pip install -r requirements.txt
python3 app.py
```

Depois abra:

```text
http://127.0.0.1:5000
```

## Estrutura

```text
esteganografia_lab/
├── app.py
├── requirements.txt
├── examples/
│   ├── ex00a_texto_bytes_bits.py
│   ├── ...
│   └── ex16e_ataque_normalizacao.py
├── static/
│   ├── index.html
│   ├── app.js
│   └── styles.css
└── tests/
    └── test_examples.py
```

## Como os scripts funcionam

Cada arquivo em `examples/` possui:

- `META`: título, capítulo, resumo (`summary`), explicação do algoritmo (`algorithm`) e referências do guia;
- `run()`: executa a demonstração e devolve uma lista de etapas;
- execução direta via terminal (`python examples/ex03b_forcar_lsb.py`).

O servidor usa apenas a biblioteca padrão do Python para a interface HTTP e **não executa código arbitrário enviado pelo navegador**. O botão Play executa apenas os exemplos didáticos que fazem parte do projeto. Isso deixa a aplicação mais simples e segura para uso em aula.

## Testar todos os exemplos

```bash
python tests/test_examples.py
```

## Observação de escopo

O projeto foi desenhado para ensino e experimentação com dados próprios/autorizados. Alguns exemplos são simplificações explícitas do guia — por exemplo, função de custo, PVD conceitual, paridade de coeficiente, pipeline multimodal e busca de funções de custo — e não reproduzem integralmente implementações de pesquisa.

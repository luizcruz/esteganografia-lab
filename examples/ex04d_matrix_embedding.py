try:
    from examples.common import step, result, cli_main
except ModuleNotFoundError:  # permite executar este arquivo diretamente
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from examples.common import step, result, cli_main
META = {
    "id": "4D",
    "title": 'Matrix embedding simplificado',
    "chapter": '4 — Frequência e codificação',
    "summary": 'Matrix embedding (3,2): esconda 2 bits alterando no máximo 1 de 3 posições.',
    "algorithm": 'A síndrome do cover é calculada como (a1 XOR a3, a2 XOR a3). Comparando-a com os 2 bits da mensagem obtém-se um \'erro\' que aponta qual posição inverter — ou nenhuma, se já coincidem. Assim, transporta-se mais informação por alteração, reduzindo a distorção.',
    "references": [24],
}
def embutir_3_2(a,mensagem):
    a=list(a)
    s=(a[0]^a[2],a[1]^a[2])
    erro=(s[0]^mensagem[0],s[1]^mensagem[1])
    mapa={(0,0):None,(1,0):0,(0,1):1,(1,1):2}
    i=mapa[erro]
    if i is not None:a[i]^=1
    return a,s,erro,i

def sindrome(a): return (a[0]^a[2],a[1]^a[2])

def run():
    cover=[0,0,0]; msg=(1,1)
    stego,s,erro,i=embutir_3_2(cover,msg)
    return result([
        step("1. Cover", "Três bits disponíveis.", cover, "json"),
        step("2. Síndrome atual", "s1=a1 XOR a3; s2=a2 XOR a3.", s, "json"),
        step("3. Mensagem desejada", "Queremos que a síndrome final seja (1,1).", msg, "json"),
        step("4. Posição a alterar", "O erro aponta qual bit precisa mudar.", i),
        step("5. Stego", "No máximo uma posição foi invertida.", stego, "json"),
        step("6. Síndrome final", "Ela agora coincide com a mensagem.", sindrome(stego), "json"),
    ], final=f"Alterações: {sum(a!=b for a,b in zip(cover,stego))}")
if __name__ == '__main__': cli_main(run)

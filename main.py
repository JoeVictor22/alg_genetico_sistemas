from copy import deepcopy
import random

TAM_POPULACAO = 10
MAX_ITERACOES = 1000
TAXA_REPRODUCAO = 2

TAM_GENOMA = 4
VALOR_ALVO = 1
PASSO = VALOR_ALVO / 4


def gera_estado_inicial():
    estados = []
    for i in range(TAM_POPULACAO):
        genomas = [bin(random.randint(-100, 100)) for _ in range(TAM_GENOMA)]
        estados.append(genomas)

    return estados


def mutacao(estado):
    rand = random.randint(0, len(estado) - 1)

    val = estado[rand]
    slice_bin = 2
    if val[0] == "-":
        slice_bin += 1

    rand_idx = random.randint(slice_bin, len(val) - 1)
    novo_valor = "1" if val[rand_idx] == "0" else "0"
    val = val[:rand_idx] + novo_valor + val[rand_idx + 1:]

    estado[rand] = bin(eval(val))

    return estado


def cross_over(genoma_x, genoma_y):
    gx = deepcopy(genoma_x)
    gy = deepcopy(genoma_y)
    cross = random.randint(0, len(gx) - 1)
    return gx[:cross] + gy[cross:], gy[:cross] + gx[cross:]


def fitness(populacao):
    scores = []
    for gnm in populacao:
        resultados = calcula_resultado(gnm[0], gnm[1], gnm[2], gnm[3])
        score = sum([PASSO if x == 0 else 0 for x in resultados]) + 1
        scores.append(score)

    return scores


def escolhe_genoma(populacao, fitness):
    fracoes = [_ / sum(fitness) for _ in fitness]

    intervalos = []
    acum = 0

    for i in fracoes:
        acum += i
        intervalos.append(round(acum, 2))

    resultado = random.randint(0, len(populacao)) / len(populacao)

    idx = 0
    while resultado > intervalos[idx]:
        idx += 1

    return populacao[idx]


def seleciona_reprodutor(populacao):
    genomas = []
    scores = fitness(populacao)
    for _ in range(2 * TAXA_REPRODUCAO):
        genoma_vencedor = escolhe_genoma(populacao, scores)
        genomas.append(genoma_vencedor)
    return genomas


def teste_meta(populacao):
    score = fitness(populacao)
    cpy = deepcopy(score)
    _, idx = min((_, idx) for (idx, _) in enumerate(cpy))
    idx = score.index(cpy[idx])

    return score[idx] - 1, populacao[idx]


def genetico():
    populacao = gera_estado_inicial()
    alvo = VALOR_ALVO
    while alvo > 0:
        for _ in range(MAX_ITERACOES):
            nova_populacao = []
            res = teste_meta(populacao)

            if res[0] > alvo:
                return res

            reprodutores = seleciona_reprodutor(populacao)
            gx = reprodutores[:TAXA_REPRODUCAO]
            gy = reprodutores[TAXA_REPRODUCAO:]

            for k, w in zip(gx, gy):
                f1, f2 = cross_over(k, w)
                nova_populacao.append(f1)
                nova_populacao.append(f2)

            res = teste_meta(nova_populacao)
            if res[0] > alvo:
                return res

            for z in nova_populacao:
                if random.randint(0, 100) < 10:
                    _ = mutacao(z)
            populacao = nova_populacao
        alvo -= PASSO

    return "Falha", populacao


def calcula_resultado(x1, y1, z1, w1):
    x = eval(f"{x1}")
    y = eval(f"{y1}")
    z = eval(f"{z1}")
    w = eval(f"{w1}")

    s1 = (x ** 2) + (y ** 3) + (z ** 4) - (w ** 5)
    s2 = (x ** 2) + 3 * (z ** 2) - w
    s3 = (z ** 5) - y + 10
    s4 = (x ** 4) - z + y * w
    return [s1, s2, s3, s4]


def main():
    res = genetico()
    if res[0] == "Falha":
        print("\nNão foi possivel encontrar solução")
        return

    print(
        f"O melhor resultado encontrado com no máximo {MAX_ITERACOES} iterações foi: X={eval(res[1][0])}, Y={eval(res[1][1])}, Z={eval(res[1][2])}, W={eval(res[1][3])}"
    )
    resultado = calcula_resultado(*res[1])
    print("X**2 + Y**3 + Z**4 - W**5 = {}".format(resultado[0]))
    print("X**2 + 3Z - W = {}".format(resultado[1]))
    print("X**5 - Y + 10 = {}".format(resultado[2]))
    print("X**4 - Z + Y*W = {}".format(resultado[3]))


if __name__ == "__main__":
    main()

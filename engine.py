import random
from abelha import Abelha

def calcular_fitness(resultado):
    if resultado >= 0:
        return 1 / (1 + resultado)
    else:
        return 1 + abs(resultado)

def executar_abc(funcao, n_colonia, dim, max_iter, limite_l):
    
    LIMITE_INF = -100
    LIMITE_SUP = 100

    n_fontes = n_colonia // 2
    colonia = []

    # inicialização das abelhas fonte
    for _ in range(n_fontes):
        pos_ini = [
            random.uniform(LIMITE_INF, LIMITE_SUP)
            for _ in range(dim)
        ]

        a = Abelha(pos_ini)
        a.resultado_funcao = funcao(a.posicao)
        a.fitness = calcular_fitness(a.resultado_funcao)

        colonia.append(a)

    melhor_solucao = colonia[0].posicao[:]
    melhor_resultado_funcao = colonia[0].resultado_funcao

    historico_progresso = []

    for it in range(max_iter):

        # --- 1. fase das abelhas empregadas ---
        for i in range(n_fontes):

            k = random.randint(0, n_fontes - 1)

            while k == i:
                k = random.randint(0, n_fontes - 1)

            j = random.randint(0, dim - 1)

            phi = random.uniform(-1, 1)

            nova_posicao = colonia[i].posicao[:]

            nova_posicao[j] = (
                colonia[i].posicao[j]
                + phi * (
                    colonia[i].posicao[j]
                    - colonia[k].posicao[j]
                )
            )

            # controle dos limites
            nova_posicao[j] = max(
                LIMITE_INF,
                min(LIMITE_SUP, nova_posicao[j])
            )

            res_candidato = funcao(nova_posicao)

            fit_candidato = calcular_fitness(res_candidato)

            if fit_candidato > colonia[i].fitness:

                colonia[i].posicao = nova_posicao[:]

                colonia[i].resultado_funcao = res_candidato

                colonia[i].fitness = fit_candidato

                colonia[i].tentativas = 0

            else:
                colonia[i].tentativas += 1

        # --- 2. fase das abelhas espectadoras ---
        soma_fitness = sum(a.fitness for a in colonia)

        probabilidades = [
            a.fitness / soma_fitness
            for a in colonia
        ]

        procuradas = 0
        i = 0

        while procuradas < n_fontes:

            r = random.random()

            if r < probabilidades[i]:

                procuradas += 1

                k = random.randint(0, n_fontes - 1)

                while k == i:
                    k = random.randint(0, n_fontes - 1)

                j = random.randint(0, dim - 1)

                phi = random.uniform(-1, 1)

                nova_posicao = colonia[i].posicao[:]

                nova_posicao[j] = (
                    colonia[i].posicao[j]
                    + phi * (
                        colonia[i].posicao[j]
                        - colonia[k].posicao[j]
                    )
                )

                # controle dos limites
                nova_posicao[j] = max(
                    LIMITE_INF,
                    min(LIMITE_SUP, nova_posicao[j])
                )

                res_candidato = funcao(nova_posicao)

                fit_candidato = calcular_fitness(res_candidato)

                if fit_candidato > colonia[i].fitness:

                    colonia[i].posicao = nova_posicao[:]

                    colonia[i].resultado_funcao = res_candidato

                    colonia[i].fitness = fit_candidato

                    colonia[i].tentativas = 0

                else:
                    colonia[i].tentativas += 1

            i = (i + 1) % n_fontes

        # --- 3. fase das abelhas escoteiras ---
        for i in range(n_fontes):

            if colonia[i].tentativas > limite_l:

                colonia[i].posicao = [
                    random.uniform(LIMITE_INF, LIMITE_SUP)
                    for _ in range(dim)
                ]

                colonia[i].resultado_funcao = funcao(
                    colonia[i].posicao
                )

                colonia[i].fitness = calcular_fitness(
                    colonia[i].resultado_funcao
                )

                colonia[i].tentativas = 0

        # memorização do melhor do enxame
        for a in colonia:

            if a.resultado_funcao < melhor_resultado_funcao:

                melhor_resultado_funcao = a.resultado_funcao

                melhor_solucao = a.posicao[:]

        historico_progresso.append(
            melhor_resultado_funcao
        )

    return melhor_resultado_funcao, historico_progresso
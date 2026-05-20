class Abelha:
    def __init__(self, posicao):
        self.posicao = posicao[:]
        self.resultado_funcao = float('inf')
        self.fitness = 0.0
        self.tentativas = 0
        
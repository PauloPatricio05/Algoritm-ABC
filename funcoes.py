import math

def sphere(x):
    total = 0
    for valor in x:
        total += valor ** 2
    return total

def rastrigin(x):
    n = len(x)
    total = 0
    for valor in x:
        total += (valor ** 2 - 10 * math.cos(2 * math.pi * valor))
    return 10 * n + total

def rosenbrock(x):
    total = 0
    for i in range(len(x) - 1):
        termo1 = 100 * (x[i+1] - x[i]**2)**2
        termo2 = (1 - x[i])**2
        total += termo1 + termo2
    return total
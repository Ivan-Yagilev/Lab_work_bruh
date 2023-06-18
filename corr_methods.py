from math import pi, sqrt, sin, cos, exp


KSI = pi / 4
EPS = 0.001


def k(x):
    if x < 0 or x > 1:
        return 0
    if x >= 0 and x < KSI:
        return sqrt(2) * cos(x)
    return cos(x) * cos(x)


def q(x):
    if x < 0 or x > 1:
        return 0
    if x >= 0 and x < KSI:
        return 1
    return x ** 2


def f(x):
    if x < 0 or x > 1:
        return 0
    if x >= 0 and x < KSI:
        return sin(2*x)
    return cos(x)


def k_test(x):
    if x < 0 or x > 1:
        return 0
    if x >= 0 and x < KSI:
        return 1
    return 0.5


def q_test(x):
    if x < 0 or x > 1:
        return 0
    if x >= 0 and x < KSI:
        return 1
    return KSI * KSI


def f_test(x):
    if x < 0 or x > 1:
        return 0
    if x >= 0 and x < KSI:
        return 1
    return sqrt(2)/2


def analytic_solution(x):
    if x < 0 or x > 1:
        return 0

    c1 = -0.3393176035227834
    c2 = 0.3393176035227834
    c3 = -0.4920418012319509
    c4 = 1.0560782612867800

    if x >= 0 and x <= KSI:
        return 1 + c1*exp(x) + c2*exp(-x)
    return c3*exp((pi*x)/(2*sqrt(2))) + c4*exp((-pi*x)/(2*sqrt(2))) + 8*sqrt(2)/(pi**2)


def get_test_task_solution(n):
    h = 1 / n
    res = []

    for i in range(n+1):
        x = i * h
        res.append(analytic_solution(x))
    return res


def get_integral(a, b, func):
    h = (b - a) / 2
    res = h / 3 * (func(a) + 4*func(a+h) + func(b))
    return res


def get_solution(n, k, q, f, border1, border2):
    # h = (1 - EPS) / n
    h = 1 / n

    a_j = []
    # x = h + EPS
    x = h

    for _ in range(1, n+1):
        if (x <= KSI or (x - h) >= KSI):
            a_j.append(k(x-0.5*h))
            # a_j.append(h/get_integral(x-h, x, k))
        else:
            tmp = (KSI-x+h)/k(0.5*(x-h+KSI))+(x-KSI)/k(0.5*(x+KSI))
            # tmp = get_integral(x-h, KSI, k) + get_integral(KSI, x, k)
            a_j.append(h / tmp)
        x += h

    d_j = []
    fi_j = []
    # x = h + EPS
    x = h
    for _ in range(1, n):
        if (x+0.5*h) <= KSI or (x-0.5*h) >= KSI:
            d_j.append(n * get_integral(x-0.5*h, x+0.5*h, q))
            fi_j.append(n * get_integral(x-0.5*h, x+0.5*h, f))
            # d_j.append(q(x))
            # fi_j.append(f(x))
        else:
            # d_j.append(n*(q(0.5*(x-0.5*h+KSI))*(KSI-x-0.5*h) + q(0.5*(KSI+x+0.5*h))*(x+0.5*h-KSI)))
            # fi_j.append(n*(f(0.5*(x-0.5*h+KSI))*(KSI-x-0.5*h) + f(0.5*(KSI+x+0.5*h))*(x+0.5*h-KSI)))
            d_j.append(n * (get_integral(x-0.5*h, KSI, q) + get_integral(KSI, x+0.5*h, q)))
            fi_j.append(n * (get_integral(x-0.5*h, KSI, f) + get_integral(KSI, x+0.5*h, f)))
        x += h

    A, B, C = [], [], []
    for i in range(n-1):
        A.append(a_j[i] / (h**2))
        B.append(a_j[i+1] / (h**2))
        C.append(a_j[i] / (h**2) + a_j[i+1] / (h**2) + d_j[i])

    xi1 = 0
    alpha = [xi1]
    beta = [border1]
    for i in range(n-1):
        alpha.append(B[i]/(C[i] - A[i]*alpha[i]))
        beta.append((fi_j[i] + A[i]*beta[i])/(C[i] - A[i]*alpha[i]))

    v = [None] * (n + 1)
    v[0] = border1
    v[n] = border2
    for i in range(n-1, 0, -1):
        v[i] = alpha[i] * v[i+1] + beta[i]
    return v


def task(n, k, q, f, border1, border2):
    v = get_solution(n, k, q, f, border1, border2)
    v2 = get_solution(2*n, k, q, f, border1, border2)

    e = []

    # x_tmp = 0.0 + EPS
    x_tmp = 0.0
    x = []
    # h = (1 - EPS)/n
    h = 1 / n

    v2 = [v2[2*i] for i in range(n+1)]
    for i in range(n+1):
        x.append(x_tmp)
        e.append(abs(v[i] - v2[i]))
        x_tmp += h

    return x, v, v2, e

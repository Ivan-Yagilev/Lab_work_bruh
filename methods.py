import numpy as np
import math


KSI = math.pi / 4


def k(x):
    if x < 0 or x > 1:
        return 0
    if x >= 0 and x < KSI:
        return math.sqrt(2) * math.sin(x)
    if x > KSI and x <= 1:
        return math.cos(x) * math.cos(x)


def q(x):
    if x < 0 or x > 1:
        return 0
    if x >= 0 and x < KSI:
        return 1
    if x > KSI and x <= 1:
        return x * x


def f(x):
    if x < 0 or x > 1:
        return 0
    if x >= 0 and x < KSI:
        return math.sin(2*x)
    if x > KSI and x <= 1:
        return math.cos(x)


def k_test(x):
    if x < 0 or x > 1:
        return 0
    if x >= 0 and x < KSI:
        return math.sqrt(2) * math.sin(KSI)
    return math.cos(KSI) * math.cos(KSI)


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
        return math.sin(2*KSI)
    return math.cos(KSI)


def test_task(x):
    if x < 0 or x > 1:
        return 0

    c1 = -0.3393176035227834
    c2 = 0.3393176035227834
    c3 = -0.4920418012319509
    c4 = 1.0560782612867800

    if x >= 0 and x <= KSI:
        return 1 + c1 * np.exp(x) + c2 * np.exp(-x)
    return c3 * np.exp(np.sqrt((KSI * KSI)/(np.cos(KSI) * np.cos(KSI))) * x) +\
        + c4 * np.exp(-np.sqrt((KSI * KSI)/(np.cos(KSI) * np.cos(KSI))) * x) + (np.cos(KSI)/(KSI*KSI))


def test_task_solution(n):
    h = 1 / n
    res = []

    for i in range(n+1):
        x = i * h
        res.append(test_task(x))
    return res


def numerical_test_task(n):
    a_i = []
    d_i = []
    fi_i = []
    x = 0.0
    h = 1 / n

    for i in range(1, n+1):
        if (x + 0.5 * h <= KSI):
            a_i.append(k_test(x+0.5*h))
        else:
            if (x >= KSI):
                a_i.append(k_test(x+0.5*h))
            else:
                tmp = n * ((KSI - x)/k_test(0.5*(x+KSI))+(x+h-KSI)/k_test(0.5*(x+h+KSI)))
                a_i.append(1 / tmp)
        x += h

    x = 0.0
    for i in range(1, n):
        if (x + 0.5 * h <= KSI):
            d_i.append(q_test(x))
            fi_i.append(f_test(x))
        else:
            if (x - 0.5 * h >= KSI):
                d_i.append(q_test(x))
                fi_i.append(f_test(x))
            else:
                d_i.append(n*((KSI-x+0.5*h)*q_test(0.5*(x-0.5*h+KSI))+(x+0.5*h-KSI)*q_test(0.5*(x+0.5*h+KSI))))
                fi_i.append(n*((KSI-x+0.5*h)*f_test(0.5*(x-0.5*h+KSI))+(x+0.5*h-KSI)*f_test(0.5*(x+0.5*h+KSI))))
        x += h
    xi1 = 0.0
    xi2 = 0.0

    v_tmp = [None] * (n+1)
    v_tmp[0] = 1.0
    v_tmp[n] = 0.0

    A = []
    B = []
    C = []

    for i in range(n-1):
        A.append(a_i[i] / (h*h))
        B.append(a_i[i+1] / (h*h))
        C.append(A[-1] + B[-1] + d_i[i])

    alpha = []
    beta = []

    alpha.append(xi1)
    beta.append(1.0)

    for i in range(n-1):
        alpha.append(B[i] / (C[i]-alpha[i]*A[i]))
        beta.append((fi_i[i] + beta[i]*A[i]) / (C[i] - alpha[i]*A[i]))

    for i in range(n-1, 0, -1):
        v_tmp[i] = alpha[i] * v_tmp[i+1] + beta[i]

    x = []
    x_tmp = 0
    e = []
    u = test_task_solution(n)
    u[n] = 0.0

    for i in range(n+1):
        x.append(x_tmp)
        e.append(np.abs(u[i]-v_tmp[i]))
        x_tmp += h

    return x, u, v_tmp, e


def numerical_task_n(n):
    a_i = []
    d_i = []
    fi_i = []
    x = 0.0
    h = 1 / n

    for i in range(1, n+1):
        x += h
        if (x <= KSI):
            a_i.append(k(x-0.5*h))
        elif (x - h >= KSI):
            a_i.append(k(x-0.5*h))
        else:
            tmp = n * ((KSI-x+h)/k(0.5*(x-h+KSI))+(x-KSI)/k(0.5*(x+KSI)))
            a_i.append(1 / tmp)

    x = 0.0
    for i in range(1, n):
        x += h
        if (x + 0.5 * h <= KSI):
            d_i.append(q(x))
            fi_i.append(f(x))
        elif (x-0.5*h >= KSI):
            d_i.append(q(x))
            fi_i.append(f(x))
        else:
            d_i.append(n*((KSI-x+0.5*h)*q(0.5*(x-0.5*h+KSI))+(x+0.5*h-KSI)*q(0.5*(x+0.5*h+KSI))))
            fi_i.append(n*((KSI-x+0.5*h)*f(0.5*(x-0.5*h+KSI))+(x+0.5*h-KSI)*f(0.5*(x+0.5*h+KSI))))

    xi1 = 0.0
    xi2 = 0.0
    v_tmp = [None] * (n + 1)
    v_tmp[0] = 1.0
    v_tmp[n] = 0.0

    A = []
    B = []
    C = []
    for i in range(n-1):
        A.append(a_i[i] / (h*h))
        B.append(a_i[i+1] / (h*h))
        C.append(A[-1] + B[-1] + d_i[i])

    alpha = []
    beta = []

    alpha.append(xi1)
    beta.append(1.0)

    for i in range(n-1):
        alpha.append(B[i] / (C[i]-alpha[i]*A[i]))
        beta.append((fi_i[i] + beta[i]*A[i]) / (C[i] - alpha[i]*A[i]))

    for i in range(n-1, 0, -1):
        v_tmp[i] = alpha[i] * v_tmp[i+1] + beta[i]

    return v_tmp


def numerical_main_task(n):
    v = numerical_task_n(n)
    v2 = numerical_task_n(2*n)

    e = []

    x_tmp = 0.0
    x = []
    h = 1/n

    v2 = [v2[2*i] for i in range(n+1)]
    for i in range(n+1):
        x.append(x_tmp)
        e.append(np.abs(v[i] - v2[i]))
        x_tmp += h

    return x, v, v2, e

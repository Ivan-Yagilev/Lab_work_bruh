from corr_methods import task, k, q, f, k_test, q_test, f_test, get_test_task_solution
import matplotlib.pyplot as plt
import csv
plt.style.use('seaborn')


def main(n):
    border1 = 1
    border2 = 0
    x, v, v2, e = task(n, k, q, f, border1, border2)

    with open('main.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['N', 'Xi', 'V(xi)', 'V2(x2i)', '|V(xi) - V2(x2i)|'])
        for i in range(0, n+1, 5):
            spamwriter.writerow([i, x[i], v[i], v2[i], e[i]])

    print(f"""    Для решения задачи использована равномерная сетка с числом разбиений n = {n};
    Задача должна быть решена с заданной точностью ε = 0.5⋅10 –6;
    Задача решена с точностью ε2 = {max(e)};
    Максимальное отклонение аналитического и численного решений наблюдается в точке x= {x[e.index(max(e))]}""")

    plt.subplot(1, 2, 1)
    plt.plot(x, v, 'b-', label='V(x)')
    plt.plot(x, v2, 'r-', label='V2(x)')
    plt.legend(loc='upper right')
    plt.title("Графики численных решений с обычным и половинным шагом")

    plt.subplot(1, 2, 2)
    plt.plot(x, e, 'g-', label='v(x)-v2(x)')
    plt.legend(loc='upper right')
    plt.title("Разность графиков численных решений")
    plt.show()


def test(n):
    border1 = 1
    border2 = 0
    x, v, v2, e = task(n, k_test, q_test, f_test, border1, border2)
    u = get_test_task_solution(n)
    e = [abs(v[i]-u[i]) for i in range(len(v))]

    with open('test.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['N', 'Xi', 'U(xi)', 'V(xi)', 'U(xi) - V(xi)'])
        for i in range(n+1):
            spamwriter.writerow([i, x[i], u[i], v[i], e[i]])

    print(f"""    Для решения задачи использована равномерная сетка с числом разбиений n = {n};
    Задача должна быть решена с погрешностью не более ε = 0.5⋅10 –6;
    Задача решена с погрешностью ε1 = {max(e)};
    Максимальное отклонение аналитического и численного решений наблюдается в точке x = {x[e.index(max(e))]}""")

    plt.subplot(1, 2, 1)
    plt.plot(x, u, 'b-', label='u')
    plt.plot(x, v, 'r-', label='v')
    plt.legend(loc='upper right')
    plt.title("Графики аналитического и численного решений")

    plt.subplot(1, 2, 2)
    plt.plot(x, e, 'g-', label='u(x)-v(x)')
    plt.legend(loc='upper right')
    plt.title("Разность графиков аналитического и численного решений")
    plt.show()


if __name__ == "__main__":
    choice = input("1. Тестовая задача, 2. Основная\n")
    n = int(input("Введите число узлов\n"))
    if choice == '1':
        test(n)
    else:
        main(n)

import methods
import matplotlib.pyplot as plt
import csv


def main(n):
    x, v, v2, e = methods.numerical_main_task(n)

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

    plt.plot(x, v, 'b-', label='V(x)')
    plt.plot(x, v2, 'r-', label='V2(x)')
    plt.legend(loc='upper right')
    plt.suptitle("Графики численных решений с обычным и половинным шагом")
    plt.grid()
    plt.show()

    plt.plot(x, e, 'g-', label='v(x)-v2(x)')
    plt.legend(loc='upper right')
    plt.suptitle("Разность графиков численного решений")
    plt.grid()
    plt.show()


def test(n):
    x, u, v_tmp, e = methods.numerical_test_task(n)

    with open('test.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['N', 'Xi', 'U(xi)', 'V(xi)', 'U(xi) - V(xi)'])
        for i in range(n+1):
            spamwriter.writerow([i, x[i], u[i], v_tmp[i], e[i]])

    print(f"""    Для решения задачи использована равномерная сетка с числом разбиений n = {n};
    Задача должна быть решена с погрешностью не более ε = 0.5⋅10 –6;
    Задача решена с погрешностью ε1 = {max(e)};
    Максимальное отклонение аналитического и численного решений наблюдается в точке x = {x[e.index(max(e))]}""")

    plt.plot(x, u, 'b-', label='u')
    plt.plot(x, v_tmp, 'r-', label='v_tmp')
    plt.legend(loc='upper right')
    plt.suptitle("Графики аналитического и численного решений")
    plt.grid()
    plt.show()

    plt.plot(x, e, 'g-', label='u(x)-v(x)')
    plt.legend(loc='upper right')
    plt.suptitle("Разность графиков аналитического и численного решений")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    choice = input("1. Тестовая задача, 2. Основная\n")
    if choice == '1':
        test(100)
    else:
        main(2500)

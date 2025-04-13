import numpy as np
import scienceplots
import matplotlib.pyplot as plt


def main():
    dbz_path_10km = "C:\\Users\\petva\\Desktop\\FMFI UK\\3. rocnik\\bakalarka\\Vysledky_matice\\dbz_statistika_10_km.txt"
    dbz_path_3km = "C:\\Users\\petva\\Desktop\\FMFI UK\\3. rocnik\\bakalarka\\Vysledky_matice\\dbz_statistika_3_km.txt"

    x10 = []
    y10 = []
    with open(dbz_path_10km) as fin:
        lines = [line.split() for line in fin]
        for line in lines:
            # pri 10 km treba odstranit dbz 32.5
            if line[0] == '32.5':
                continue
            x10.append(float(line[0]))
            y10.append(float(line[1]))

    x3 = []
    y3 = []
    with open(dbz_path_3km) as fin:
        lines = [line.split() for line in fin]
        for line in lines:
            x3.append(float(line[0]))
            y3.append(float(line[1]))

    sum_all_10 = np.sum(y10)
    for i in range(len(y10)):
        y10[i] = y10[i] / sum_all_10 * 100

    sum_all_3 = np.sum(y3)
    for i in range(len(y3)):
        y3[i] = y3[i] / sum_all_3 * 100

    print(np.sum(y10))

    plt.style.use(['science', 'notebook', 'grid'])
    # plt.title('Relatívna početnosť dbz hodnôt v okolí bleskov do 3 km')
    # plt.axvline(30, color='r')
    # plt.text(30, -0.1, '30', color='red', ha='center', fontsize=17)
    plt.plot(x3, y3, label='distance from lightning < 3 km')
    plt.plot(x10, y10, color='green', label='distance from lightning < 10 km')
    plt.xlabel('dBZ')
    plt.ylabel('%', rotation='horizontal', labelpad=15)
    plt.yticks(np.arange(0, 2.2, 0.2))
    plt.xticks(np.arange(0, 90, 10))
    plt.xlim(0, 95.5)
    plt.ylim(0, 2.2)
    plt.legend(edgecolor='k', fontsize=12)
    # plt.show()


if __name__ == '__main__':
    main()

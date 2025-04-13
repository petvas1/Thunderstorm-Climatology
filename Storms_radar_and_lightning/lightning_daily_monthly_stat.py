import os
import matplotlib.pyplot as plt
import numpy as np
import scienceplots


def main():
    blesky_dir_path = "Blesky_5min_synopt\\"

################ daily lightning distributions (5 minute time window) ################
    hours_values = np.zeros(12*24)  # every 5 minutes
    for root, dirs, files in os.walk(blesky_dir_path):
        for f in files:
            hours_now = int(f[-8:-6])
            minutes_now = int(f[-6:-4])
            index = int(hours_now * 12 + minutes_now / 5)
            full_name = os.path.join(root, f)
            with open(full_name, 'r') as fin:
                number_of_lines = len(fin.readlines())
                hours_values[index] += number_of_lines

    hours_values = hours_values / np.sum(hours_values) * 100

    plt.style.use(['science', 'notebook', 'grid'])
    plt.figure(figsize=(10, 5))
    x = np.linspace(0, 24, 12*24)
    plt.plot(x, hours_values)
    plt.xlim(0, 24)
    plt.ylim(0, )
    plt.xticks(range(0, 25))
    plt.tick_params(labelsize=12)
    # plt.title('Relatívna početnosť bleskov počas dňa', fontsize=25, pad=20)
    plt.xlabel('Time (UTC)')
    plt.ylabel('%', rotation='horizontal', labelpad=15)
    # plt.show()

########### total lightning strikes by each month #############
    # months_lightning_count = np.zeros([12])
    # for root, dirs, files in os.walk(blesky_dir_path):
    #     for f in files:
    #         month = int(f[4:6])
    #         full_name = os.path.join(root, f)
    #         with open(full_name, 'r') as fin:
    #             number_of_lines = len(fin.readlines())
    #             months_lightning_count[month-1] += number_of_lines
    #
    #
    # for i in range(len(months_lightning_count)):
    #     months_lightning_count[i] /= 13  # normovanie na pocet rokov
    #     months_lightning_count[i] /= 149132  # normovanie na km^2

    # print(months_lightning_count)

    # plt.style.use(['science', 'notebook', 'grid'])
    # fig, ax = plt.subplots()
    # months_lightning_count = np.loadtxt('blesky_mesiace_stat.txt')
    # months = np.arange(1, 13)
    # mesiace_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    # plt.bar(months, months_lightning_count)
    # plt.xticks(months, mesiace_labels)
    # ax.xaxis.set_ticks_position('none')
    # ax.xaxis.grid(False)
    # plt.ylabel(r'lightning strikes $\mathregular{km^{-2}}$ $\mathregular{yr^{-1}}$')
    # plt.savefig(r"Figure 7b.jpeg", dpi=1000)


if __name__ == '__main__':
    main()

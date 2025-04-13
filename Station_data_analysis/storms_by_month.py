import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scienceplots
from collections import Counter
from scipy.stats import linregress


def main():
    storms_data_path = "burky_javy.xlsx"
    df_storm_station = pd.read_excel(storms_data_path, sheet_name=0)
    df_storm_station = df_storm_station[df_storm_station['rok'] >= 1965]
    # prof_stations = [11813, 11816, 11826, 11858, 11868, 11903, 11930, 11933, 11934, 11938, 11968, 11993]
    # df_storm_station = df_storm_station[df_storm_station['ind_kli'].isin(prof_stations)]

    # priemerny pocet burkovych dni za mesiac na stanicu v rokoch, normal 1981 - 2010
######################### pocet stanic za rok ################
    pocet_burok_roky_s = dict(Counter(df_storm_station['rok'].values))
    roky_s, pocet_burok_rok_s = list(pocet_burok_roky_s.keys()), list(pocet_burok_roky_s.values())

    pocet_stanic_rok_s = dict()
    for rok in sorted(roky_s):
        set1 = set(df_storm_station['ind_kli'].where(df_storm_station['rok'] == rok))
        set2 = [x for x in set1 if x == x]  # remove NaN
        pocet_stanic_rok_s[rok] = len(set2)

    roky, pocet_stanic = list(pocet_stanic_rok_s.keys()), list(pocet_stanic_rok_s.values())
    ########################

    df_group_roky = [g.drop(['den', 'jav_r'], axis=1) for _, g in df_storm_station.groupby(['rok'])]  # list df pre kazdu stanicu vlastny
    rok_mesiace = []
    for i in range(len(df_group_roky)):
        mes_pocetnosti = np.array([0]*12)
        mes_counter = dict(Counter(df_group_roky[i]['mesiac'].values))
        for key, value in mes_counter.items():
            mes_pocetnosti[key-1] = value
        mes_pocetnosti = mes_pocetnosti / pocet_stanic[i]  # ku kazdemu mesiacu priemerny pocet burkovych dni za rok na 1 stanicu
        rok_mesiace.append(mes_pocetnosti)
################# nasledujuca sekcia pre rocne obdobia za cele obdobie #########
    # mesiace_roky = [0]*12  # ku kazdemu mesiacu da priemerny pocet burok pre kazdy rok
    # for j in range(12):
    #     mes_pocty = []
    #     for i in range(len(roky)):
    #         mes_pocty.append(rok_mesiace[i][j])
    #     mesiace_roky[j] = mes_pocty
    #
    # rocne_obdobia = [0]*4
    # rocne_obdobia[0] = np.array(mesiace_roky[2]) + np.array(mesiace_roky[3]) + np.array(mesiace_roky[4])
    # rocne_obdobia[1] = np.array(mesiace_roky[5]) + np.array(mesiace_roky[6]) + np.array(mesiace_roky[7])
    # rocne_obdobia[2] = np.array(mesiace_roky[8]) + np.array(mesiace_roky[9]) + np.array(mesiace_roky[10])
    # rocne_obdobia[3] = np.array(mesiace_roky[11]) + np.array(mesiace_roky[0]) + np.array(mesiace_roky[1])
    #
    # # Plot
    # plt.style.use(['science', 'notebook', 'grid'])
    # fig, ax = plt.subplots()
    #
    # obdobia = ['spring', 'summer', 'fall', 'winter']
    # colors = ['g', 'r', 'k', 'b']
    #
    # # Lists to keep track of handles and labels for the legends
    # data_handles = []
    # data_labels = []
    # trendline_handles = []
    # trendline_labels = []
    #
    # for i in range(4):
    #     # Perform linear regression
    #     x = np.array(roky) - 1965
    #     y = rocne_obdobia[i]
    #     slope, intercept, r_value, p_value, std_err = linregress(x, y)
    #     trendline = slope * x + intercept
    #
    #     # Plot data
    #     data_label = obdobia[i]
    #     data_handle, = ax.plot(roky, y, 'o-', markersize=3, lw=1.5, color=colors[i], label=data_label)
    #     data_handles.append(data_handle)
    #     data_labels.append(data_label)
    #
    #     # Plot the trendline
    #     trendline_label = f'y={slope: .3f}x +{intercept: .1f}, $R^{2}$={r_value**2: .2f}'
    #     trendline_handle, = ax.plot(roky, trendline, label=trendline_label, color=colors[i])
    #     trendline_handles.append(trendline_handle)
    #     trendline_labels.append(trendline_label)
    #
    # data_legend = ax.legend(data_handles, data_labels, fontsize=13, edgecolor='k', bbox_to_anchor=(0.23, 0.7))
    # trendline_legend = ax.legend(trendline_handles, trendline_labels, fontsize=9, edgecolor='k', bbox_to_anchor=(0.61, 0.74))
    # ax.add_artist(data_legend)
    # ax.add_artist(trendline_legend)
    #
    # plt.ylabel('number of TDs')
    # # plt.title('Počet búrkových dní v ročných obdobiach')
    # plt.ylim([-0.5, 15])
    # # plt.show()
###################################################

############### rozdelenie podla mesiacov #########
    # # hranicne roky (okrem posledneho)
    # rok_1 = 1965
    # rok_2 = 1985
    # rok_3 = 2005
    # rok_4 = 2024
    #
    # roky_12 = rok_mesiace[(rok_1-1951):(rok_2-1951)]
    # roky_23 = rok_mesiace[(rok_2-1951):(rok_3-1951)]
    # roky_34 = rok_mesiace[(rok_3-1951):(rok_4-1951)]
    # mesiace_priemer_12 = np.mean(roky_12, axis=0)
    # mesiace_priemer_23 = np.mean(roky_23, axis=0)
    # mesiace_priemer_34 = np.mean(roky_34, axis=0)
    #
    # mesiace_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    # months = np.arange(1, 13)
    # bar_width = 0.22
    #
    # ############ plot pre viac dekady mesiacov #############
    # # plt.title('Počet búrkových dní v jednotlivých mesiacoch')
    # #### plt.bar(months, mesiace_priemer_12)
    # plt.style.use(['science', 'notebook', 'grid'])
    # fig, ax = plt.subplots()
    # plt.bar(months - bar_width, mesiace_priemer_12, width=bar_width, label=f'{rok_1} - {rok_2-1}')
    # plt.bar(months, mesiace_priemer_23, width=bar_width, label=f'{rok_2} - {rok_3-1}')
    # plt.bar(months + bar_width, mesiace_priemer_34, width=bar_width, label=f'{rok_3} - {rok_4-1}')
    # plt.ylabel('number of TDs / year')
    # plt.xticks(months, mesiace_labels)
    # ax.xaxis.set_ticks_position('none')
    # ax.xaxis.grid(False)
    # # ax.yaxis.grid(True, which='both', linestyle='--', linewidth=0.7, color='gray')
    # plt.legend(edgecolor='k', fontsize=13)
    #
    # # plt.show()

    ########### plot pre mesiace a blesky spolu ##############
    # bar_width = 0.4
    # blesky_pocet = np.loadtxt('blesky_mesiace_stat.txt')
    #
    # fig, ax1 = plt.subplots()
    # spacing = 0.21
    # bar_positions1 = months - spacing
    # bar_positions2 = months + spacing
    #
    # ax1.bar(bar_positions1, mesiace_priemer_12, width=bar_width, color='b')
    # ax1.set_ylabel('počet búrkových dní / rok', color='b')
    #
    # ax2 = ax1.twinx()
    # ax2.bar(bar_positions2, blesky_pocet, width=bar_width, color='r')
    # ax2.set_ylabel(r'počet bleskov / rok / $km^2$', color='r')
    #
    # plt.xticks(months, mesiace_labels)
    # plt.tight_layout()
    # plt.show()


if __name__ == '__main__':
    main()

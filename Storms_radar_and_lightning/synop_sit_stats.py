from collections import Counter
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scienceplots
import time
from scipy.stats import linregress


def main():
    syn_sit_path = "C:\\Users\\petva\\Desktop\\FMFI UK\\3. rocnik\\bakalarka\\Burkove dni - javy\\syn_sit_all.xlsx"
    burky_na_stanici_path = "C:\\Users\\petva\\Desktop\\FMFI UK\\3. rocnik\\bakalarka\\Burkove dni - javy\\burky_javy.xlsx"
    df_situacie = pd.read_excel(syn_sit_path)
    df_burky = pd.read_excel(burky_na_stanici_path)
    df_burky.drop_duplicates(subset=['rok', 'mesiac', 'den'], inplace=True)
    df_burky = df_burky[df_burky['rok'] >= 1965]
    df_situacie = df_situacie[df_situacie['rok'] >= 1965]
    # df_burky = df_burky[df_burky['rok'] >= 2011]
    # df_burky = df_burky[df_burky['rok'] <= 2022]
    # df_situacie = df_situacie[df_situacie['rok'] >= 2011]
    # df_situacie = df_situacie[df_situacie['rok'] <= 2022]
    df_merged = pd.merge(df_burky, df_situacie, on=['rok', 'mesiac', 'den'], how='inner')
    pocet_rokov = 59

########### percenta burkove dni/vsetky dni ##########
    # situacie = df_situacie['situacia']
    # situacie_pocty = dict(Counter(situacie))
    # situacie_pocty = dict(sorted(situacie_pocty.items()))
    # situacie_pocty = {k: v / pocet_rokov for k, v in situacie_pocty.items()}  # normovanie na 1 rok za obdobie 1965-2023
    # print(situacie_pocty)
    #
    # burky_situacie = df_merged['situacia']
    # burky_situacie_pocty = dict(Counter(burky_situacie))
    # # burky_situacie_pocty['Ap4'] = 0     ############# pri 2011-2022 #####
    # burky_situacie_pocty = dict(sorted(burky_situacie_pocty.items()))
    # burky_situacie_pocty = {k: v / pocet_rokov for k, v in burky_situacie_pocty.items()}  # normovanie na 1 rok za obdobie 1965-2023
    # print(burky_situacie_pocty)
    # print(df_merged)
    #
    # percenta_burky_vs_dni = dict()
    # for sit, val in situacie_pocty.items():
    #     for burky_sit, burky_val in burky_situacie_pocty.items():
    #         if sit == burky_sit:
    #             percenta_burky_vs_dni[sit] = burky_val / val * 100
    #
    # print(percenta_burky_vs_dni)
    #
    # situacie_typy = list(situacie_pocty.keys())
    # situacie_values = list(situacie_pocty.values())
    # burky_situacie_values = list(burky_situacie_pocty.values())
    # percenta = list(percenta_burky_vs_dni.values())
    #
    # # print(sum(situacie_values))
    # # print(sum(burky_situacie_values))
    #
    # plt.figure(figsize=(10, 5))
    # plt.bar(situacie_typy, situacie_values, color='orange', label='Days without thunderstorms')
    # plt.bar(situacie_typy, burky_situacie_values, color='blue', label='Thunderstorm days')
    # for i in range(len(situacie_typy)):
    #     plt.text(situacie_typy[i], burky_situacie_values[i] + 0.5, f'{percenta[i]: .0f}', ha='center', weight='bold', color='k', fontsize=7)
    #
    # plt.xticks(fontsize=6)
    # plt.xlabel('Synoptic situation')
    # plt.ylabel('Days in 1 year')
    # plt.legend(edgecolor='k', loc='upper center')
    # # plt.tight_layout()
    # # plt.show()

################# cyklonalne a anticyklonalne trend za rok #########
    cyklonalne = ['B', 'Bp', 'C', 'Cv', 'Ec', 'NEc', 'NWc', 'Nc', 'SEc', 'SWc1', 'SWc2', 'SWc3', 'Vfz', 'Wc', 'Wcs']
    anticyklonalne = ['A', 'Ap1', 'Ap2', 'Ap3', 'Ap4', 'Ea', 'NEa', 'NWa', 'SEa', 'SWa', 'Sa', 'Wa', 'Wal']
    roky_cyklonalne = np.zeros(59)
    roky_anticyklonalne = np.zeros(59)

    df_group_roky = [g for _, g in df_situacie.groupby(['rok'])]  # list df pre kazdu stanicu vlastny
    for i in range(len(df_group_roky)):
        rocny_count_situacii = dict(Counter(df_group_roky[i]['situacia']))
        cyklonalne_rocny_pocet = 0
        for sit, value in rocny_count_situacii.items():
            if sit in cyklonalne:
                cyklonalne_rocny_pocet += value
        anticyklonalne_rocny_pocet = len(df_group_roky[i]) - cyklonalne_rocny_pocet

        roky_cyklonalne[i] = cyklonalne_rocny_pocet
        roky_anticyklonalne[i] = anticyklonalne_rocny_pocet

    #### aj pre burkove dni ##########
    roky_cyklonalne_burky = np.zeros(59)
    roky_anticyklonalne_burky = np.zeros(59)
    df_group_roky_burky = [g for _, g in df_merged.groupby(['rok'])]  # list df pre kazdu stanicu vlastny
    for i in range(len(df_group_roky)):
        rocny_count_situacii = dict(Counter(df_group_roky_burky[i]['situacia']))
        cyklonalne_rocny_pocet = 0
        anticyklonalne_rocny_pocet = 0
        for sit, value in rocny_count_situacii.items():
            if sit in cyklonalne:
                cyklonalne_rocny_pocet += value
            else:
                anticyklonalne_rocny_pocet += value

        roky_cyklonalne_burky[i] = cyklonalne_rocny_pocet
        roky_anticyklonalne_burky[i] = anticyklonalne_rocny_pocet

    roky = np.arange(1965, 2024)
    plt.style.use(['science', 'notebook', 'grid'])
    fig, ax = plt.subplots()

    # Lists to keep track of handles and labels for the legends
    data_handles = []
    data_labels = []
    trendline_handles = []
    trendline_labels = []

    situacie_all = [roky_cyklonalne, roky_anticyklonalne, roky_cyklonalne_burky, roky_anticyklonalne_burky]
    labels = ['Cyclonic', 'Anticyclonic', 'cyklonálne_búrky', 'anticyklonálne_búrky']
    colors = ['green', 'blue', 'black', 'red']
    for i in range(2):  # use 4 to add burkove dni
        # Perform linear regression
        x = roky - 1965
        y = situacie_all[i]
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        trendline = slope * x + intercept

        # Plot data
        data_label = labels[i]
        data_handle, = ax.plot(roky, y, 'o-', markersize=3, lw=1.5, color=colors[i], label=data_label)
        data_handles.append(data_handle)
        data_labels.append(data_label)

        # Plot the trendline
        trendline_label = f'y={slope: .2f}x +{intercept: .0f}, $R^{2}$={r_value ** 2: .2f}'
        trendline_handle, = ax.plot(roky, trendline, label=trendline_label, color=colors[i])
        trendline_handles.append(trendline_handle)
        trendline_labels.append(trendline_label)

    data_legend = ax.legend(data_handles, data_labels, fontsize=13, edgecolor='k', bbox_to_anchor=(0.65, 0.82))
    trendline_legend = ax.legend(trendline_handles, trendline_labels, fontsize=9, edgecolor='k',
                                 bbox_to_anchor=(0.62, 0.15))
    ax.add_artist(data_legend)
    ax.add_artist(trendline_legend)

    # plt.xlabel('rok')
    plt.ylabel('Days in 1 year')
    plt.ylim([75, 295])
    # plt.title('Vývoj cyklonálnych a anticyklonálnych situácií')


if __name__ == '__main__':
    main()

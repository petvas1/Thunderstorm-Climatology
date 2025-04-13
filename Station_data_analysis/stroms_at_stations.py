import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scienceplots
from collections import Counter


burky_data_path = "C:\\Users\\petva\\Desktop\\FMFI UK\\3. rocnik\\bakalarka\\Burkove dni - javy\\burky_javy.xlsx"
df_burka_stanica = pd.read_excel(burky_data_path, sheet_name=0)
# df_burka_vzdialena = pd.read_excel(burky_data_path, sheet_name=1)
# df_blyskavica = pd.read_excel(burky_data_path, sheet_name=2)

# stanice_burka_stanica = set(df_burka_stanica['ind_kli'].values)
# stanice_burka_vzdialena = set(df_burka_vzdialena['ind_kli'].values)
# stanice_blyskavica = set(df_blyskavica['ind_kli'].values)
# stanice = set.union(stanice_burka_stanica, stanice_burka_vzdialena, stanice_blyskavica)

# vypise roky pre kazdu stanicu
# stanica_burka_stanica_roky = dict()
# for index in stanice_burka_stanica:
#     roky = set(df_burka_stanica['rok'].where(df_burka_stanica['ind_kli'] == index))
#     roky2 = [x for x in roky if x == x]  # remove nan
#     stanica_burka_stanica_roky[index] = roky2
#
# with open('stanice_roky.txt', 'w') as fout:
#     for key, value in stanica_burka_stanica_roky.items():
#         fout.write('{}\t{}\n'.format(key, '\t'.join(map(str, value))))


# ku kazdej stanici vypise roky a ich pocet + zobrazi histogram
# pocet_za_rok_na_stanici = []
# pocet_za_rok = []
# for i in range(len(df_burka_stanica['ind_kli'].values)-1):
#     if df_burka_stanica['ind_kli'].values[i+1] == df_burka_stanica['ind_kli'].values[i]:
#         pocet_za_rok.append(df_burka_stanica['rok'].values[i])
#     else:
#         pocet_za_rok.append(df_burka_stanica['rok'].values[i])  # pripocita poslednu hodnotu
#         for value in dict(Counter(pocet_za_rok)).values():
#             pocet_za_rok_na_stanici.append(value)
#         pocet_za_rok = []
#
# plt.style.use(['science', 'notebook', 'grid'])
# plt.hist(pocet_za_rok_na_stanici,
#          rwidth=0.95,
#          bins=range(0, 44, 2),
#          align='mid')
# plt.xlabel('pocet burkovych dni za rok')
# plt.ylabel('pocetnost javov')
# plt.xticks(range(0, 44, 2))
# plt.xlim(0, 44)
# plt.show()

# vyvoj poctu stanic v pozorovanom obdobi
# pocet_burok_roky_s = dict(Counter(df_burka_stanica['rok'].values))
# roky_s, pocet_burok_rok_s = list(pocet_burok_roky_s.keys()), list(pocet_burok_roky_s.values())
#
# pocet_stanic_rok_s = dict()
# for rok in sorted(roky_s):
#     set1 = set(df_burka_stanica['ind_kli'].where(df_burka_stanica['rok'] == rok))
#     set2 = [x for x in set1 if x == x]  # remove NaN
#     pocet_stanic_rok_s[rok] = len(set2)
#
# roky, pocet_stanic = list(pocet_stanic_rok_s.keys()), list(pocet_stanic_rok_s.values())
# plt.style.use(['science', 'notebook', 'grid'])
# plt.plot(roky, pocet_stanic, 'o-', markersize=4)
# plt.xlabel('rok')
# plt.ylabel('pocet stanic')
# plt.show()

# odstranenie rokov kde pocet zaznamov je <= 5
#
df_group_stanice = [g.drop(['mes', 'den'], axis=1) for _, g in df_burka_stanica.groupby(['ind_kli'])]  # list df pre kazdu stanicu vlastny
rok_counter = dict(Counter(df_group_stanice[16]['rok'].values))
roky, pocty = list(rok_counter.keys()), list(rok_counter.values())
#
# plt.style.use(['science', 'notebook', 'grid'])
# plt.plot(roky, pocty, 'o-')
# plt.show()

roky_celkovo = []
for i in range(len(df_group_stanice)):
    rok_counter = dict(Counter(df_group_stanice[i]['rok'].values))
    #
    # roky_zle = []
    # for rok, pocet in rok_counter.items():
    #     if pocet <= 5:
    #         roky_zle.append(rok)
    #
    # for rok in roky_zle:
    #     for index, row in df_group_stanice[i].iterrows():
    #         if row['rok'] == rok:
    #             df_group_stanice[i].drop(index, inplace=True)

    for rok in set(df_group_stanice[i]['rok']):
        roky_celkovo.append(rok)
# vyvoj poctu stanic
roky_counter = dict(sorted(Counter(roky_celkovo).items()))
roky, pocet_stanic = list(roky_counter.keys()), list(roky_counter.values())
# sum = 0
# for i in range(len(roky)):
#     if roky[i] in range(1981, 2011):
#         sum += pocet_stanic[i]
# priemer_poctu_stanic = sum / (2011-1981)

#
# plt.plot(roky, pocet_stanic, 'o-', markersize=4)
# plt.xlabel('rok')
# plt.ylabel('pocet stanic')
# plt.show()

# priemerny pocet burkovych dni za mesiac na stanicu v rokoch, normal 1981 - 2010

df_group_roky = [g.drop(['den', 'jav_r'], axis=1) for _, g in df_burka_stanica.groupby(['rok'])]  # list df pre kazdu stanicu vlastny

rok_mesiace = []
for i in range(len(df_group_roky)):
    mes_pocetnosti = np.array([0]*12)
    mes_counter = dict(Counter(df_group_roky[i]['mes'].values))
    for key, value in mes_counter.items():
        mes_pocetnosti[key-1] = value
    mes_pocetnosti = mes_pocetnosti / pocet_stanic[i]
    rok_mesiace.append(mes_pocetnosti)

mesiace_roky = [0]*12  # ku kazdemu mesiacu da priemerny pocet burok pre kazdy rok
for j in range(12):
    mes_pocty = []
    for i in range(len(roky)):
        mes_pocty.append(rok_mesiace[i][j])
    mesiace_roky[j] = mes_pocty

rocne_obdobia = [0]*4
rocne_obdobia[0] = np.array(mesiace_roky[2]) + np.array(mesiace_roky[3]) + np.array(mesiace_roky[4])
rocne_obdobia[1] = np.array(mesiace_roky[5]) + np.array(mesiace_roky[6]) + np.array(mesiace_roky[7])
rocne_obdobia[2] = np.array(mesiace_roky[8]) + np.array(mesiace_roky[9]) + np.array(mesiace_roky[10])
rocne_obdobia[3] = np.array(mesiace_roky[11]) + np.array(mesiace_roky[0]) + np.array(mesiace_roky[1])

# mesiace
# for i in range(12):
#     trendline = np.polyfit(roky, mesiace_roky[i], 1)
#     p = np.poly1d(trendline)
#     plt.plot(roky, mesiace_roky[i], 'o-', markersize=2, lw=1)
#     plt.plot(roky, p(roky))

plt.style.use(['science', 'notebook', 'grid'])
colors = ['g', 'r', 'brown', 'b']
for i in range(4):
    trendline = np.polyfit(roky, rocne_obdobia[i], 1)
    p = np.poly1d(trendline)
    plt.plot(roky, rocne_obdobia[i], 'o-', markersize=2, lw=1.5, color=colors[i])
    plt.plot(roky, p(roky), color=colors[i], label='_nolegend_', lw=1)
plt.legend(['jar', 'leto', 'jeseň', 'zima'], fontsize=12)
plt.xlabel('rok')
plt.axhline(y=0, color='k')
plt.ylabel('number of TDs')
plt.ylim([0, 15])
plt.show()


# pocet_burok_mes = np.divide(pocet_burok_mes, pocet_stanic)
# mesiace_spolu = []
# for i in range(len(df_burka_stanica['mes'].values)):
#     if df_burka_stanica['rok'][i] in range(1981, 2011):
#         mesiace_spolu.append(df_burka_stanica['mes'][i])
#
#
# pocet_burok_mesiace = dict(sorted(Counter(df_burka_stanica['mes'].values).items()))
# mesiace, pocet_burok_mes = np.array(list(pocet_burok_mesiace.keys())), np.array(list(pocet_burok_mesiace.values()))
# pocet_burok_mes = pocet_burok_mes / priemer_poctu_stanic / (2011 - 1981)
#
# plt.bar(mesiace, pocet_burok_mes)
# plt.xlabel('mesiac')
# plt.ylabel('pocet burok')
# plt.xticks(range(1, 13))
# plt.xlim([0, 13])
# plt.show()

# pocet_burok_na_den = df_burka_stanica.pivot_table(index=['rok', 'mes', 'den'], aggfunc='size').reset_index()
# pocet_burok_na_den.rename(columns={0: 'pocet'}, inplace=True)
# pocet_burok_na_den.sort_values('pocet', ascending=False, inplace=True)
#
# dni_podm = pocet_burok_na_den.loc[(pocet_burok_na_den['rok'] == 2013) & ((pocet_burok_na_den['mes'] == 5)
#                                   | (pocet_burok_na_den['mes'] == 6) | (pocet_burok_na_den['mes'] == 7))].head(20)
# print(dni_podm)

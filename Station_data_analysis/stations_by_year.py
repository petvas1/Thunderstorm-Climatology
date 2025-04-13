import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scienceplots
from collections import Counter

burky_data_path = "C:\\Users\\petva\\Desktop\\FMFI UK\\3. rocnik\\bakalarka\\Burkove dni - javy\\burky_javy.xlsx"
df_burka_stanica = pd.read_excel(burky_data_path, sheet_name=0)

pocet_burok_roky_s = dict(Counter(df_burka_stanica['rok'].values))
roky_s, pocet_burok_rok_s = list(pocet_burok_roky_s.keys()), list(pocet_burok_roky_s.values())

pocet_stanic_rok_s = dict()
for rok in sorted(roky_s):
    set1 = set(df_burka_stanica['ind_kli'].where(df_burka_stanica['rok'] == rok))
    set2 = [x for x in set1 if x == x]  # remove NaN
    pocet_stanic_rok_s[rok] = len(set2)

roky, pocet_stanic = list(pocet_stanic_rok_s.keys()), list(pocet_stanic_rok_s.values())
plt.style.use(['science', 'notebook', 'grid'])
plt.plot(roky, pocet_stanic, 'o-', markersize=4)
plt.xlabel('rok')
plt.ylabel('pocet stanic')
plt.show()

# # odstranenie rokov kde pocet zaznamov je <= 5
# df_group_stanice = [g.drop(['mes', 'den'], axis=1) for _, g in df_burka_stanica.groupby(['ind_kli'])]  # list df pre kazdu stanicu vlastny
# rok_counter = dict(Counter(df_group_stanice[16]['rok'].values))
# roky, pocty = list(rok_counter.keys()), list(rok_counter.values())
# #
# # plt.style.use(['science', 'notebook', 'grid'])
# # plt.plot(roky, pocty, 'o-')
# # plt.show()
#
# roky_celkovo = []
# for i in range(len(df_group_stanice)):
#     rok_counter = dict(Counter(df_group_stanice[i]['rok'].values))
#     #
#     # roky_zle = []
#     # for rok, pocet in rok_counter.items():
#     #     if pocet <= 5:
#     #         roky_zle.append(rok)
#     #
#     # for rok in roky_zle:
#     #     for index, row in df_group_stanice[i].iterrows():
#     #         if row['rok'] == rok:
#     #             df_group_stanice[i].drop(index, inplace=True)
#
#     for rok in set(df_group_stanice[i]['rok']):
#         roky_celkovo.append(rok)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import scienceplots
import geopandas as gpd
from shapely.geometry import Point
from collections import Counter


df_stanice = pd.read_excel("stanice_surad.xlsx")
burky_data_path = "burky_javy.xlsx"
df_burka_stanica = pd.read_excel(burky_data_path, sheet_name=0)
# europe_countries = gpd.read_file("europe.geojson")
# mapa_sr = gpd.read_file("mapa_sr.csv")
mapa_sr_kraje = gpd.read_file("mapa_sr_kraje.csv")
# mapa_sr_okresy = gpd.read_file("mapa_sr_okresy.csv")

#################################
# rozdelenie podla krajov
kraje_polygons = [i for i in mapa_sr_kraje.geometry]
stredy_krajov = [(kraje_polygons[i].centroid.x, kraje_polygons[i].centroid.y) for i in range(8)]
kraje = mapa_sr_kraje['TXT'].values

df_stanice['kraj'] = ''
for j in range(len(df_stanice['ind_kli'].values)):
    point = Point(df_stanice['longitude'][j], df_stanice['latitude'][j])
    for i in range(8):
        if point.within(kraje_polygons[i]):
            df_stanice.loc[df_stanice['ind_kli'][j] == df_stanice['ind_kli'], 'kraj'] = kraje[i]

df_merged = df_burka_stanica.merge(df_stanice, on='ind_kli')
df_merged = df_merged[df_merged['rok'] >= 1965]
group_kraj = [g.drop(['mesiac', 'den', 'jav_r', 'h'], axis=1) for _, g in df_merged.groupby('kraj')]

priemerny_pocet_burok_kraje = []
for j in range(8):
    pocet_burok_za_rok = list(dict(Counter(group_kraj[j]['rok'].values)).values())
    group_kraj_rok = [g for _, g in group_kraj[j].groupby('rok')]
    pocet_stanic_za_rok = []
    for i in range(len(group_kraj_rok)):
        pocet_stanic = len(set(group_kraj_rok[i]['ind_kli'].values))
        pocet_stanic_za_rok.append(pocet_stanic)

    pocet_burok_za_rok_normovany = np.divide(np.array(pocet_burok_za_rok), np.array(pocet_stanic_za_rok))
    priemerny_pocet_burok = np.mean(pocet_burok_za_rok_normovany)
    priemerny_pocet_burok_kraje.append(priemerny_pocet_burok)

fig, ax = plt.subplots()
mapa_sr_kraje.plot(ax=ax, color=(0, 0, 1, 0.2), edgecolor='k')
ax.plot(df_stanice.longitude, df_stanice.latitude, 'o', markersize=2, color='r')
for i in range(len(stredy_krajov)):
    ax.text(stredy_krajov[i][0], stredy_krajov[i][1], '{:.1f}'.format(priemerny_pocet_burok_kraje[i]), fontsize=13)

# ax.set_xticks(np.arange(17, 23, 0.5))
# ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.1f}°"))
# ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.2f}°"))
hillsade = plt.imread("imagesr.png")
hraniceSR = [16.8327, 22.566, 47.732, 49.614]
plt.imshow(hillsade, alpha=0.5, extent=hraniceSR)

plt.show()

######################################
# rozdelenie podla nadmorskej vysky
# df_merged = df_burka_stanica.merge(df_stanice, on='ind_kli')
# df_merged = df_merged[df_merged['rok'] >= 1965][['ind_kli', 'rok', 'h']]
# group_stanica = [g for _, g in df_merged.groupby('ind_kli')]
# vysky = []
# priemer_za_rok = []
# for i in range(len(group_stanica)):
#     pocet_burok_za_rok = list(dict(Counter(group_stanica[i]['rok'].values)).values())
#     priemerny_pocet_burok_za_rok = np.mean(np.array(pocet_burok_za_rok))
#     if priemerny_pocet_burok_za_rok < 5:
#         continue
#     vyska = group_stanica[i]['h'].values[0]
#     vysky.append(vyska)
#     priemer_za_rok.append(priemerny_pocet_burok_za_rok)
#
# # levels = [100, 200, 300, 500, 700, 1000, 2700]
# levels = range(100, 2800, 100)
# priemery_rozdelene = [0]*(len(levels)-1)
# vysky_rozdelene = [(levels[i] + levels[i+1]) / 2 for i in range(len(levels)-1)]
# for i in range(len(levels)-1):
#     for j in range(len(vysky)):
#         if levels[i] <= vysky[j] < levels[i+1]:
#             priemery_rozdelene[i] += priemer_za_rok[j]
#
# counts, edges = np.histogram(vysky, bins=levels)
# priemery_rozdelene_norm = np.divide(priemery_rozdelene, counts)
# priemery_rozdelene_norm = [i if i == i else -10 for i in priemery_rozdelene_norm]
#
# plt.style.use(['science', 'notebook', 'grid'])
# fig, ax = plt.subplots()
# ax.bar(vysky_rozdelene, priemery_rozdelene_norm, width=90, edgecolor='k')
# ax.bar_label(ax.containers[0], fmt='%.1f')
# ax.set_ylim(0, 18)
# ax.set_xlabel('nadmorska vyska')
# ax.set_ylabel('priemerny pocet burkovych dni za rok')
# plt.show()

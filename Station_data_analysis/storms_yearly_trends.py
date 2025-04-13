import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scienceplots
from collections import Counter
from scipy.stats import linregress

burky_data_path = "burky_javy.xlsx"
burka_stanica = pd.read_excel(burky_data_path, sheet_name=0)
burka_stanica = burka_stanica[burka_stanica['rok'] >= 1965]

prof_stanice = [11813, 11816, 11826, 11858, 11868, 11903, 11930, 11933, 11934, 11938, 11968, 11993]
prof_burka_stanica = burka_stanica[burka_stanica['ind_kli'].isin(prof_stanice)]

### vsetky stanice
pocet_burok_v_rokoch= dict(Counter(burka_stanica['rok'].values))
roky, pocet_burok_rok = np.array(list(pocet_burok_v_rokoch.keys())), np.array(list(pocet_burok_v_rokoch.values()))

pocet_stanic_v_rokoch = dict()
for rok in roky:
    set1 = set(burka_stanica['ind_kli'].where(burka_stanica['rok'] == rok))
    set2 = [x for x in set1 if x == x]  # remove NaN
    pocet_stanic_v_rokoch[rok] = len(set2)

pocet_burok_v_rokoch_norm = np.divide(pocet_burok_rok, np.array(list(pocet_stanic_v_rokoch.values())))

### prof stanice
prof_pocet_burok_v_rokoch= dict(Counter(prof_burka_stanica['rok'].values))
prof_roky, prof_pocet_burok_rok = np.array(list(prof_pocet_burok_v_rokoch.keys())), np.array(list(prof_pocet_burok_v_rokoch.values()))

prof_pocet_stanic_v_rokoch = dict()
for rok in prof_roky:
    set1 = set(prof_burka_stanica['ind_kli'].where(prof_burka_stanica['rok'] == rok))
    set2 = [x for x in set1 if x == x]  # remove NaN
    prof_pocet_stanic_v_rokoch[rok] = len(set2)

prof_pocet_burok_v_rokoch_norm = np.divide(prof_pocet_burok_rok, np.array(list(prof_pocet_stanic_v_rokoch.values())))

### plot
plt.style.use(['science', 'notebook', 'grid'])
fig, ax = plt.subplots()

# Lists to keep track of handles and labels for the legends
data_handles = []
data_labels = []
trendline_handles = []
trendline_labels = []

data_all = [pocet_burok_v_rokoch_norm, prof_pocet_burok_v_rokoch_norm]
labels = ['All stations', 'High-quality stations']
colors = ['k', 'r']
for i in range(2):
    # Perform linear regression
    x = roky - 1965
    y = data_all[i]
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    trendline = slope * x + intercept

    # Plot data
    data_label = labels[i]
    data_handle, = ax.plot(roky, y, 'o-', markersize=3, lw=1.5, color=colors[i], label=data_label)
    data_handles.append(data_handle)
    data_labels.append(data_label)

    # Plot the trendline
    trendline_label = f'y = {slope: .2f}x +{intercept: .1f}, $R^{2}$={r_value ** 2: .2f}'
    trendline_handle, = ax.plot(roky, trendline, label=trendline_label, color=colors[i])
    trendline_handles.append(trendline_handle)
    trendline_labels.append(trendline_label)

data_legend = ax.legend(data_handles, data_labels, fontsize=13, edgecolor='k', bbox_to_anchor=(0.55, 0.8))
trendline_legend = ax.legend(trendline_handles, trendline_labels, fontsize=8, edgecolor='k', bbox_to_anchor=(0.4, 0.15))
ax.add_artist(data_legend)
ax.add_artist(trendline_legend)

# plt.xlabel('rok')
plt.ylabel('number of TDs')
# plt.legend(['búrka na stanici', 'búrka vzdialená', 'blýskavica'], loc='best', edgecolor='k', fontsize=10)
# plt.show()

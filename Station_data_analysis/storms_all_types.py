import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scienceplots
from collections import Counter
from scipy.stats import linregress


# storms by year, all types
burky_data_path = "burky_javy.xlsx"
burka_stanica = pd.read_excel(burky_data_path, sheet_name=0)
burka_vzdialena = pd.read_excel(burky_data_path, sheet_name=1)
blyskavica = pd.read_excel(burky_data_path, sheet_name=2)

stanice_burka_stanica = set(burka_stanica['ind_kli'].values)
stanice_burka_vzdialena = set(burka_vzdialena['ind_kli'].values)
stanice_blyskavica = set(blyskavica['ind_kli'].values)
stanice = set.union(stanice_burka_stanica, stanice_burka_vzdialena, stanice_blyskavica)
pocet_stanic_b_s = dict(Counter(burka_stanica['ind_kli'].values))

pocet_burok_roky_s = dict(Counter(burka_stanica['rok'].values))
roky_s, pocet_burok_rok_s = np.array(list(pocet_burok_roky_s.keys())), np.array(list(pocet_burok_roky_s.values()))
roky_s_new = []
pocet_burok_rok_s_new = []
for i in range(len(roky_s)):
    if roky_s[i] in range(1981, 2011):
        roky_s_new.append(roky_s[i])
        pocet_burok_rok_s_new.append(pocet_burok_rok_s[i])

roky_s, pocet_burok_rok_s = roky_s_new, pocet_burok_rok_s_new

pocet_stanic_rok_s = dict()
for rok in roky_s:
    set1 = set(burka_stanica['ind_kli'].where(burka_stanica['rok'] == rok))
    set2 = [x for x in set1 if x == x]  # remove NaN
    pocet_stanic_rok_s[rok] = len(set2)

pocet_burok_rok_s = np.divide(pocet_burok_rok_s, np.array(list(pocet_stanic_rok_s.values())))

pocet_burok_roky_v = dict(Counter(burka_vzdialena['rok'].values))
roky_v, pocet_burok_rok_v = np.array(list(pocet_burok_roky_v.keys())), np.array(list(pocet_burok_roky_v.values()))

roky_v_new = []
pocet_burok_rok_v_new = []
for i in range(len(roky_v)):
    if roky_v[i] in range(1981, 2011):
        roky_v_new.append(roky_v[i])
        pocet_burok_rok_v_new.append(pocet_burok_rok_v[i])

roky_v, pocet_burok_rok_v = roky_v_new, pocet_burok_rok_v_new

pocet_stanic_rok_v = dict()
for rok in roky_v:
    set1 = set(burka_vzdialena['ind_kli'].where(burka_vzdialena['rok'] == rok))
    set2 = [x for x in set1 if x == x]  # remove NaN
    pocet_stanic_rok_v[rok] = len(set2)

pocet_burok_rok_v = np.divide(pocet_burok_rok_v, np.array(list(pocet_stanic_rok_v.values())))

pocet_burok_roky_b = dict(Counter(blyskavica['rok'].values))
roky_b, pocet_burok_rok_b = np.array(list(pocet_burok_roky_b.keys())), np.array(list(pocet_burok_roky_b.values()))
roky_b.sort()

roky_b_new = []
pocet_burok_rok_b_new = []
for i in range(len(roky_b)):
    if roky_b[i] in range(1981, 2011):
        roky_b_new.append(roky_b[i])
        pocet_burok_rok_b_new.append(pocet_burok_rok_b[i])

roky_b, pocet_burok_rok_b = roky_b_new, pocet_burok_rok_b_new

pocet_stanic_rok_b = dict()
for rok in roky_b:
    set1 = set(blyskavica['ind_kli'].where(blyskavica['rok'] == rok))
    set2 = [x for x in set1 if x == x]  # remove NaN
    pocet_stanic_rok_b[rok] = len(set2)

pocet_burok_rok_b = np.divide(pocet_burok_rok_b, np.array(list(pocet_stanic_rok_b.values())))  # normovanie poctu burok na pocet stanic

plt.style.use(['science', 'notebook', 'grid'])
fig, ax = plt.subplots()

# Lists to keep track of handles and labels for the legends
data_handles = []
data_labels = []
trendline_handles = []
trendline_labels = []

data_all = [pocet_burok_rok_s, pocet_burok_rok_v, pocet_burok_rok_b]
labels = ['búrka na stanici', 'búrka vzdialená', 'blýskavica']
colors = ['k', 'r', 'b']
for i in range(3):
    # Perform linear regression
    x = np.array(roky_s) - 1981
    y = data_all[i]
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    trendline = slope * x + intercept

    # Plot data
    data_label = labels[i]
    data_handle, = ax.plot(roky_s, y, 'o-', markersize=3, lw=1.5, color=colors[i], label=data_label)
    data_handles.append(data_handle)
    data_labels.append(data_label)

    # Plot the trendline
    trendline_label = f'y={slope: .2f}x +{intercept: .1f}, $R^{2}$={r_value ** 2: .2f}'
    trendline_handle, = ax.plot(roky_s, trendline, label=trendline_label, color=colors[i])
    trendline_handles.append(trendline_handle)
    trendline_labels.append(trendline_label)

data_legend = ax.legend(data_handles, data_labels, fontsize=13, edgecolor='k', bbox_to_anchor=(0.62, 0.76))
trendline_legend = ax.legend(trendline_handles, trendline_labels, fontsize=9, edgecolor='k',
                             bbox_to_anchor=(0.62, 0.15))
ax.add_artist(data_legend)
ax.add_artist(trendline_legend)

plt.xlabel('rok')
plt.ylabel('počet búrkových dní')
plt.ylim([1, 20])
# plt.title('Vývoj počtu búrok podľa typov')
# plt.legend(['búrka na stanici', 'búrka vzdialená', 'blýskavica'], loc='best', edgecolor='k', fontsize=10)
# plt.show()

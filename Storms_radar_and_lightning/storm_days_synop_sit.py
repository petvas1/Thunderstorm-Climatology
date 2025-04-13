import numpy as np
import os
import matplotlib.pyplot as plt
import scienceplots

blesky_path = "Blesky_5min_synopt\\"
# years = np.zeros([14])
# burkove_dni = set()
# for root, dirs, files in os.walk(blesky_path):
#     for f in files:
#         day = f[:8]
#         burkove_dni.add(day)

# burkove_dni = list(burkove_dni)

situations_per_year = {'A': 0.3076923076923077, 'Ap1': 1.9230769230769231, 'Ap2': 1.2307692307692308,
                         'Ap3': 0.38461538461538464, 'Ap4': 0.07692307692307693, 'B': 14.307692307692308,
                         'Bp': 13.923076923076923, 'C': 2.5384615384615383, 'Cv': 2.6923076923076925,
                         'Ea': 2.769230769230769, 'Ec': 2.923076923076923, 'NEa': 1.9230769230769231,
                         'NEc': 5.230769230769231, 'NWa': 1.6153846153846154, 'NWc': 3.923076923076923,
                         'Nc': 1.9230769230769231, 'SEa': 1.0769230769230769, 'SEc': 1.7692307692307692,
                         'SWa': 2.923076923076923, 'SWc1': 3.923076923076923, 'SWc2': 3.6153846153846154,
                         'SWc3': 0.46153846153846156, 'Sa': 2.3846153846153846, 'Vfz': 0.6923076923076923,
                         'Wa': 0.6923076923076923, 'Wal': 5.0, 'Wc': 4.846153846153846, 'Wcs': 2.0}

situacie = list(situations_per_year.keys())
situacie_burkove_dni = dict()

for i in range(len(situacie)):
    sit_path = blesky_path + situacie[i]
    burkove_dni = set()
    for root, dirs, files in os.walk(sit_path):
        for f in files:
            day = f[:8]
            burkove_dni.add(day)
    situacie_burkove_dni[situacie[i]] = len(burkove_dni) / 12

print(situacie_burkove_dni)
print(sum(situacie_burkove_dni.values()))

plt.figure(figsize=(10, 5))
plt.bar(situacie, situacie_burkove_dni.values())
plt.xticks(fontsize=6)
plt.xlabel('Synoptická situácia')
plt.ylabel('Počet "bleskových" dní za 1 rok')

# for day in days:
#     year = int(day[:4])
#     years[year-2010] += 1
# months = np.zeros([12])
# for day in burkove_dni:
#     month = int(day[4:6])
#     months[month - 1] += 1
#
# months /= 13
#
# # plt.style.use(['science', 'notebook', 'grid'])
# plt.bar(np.arange(1, 13), months)
# plt.xticks(np.arange(1, 13))

# plt.show()

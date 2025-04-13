import os
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from matplotlib.ticker import StrMethodFormatter
import time
import pandas as pd
from collections import Counter


def main():
    start = time.perf_counter()

    sit = 'SWc3'
    situation_array_dir = f"C:\\Users\\petva\\Desktop\\FMFI UK\\3. rocnik\\bakalarka\\Vysledky_matice\\km_10_dbz_30\\Situacie_matice_13_rokov\\{sit}.txt"
    mapa_sr_kraje = gpd.read_file("C:\\Users\\petva\\Desktop\\FMFI UK\\3. rocnik\\bakalarka\\Mapy krajin\\mapa_sr_kraje.csv")
    with open(situation_array_dir, 'r') as fin:
        grid = np.array([line.split() for line in fin], dtype='float64')

    pocty_situacii_za_rok = {'A': 0.25, 'Ap1': 1.9166666666666667, 'Ap2': 1.1666666666666667, 'Ap3': 0.4166666666666667, 'Ap4': 0.1, 'B': 14.583333333333334, 'Bp': 13.5, 'C': 2.6666666666666665, 'Cv': 2.5833333333333335, 'Ea': 2.5, 'Ec': 2.9166666666666665, 'NEa': 1.9166666666666667, 'NEc': 5.666666666666667, 'NWa': 1.5833333333333333, 'NWc': 4.083333333333333, 'Nc': 2.0833333333333335, 'SEa': 1.1666666666666667, 'SEc': 1.8333333333333333, 'SWa': 3.0, 'SWc1': 4.083333333333333, 'SWc2': 3.5, 'SWc3': 0.5, 'Sa': 2.5, 'Vfz': 0.75, 'Wa': 0.75, 'Wal': 4.666666666666667, 'Wc': 4.666666666666667, 'Wcs': 1.8333333333333333}
    grid *= 60 / pocty_situacii_za_rok[sit]

    # some constants
    y1, y2 = (135, 573)  # coords of rectangle in pixels (columns)
    x1, x2 = (267, 1047)  # coords of rectangle in pixels (rows)
    x_0 = 15.99711894
    y_0 = 49.93
    pixel_x = 0.008977974  # size of pixel in degrees of longitude
    pixel_y = 0.006  # size of pixel in degrees of latitude

    y1 *= 2
    y2 *= 2
    x1 *= 2
    x2 *= 2
    pixel_x /= 2
    pixel_y /= 2

    fig, ax = plt.subplots()
    X, Y = np.meshgrid(np.linspace(x_0, x_0 + (x2 - x1) * pixel_x, x2 - x1),
                       np.linspace(y_0, y_0 - (y2 - y1) * pixel_y, y2 - y1))
    plt.contourf(X, Y, grid, levels=50, cmap='turbo', vmin=0)
    mapa_sr_kraje.plot(ax=ax, color=(0, 0, 0, 0), edgecolor='k')
    cb = plt.colorbar(shrink=0.6, format='%.0f', ticks=np.arange(0, 30, 5))
    cb.set_label('minutes/TD', fontsize=10, rotation='horizontal', labelpad=-10, y=1.1)
    ax.text(0.7, 0.2, f'{sit}', fontsize=10, ha='left', va='top', transform=ax.transAxes, color='white',
            bbox=dict(facecolor='black', edgecolor='black', boxstyle='round,pad=0.1', alpha=0.5))
    plt.xticks([])
    plt.yticks([])
    # cs = plt.contour(X, Y, grid, levels=4, alpha=1, linewidths=0.8)
    # plt.clabel(cs, fontsize=8, colors='k', inline=True)

    # ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
    # ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.1f}°"))
    # plt.show()
    print('time =', time.perf_counter() - start)


if __name__ == '__main__':
    main()

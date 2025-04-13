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

    situations_per_year = {'A': 0.25, 'Ap1': 1.9166666666666667, 'Ap2': 1.1666666666666667, 'Ap3': 0.4166666666666667, 'Ap4': 0.0001, 'B': 14.583333333333334, 'Bp': 13.5, 'C': 2.6666666666666665, 'Cv': 2.5833333333333335, 'Ea': 2.5, 'Ec': 2.9166666666666665, 'NEa': 1.9166666666666667, 'NEc': 5.666666666666667, 'NWa': 1.5833333333333333, 'NWc': 4.083333333333333, 'Nc': 2.0833333333333335, 'SEa': 1.1666666666666667, 'SEc': 1.8333333333333333, 'SWa': 3.0, 'SWc1': 4.083333333333333, 'SWc2': 3.5, 'SWc3': 0.5, 'Sa': 2.5, 'Vfz': 0.75, 'Wa': 0.75, 'Wal': 4.666666666666667, 'Wc': 4.666666666666667, 'Wcs': 1.8333333333333333}

    situations_array_dir = "Situacie_matice_13_rokov\\"
    mapa_sr_kraje = gpd.read_file("mapa_sr_kraje.csv")
    situacie = situations_per_year.keys()

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
    X, Y = np.meshgrid(np.linspace(x_0, x_0 + (x2 - x1) * pixel_x, x2 - x1),
                       np.linspace(y_0, y_0 - (y2 - y1) * pixel_y, y2 - y1))
    fig, axs = plt.subplots(10, 3, figsize=(6, 10))
    fig.delaxes(axs[9, 1])
    fig.delaxes(axs[9, 2])
    for sit, ax in zip(situacie, axs.ravel()):
        sit_path = situations_array_dir + sit + '.txt'
        with open(sit_path, 'r') as fin:
            grid = np.array([line.split() for line in fin], dtype='float64')

        # norm by synoptic situation
        for key, value in situations_per_year.items():
            if key == sit:
                if key == 'Ap4':
                    grid *= 0
                else:
                    grid *= 60 / value  # minutes per 1 day of situation instead of hours per year

        im = ax.contourf(X, Y, grid, levels=50, cmap='turbo', vmin=0, vmax=25)  # pre dbz 50 vmax=3
        if sit == 'Cv':  # pre dbz 50 'B'
            image = im
        mapa_sr_kraje.plot(ax=ax, color=(0, 0, 0, 0), edgecolor='white', lw=0.5)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(0.7, 0.2, f'{sit}', fontsize=10, ha='left', va='top', transform=ax.transAxes, color='white',
                bbox=dict(facecolor='black', edgecolor='black', boxstyle='round,pad=0.1', alpha=0.5))
        # plt.subplots_adjust(wspace=0.01, hspace=0.01)

    cbar_ax = fig.add_axes([0.15, 0.05, 0.65, 0.02])   # Position [left, bottom, width, height]
    cb = fig.colorbar(image, ax=axs[:, -1], cax=cbar_ax, location='bottom', format='%.0f', ticks=np.arange(0, 30, 5))  # pre dbz 50 format='%.1f', ticks=np.arange(0, 5, 0.5)
    cb.set_label('minutes/day', fontsize=12, rotation='horizontal', labelpad=0, y=1)
    plt.subplots_adjust(wspace=0.02, hspace=0.02, right=0.8)
    plt.savefig("image.jpeg", dpi=1000)

    print('time =', time.perf_counter() - start)  # 80 sec
    # plt.show()


if __name__ == '__main__':
    main()

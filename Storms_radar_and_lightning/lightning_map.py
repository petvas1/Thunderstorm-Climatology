import os
import numpy as np
import matplotlib.pyplot as plt
import scienceplots
from matplotlib.ticker import StrMethodFormatter
import geopandas as gpd
from scipy import ndimage



def main():
    blesky_dir_path = "C:\\Users\\petva\\Desktop\\FMFI UK\\3. rocnik\\bakalarka\\Blesky_5min_synopt\\"

    x_borders = [16, 23]
    y_borders = [47.3, 49.9]
    x_length_km = 521  # 1 km step
    y_length_km = 289
    x_length_deg = x_borders[1] - x_borders[0]
    y_length_deg = y_borders[1] - y_borders[0]

    # grid = np.zeros((y_length_km, x_length_km))
    #
    # for root, dirs, files in os.walk(blesky_dir_path):
    #     for f in files:
    #         full_name = os.path.join(root, f)
    #         with open(full_name, 'r') as fin:
    #             for line in fin:
    #                 line = line.split()  # [time, latitude, longitude]
    #                 x = round((float(line[2]) - x_borders[0]) / x_length_deg * x_length_km - 1)
    #                 y = round((float(line[1]) - y_borders[0]) / y_length_deg * y_length_km - 1)
    #                 grid[y, x] += 1
    #
    # grid /= 13
    # grid /= 25
    # np.savetxt("grid_blesky.txt", grid)


    grid = np.loadtxt("grid_blesky.txt")
    grid[grid > 25] = 25
    print(np.mean(grid))
    mapa_sr_kraje = gpd.read_file(
        "C:\\Users\\petva\\Desktop\\FMFI UK\\3. rocnik\\bakalarka\\Mapy krajin\\mapa_sr_kraje.csv")

    fig, ax = plt.subplots()
    X, Y = np.meshgrid(np.linspace(x_borders[0], x_borders[1], x_length_km),
                       np.linspace(y_borders[0], y_borders[1], y_length_km))
    plt.contourf(X, Y, grid, levels=50, cmap='turbo', vmin=0, vmax=25)
    mapa_sr_kraje.plot(ax=ax, color=(0, 0, 0, 0), edgecolor='k')
    cb = plt.colorbar(shrink=0.6, format='%.0f', ticks=np.arange(0, 35, 5))
    cb.set_label(r'flashes $\mathregular{km^{-2}}$ $\mathregular{yr^{-1}}$', fontsize=10, rotation='horizontal', labelpad=-10, y=1.1)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
    ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.1f}°"))
    # plt.show()


if __name__ == '__main__':
    main()

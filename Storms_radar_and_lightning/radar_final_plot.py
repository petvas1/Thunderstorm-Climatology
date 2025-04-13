import os
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from matplotlib.ticker import StrMethodFormatter
from scipy import ndimage


def main():
    synopt_arrays_dir = "C:\\Users\\petva\\Desktop\\FMFI UK\\3. rocnik\\bakalarka\\Vysledky_matice\\km_10_dbz_30\\Situacie_matice_13_rokov"
    mapa_sr_kraje = gpd.read_file("C:\\Users\\petva\\Desktop\\FMFI UK\\3. rocnik\\bakalarka\\Mapy krajin\\mapa_sr_kraje.csv")

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

    # grid = np.loadtxt('grid.txt')
    # grid = ndimage.zoom(grid, 0.1)
    grid = np.zeros((y2 - y1, x2 - x1))

    for root, dirs, files in os.walk(synopt_arrays_dir):
        for f in files:
            fullname = os.path.join(root, f)
            with open(fullname, 'r') as fin:
                grid_file = np.array([line.split() for line in fin], dtype='float64')
                grid += grid_file

    # grid[grid > 2.05] = 2.05  # for 50 dbz
    fig, ax = plt.subplots()
    X, Y = np.meshgrid(np.linspace(x_0, x_0 + (x2 - x1) * pixel_x, x2 - x1),
                       np.linspace(y_0, y_0 - (y2 - y1) * pixel_y, y2 - y1))
    plt.contourf(X, Y, grid, levels=50, cmap='turbo', vmin=0)
    mapa_sr_kraje.plot(ax=ax, color=(0, 0, 0, 0), edgecolor='k')

    cb = plt.colorbar(shrink=0.6, ticks=np.arange(0, 18, 2))  # ticks=np.arange(0, 18, 2) for 30 dbz,  ticks=np.arange(0, 2.5, 0.5) for 50 dbz
    cb.set_label(r'hours $\mathregular{yr^{-1}}$', fontsize=10, rotation='horizontal', labelpad=-10, y=1.1)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
    ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.1f}°"))
    # plt.show()


if __name__ == '__main__':
    main()

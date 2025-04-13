import os
import concurrent.futures
import numpy as np
import skimage.io
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import time
import geopandas as gpd
from scipy import ndimage


def process():
    radar_dir_path = "20230923"

    # go through all radars (files)
    radar_names_old = []  # change of pixels old(1135x780) -> new(2270x1560), last old image 20160812.1215
    radar_names_new = []
    for root, dirs, files in os.walk(radar_dir_path):
        for radar_name in files:
            radar_name_time = radar_name[10:23]
            if float(radar_name_time) <= 20160812.1215:
                radar_names_old.append(radar_name_time)
            else:
                radar_names_new.append(radar_name_time)

    # some constants
    y1, y2 = (135, 573)  # coords of rectangle in pixels (columns)
    x1, x2 = (267, 1047)  # coords of rectangle in pixels (rows)
    x_0 = 15.99711894
    y_0 = 49.93
    pixel_x = 0.008977974  # size of pixel in degrees of longitude
    pixel_y = 0.006  # size of pixel in degrees of latitude

    grid = np.zeros((y2 - y1, x2 - x1))

    def process_image(radar_name_time):
        full_radar_name = f'{radar_dir_path}/data.cmax/cmax.kruh.{radar_name_time}.0.png'
        # read radar data
        image = skimage.io.imread(full_radar_name)
        image = image[y1:y2, x1:x2]

        # go through all pixels from above and check conditions
        rows, cols = np.where(((image[:, :, 0] >= 240) & (image[:, :, 2] <= 120)) |  # 30 <= dbz <= 65
                              ((image[:, :, 0] >= 148) & (image[:, :, 1] < 50)))     # some values in between

        for i in range(len(rows)):  # increase pixel value when conditions are met
            grid[rows[i], cols[i]] += 1

        print(f'image {full_radar_name[-19:-6]} processed')

    for rad in radar_names_old:
        process_image(rad)

    # change of image size
    grid = ndimage.zoom(grid, 2)
    y1 *= 2
    y2 *= 2
    x1 *= 2
    x2 *= 2
    pixel_x /= 2
    pixel_y /= 2

    count = 0
    for rad in radar_names_new:
        process_image(rad)


    mapa_sr_kraje = gpd.read_file("mapa_sr_kraje.csv")
    fig, ax = plt.subplots()
    X, Y = np.meshgrid(np.linspace(x_0, x_0 + (x2 - x1) * pixel_x, x2 - x1),
                       np.linspace(y_0, y_0 - (y2 - y1) * pixel_y, y2 - y1))
    plt.contourf(X, Y, grid, levels=50, cmap='turbo', vmin=0, vmax=np.max(grid))
    mapa_sr_kraje.plot(ax=ax, color=(0, 0, 0, 0), edgecolor='k')
    cb = plt.colorbar(shrink=0.6)
    cb.set_label('hodiny/rok', fontsize=14, rotation='horizontal', labelpad=-10, y=1.1)
    plt.title(f'Radar 2010-2023, dbz >= 30', fontsize=20)
    ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
    ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.1f}°"))


def main():
    start_time = time.perf_counter()
    process()
    print(time.perf_counter() - start_time)
    plt.show()


if __name__ == '__main__':
    main()

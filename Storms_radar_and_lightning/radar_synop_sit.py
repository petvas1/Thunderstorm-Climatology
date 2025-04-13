import os
import concurrent.futures
import numpy as np
import skimage.io
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import time
import geopandas as gpd
from scipy import ndimage


def process_syn_sit(syn_sit):
    start_time = time.perf_counter()

    radar_dir_path = "Radar"
    blesky_dir_path = "Blesky_5min_synopt/" + syn_sit

    # go through all lightnings (files)
    lightning_names_old = []  # change of pixels old(1135x780) -> new(2270x1560), last old image 20160812.1215
    lightning_names_new = []
    for root, dirs, files in os.walk(blesky_dir_path):
        for lightning_name in files:
            full_lightning_name = os.path.join(root, lightning_name)
            if float(lightning_name[:-4]) <= 20160812.1215:
                lightning_names_old.append(full_lightning_name)
            else:
                lightning_names_new.append(full_lightning_name)

    distance_radius = 3  # in km (of storm)
    radius = int(distance_radius * 1.5)  # in pixels

    # some constants
    y1, y2 = (135, 573)  # coords of rectangle in pixels (columns)
    x1, x2 = (267, 1047)  # coords of rectangle in pixels (rows)
    x_0 = 15.99711894
    y_0 = 49.93
    pixel_x = 0.008977974  # size of pixel in degrees of longitude
    pixel_y = 0.006  # size of pixel in degrees of latitude

    grid = np.zeros((y2 - y1, x2 - x1))

    def degrees_to_pixels(y, x):
        y_in_pixels = round((y_0 - y) / pixel_y)
        x_in_pixels = round((x - x_0) / pixel_x)
        return y_in_pixels, x_in_pixels

    def process_image(full_lightning_name):
        # read lightning data
        points_yx = set()  # set of tuples (y, x) - coords of pixel of interest (row, col)
        with open(full_lightning_name) as fin:
            for line in fin:
                line = line.split()  # [time, latitude, longitude]
                center_y, center_x = degrees_to_pixels(float(line[1]), float(line[2]))

                # get pixels around lightnings
                for y_ in range(center_y - radius, center_y + radius + 1):
                    for x_ in range(center_x - radius, center_x + radius + 1):
                        if 0 <= y_ < y2-y1 and 0 <= x_ < x2-x1:  # check if point is within (cropped) image boundaries
                            if (y_ - center_y) ** 2 + (x_ - center_x) ** 2 <= radius ** 2:  # find points inside circle
                                points_yx.add((y_, x_))
        points_yx_list = [elem for elem in points_yx]

        # find corresponding radar image (file)
        radar_image_name = 'cmax.kruh.' + full_lightning_name[-17:-4] + '.0.png'
        full_radar_name = radar_dir_path + '/' + full_lightning_name[-17:-9] + '/data.cmax/' + radar_image_name
        if os.path.isfile(full_radar_name):
            image = skimage.io.imread(full_radar_name)
            image = image[y1:y2, x1:x2]

            # go through all pixels from above and check conditions
            for i in range(len(points_yx_list)):
                row, col = points_yx_list[i]  # unpack coords of pixels
                # check_reflectivity
                if image[row, col][0] >= 240 and image[row, col][2] <= 120:  # 30 <= dbz <= 65
                    grid[row, col] += 1/156  # 5/60/12 -> 5 minutes per 60 mins over 12 years = hour/year
                elif image[row, col][0] >= 148 and image[row, col][1] < 50:  # some values in between
                    grid[row, col] += 1/156

        # print(f'image {radar_image_name} processed', syn_sit)

    for light in lightning_names_old:
        process_image(light)

    # change of image size
    grid = ndimage.zoom(grid, 2)
    y1 *= 2
    y2 *= 2
    x1 *= 2
    x2 *= 2
    radius = int(distance_radius * 3)
    pixel_x /= 2
    pixel_y /= 2

    for light in lightning_names_new:
        process_image(light)

    print(f'time({syn_sit}) =', time.perf_counter() - start_time)

    # mapa_sr_kraje = gpd.read_file("mapa_sr_kraje.csv")
    # fig, ax = plt.subplots()
    # X, Y = np.meshgrid(np.linspace(x_0, x_0 + (x2 - x1) * pixel_x, x2 - x1),
    #                    np.linspace(y_0, y_0 - (y2 - y1) * pixel_y, y2 - y1))
    # plt.contourf(X, Y, grid, levels=50, cmap='turbo', vmin=0, vmax=np.max(grid))
    # mapa_sr_kraje.plot(ax=ax, color=(0, 0, 0, 0), edgecolor='k')
    # cb = plt.colorbar(shrink=0.6)
    # cb.set_label('hodiny/rok', fontsize=14, rotation='horizontal', labelpad=-10, y=1.1)
    # plt.title(f'Situácia {syn_sit}', fontsize=20)
    # ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
    # ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.1f}°"))
    # plt.savefig(f"Vysledky/{syn_sit}.png", dpi=400)
    # plt.show()
    np.savetxt(f"Vysledky/Np_arrays/{syn_sit}.txt", grid)


def main():
    synopt_root_path = "Blesky_5min_synopt"
    situacie = []
    for root, dirs, files in os.walk(synopt_root_path):
        for dir_ in dirs:
            situacie.append(dir_)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(process_syn_sit, situacie)


if __name__ == '__main__':
    main()

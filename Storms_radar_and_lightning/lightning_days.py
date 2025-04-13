import os
import numpy as np
import matplotlib.pyplot as plt
import scienceplots
from matplotlib.ticker import StrMethodFormatter
import geopandas as gpd
from scipy import ndimage
from collections import defaultdict


def main():
    blesky_dir_path = "Blesky_5min_synopt\\"
    blesky_dni_dir_path = "Blesky_dni\\"
################ create files of lightning days ############
    # def merge_files_by_date(input_dir, output_dir):
    #     # Create the output directory if it doesn't exist
    #     if not os.path.exists(output_dir):
    #         os.makedirs(output_dir)
    #
    #     # Dictionary to hold lists of file contents by filename prefix
    #     files_content = defaultdict(list)
    #
    #     # Scan the input directory for all files
    #     for root, dirs, files in os.walk(blesky_dir_path):
    #         for filename in files:
    #             # Extract the first 8 digits (date part) of the filename
    #             date_part = filename[:8]
    #             file_path = os.path.join(root, filename)
    #             with open(file_path, 'r') as file:
    #                 content = file.read()
    #                 files_content[date_part].append(content)
    #
    #     # Write merged contents to new files in the output directory
    #     for date_part, contents in files_content.items():
    #         output_filename = f"{date_part}.txt"
    #         output_path = os.path.join(output_dir, output_filename)
    #         with open(output_path, 'w') as output_file:
    #             for content in contents:
    #                 output_file.write(content)
    #
    # input_directory = blesky_dir_path
    # output_directory = blesky_dni_dir_path
    # merge_files_by_date(input_directory, output_directory)
#####################################
######### lightning days ###############
    x_borders = [16, 23]
    y_borders = [47.3, 49.9]
    x_length_km = 104   # 5 km step
    y_length_km = 58
    x_length_deg = x_borders[1] - x_borders[0]
    y_length_deg = y_borders[1] - y_borders[0]

    grid = np.zeros((y_length_km, x_length_km))   # 5x5 km

    for root, dirs, files in os.walk(blesky_dni_dir_path):
        for f in files:
            full_name = os.path.join(root, f)
            points_yx = set()  # set of tuples (y, x) - coords of pixel of interest (row, col)
            with open(full_name, 'r') as fin:
                for line in fin:
                    line = line.split()  # [time, latitude, longitude]
                    x = round((float(line[2]) - x_borders[0]) / x_length_deg * x_length_km - 1)
                    y = round((float(line[1]) - y_borders[0]) / y_length_deg * y_length_km - 1)
                    points_yx.add((y, x))

            for y, x in points_yx:
                grid[y, x] += 1

    grid /= 13  # norm to 1 year

    fig, ax = plt.subplots()
    X, Y = np.meshgrid(np.linspace(x_borders[0], x_borders[1], x_length_km),
                       np.linspace(y_borders[0], y_borders[1], y_length_km))
    plt.contourf(X, Y, grid, levels=10, cmap='turbo', vmin=0)
    mapa_sr_kraje.plot(ax=ax, color=(0, 0, 0, 0), edgecolor='k')
    cb = plt.colorbar(shrink=0.6, format='%.0f')  # ticks=np.arange(0, 30, 5)
    cb.set_label(r'TDs $\mathregular{yr^{-1}}$', fontsize=10, rotation='horizontal', labelpad=-10, y=1.1)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
    ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.1f}°"))
    # plt.show()


if __name__ == '__main__':
    main()

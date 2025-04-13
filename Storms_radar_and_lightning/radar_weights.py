import os
import concurrent.futures
import numpy as np
import skimage
import matplotlib.pyplot as plt
import time
import geopandas as gpd

old_radar_image = False  # change of pixels old(1135x780) -> new(2270x1560), last old image 20160812.1215

radar_dir_path = "20230923"
blesky_dir_path = "blesky_zoznam_komplet.txt"

distance_radius = 10  # in km (of storm)
radius = distance_radius * 1.5  # in pixels

# some constants
y1, y2 = (135, 573)  # coords of rectangle in pixels (columns)
x1, x2 = (267, 1047)  # coords of rectangle in pixels (rows)
x_0 = 15.99711894
y_0 = 49.93
pixel_x = 0.008977974  # size of pixel in degrees of longitude
pixel_y = 0.006  # size of pixel in degrees of latitude

if not old_radar_image:
    y1 *= 2
    y2 *= 2
    x1 *= 2
    x2 *= 2
    radius *= 2
    pixel_x /= 2
    pixel_y /= 2

radius = int(radius)
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
    # for root_r, dirs_r, files_r in os.walk(radar_dir_path):  # find file in directory
    #     if radar_image_name in files_r:
    #         full_radar_name = os.path.join(root_r, radar_image_name)
    full_radar_name = radar_dir_path + '/data.cmax/' + radar_image_name
    image = skimage.io.imread(full_radar_name)
    image = image[y1:y2, x1:x2]

    for i in range(len(points_yx_list)):
        row, col = points_yx_list[i]  # unpack coords of pixels
        # check_reflectivity
        if image[row, col][0] >= 240 and image[row, col][2] <= 120:  # 30 <= dbz <= 65
            grid[row, col] += 1
        elif image[row, col][0] >= 148 and image[row, col][1] < 50:  # some values in between
            grid[row, col] += 1

    # print(f'image {radar_image_name} processed')


def main():
    start_time = time.perf_counter()

    # go through all lightnings (files)
    lightning_names = []
    for root, dirs, files in os.walk(blesky_dir_path):
        for lightning_name in files:
            full_lightning_name = os.path.join(root, lightning_name)
            lightning_names.append(full_lightning_name)

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.map(process_image, lightning_names)
    for light in lightning_names:
        process_image(light)

    print('time =', time.perf_counter() - start_time)  # 23 sec for entire day

    mapa_sr_kraje = gpd.read_file(mapa_sr_kraje.csv")

    fig, ax = plt.subplots()
    X, Y = np.meshgrid(np.linspace(x_0, x_0 + (x2 - x1) * pixel_x, x2 - x1),
                       np.linspace(y_0, y_0 - (y2 - y1) * pixel_y, y2 - y1))
    plt.contourf(X, Y, grid)
    mapa_sr_kraje.plot(ax=ax, color=(0, 0, 0, 0), edgecolor='k')
    plt.colorbar()
    plt.show()


if __name__ == '__main__':
    main()

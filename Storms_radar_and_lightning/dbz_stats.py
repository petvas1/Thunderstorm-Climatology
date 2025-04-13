import os
import matplotlib.pyplot as plt
import numpy as np
import skimage.io
import time
import scienceplots


def process():
    radar_dir_path = "20230923"
    blesky_dir_path = 'blesky_zoznam_20230923'
    dbz_palette_path = "C:\\Users\\petva\\Desktop\\FMFI UK\\3. rocnik\\bakalarka\\Radary\\dbz_palette.txt"

    # radar_dir_path = "/mnt/Qnas/Vas/Radar"
    # blesky_dir_path = "/home/vas/Blesky_5min"
    # dbz_palette_path = '/mnt/Qnas/Vas/dbz_palette.txt'

    distance_radius = 3  # in km (of storm)
    radius = int(distance_radius * 1.5)  # in pixels

    # some constants
    y1, y2 = (135, 573)  # coords of rectangle in pixels (columns)
    x1, x2 = (267, 1047)  # coords of rectangle in pixels (rows)
    x_0 = 15.99711894
    y_0 = 49.93
    pixel_x = 0.008977974  # size of pixel in degrees of longitude
    pixel_y = 0.006  # size of pixel in degrees of latitude

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

    dbz_values = np.zeros([192], dtype='uint64')  # occurrences of each dbz value

    with open(dbz_palette_path, 'r') as fin:  # columns = (R, G, B)
        dbz_array = np.array([line.split() for line in fin])

    def degrees_to_pixels(y, x):
        y_in_pixels = round((y_0 - y) / pixel_y)
        x_in_pixels = round((x - x_0) / pixel_x)
        return y_in_pixels, x_in_pixels


    def process_image(full_lightning_name):
        # read lightning data
        points_yx = set()  # set of tuples (y, x) - coords of pixel of interest (row, col)
        with open(full_lightning_name) as fin2:
            for line in fin2:
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
        # full_radar_name = radar_dir_path + '/' + full_lightning_name[-17:-9] + '/data.cmax/' + radar_image_name
        full_radar_name = full_lightning_name[-17:-9] + '/data.cmax/' + radar_image_name
        if os.path.isfile(full_radar_name):
            image = skimage.io.imread(full_radar_name)
            image = image[y1:y2, x1:x2]

            # go through all pixels from above and find dbz
            for i in range(len(points_yx_list)):
                row, col = points_yx_list[i]  # unpack coords of pixels
                g = str(image[row, col][1])  # get green value
                indexes = np.where(dbz_array[:, 1] == g)[0]  # find indexes of corresponding dbz values

                if len(indexes) != 0:
                    for index in indexes:  # go through indexes and check red and blue values
                        if dbz_array[index, 0] == str(image[row, col][0]) and dbz_array[index, 2] == str(image[row, col][2]):
                            dbz_values[index] += 1  # increase counter for specific dbz value
        # print(f'image {radar_image_name} processed')

    for light in lightning_names_old:
        process_image(light)

    # change of image size
    y1 *= 2
    y2 *= 2
    x1 *= 2
    x2 *= 2
    radius = int(distance_radius * 3)
    pixel_x /= 2
    pixel_y /= 2

    for light in lightning_names_new:
        process_image(light)

    for i in range(len(dbz_values)):
        if i / 2 in [35, 35.5, 38.5, 39, 50, 50.5, 51.5, 52]:  # remove duplicates
            dbz_values[i] /= 2

    dbz_values_norm = dbz_values / np.sum(dbz_values) * 100

    plt.style.use(['science', 'notebook', 'grid'])
    plt.plot(np.arange(0, 96, 0.5), dbz_values_norm)
    plt.title('Relative dbz count')
    plt.xlim(0, 95.5)
    plt.ylim(0, )

def main():
    start_time = time.perf_counter()
    process()
    print('time = ', time.perf_counter() - start_time)
    plt.show()


if __name__ == '__main__':
    main()

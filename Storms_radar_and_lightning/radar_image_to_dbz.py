import os
import concurrent.futures
import numpy as np
import skimage
import time

old_radar_image = False  # change of pixels old(1135x780) -> new(2270x1560), last old image 20160812.1215
radar_dir_path = ""
dbz_palette_path = ""

# coords of rectangle in pixels
y1, y2 = 135, 573
x1, x2 = 267, 1047

if not old_radar_image:
    y1 *= 2
    y2 *= 2
    x1 *= 2
    x2 *= 2


def image2dbz(radar_image_name):
    with open(dbz_palette_path, 'r') as fin:  # columns = (dbz, R, G, B)
        dbz_values = np.array([line.split() for line in fin])

        dbz_array = np.zeros((y2 - y1, x2 - x1))
        image = skimage.io.imread(radar_image_name)
        image = image[y1:y2, x1:x2]

        for row in range(image.shape[0]):
            for col in range(image.shape[1]):
                r = str(image[row, col][0])  # get red value
                r_index = np.where(dbz_values[:, 0] == r)[0]  # find indexes of corresponding dbz values
                if len(r_index) != 0:
                    for i in r_index:  # go through indexes and find green and blue values
                        if dbz_values[i, 1] == str(image[row, col][1]) and dbz_values[i, 2] == str(image[row, col][2]):
                            dbz_array[row][col] = i  # write to array dbz * 2

        skimage.io.imsave(f'Radar_dbz/{radar_image_name[-19:-6]}.png', dbz_array.astype(np.uint32))
        print(f'{radar_image_name[-19:-6]}.png saved')


def main():
    start_time = time.perf_counter()

    # go through radar images
    radar_image_names = []
    for root, dirs, files in os.walk(radar_dir_path):
        for file_name in files:
            full_name = os.path.join(root, file_name)
            radar_image_names.append(full_name)

    # multiprocessing
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(image2dbz, radar_image_names[:10])

    print(f'time elapsed: {time.perf_counter() - start_time}')


if __name__ == '__main__':
    main()

# show new image
# image = skimage.io.imread('{path}')
# skimage.io.imshow(image)
# plt.show()

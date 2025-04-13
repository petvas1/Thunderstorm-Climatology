import os
import numpy as np
import skimage
import matplotlib.pyplot as plt
import time
import geopandas as gpd

old_radar_image = False  # change of pixels old(1135x780) -> new(2270x1560), last old image 20160812.1215

radar_dir_path = "/mnt/Qnas/Vas/Radar"
blesky_dir_path = "/home/vas/Blesky_5min"

distance_radius = 10  # in km (of storm)
radius = distance_radius * 1.5  # in pixels

y1, y2 = (135, 573)  # coords of rectangle in pixels
x1, x2 = (267, 1047)
x_0 = 15.99711894
y_0 = 49.93
pixel_x = 0.008977974  # size of pixel in degrees of longitude
pixel_y = 0.006  # size of pixel in degrees of latitude
RGB_array = [254, 254, 254, 254]
if not old_radar_image:
    y1 *= 2
    y2 *= 2
    x1 *= 2
    x2 *= 2
    radius *= 2
    pixel_x /= 2
    pixel_y /= 2
    # RGB_array = [254, 254, 254]


def degrees_to_pixels(y, x):
    x_in_pixels = round((x - x_0) / pixel_x)
    y_in_pixels = round((y_0 - y) / pixel_y)
    return x_in_pixels, y_in_pixels


start_time = time.time()
grid = np.zeros((y2-y1, x2-x1))
# i = 0

# go through all lightnings (files)
for root, dirs, files in os.walk(blesky_dir_path):
    for lightning_name in files:
        if lightning_name[:8] == '20230923':
            full_lightning_name = os.path.join(root, lightning_name)

            # find corresponding radar image (file)
            radar_image_name = 'cmax.kruh.' + lightning_name[:-4] + '.0.png'
            for root_r, dirs_r, files_r in os.walk(radar_dir_path):  # find file in directory
                if radar_image_name in files_r:
                    full_radar_name = os.path.join(root_r, radar_image_name)
                    image = skimage.io.imread(full_radar_name)
                    image = image[y1:y2, x1:x2]
                    im_shape = image.shape

                    # read lightning data
                    with open(full_lightning_name) as fin:
                        for line in fin:
                            line = line.split()  # [time, latitude, longitude]
                            center_x, center_y = degrees_to_pixels(float(line[1]), float(line[2]))

                            # go through radar image and mark points where storm occurred
                            for col in range(im_shape[0]):
                                for row in range(im_shape[1]):
                                    if (col - center_y)**2 + (row - center_x)**2 <= radius**2:  # find points inside circle
                                        # check_reflectivity
                                        if image[col][row][0] >= 240 and image[col][row][2] <= 120:  # 30 <= dbz <= 65
                                            image[col][row] = RGB_array
                                        elif image[col][row][0] >= 148 and image[col][row][1] < 50:  # some values in between
                                            image[col][row] = RGB_array

                    # go through radar image again, find marked points and increase value of the grid
                    for col in range(im_shape[0]):
                        for row in range(im_shape[1]):
                            if image[col][row][0] == RGB_array[0] == image[col][row][1] == image[col][row][2]:
                                grid[col][row] += 1
            # i += 1
            # if i == 1:
            #     break

print('time =', time.time() - start_time)  # 1620 sec for entire day

mapa_sr_kraje = gpd.read_file("/mnt/Qnas/Vas/Mapy_krajin/mapa_sr_kraje.csv")

fig, ax = plt.subplots()
X, Y = np.meshgrid(np.linspace(x_0, x_0 + (x2-x1)*pixel_x, x2-x1), np.linspace(y_0, y_0 - (y2-y1)*pixel_y, y2-y1))
plt.contourf(X, Y, grid)
mapa_sr_kraje.plot(ax=ax, color=(0, 0, 0, 0), edgecolor='k')
plt.colorbar()
# skimage.io.imsave('image2.png', image)
plt.savefig('image.png')
plt.show()

import matplotlib.pyplot as plt
import numpy as np
import skimage.io

old_radar_image = False  # change of pixels old(1135x780) -> new(2270x1560), last old image 20160812.1215

radar_image_path = "20230923/data.cmax/cmax.kruh.20230923.1930.0.png"
blesky_path = 'blesky_zoznam_20230923/20230923.1930.txt'

y1, y2 = (135, 573)
x1, x2 = (267, 1047)
distance_radius = 10  # in km (of storm)
radius = int(distance_radius * 3)  # in pixels
pixel_x = 0.008977974
pixel_y = 0.006
if not old_radar_image:
    y1 *= 2
    y2 *= 2
    x1 *= 2
    x2 *= 2
    pixel_x /= 2
    pixel_y /= 2


def degrees_to_pixels(y, x):
    x_0 = 15.99711894
    y_0 = 49.93
    x_in_pixels = round((x - x_0) / pixel_x)
    y_in_pixels = round((y_0 - y) / pixel_y)
    return x_in_pixels, y_in_pixels


x_all = []
y_all = []

# read lightning data
points_yx = set()  # set of tuples (y, x) - coords of pixel of interest (row, col)
with open(blesky_path) as fin:
    for line in fin:
        line_split = line.split()
        center_x, center_y = degrees_to_pixels(float(line_split[1]), float(line_split[2]))
        x_all.append(center_x)
        y_all.append(center_y)

        # get pixels around lightnings
        for y_ in range(center_y - radius, center_y + radius + 1):
            for x_ in range(center_x - radius, center_x + radius + 1):
                if 0 <= y_ < y2 - y1 and 0 <= x_ < x2 - x1:  # check if point is within (cropped) image boundaries
                    if (y_ - center_y) ** 2 + (x_ - center_x) ** 2 <= radius ** 2:  # find points inside circle
                        points_yx.add((y_, x_))
points_yx_list = [elem for elem in points_yx]

image = skimage.io.imread(radar_image_path)
image = image[y1:y2, x1:x2]
plt.plot(x_all, y_all, '+', markersize=5, color='black')

theta = np.linspace(0, 2 * np.pi, 1000)
for i in range(len(x_all)):
    x_circle = radius * np.cos(theta) + x_all[i]
    y_circle = radius * np.sin(theta) + y_all[i]
    plt.plot(x_circle, y_circle, '-', color='w', markersize=0.3)

plt.imshow(image)
plt.show()
plt.close()

for i in range(len(points_yx_list)):
    row, col = points_yx_list[i]  # unpack coords of pixels
    # check_reflectivity
    if image[row, col][0] >= 240 and image[row, col][2] <= 120:  # 30 <= dbz <= 65
        image[row, col] = [255, 255, 255]
    elif image[row, col][0] >= 148 and image[row, col][1] < 50:  # some values in between
        image[row, col] = [255, 255, 255]
    else:
        image[row, col] = [0, 0, 0]

for row in range(image.shape[0]):
    for col in range(image.shape[1]):
        if image[row, col][0] != 255 and image[row, col][1] != 255:
            image[row, col] = [0, 0, 0]

# image = image[200:860, 1200:1560]
plt.imshow(image)
plt.show()

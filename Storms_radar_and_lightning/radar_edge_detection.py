import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import skimage.io
from skimage.filters import sobel, roberts, prewitt, laplace
from shapely.geometry import Polygon

# finding edges
# image_path = 'cmax.kruh.20130510.1830.0.png'
# image = skimage.io.imread(image_path, as_gray=True)
# im_shape = image.shape
# # im_2D = np.zeros((im_shape[0], im_shape[1]))
# # for col in range(im_shape[0]):
# #     for row in range(im_shape[1]):
# #         image[col][row] = [255, 255, 255, 255]
#
# rows = []
# cols = []
# edges = np.array(sobel(image))
# # print(edges.shape)
# # edges = edges[edges > 0.2]
# for col in range(edges.shape[0]):
#     for row in range(edges.shape[1]):
#         if edges[col][row] > 0.3:
#             rows.append(row)
#             cols.append(col)
#
# plt.plot(rows, cols, 'o', markersize=0.4)
# # plt.imshow(edges)
# plt.show()




# image = Image.open(image_path)
# print(image.tobitmap())
# image = plt.imread(image_path)
# plt.imshow(image)
# plt.show()
# im_shape = image.shape
# plt.subplot(1, 2, 1)
# plt.xticks([])
# plt.yticks([])
# plt.imshow(image)
# for col in range(im_shape[0]):
#     for row in range(im_shape[1]):
#         if image[col][row][0] < 0.7:
#             image[col][row] = [1, 1, 1, 1]
#         elif image[col][row][0] > 0.5 and image[col][row][1] > 0.5 and image[col][row][2] > 0.5:
#             image[col][row] = [1, 1, 1, 1]
#         # elif image[col][row][0] < 0.1 and image[col][row][1] < 0.1 and image[col][row][2] < 0.1:
#         #     image[col][row] = [0, 0, 0, 1]
#
# plt.subplot(1, 2, 2)
# plt.xticks([])
# plt.yticks([])
# plt.imshow(image)
# plt.show()

image_path = 'cmax.kruh.20200601.0035.0.png'
image = plt.imread(image_path)

im_shape = image.shape
print(im_shape)

fig, ax = plt.subplots()

theta = np.linspace(0, 2 * np.pi, 1000)
radius = 9
x = radius * np.cos(theta) + 1285
y = radius * np.sin(theta) + 505

ax.plot(x, y)
plt.imshow(image)
plt.show()

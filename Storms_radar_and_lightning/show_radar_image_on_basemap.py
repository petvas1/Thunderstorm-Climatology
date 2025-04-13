import skimage
import matplotlib.pyplot as plt
import geopandas as gpd


image = skimage.io.imread("cmax.kruh.20130510.1830.0.png")

# some constants
y1, y2 = (135, 573)  # coords of rectangle in pixels (columns)
x1, x2 = (267, 1047)  # coords of rectangle in pixels (rows)
x_0 = 15.99711894
y_0 = 49.93
pixel_x = 0.008977974  # size of pixel in degrees of longitude
pixel_y = 0.006  # size of pixel in degrees of latitude

image = image[y1:y2, x1:x2]
image_borders = [x_0, x_0 + (x2 - x1) * pixel_x, y_0 - (y2 - y1) * pixel_y, y_0]

map_path = "C:\\Users\\petva\\Desktop\\FMFI UK\\3. rocnik\\bakalarka\\Mapy krajin\\mapa_sr_kraje.csv"
mapa_sr_kraje = gpd.read_file(map_path)
fig, ax = plt.subplots()
mapa_sr_kraje.plot(ax=ax, color=(0, 0, 0, 0), edgecolor='k')
ax.imshow(image, extent=image_borders)
plt.gca().set_aspect(pixel_x / pixel_y)
plt.title('20130623.0225')
plt.show()

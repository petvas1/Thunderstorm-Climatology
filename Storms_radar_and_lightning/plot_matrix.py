import matplotlib.pyplot as plt
import numpy as np
import skimage.io
from matplotlib.ticker import StrMethodFormatter
import geopandas as gpd
from scipy import ndimage
import os
import earthpy.plot as ep
import rioxarray as rxr


file_name_old = "C:\\Users\\petva\\Desktop\\FMFI UK\\3. rocnik\\bakalarka\\Vysledky_matice\\radar_dbz_30_old.txt"
file_name_new = "C:\\Users\\petva\\Desktop\\FMFI UK\\3. rocnik\\bakalarka\\Vysledky_matice\\radar_dbz_30_new.txt"
with open(file_name_old, 'r') as fin:
    grid_old = np.array([line.split() for line in fin], dtype=np.int64)
with open(file_name_new, 'r') as fin:
    grid_new = np.array([line.split() for line in fin], dtype=np.int64)

grid_old = ndimage.zoom(grid_old, 2)
grid = grid_new + grid_old

y1, y2 = (135, 573)  # coords of rectangle in pixels (columns)
x1, x2 = (267, 1047)  # coords of rectangle in pixels (rows)
x_0 = 15.99711894
y_0 = 49.93
pixel_x = 0.008977974  # size of pixel in degrees of longitude
pixel_y = 0.006  # size of pixel in degrees of latitude
y1 *= 2
y2 *= 2
x1 *= 2
x2 *= 2
pixel_x /= 2
pixel_y /= 2


mapa_sr_kraje = gpd.read_file("C:\\Users\\petva\\Desktop\\FMFI UK\\3. rocnik\\bakalarka\\Mapy krajin\\mapa_sr_kraje.csv")
fig, ax = plt.subplots()

# file_path = "C:\\Users\\petva\\Desktop\\FMFI UK\\3. rocnik\\GIS\\Uloha4\\Hillshade_SR.tif"
# hillshade = rxr.open_rasterio(file_path, masked=True)
# ep.plot_bands(hillshade, cmap='Greys', alpha=1, ax=ax, cbar=False, extent=[16.8, 22.5, 47.7, 49.7])

X, Y = np.meshgrid(np.linspace(x_0, x_0 + (x2 - x1) * pixel_x, x2 - x1),
                   np.linspace(y_0, y_0 - (y2 - y1) * pixel_y, y2 - y1))
plt.contourf(X, Y, grid, alpha=0.5, levels=50, cmap='turbo', vmin=0, vmax=20000)
mapa_sr_kraje.plot(ax=ax, color=(0, 0, 0, 0), edgecolor='k')
cb = plt.colorbar(shrink=0.6)
cb.set_label('hodiny/rok', fontsize=14, rotation='horizontal', labelpad=-10, y=1.1)
plt.title(f'Radar 2010-2023, dbz >= 30', fontsize=20)
ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.1f}°"))
plt.savefig('Radary_ciste_30dbz.png', dpi=300)
plt.show()


# radary_path = "C:\\MOJE\\Radary"
#
# for root, dirs, files in os.walk(radary_path):
#     for f in files:
#         new_name = f[-19:-6]
#         full_name = os.path.join(root, f)
#         new_full_name = os.path.join(root, new_name)
#         os.rename(full_name, new_full_name + ".png")

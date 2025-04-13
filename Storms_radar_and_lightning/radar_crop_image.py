import os
import skimage
import concurrent.futures


# crop image
# y1, y2 = (270, 1146)
# x1, x2 = (534, 2094)
#
# for root, dirs, files in os.walk('20230923'):  # find file in directory
#     for f in files:
#         fullname = os.path.join(root, f)
#         image = skimage.io.imread(fullname)
#         image_cropped = image[y1:y2, x1:x2]
#         skimage.io.imsave(fullname, image_cropped)

def remove_dbz(image_file_name):
    image = skimage.io.imread(image_file_name)
    im_shape = image.shape
    for col in range(im_shape[0]):
        for row in range(im_shape[1]):
            if image[col][row][0] >= 240 and image[col][row][2] <= 120:  # 30 <= dbz <= 65
                pass
            elif image[col][row][0] >= 148 and image[col][row][1] < 50:  # some values in between
                pass
            else:
                image[col][row] = [0, 0, 0]

    skimage.io.imsave(image_file_name, image)
    print(f'{image_file_name} saved')


def main():
    radar_path = '20230923'
    radarnames = []
    for root, dirs, files in os.walk(radar_path):  # find file in directory
        for f in files:
            fullname = os.path.join(root, f)
            radarnames.append(fullname)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(remove_dbz, radarnames)


if __name__ == '__main__':
    main()

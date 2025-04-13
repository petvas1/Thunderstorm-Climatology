import os
import datetime


# # remove empty files
# for root, dirs, files in os.walk('linet 2016 sk'):
#     for f in files:
#         fullname = os.path.join(root, f)
#         if os.path.getsize(fullname) == 0:
#             os.remove(fullname)

# write contents from every file to 1 file
blesky_path = "C:\\Users\\petva\\Desktop\\FMFI UK\\3. rocnik\\bakalarka\\Radary\\Blesky sample\\20230923"
blesky_total_file = 'blesky_zoznam_komplet.txt'

# with open(blesky_total_file, 'w') as file_w:
#     for root, dirs, files in os.walk(blesky_path):
#         for f in files:
#             fullname = os.path.join(root, f)
#             with open(fullname, 'r') as file_r:
#                 contents = file_r.read()
#             file_w.write(contents)


def convert_to_datetime(time_string):  # round time
    datetime_object = datetime.datetime.strptime(time_string, '%Y%m%d %H:%M:%S.%f')  # returns in default format
    datetime_object += datetime.timedelta(minutes=2.5)
    datetime_object -= datetime.timedelta(minutes=datetime_object.minute % 5,
                                          seconds=datetime_object.second,
                                          microseconds=datetime_object.microsecond)
    time_string = datetime_object.strftime('%Y%m%d.%H%M')
    return time_string


# make directory of files - each file every 5 min (except non data)
with open(blesky_total_file, 'r') as fin:
    dir_name = 'blesky_zoznam_20230923'
    os.mkdir(dir_name)

    for line in fin:
        # if line[:8].isdigit():
        #     if '20:24:01.3032043' in line:
        #         continue
        line = line.split()
        line[0] = line[0] + ' ' + line[1][:-1]  # create readable datetime string
        del line[1]
        line[0] = convert_to_datetime(line[0])

        if (47.3 <= float(line[1]) <= 49.9) and (16 <= float(line[2]) <= 23):  # rectangle
            file_path = os.path.join(dir_name, line[0] + '.txt')
            with open(file_path, 'a') as fout:
                fout.write(' '.join(line[:3]) + '\n')

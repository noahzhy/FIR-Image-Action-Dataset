######################
# Recording the data #
######################
import picamera
import picamera.array
import time, datetime
import board, busio
import numpy as np
import pandas as pd
import adafruit_mlx90640

from IPython import display
from subprocess import call
from matplotlib import pyplot as plt

# 01-15
indoor_scene = '01'
# natural, light, dark
lighting = 'light'
# none
heat_source = 'none'

# init the i2c and mlx90640
i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ

# init csv file
file_create_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
file_header = ['Time', 'RT'] + ['P{:03d}'.format(i) for i in range(768)]
csv_file_name = "{}_mlx90640_{}_{}_{}.csv".format(file_create_time, indoor_scene, lighting, heat_source)

# init dataframe header
# df = pd.DataFrame(columns=file_header)
# df.to_csv(csv_file_name, index=False, header=file_header)

frame = np.zeros(768)

camera = picamera.PiCamera()
camera.resolution = (320, 240)
camera.framerate = 24
camera.vflip = True

camera.start_recording('{}.h264'.format(file_create_time))

_start = time.time()
data = list()

try:
    while True:
        try:

            local_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2]
            _start = time.time()
            mlx.getFrame(frame)

        except ValueError as e:
            print('ValueError', e)
            continue

        res = np.around(frame, 2).tolist()
        data.append([local_time, 0] + res)

        print(1 / (time.time() - _start))

except KeyboardInterrupt as e:
    print('KeyboardInterrupt', e)
    df = pd.DataFrame(data, columns=file_header)
    df.to_csv(csv_file_name, mode='a', index=False, header=file_header)
    camera.stop_recording()
    camera.close()

convert = "MP4Box -add {}.h264 {}.mp4".format(file_create_time, file_create_time) # defining convert
call ([convert], shell=True) # executing convert using call
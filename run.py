######################
# Recording the data #
######################
import picamera
import picamera.array
import time, datetime
import board, busio
import numpy as np
import pandas as pd
import cv2
import adafruit_mlx90640
import Adafruit_DHT

from IPython import display
from subprocess import call
from matplotlib import pyplot as plt

# 01-15
indoor_scene = '03'
# natural, light, dark
lighting = 'light'
# none
heat_source = 'none'

# init the i2c and mlx90640
i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ
sensor = Adafruit_DHT.DHT22
gpio = 17
_start = time.time()

frame = np.zeros(768)

zero = time.time()
data = list()

start_rec = False

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

def get_temperature(gpio=17):
    try:
        _, temperature = Adafruit_DHT.read_retry(sensor, gpio)
    except Exception as e:
        return 0
    return round(temperature, 2)

def data_to_frame(data):
    data = np.array(data).reshape((24,32))
    out_data = None
    out_data = cv2.normalize(data, out_data, 0, 255, cv2.NORM_MINMAX)
    img_gray = (out_data).astype('uint8')
    heatmap_g = img_gray.astype('uint8')
    frame = cv2.applyColorMap(heatmap_g, cv2.COLORMAP_JET)
    frame = cv2.resize(frame, (320, 240), interpolation = cv2.INTER_AREA)
    return frame

try:
    while True:
        keep_time = time.time() - zero
        
        try:
            local_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2]
            _start = time.time()
            mlx.getFrame(frame)
        except ValueError as e:
            print('ValueError', e)
            continue
        _, c_frame = camera.read()
        c_frame = cv2.flip(c_frame, 0)
        if start_rec == True:
            out.write(c_frame)
            res = np.around(frame, 2).tolist()
            data.append([local_time, 0] + res)
        cv2.imshow("mlx", data_to_frame(frame))
        cv2.imshow("camera", c_frame)
        key = cv2.waitKey(1)
        if key != -1:
            print(key)
        if key & 0xFF == ord('s') and start_rec == False:
            # init csv file
            file_create_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            file_header = ['Time', 'RT'] + ['P{:03d}'.format(i) for i in range(768)]
            base_file_name = "{}_mlx90640_{}_{}_{}".format(file_create_time, indoor_scene, lighting, heat_source)
            csv_file_name = "{}.csv".format(base_file_name)
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter("{}.mp4".format(base_file_name), fourcc, 8, (320, 240))
            
            start_rec = True
        elif key & 0xFF == ord('e') and start_rec == True:
            df = pd.DataFrame(data, columns=file_header)
            df.to_csv(csv_file_name, mode='a', index=False, header=file_header)
            out.release()
            data = list()
            start_rec = False

except KeyboardInterrupt as e:
    print('KeyboardInterrupt', e)


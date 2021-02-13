import os
import glob
# from cv2 import *
from numpy import array, reshape, where, mean
from pandas import read_csv
import cv2

file_path = "data/20200626_155021_mlx90640_01_light_none.csv"
frame_pos = 400


def data_to_frame(data):
    out_data = None
    out_data = cv2.normalize(data, out_data, 0, 255, cv2.NORM_MINMAX)
    frame = (out_data).astype('uint8')
    cnts, hierarchy = cv2.findContours(
        frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)  # COLORMAP_JET

    cnt = max(cnts, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cnt)
    if w * h > 16:
        x, y, w, h = center_point(x, y, w, h)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)  # blue

    return frame


def center_point(x, y, w, h):
    x0 = x + w/2
    y0 = y + h/2
    xl = x0 - 8
    yl = y0 - 8
    return int(xl), int(yl), 16, 16


data = read_csv(file_path, index_col=False).iloc[:, 2:]
data = data[frame_pos:frame_pos+1].values
_mean = mean(data)
# _max = max(data)
# print(_mean, _max)
data = where(data > _mean*1.05, data, 0)

data = array(data).reshape((24, 32))
frame = data_to_frame(data)
frame = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_NEAREST)
cv2.imshow("view", frame)
cv2.waitKey(0)

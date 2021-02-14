import os
import glob
# from cv2 import *
from numpy import array, reshape, where, mean, argmax
from pandas import read_csv
import cv2


file_path = "data/20200626_154313_mlx90640_01_light_none.csv"
frame_pos = 305
frame_pos = 560
frame_pos = 0

file_path = "data/20200626_160219_mlx90640_01_light_none.csv"
frame_pos = 920


def data_to_frame(data):
    out_data = None
    out_data = cv2.normalize(data, out_data, 0, 255, cv2.NORM_MINMAX)
    frame = (out_data).astype('uint8')

    frame = cv2.blur(frame, (2,2))
    m = argmax(out_data)
    x0, y0 = divmod(m, out_data.shape[1])
    print(x0, y0)

    cnts, hierarchy = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)  # COLORMAP_JET
    frame = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_NEAREST)

    if cnts:
        cnt = max(cnts, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cnt)
        if in_it(x0, y0, x, y, w, h):
            print(cv2.contourArea(cnt))
            if cv2.contourArea(cnt) >= 2:
                x, y, w, h = center_point(x, y, w, h)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame


def in_it(x0, y0, x, y, w, h) -> bool:
    if (x0>x and x0<x+w) and (y0>y and y0<y+h):
        return True
    return True


def center_point(x, y, w, h):
    x0 = x + w/2
    y0 = y + h/2
    xl = x0 - 8
    yl = y0 - 8
    return int(xl)*10, int(yl)*10, 16*10, 16*10


data = read_csv(file_path, index_col=False).iloc[:, 2:]
data = data[frame_pos:frame_pos+1].values
_mean = mean(data)
# data = where(data > _mean*1.041, data, 0)

data = array(data).reshape((24, 32))
frame = data_to_frame(data)
cv2.imshow("view", frame)
cv2.waitKey(0)

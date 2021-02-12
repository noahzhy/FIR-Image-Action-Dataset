import os
import glob
from cv2 import *
from numpy import array, cumsum, insert, mean, ndarray, reshape, sort, sqrt, where
from pandas import read_csv

file_path = "data/20200626_155021_mlx90640_01_light_none.csv"
frame_pos = 400

def data_to_frame(data):
    out_data = None
    out_data = normalize(data, out_data, 0, 255, NORM_MINMAX)
    img_gray = (out_data).astype('uint8')
    heatmap_g = img_gray.astype('uint8')
    frame = applyColorMap(heatmap_g, COLORMAP_JET) # COLORMAP_JET
    return frame

data = read_csv(file_path, index_col=None).iloc[:, 2:]
data = data[frame_pos:frame_pos+1]
data = array(data).reshape((24, 32))
frame = data_to_frame(data)
frame = resize(frame, (320, 240), interpolation=INTER_NEAREST)
imshow("view", frame)
waitKey(0)

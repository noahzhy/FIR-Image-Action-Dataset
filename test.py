import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize


raw_data = np.loadtxt("test_data.csv", delimiter=',')
raw_data = np.resize(raw_data, (24,32))
v = raw_data
raw_data = (v - v.min()) / (v.max() - v.min())
plt.imshow(raw_data, cmap='jet')
plt.colorbar(shrink=0.8)
plt.show()
# print(raw_data)
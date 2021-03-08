import pandas as pd
import numpy as np
import glob
import os
import csv


# df = pd.read_csv("labels/labels.csv", error_bad_lines=False)
# print(df)

rows = list()

with open("labels/labels.csv", "r", encoding = "utf-8") as f:
    reader = csv.reader(f)
    rows = [row[:-1] for row in reader]

print(rows)
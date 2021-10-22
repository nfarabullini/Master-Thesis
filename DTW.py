import numpy as np
import pandas as pd
import os
import json
import warnings
import math
warnings.filterwarnings('ignore')
from metrics_msproject import compute_angle_vector

def dtw(s, t):
    # number of columns in each df, corresponding to number of frames
    n, m = len(s.columns), len(t.columns)
    dtw_matrix = np.zeros((n + 1, m + 1))
    for i in range(n + 1):
        for j in range(m + 1):
            dtw_matrix[i, j] = np.inf
    dtw_matrix[0, 0] = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            sum_entries = 0
            # multi-dimensional case
            for k in range(0, len(s[i - 1]) - 1):
                if not (math.isnan((s[i - 1][k] - t[j - 1][k]))):
                    sum_entries += (s[i - 1][k] - t[j - 1][k])
                else:
                    continue
            cost = abs(sum_entries)
            # take last min from a square box
            last_min = np.min([dtw_matrix[i - 1, j], dtw_matrix[i, j - 1], dtw_matrix[i - 1, j - 1]])
            dtw_matrix[i, j] = cost + last_min
    return dtw_matrix[n, m]

path = "./files_keyframes"
files_AR = []

# extract json files corresponding to videos
n = 0
m = 0
files_ls = [[] for i in range(0, 85)]

# group files belonging to each video in a different sublist, combine all sublist into one list
for file in sorted(os.listdir(path)):
    file_name_new = str(file)
    if m == 0:
        files_ls[n].append(file)
        files_AR.append(file)
        m = m + 1
    elif file_name_new[0] == file_name[0] and file_name_new[1] == file_name[1] and \
            file_name_new[2] == file_name[2] and file_name_new[3] == file_name[3] and file_name_new[4] == file_name[4]\
            and file_name_new[5] == file_name[5]:
        files_ls[n].append(file)
    else:
        n = n + 1
        files_ls[n].append(file)
    file_name = str(file)

# compute angle vectors for first video, it will be treated as the query
newDF_AR = pd.DataFrame(index=range(29))
i = 0
for data in files_ls[0]:
    f = open(os.path.join(path, data), 'r')
    data = json.load(f)
    bodyvector1 = compute_angle_vector(data)
    new_bodyvector = pd.DataFrame(bodyvector1)

    newDF_AR[i] = new_bodyvector
    i += 1
    f.close()

# loop over all other videos to be compared with query
for g in range(0, 85):
    i = 0
    # entries in this list are empty
    if g == 81 or g == 82 or g == 83 or g == 84 or g == 85:
        continue
    newDF = pd.DataFrame(index=range(29))
    # compute angle vectors of each candidate video
    for data in files_ls[g]:
        f = open(os.path.join(path, data), 'r')
        d = json.load(f)
        if g == 36 and i == 62:
            continue
        bodyvector1 = compute_angle_vector(d)
        new_bodyvector = pd.DataFrame(bodyvector1)

        newDF[i] = new_bodyvector
        i += 1
        f.close()
    # compute DTW similarity
    print(dtw(newDF, newDF_AR))


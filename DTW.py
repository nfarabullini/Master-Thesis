from common_funs import dtw_steps, compute_df_query, compute_files_ls, compute_query_ls

import numpy as np
import pandas as pd
import os
import json
import warnings
import math
import time
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
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
    # divide by length of DTW path, aka the number of steps
    n_steps = dtw_steps(dtw_matrix, n, m)
    dtw_final = dtw_matrix[n, m]/n_steps
    return dtw_final

start = time.time()

path = "./files_keyframes"
files_AR = []

# extract json files corresponding to videos
# group files belonging to each video in a different sublist, combine all sublist into one list
files_ls = compute_files_ls(path)
files_AR = compute_query_ls(path)

# compute angle vectors for first video, it will be treated as the query
newDF_AR = compute_df_query(path, files_ls)

dtw_sim_ls = []
dtw_sim_labels = []
dtw_sim_labels_ls = []
# loop over all other videos to be compared with query
for g in range(0, 85):
    i = 0
    # entries in this list are empty
    if g == 36 or g == 81 or g == 82 or g == 83 or g == 84 or g == 85:
        continue
    newDF = pd.DataFrame(index=range(29))
    # compute angle vectors of each candidate video
    for data in files_ls[g]:
        f = open(os.path.join(path, data), 'r')
        d = json.load(f)
        bodyvector1 = compute_angle_vector(d)
        new_bodyvector = pd.DataFrame(bodyvector1)

        newDF[i] = new_bodyvector
        i += 1
        f.close()
    # compute DTW similarity
    dtw_sim = dtw(newDF, newDF_AR)
    print(g)
    dtw_sim_labels_ls.append([dtw_sim, files_ls[g][0]])
    dtw_sim_ls.append(dtw_sim)
    dtw_sim_labels.append(files_ls[g][0])

# sort array wrt to sim measure, very inefficient method, but just needed to get an overview of results
dtw_sim_sorted = sorted(dtw_sim_labels_ls, key=lambda x: x[0])
print(dtw_sim_sorted)
file2 = open("DTW_ED.txt","w")
file2.writelines(str(dtw_sim_sorted))
file2.close()

# create dendrogram
Z = linkage(np.reshape(dtw_sim_ls, (len(dtw_sim_ls), 1)), 'single')
plt.figure()
dn = dendrogram(Z, labels=dtw_sim_labels)
plt.savefig('./Dendrograms/DTW_dendro.png', format='png', bbox_inches='tight')

# print time for simulation
end = time.time()
print(end - start)
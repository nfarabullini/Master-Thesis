from common_funs import compute_df_query, compute_files_ls, compute_query_ls

import os
import time
import json
import pandas as pd
import numpy as np
import math
import warnings
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
#from settings import DATA_PATH
from metrics_msproject import compute_angle_vector as compute_angle_vector_new
from sklearn.metrics.pairwise import cosine_similarity
#from tslearn.metrics import dtw_path
warnings.filterwarnings('ignore')

def dtw_path(s, t):
    # number of columns in each df, corresponding to number of frames
    n, m = len(s.columns), len(t.columns)
    dtw_path_ls = []
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
            if last_min == dtw_matrix[i - 1, j - 1]:
                dtw_path_ls.append([i - 1, j - 1])
            elif last_min == dtw_matrix[i - 1, j]:
                dtw_path_ls.append([i - 1, j])
            elif last_min == dtw_matrix[i, j - 1]:
                dtw_path_ls.append([i, j - 1])
            dtw_matrix[i, j] = cost + last_min
    dtw_path_ls = [[n - 1, m - 1]]
    i = n - 1
    j = m - 1
    while i > 0 and j > 0:
        if i == 0:
            j = j - 1
        elif j == 0:
            i = i - 1
        else:
            if dtw_matrix[i - 1, j] == min(dtw_matrix[i - 1, j - 1], dtw_matrix[i - 1, j],
                                                 dtw_matrix[i, j - 1]):
                i = i - 1
            elif dtw_matrix[i, j - 1] == min(dtw_matrix[i - 1, j - 1], dtw_matrix[i - 1, j],
                                                   dtw_matrix[i, j - 1]):
                j = j - 1
            else:
                i = i - 1
                j = j - 1
        dtw_path_ls.append([i, j])
    return dtw_path_ls

start = time.time()
path = "./files_keyframes"

# extract json files corresponding to videos
# group files belonging to each video in a different sublist, combine all sublist into one list
files_ls = compute_files_ls(path)
files_AR = compute_query_ls(path)

# compute angle vectors for first video, it will be treated as the query
newDF_AR = compute_df_query(path, files_ls)

dtw_sim_labels_ls = []
dtw_sim_ls = []
dtw_sim_labels = []
for g in range(0, 85):
    i = 0
    if g == 36 or g == 81 or g == 82 or g == 83 or g == 84 or g == 85:
        continue
    newDF = pd.DataFrame(index=range(29))
    for data in files_ls[g]:
        f = open(os.path.join("./files_keyframes", data), 'r')
        d = json.load(f)
        bodyvector1 = compute_angle_vector_new(d)
        new_bodyvector = pd.DataFrame(bodyvector1)

        newDF[i] = new_bodyvector
        i += 1
        f.close()
    # compute similarity
    similar_num = 0
    cos_vector = np.array([])
    #path = dtw_path(newDF_AR.T, newDF.T)[0]
    path = dtw_path(newDF_AR, newDF)
    # reverse order of array such that it is ascending
    path = path[::-1]
    path_dict = dict()
    for f1, f2 in path:
        path_dict.setdefault(f1, []).append(f2)
    i = 0
    for i, j in path:
        skip_it = False
        for k in range(0, len(newDF_AR[i])):
            if str(newDF_AR[i][k]) == "nan":
                skip_it = True
        for k in range(0, len(newDF[j])):
            if str(newDF[j][k]) == "nan":
                skip_it = True
        if skip_it:
            continue
        a = cosine_similarity(newDF_AR[i].values.reshape(1, -1), newDF[j].values.reshape(1, -1))
        if a != (np.array([0])):
            cos_vector = np.append(cos_vector, a)
    similar_num = round(np.mean(cos_vector), 3)
    print(g)
    dtw_sim_labels_ls.append([similar_num, files_ls[g][0]])
    if str(similar_num) != "nan":
        dtw_sim_ls.append(similar_num)
        dtw_sim_labels.append(files_ls[g][0])

# end time for simulation
end = time.time()

# create dendrogram
Z = linkage(np.reshape(dtw_sim_ls, (len(dtw_sim_ls), 1)), 'single')
plt.figure()
dn = dendrogram(Z, labels=dtw_sim_labels)
plt.savefig('./Dendrograms/cosSim_dendro.png', format='png', bbox_inches='tight')

# sort array wrt to sim measure, very inefficient method, but just needed to get an overview of results
dtw_sorted = sorted(dtw_sim_labels_ls, key=lambda x: x[0], reverse=True)
print(dtw_sorted)
file3 = open("cosSim.txt","w")
txt_time = "time taken for simulation " + str(end - start)
file3.writelines(str(dtw_sorted) + txt_time)
file3.close()


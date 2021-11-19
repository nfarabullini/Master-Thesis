from common_funs import dtw_steps, compute_df_query, compute_files_ls

import numpy as np
import pandas as pd
import os
import json
import warnings
import math
import time
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')
from metrics_msproject import compute_angle_vector

def dtw_cosSim(s, t):
    # number of columns in each df, corresponding to number of frames
    n, m = len(s.columns), len(t.columns)
    dtw_matrix = np.zeros((n + 1, m + 1))
    for i in range(n + 1):
        for j in range(m + 1):
            dtw_matrix[i, j] = np.inf
    dtw_matrix[0, 0] = 0
    vec_vals = [0] * (m + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s_squared_sum = 0
            t_squared_sum = 0
            sum_entries = 0
            count = 0
            # multi-dimensional case
            for k in range(0, len(s[i - 1])):
                if not (math.isnan((s[i - 1][k] * t[j - 1][k]))):
                    sum_entries += (s[i - 1][k] * t[j - 1][k])
                    s_squared_sum += pow(s[i - 1][k], 2)
                    t_squared_sum += pow(t[j - 1][k], 2)
                    count += 1

            if count > 0:
                cost = sum_entries/(math.sqrt(s_squared_sum)*math.sqrt(t_squared_sum))
                # adjust cost with subtracting 1
                cost = 1 - round(cost, 5)
                # take last min from a square box
                last_min = np.min([dtw_matrix[i - 1, j], dtw_matrix[i, j - 1], dtw_matrix[i - 1, j - 1]])
                dtw_matrix[i, j] = cost + last_min
                vec_vals[j] = cost + last_min
            else:
                dtw_matrix[i, j] = vec_vals[j]
    # divide by length of DTW path, aka the number of steps
    n_steps = dtw_steps(dtw_matrix, n, m)
    dtw_final = dtw_matrix[n, m]/n_steps
    return dtw_final

#path = "./files_keyframes"
path = "./files_dances"

#dendro_ls = []
dtw_sim_labels = []
# group files belonging to each video in a different sublist, combine all sublist into one list
files_ls = compute_files_ls(path)
dendro_arr_fill = np.zeros((52, 52))
start = time.time()
for index_query in range(0, 52):
    # compute angle vectors for query video
    newDF_query = compute_df_query(path, files_ls, index_query)

    dtw_sim_labels.append(files_ls[index_query][0][0:10])
    #dtw_sim_ls = []
    #dtw_sim_labels = []
    # loop over all other videos to be compared with query
    for g in range(index_query + 1, 52):
        if index_query == 72:
            continue
        i = 0
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
        # compute DTW cosine similarity
        dtw_sim = dtw_cosSim(newDF, newDF_query)
        #dtw_sim_labels_ls.append([dtw_sim, files_ls[g][0]])
        #dtw_sim_ls.append(dtw_sim)
        #dendro_ls.append(dtw_sim)
        dendro_arr_fill[index_query, g] = dtw_sim
        print(g)
    print(index_query)

    #dendro_ls.append(dtw_sim_ls)

end = time.time()
print(end - start)

dendro_arr_complete = dendro_arr_fill + dendro_arr_fill.T - np.diag(np.diag(dendro_arr_fill))
clustering = AgglomerativeClustering(n_clusters = 9, affinity = 'precomputed', linkage = 'average').fit(dendro_arr_complete)
file1 = open("DTW_cosSim_arr_filtered.txt","w")
txt_time = "time taken for simulation " + str(end - start)
file1.writelines(str(clustering.labels_) + txt_time)
file1.close()

# create dendrogram
files_names = []
for i in range(0, 52):
    cont = False
    for j in range(len(files_ls[i][0])):
        if cont:
           continue
        elif files_ls[i][0][j] == "0":
           files_names.append(files_ls[i][0][0:j])
           cont = True
    if cont:
        continue

#dendro_array = np.array(dendro_ls)
#dists = squareform(dendro_array)
dendro_arr_complete = dendro_arr_fill + dendro_arr_fill.T - np.diag(np.diag(dendro_arr_fill))
dists = squareform(dendro_arr_complete)
Z = linkage(dists, 'average')
plt.figure()
dn = dendrogram(Z, labels = files_names)
plt.savefig('./Dendrograms/DTW_cosSim_dendro_filtered.png', format='png', bbox_inches='tight')

# clustering = AgglomerativeClustering(n_clusters = 20, affinity = 'precomputed', linkage = 'average').fit(dendro_arr_complete)
# cluster_ls = []
# for i in range(len(clustering.labels_)):
#     cluster_ls.append(clustering.labels_[i] + 1)
# print(cluster_ls)

# sort array wrt to sim measure, very inefficient method, but just needed to get an overview of results

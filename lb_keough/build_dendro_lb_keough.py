'''Script to build dendrogram for LB_Keough as a distance measure using values from DTW_lb_N_alg.py'''

from common_funs import compute_df, compute_files_ls
from lb_funs import calc_min_dist_MD, upper_envelope, lower_envelope, construct_lower_MBRs, construct_upper_MBRs

import numpy as np
import pandas as pd
import warnings
import time
import os

from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

path = "./files_dances"
n_videos = 52
n_clusters = 9
N = 15
sakoe_chiba = 3

# group files belonging to each video in a different sublist, combine all sublist into one list
files_ls = compute_files_ls(path)
dendro_arr_fill = np.zeros((n_videos, n_videos))
start = time.time()
for index_query in range(0, n_videos):
    # compute angle vectors for query video
    newDF_query = compute_df(path, files_ls, index_query)

    u = upper_envelope(newDF_query, sakoe_chiba)
    l = lower_envelope(newDF_query, sakoe_chiba)

    Q_u_r = construct_upper_MBRs(u, N)
    Q_l_r = construct_lower_MBRs(l, N)

    # loop over all other videos to be compared with query
    for g in range(index_query + 1, n_videos):
        newDF = compute_df(path, files_ls, g)
        # compute DTW similarity

        T_u_r = construct_upper_MBRs(newDF, N)
        T_l_r = construct_lower_MBRs(newDF, N)
        lb1 = calc_min_dist_MD(T_u_r, T_l_r, Q_u_r, Q_l_r, N)
        dendro_arr_fill[index_query, g] = lb1
    print(index_query)

end = time.time()
print(end - start)

dendro_arr_complete = dendro_arr_fill + dendro_arr_fill.T - np.diag(np.diag(dendro_arr_fill))
pd.DataFrame(dendro_arr_complete).to_csv("LB_sim_arr_horizontal_filtered_csv")
clustering = AgglomerativeClustering(n_clusters = n_clusters, affinity = 'precomputed', linkage = 'average').fit(dendro_arr_complete)
file1 = open("LB_sim_arr_horizontal_filtered.txt", "w")
txt_time = "time taken for simulation " + str(end - start)
file1.writelines(str(clustering.labels_) + txt_time)
file1.close()

# create dendrogram
files_names = []
for i in range(0, n_videos):
    cont = False
    for j in range(len(files_ls[i][0])):
        if cont:
           continue
        if files_ls[i][0][j] == "0":
           files_names.append(files_ls[i][0][0:j])
           cont = True
    if cont:
        continue

dists = squareform(dendro_arr_complete)
Z = linkage(dists, 'average')
plt.figure()
dn = dendrogram(Z, labels = files_names)
os.path.abspath('/Dendrograms/')
plt.savefig('./LB_dendro_horizontal_filtered.png', format='png', bbox_inches='tight')

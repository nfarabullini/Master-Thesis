from common_funs import compute_df_query, compute_files_ls
from lb_funs import calc_min_dist_MD, upper_envelope, lower_envelope, construct_lower_MBRs, construct_upper_MBRs

import numpy as np
import pandas as pd
import os
import json
import warnings
import time
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')
from metrics_msproject import compute_angle_vector

sakoe_chiba = 20
N = 15

path = "./files_dances"
# group files belonging to each video in a different sublist, combine all sublist into one list
files_ls = compute_files_ls(path)
dendro_arr_fill = np.zeros((52, 52))
start = time.time()
for index_query in range(0, 52):
    # compute angle vectors for query video
    newDF_query = compute_df_query(path, files_ls, index_query)

    u = upper_envelope(newDF_query, sakoe_chiba)
    l = lower_envelope(newDF_query, sakoe_chiba)

    Q_u_r = construct_upper_MBRs(u, N)
    Q_l_r = construct_lower_MBRs(l, N)

    # loop over all other videos to be compared with query
    for g in range(index_query + 1, 52):
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
        # compute DTW similarity

        T_u_r = construct_upper_MBRs(newDF, N)
        T_l_r = construct_lower_MBRs(newDF, N)
        lb1 = calc_min_dist_MD(T_u_r, T_l_r, Q_u_r, Q_l_r, N)
        dendro_arr_fill[index_query, g] = lb1
        print(g)
    print(index_query)

end = time.time()
print(end - start)

dendro_arr_complete = dendro_arr_fill + dendro_arr_fill.T - np.diag(np.diag(dendro_arr_fill))
pd.DataFrame(dendro_arr_complete).to_csv("DTW_lb_sim_arr_filtered_csv")
clustering = AgglomerativeClustering(n_clusters = 9, affinity = 'precomputed', linkage = 'average').fit(dendro_arr_complete)
file1 = open("DTW_lb_sim_arr_filtered.txt","w")
txt_time = "time taken for simulation " + str(end - start)
file1.writelines(str(clustering.labels_) + txt_time)
file1.close()

# # create dendrogram
files_names = []
for i in range(0, 52):
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
plt.savefig('./Dendrograms/DTW_lb_dendro_filtered.png', format='png', bbox_inches='tight')
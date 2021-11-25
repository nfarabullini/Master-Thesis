from common_funs import compute_df_query, compute_files_ls, dtw_cosSim_horizontal

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

path = "./files_dances"

#dendro_ls = []
#dtw_sim_labels = []
# group files belonging to each video in a different sublist, combine all sublist into one list
files_ls = compute_files_ls(path)
dendro_arr_fill = np.zeros((52, 52))
start = time.time()
for index_query in range(0, 52):
    # compute angle vectors for query video
    newDF_query = compute_df_query(path, files_ls, index_query)

    #dtw_sim_labels.append(files_ls[index_query][0][0:10])

    #dtw_sim_ls = []
    #dtw_sim_labels = []
    #dtw_sim_labels_ls = []
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
        dtw_sim = dtw_cosSim_horizontal(newDF, newDF_query)
        #dtw_sim_labels_ls.append([dtw_sim, files_ls[g][0]])
        #dtw_sim_ls.append(dtw_sim)
        #dtw_sim_labels.append(files_ls[g])
        dendro_arr_fill[index_query, g] = dtw_sim
        print(g)
    print(index_query)

    #dendro_ls.append(dtw_sim_ls)

end = time.time()
print(end - start)

dendro_arr_complete = dendro_arr_fill + dendro_arr_fill.T - np.diag(np.diag(dendro_arr_fill))
pd.DataFrame(dendro_arr_complete).to_csv("DTW_cosSim_dendro_h_filtered_csv")
clustering = AgglomerativeClustering(n_clusters = 9, affinity = 'precomputed', linkage = 'average').fit(dendro_arr_complete)
file1 = open("DTW_cosSim_dendro_h_filtered_csv.txt","w")
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

#dendro_arr_complete = dendro_arr_fill + dendro_arr_fill.T - np.diag(np.diag(dendro_arr_fill))
#dendro_arr_complete.to_csv("DTW_cosSim_dendro_h_filtered_csv", encoding='utf-8', index=False)
dists = squareform(dendro_arr_complete)
Z = linkage(dists, 'average')
plt.figure()
dn = dendrogram(Z, labels = files_names)
plt.savefig('./Dendrograms/DTW_cosSim_dendro_h_filtered.png', format='png', bbox_inches='tight')

# clustering = AgglomerativeClustering(n_clusters = 20, affinity = 'precomputed', linkage = 'average').fit(dendro_arr_complete)
# cluster_ls = []
# for i in range(len(clustering.labels_)):
#     cluster_ls.append(clustering.labels_[i] + 1)
# print(cluster_ls)

# sort array wrt to sim measure, very inefficient method, but just needed to get an overview of results
# dtw_sim_sorted = sorted(dtw_sim_labels_ls, key=lambda x: x[0])
# print(dtw_sim_sorted)
# file2 = open("DTW.txt","w")
# txt_time = "time taken for simulation " + str(end - start)
# file2.writelines(str(dtw_sim_sorted) + txt_time)
# file2.close()
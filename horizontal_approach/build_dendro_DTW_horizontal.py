from common_funs import compute_df, compute_files_ls, dtw_horizontal

import numpy as np
import pandas as pd
import warnings
import time

from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

path = "../files_dances"
n_videos = 52
n_clusters = 9

# group files belonging to each video in a different sublist, combine all sublist into one list
files_ls = compute_files_ls(path)
dendro_arr_fill = np.zeros((n_videos, n_videos))
start = time.time()
for index_query in range(0, n_videos):
    # compute angle vectors for query video
    newDF_query = compute_df(path, files_ls, index_query)
    # loop over all other videos to be compared with query
    for g in range(index_query + 1, n_videos):
        newDF = compute_df(path, files_ls, g)
        # compute DTW similarity
        dtw_sim = dtw_horizontal(newDF, newDF_query)
        dendro_arr_fill[index_query, g] = dtw_sim
        print(g)
    print(index_query)

end = time.time()
print(end - start)

dendro_arr_complete = dendro_arr_fill + dendro_arr_fill.T - np.diag(np.diag(dendro_arr_fill))
pd.DataFrame(dendro_arr_complete).to_csv("DTW_sim_arr_horizontal_csv")
clustering = AgglomerativeClustering(n_clusters = n_clusters, affinity = 'precomputed', linkage = 'average').fit(dendro_arr_complete)
file1 = open("DTW_sim_arr_horizontal.txt", "w")
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
plt.savefig('Master-Thesis/Dendrograms/DTW_dendro_horizontal.png', format='png', bbox_inches='tight')

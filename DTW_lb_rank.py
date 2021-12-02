from common_funs import compute_df_query, compute_files_ls, dtw_horizontal
from lb_funs import calc_min_dist_MD_filtered, upper_envelope, lower_envelope, construct_lower_MBRs, construct_upper_MBRs

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
th = 30

path = "./files_dances"
# group files belonging to each video in a different sublist, combine all sublist into one list
files_ls = compute_files_ls(path)
dendro_arr_fill = np.zeros((52, 52))
start = time.time()
ls_lb_files = []
index_query = 5

# compute angle vectors for query video
newDF_query = compute_df_query(path, files_ls, index_query)

u = upper_envelope(newDF_query, sakoe_chiba)
l = lower_envelope(newDF_query, sakoe_chiba)

Q_u_r = construct_upper_MBRs(u, N)
Q_l_r = construct_lower_MBRs(l, N)

# loop over all other videos to be compared with query
for g in range(0, 52):
    if g != index_query:
        newDF = compute_df_query(path, files_ls, g)

        T_u_r = construct_upper_MBRs(newDF, N)
        T_l_r = construct_lower_MBRs(newDF, N)

        # compute LB Keough similarity
        lb1 = calc_min_dist_MD_filtered(T_u_r, T_l_r, Q_u_r, Q_l_r, N, th)
        dendro_arr_fill[index_query, g] = lb1
        # Maybe 50 instead of 30
        if lb1 < th:
            ls_lb_files.append([g, newDF, lb1])
        print(g)
#print(index_query)


#Display LB Keough ranking
ls_lb_sorted = sorted(ls_lb_files, key=lambda x: x[2])
for i in range(len(ls_lb_sorted)):
    file_index = ls_lb_sorted[i][0]
    print(files_ls[file_index][0])

#Calculate accurate DTW
actual_dtw_ls = []
for i in range(len(ls_lb_files)):
    newDF = ls_lb_files[i][1]
    actual_dtw = dtw_horizontal(newDF, newDF_query)
    actual_dtw_ls.append([ls_lb_files[i][0], actual_dtw])
    print(i)
actual_dtw_sorted = sorted(actual_dtw_ls, key=lambda x: x[1])

#Display DTW ranking
for i in range(len(actual_dtw_sorted)):
    file_index = actual_dtw_sorted[i][0]
    print(files_ls[file_index][0])
files_ls[index_query][0]



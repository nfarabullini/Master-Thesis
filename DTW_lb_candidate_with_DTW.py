from common_funs import compute_df_query, compute_files_ls, dtw_horizontal
from lb_funs import calc_min_dist_MD_filtered, upper_envelope, lower_envelope, construct_lower_MBRs, construct_upper_MBRs

import numpy as np
import warnings
import time
import math

warnings.filterwarnings('ignore')
# initial values to be set by the user
th = 200
index_query = 5

# start up values for computation
sc_N_comb = []

path = "./files_dances"
start = time.time()
# group files belonging to each video in a different sublist, combine all sublist into one list
files_ls = compute_files_ls(path)
ls_lb_files = []

# compute angle vectors for query video
newDF_query = compute_df_query(path, files_ls, index_query)

u = upper_envelope(newDF_query, 1)
l = lower_envelope(newDF_query, 1)

Q_u_r = construct_upper_MBRs(u, 17)
Q_l_r = construct_lower_MBRs(l, 17)

# loop over all other videos to be compared with query
for g in range(0, 52):
    if g != index_query:
        newDF = compute_df_query(path, files_ls, g)

        T_u_r = construct_upper_MBRs(newDF, 17)
        T_l_r = construct_lower_MBRs(newDF, 17)

        # compute LB Keough similarity
        lb1 = math.floor(calc_min_dist_MD_filtered(T_u_r, T_l_r, Q_u_r, Q_l_r, 17, th))
        if lb1 <= th:
            ls_lb_files.append([g, newDF, lb1])
        print(g)

# Calculate accurate DTW
actual_lb_DTW_ls = []
for i in range(len(ls_lb_files)):
    newDF = ls_lb_files[i][1]

    actual_lb_DTW = dtw_horizontal(newDF, newDF_query)
    if actual_lb_DTW <= th:
        actual_lb_DTW_ls.append([ls_lb_files[i][0], actual_lb_DTW])
    print(i)

end = time.time()
tot_time = end - start

print(actual_lb_DTW_ls, tot_time)



from common_funs import compute_df_query, compute_files_ls, dtw_horizontal
from lb_funs import calc_min_dist_MD_filtered, upper_envelope, lower_envelope, construct_lower_MBRs, construct_upper_MBRs

import numpy as np
import warnings
import time

warnings.filterwarnings('ignore')
# initial values to be set by the user
th = 30
index_query = 5

# start up values for computation
tot_time_current = np.inf
sc_N_comb = []

path = "./files_dances"
for sakoe_chiba in range(1, 21):
    for N in range(1, 21):
        start = time.time()
        # group files belonging to each video in a different sublist, combine all sublist into one list
        files_ls = compute_files_ls(path)
        ls_lb_files = []

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
                if lb1 <= th*N:
                    ls_lb_files.append([g, newDF, lb1])
                print(g)

        # Calculate accurate DTW
        actual_dtw_ls = []
        for i in range(len(ls_lb_files)):
            newDF = ls_lb_files[i][1]
            actual_dtw = dtw_horizontal(newDF, newDF_query)
            if actual_dtw <= th:
                actual_dtw_ls.append([ls_lb_files[i][0], actual_dtw])
            print(i)

        end = time.time()
        tot_time = end - start
        if tot_time < tot_time_current:
            tot_time_current = tot_time
            sc_N_comb = [sakoe_chiba, N]

print(sc_N_comb, tot_time_current)
print(actual_dtw_ls)
# #Display LB Keough ranking
# ls_lb_sorted = sorted(ls_lb_files, key=lambda x: x[2])
# for i in range(len(ls_lb_sorted)):
#     file_index = ls_lb_sorted[i][0]
#     print(files_ls[file_index][0])

#actual_dtw_sorted = sorted(actual_dtw_ls, key=lambda x: x[1])

# #Display DTW ranking
# for i in range(len(actual_dtw_sorted)):
#     file_index = actual_dtw_sorted[i][0]
#     print(files_ls[file_index][0])
# files_ls[index_query][0]



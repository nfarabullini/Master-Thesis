'''Script to find all times for MBRs and Sakoe-Chiba lengths combinations with DTW for query video'''

from common_funs import compute_df, compute_files_ls, dtw_horizontal
from lb_funs import calc_min_dist_MD_filtered, upper_envelope, lower_envelope, construct_lower_MBRs, calc_min_dist_MD_normalized, construct_upper_MBRs

import warnings
import time

warnings.filterwarnings('ignore')
# initial values to be set by the user
th = 200
index_query = 5

path = "../files_dances"
n_videos = 52
N_max = 21
sc_max = 21

# start up values for computation
ls_time = []

for sakoe_chiba in range(1, sc_max):
    for N in range(1, N_max):
        start = time.time()
        # group files belonging to each video in a different sublist, combine all sublist into one list
        files_ls = compute_files_ls(path)
        ls_lb_files = []

        # compute angle vectors for query video
        newDF_query = compute_df(path, files_ls, index_query)

        u = upper_envelope(newDF_query, sakoe_chiba)
        l = lower_envelope(newDF_query, sakoe_chiba)

        Q_u_r = construct_upper_MBRs(u, N)
        Q_l_r = construct_lower_MBRs(l, N)

        # loop over all other videos to be compared with query
        for g in range(0, n_videos):
            if g != index_query:
                newDF = compute_df(path, files_ls, g)

                T_u_r = construct_upper_MBRs(newDF, N)
                T_l_r = construct_lower_MBRs(newDF, N)

                # compute LB Keough distance
                lb1 = calc_min_dist_MD_normalized(T_u_r, T_l_r, Q_u_r, Q_l_r, N)
                #lb1 = calc_min_dist_MD_filtered(T_u_r, T_l_r, Q_u_r, Q_l_r, N, th)
                if lb1 <= th:
                    ls_lb_files.append([g, newDF, lb1])
        print(ls_lb_files)

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
        ls_time.append([[sakoe_chiba, N], tot_time])

file3 = open("DTW_lb_times.txt", "w")
file3.writelines(str(ls_time))
file3.close()




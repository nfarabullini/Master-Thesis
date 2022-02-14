'''Script to find minimum threshold for the candidate set with optimal values for MBRs and Sakoe-Chiba lengths for LB_Keough only given a query'''

from common_funs import compute_df, compute_files_ls
from lb_funs import calc_min_dist_MD_filtered, upper_envelope, lower_envelope, construct_lower_MBRs, calc_min_dist_MD_normalized, construct_upper_MBRs

import numpy as np
import warnings
import time

warnings.filterwarnings('ignore')

# initial values to be set by the user
n_videos = 52
index_query = 5

# start up values for computation
path = "../files_dances"
sakoe_chiba = 19
N = 15
th = 200
# solution set of videos from DTW only
ls_solutions = [18, 20, 21, 26]

th_best = []
current_candidate_length = np.Inf

for th_lb in range(1, th):

    start = time.time()
    # group files belonging to each video in a different sublist, combine all sublist into one list
    files_ls = compute_files_ls(path)
    ls_lb_files = []
    ls_lb_indexes = []

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

            # lb1 = calc_min_dist_MD_filtered(T_u_r, T_l_r, Q_u_r, Q_l_r, N, th)
            if lb1 <= th_lb:
                ls_lb_files.append([g, newDF, lb1])
                ls_lb_indexes.append(g)

    # check that candidate set contains all entries in solutions set
    if len(ls_lb_indexes) >= len(ls_solutions):
        count_correct_entries = 0
        for ind_lb in ls_lb_indexes:
            if ind_lb in ls_solutions:
                count_correct_entries += 1

        if count_correct_entries == len(ls_solutions):
            if len(ls_lb_indexes) < current_candidate_length:
                end = time.time()
                tot_time = end - start
                th_best = [th_lb, tot_time]
                current_candidate_length = len(ls_lb_indexes)
                print(th_best)
                print(ls_lb_indexes)
                break
        else:
            print("Threshold value of " + str(th_lb) + " is too low")
    else:
        print("Threshold value of " + str(th_lb) + " is too low")

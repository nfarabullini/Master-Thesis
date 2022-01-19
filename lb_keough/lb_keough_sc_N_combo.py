from common_funs import compute_df, compute_files_ls
from lb_funs import calc_min_dist_MD, upper_envelope, lower_envelope, construct_lower_MBRs, construct_upper_MBRs, match_clustering_groups

import numpy as np
import warnings
import time
from sklearn.cluster import AgglomerativeClustering
warnings.filterwarnings('ignore')

path = "../files_dances"
n_videos = 52
N_max = 21
sc_max = 21
n_clusters = 9

files_ls = compute_files_ls(path)
highest_n_matches = 0
sc_N_comb = []

for sakoe_chiba in range(1, N_max):
    for N in range(1, sc_max):
        files_ls = compute_files_ls(path)
        ground_truth = [
            ['BS_F_BK_', 'BS_F_LT_', 'BS_F_RT_', 'BS_S_BK_', 'BS_S_FT_', 'BS_S_LT_', 'BS_S_RT_', 'SS_F_BK_', 'SS_F_FT_',
             'SS_F_LT_', 'SS_F_RT_', 'SS_S_BK_', 'SS_S_LT_', 'SS_S_RT_', 'SYN_R_', 'SYN_U_'],
            ['LD_F_dis_', 'LD_F_small_', 'LD_S_dis_', 'LD_S_small_', 'LU_F_dis_', 'LU_S_dis_'],
            ['BJ_FT_', 'SJ_FT_'],
            ['AR_', 'TA_', 'LU_F_big_', 'LU_S_big_'],
            ['BJ_RT_', 'SJ_RT_', 'BJ_LT_', 'SJ_LT_'],
            ['BBS_F_BK_', 'BBS_F_FT_', 'BBS_S_BK_', 'BBS_S_FT_', 'BSS_S_BK_', 'BSS_S_FT_'],
            ['TB_F_FB_', 'TB_S_', 'TB_S_FB_', 'TF_F_', 'TF_S_', 'TL_F_', 'TL_S_', 'TOS_F_', 'TOS_S_', 'TR_F_', 'TR_S_'],
            ['SYN_K_'],
            ['BJ_BK_', 'SJ_BK_']]
        # group files belonging to each video in a different sublist, combine all sublist into one list
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

        dendro_arr_complete = dendro_arr_fill + dendro_arr_fill.T - np.diag(np.diag(dendro_arr_fill))
        clustering = AgglomerativeClustering(n_clusters = n_clusters, affinity = 'precomputed', linkage = 'average').fit(dendro_arr_complete)
        end = time.time()
        tot_time = end - start

        # compare clustering groups with ground truth
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

        number_matches = match_clustering_groups(ground_truth, files_names, clustering.labels_, n_clusters)
        if number_matches > highest_n_matches:
            highest_n_matches = number_matches
            sc_N_comb = [sakoe_chiba, N, number_matches, tot_time]
            tot_time_current = tot_time
        elif number_matches >= highest_n_matches and tot_time < tot_time_current:
            highest_n_matches = number_matches
            sc_N_comb = [sakoe_chiba, N, number_matches, tot_time]
            tot_time_current = tot_time

print(sc_N_comb)
file1 = open("lb_sc_N_combination.txt", "w")
file1.writelines(str(sc_N_comb) + "Total time taken: " + str(tot_time_current))
file1.close()
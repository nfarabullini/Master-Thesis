from common_funs import compute_df, compute_files_ls
from lb_funs import calc_min_dist_MD, upper_envelope, lower_envelope, construct_lower_MBRs, construct_upper_MBRs, match_clustering_groups

import numpy as np
import warnings
import time
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform
from sklearn.cluster import AgglomerativeClustering
warnings.filterwarnings('ignore')

path = "../files_dances"
files_ls = compute_files_ls(path)
n_videos = 15
n_clusters = 4
files_ls = files_ls[0:n_videos]
highest_n_matches = 0
sc_N_comb = []
for sakoe_chiba in range(1, 31):
    for N in range(1, 31):
        files_ls = compute_files_ls(path)
        files_ls = files_ls[0:n_videos]
        ground_truth = [
            ['AR_'],
            ['BBS_F_BK_', 'BBS_F_FT_', 'BBS_S_BK_', 'BBS_S_FT_', 'BSS_S_BK_', 'BSS_S_FT_', 'BS_F_BK_', 'BS_F_LT_',
             'BS_F_RT_', 'BS_S_BK_'],
            ['BJ_BK_', 'BJ_FT_'],
            ['BJ_LT_', 'BJ_RT_']
        ]
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
                #print(g)
            print(index_query)

        dendro_arr_complete = dendro_arr_fill + dendro_arr_fill.T - np.diag(np.diag(dendro_arr_fill))
        # pd.DataFrame(dendro_arr_complete).to_csv("DTW_lb_sim_arr_cut_filtered_csv")
        clustering = AgglomerativeClustering(n_clusters = n_clusters, affinity = 'precomputed', linkage = 'average').fit(dendro_arr_complete)
        # file1 = open("DTW_lb_sim_arr_cut_filtered.txt","w")
        # txt_time = "time taken for simulation " + str(end - start)
        # file1.writelines(str(clustering.labels_) + txt_time)
        # file1.close()
        end = time.time()
        tot_time = end - start

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
        #
        # dists = squareform(dendro_arr_complete)
        # Z = linkage(dists, 'average')
        # plt.figure()
        # dn = dendrogram(Z, labels = files_names)
        # plt.savefig('./Dendrograms/DTW_lb_dendro_cut_filtered.png', format='png', bbox_inches='tight')

        # compare clustering groups with ground truth
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
# file1 = open("DTW_lb_sc_N_combination.txt","w")
# file1.writelines(str(sc_N_comb) + "Total time taken: " + str(tot_time_current))
# file1.close()
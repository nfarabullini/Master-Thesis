from common_funs import compute_files_ls
from lb_funs import match_clustering_groups

path = "./files_dances"
files_ls = compute_files_ls(path)
n_clusters = 9
n_videos = 52

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

clustering_labels = [7, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 3, 5, 4, 6, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
number_matches = match_clustering_groups(ground_truth, files_names, clustering_labels, n_clusters)
print(number_matches)
'''Script to measure time, recall, and precision of candidate sets for different Sakoe-Chiba lengths for LB_Keough for query video'''

from common_funs import compute_df, compute_files_ls, dtw_horizontal
from lb_funs import upper_envelope, lower_envelope, construct_lower_MBRs, calc_min_dist_MD_normalized, construct_upper_MBRs

import warnings
import time
import matplotlib.pyplot as plt
import pandas as pd
warnings.filterwarnings('ignore')

# initial values to be set by the user
th = 200
index_query = 5

path = "./files_dances"
n_videos = 52
N = 15
# solution set of videos from DTW only
ls_solutions = [18, 20, 21, 26]
ls_measurements = []

for sakoe_chiba in range(1, 21):
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
            if lb1 <= th:
                ls_lb_files.append(g)

    end = time.time()
    tot_time = end - start

    # check how many entries of the final set the candidate set has
    TP = 0
    for ind_lb in ls_lb_files:
        if ind_lb in ls_solutions:
            TP += 1
    FP = len(ls_lb_files) - TP

    FN = len(ls_solutions) - TP

    # compute accuracy measures
    recall = TP/(TP+FN)
    precision = TP/(TP+FP)
    f_score = 2*(precision*recall)/(precision+recall)

    ls_measurements.append([sakoe_chiba, recall, precision, f_score, tot_time])

pd_measurements = pd.DataFrame(ls_measurements, columns = ['sakoe_chiba', 'recall', 'precision', 'f_score', 'tot_time'])

# Precision plot
plt.figure()
plt.plot(pd_measurements["sakoe_chiba"], pd_measurements["precision"])
plt.legend()
plt.xlabel('Sakoe-Chiba lengths')
plt.ylabel('Precision')
plt.title("Precision VS Sakoe-Chiba lengths")
plt.savefig('./query_files/plots/precision_VS_sc.png', format='png', bbox_inches='tight')

# Recall plot
plt.figure()
plt.plot(pd_measurements["sakoe_chiba"], pd_measurements["recall"])
plt.legend()
plt.xlabel('Sakoe-Chiba lengths')
plt.ylabel('Recall')
plt.title("Recall VS Sakoe-Chiba lengths")
plt.savefig('./query_files/plots/recall_VS_sc.png', format='png', bbox_inches='tight')

# F-Score plot
plt.figure()
plt.plot(pd_measurements["sakoe_chiba"], pd_measurements["f_score"])
plt.legend()
plt.xlabel('Sakoe-Chiba lengths')
plt.ylabel('F-Score')
plt.title("F-Score VS Sakoe-Chiba lengths")
plt.savefig('./query_files/plots/f_score_VS_sc.png', format='png', bbox_inches='tight')

# Run time plot
plt.figure()
plt.plot(pd_measurements["sakoe_chiba"], pd_measurements["tot_time"])
plt.legend()
plt.xlabel('Sakoe-Chiba lengths')
plt.ylabel('Time (s)')
plt.ylim([0,10])
plt.title("Time VS Sakoe-Chiba lengths")
plt.savefig('./query_files/plots/time_VS_sc.png', format='png', bbox_inches='tight')

plt.show()

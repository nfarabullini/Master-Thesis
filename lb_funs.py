import numpy as np
import pandas as pd
import math

def dist_fun(a, b):
    return pow(a - b, 2)

def calc_min_dist(T_h, T_l, Q_U, Q_L, N):
    lb_cum = 0
    len_d = len(T_h)
    for p in range(len_d):
        d = 0
        if T_l[p] > Q_U[p]:
            d = dist_fun(T_l[p], Q_U[p])
        if T_h[p] < Q_L[p]:
            d = dist_fun(T_h[p], Q_L[p])
        lb_cum += (len_d / N) * d
    return math.sqrt(lb_cum)

def calc_min_dist_MD(T_h, T_l, Q_U, Q_L, N):
    cum_d = 0
    for i in range(len(T_h)):
        cum_d += calc_min_dist(T_h.iloc[i], T_l.iloc[i], Q_U.iloc[i], Q_L.iloc[i], N)
    return cum_d

def calc_min_dist_filtered(T_h, T_l, Q_U, Q_L, N, th):
    lb_cum = 0
    len_d = len(T_h)
    th_2 = pow(th, 2)
    for p in range(len_d):
        d = 0
        if T_l[p] > Q_U[p]:
            d = dist_fun(T_l[p], Q_U[p])
        if T_h[p] < Q_L[p]:
            d = dist_fun(T_h[p], Q_L[p])
        lb_cum += (len_d / N) * d
        if lb_cum > th_2:
            return lb_cum
    return math.sqrt(lb_cum)

def calc_min_dist_MD_filtered(T_h, T_l, Q_U, Q_L, N, th):
    cum_d = 0
    for i in range(len(T_h)):
        if cum_d > th:
            return cum_d
        cum_d += calc_min_dist_filtered(T_h.iloc[i], T_l.iloc[i], Q_U.iloc[i], Q_L.iloc[i], N, th)
    return cum_d

def upper_envelope(series, sakoe_chiba):
    n_s = len(series)
    ls_up = []
    for i in range(n_s):
        series_i = series.iloc[i]
        u_p = []
        for w in range(len(series_i)):
            index_1 = w - sakoe_chiba
            index_2 = w + sakoe_chiba
            if index_1 >= 0 and index_2 < len(series_i):
                arr = []
                for c in range(index_1, index_2):
                    arr.append(series_i[c])
                max_val = max(arr)
                u_p.append(max_val)
            elif index_1 >= 0:
                arr = []
                for c in range(index_1, len(series_i)):
                    arr.append(series_i[c])
                max_val = max(arr)
                u_p.append(max_val)

        # fill in tails of envelope
        for w in range(sakoe_chiba):
            u_p.insert(w, u_p[0])
        ls_up.append(u_p)
    return pd.DataFrame(ls_up)

def lower_envelope(series, sakoe_chiba):
    n_s = len(series)
    ls_lp = []
    for i in range(n_s):
        series_i = series.iloc[i]
        l_p = []
        for w in range(0, len(series_i)):
            index_1 = w - sakoe_chiba
            index_2 = w + sakoe_chiba
            if index_1 >= 0 and index_2 < len(series_i):
                arr = []
                for c in range(index_1, index_2):
                    arr.append(series_i[c])
                min_val = min(arr)
                l_p.append(min_val)
            elif index_1 >= 0:
                arr = []
                for c in range(index_1, len(series_i)):
                    arr.append(series_i[c])
                min_val = min(arr)
                l_p.append(min_val)

        # fill in tails of envelope
        for w in range(0, sakoe_chiba):
            l_p.insert(w, l_p[0])
        ls_lp.append(l_p)
    return pd.DataFrame(ls_lp)

def construct_lower_MBRs(series, N):
    n_s = len(series)
    ls_l_mbr = []
    for i in range(n_s):
        series_i = series.iloc[i]
        n = len(series_i) // N
        entry = 0
        ls_i = []
        for i in range(1, N + 1):
            range_entries = n*i
            ls_j = []
            for j in range(entry, range_entries):
                ls_j.append(series_i[j])
            ls_i.append(ls_j)
            entry = range_entries
        l_a = []
        for w in range(len(ls_i)):
            min_val = min(ls_i[w])
            # for z in range(len(ls_i[w])):
            #     l_a.append(min_val)
            l_a.append(min_val)
        ls_l_mbr.append(l_a)
    return pd.DataFrame(ls_l_mbr)

def construct_upper_MBRs(series, N):
    n_s = len(series)
    ls_u_mbr = []
    for i in range(n_s):
        series_i = series.iloc[i]
        n = len(series_i) // N
        entry = 0
        ls_i = []
        for i in range(1, N + 1):
            range_entries = n*i
            ls_j = []
            for j in range(entry, range_entries):
                ls_j.append(series_i[j])
            ls_i.append(ls_j)
            entry = range_entries
        u_a = []
        for w in range(len(ls_i)):
            max_val = max(ls_i[w])
            # for z in range(len(ls_i[w])):
            #     u_a.append(max_val)
            u_a.append(max_val)
        ls_u_mbr.append(u_a)
    return pd.DataFrame(ls_u_mbr)

def dtw(s, t):
    n, m = len(s), len(t)
    dtw_matrix = np.zeros((n + 1, m + 1))
    for i in range(n + 1):
        for j in range(m + 1):
            dtw_matrix[i, j] = np.inf
    dtw_matrix[0, 0] = 0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = abs(s[i - 1] - t[j - 1])
            # take last min from a square box
            last_min = np.min([dtw_matrix[i - 1, j], dtw_matrix[i, j - 1], dtw_matrix[i - 1, j - 1]])
            dtw_matrix[i, j] = cost + last_min

    return dtw_matrix[n, m]

def FindMaxLength(lst):
    maxList = max(lst, key=len)
    return maxList

def match_clustering_groups(ground_truth, files_names, clustering_labels, n_clusters):
    match = 0
    ls_1 = files_names
    ls_2 = clustering_labels.tolist()
    d_candidate = {'names': ls_1, 'groups': ls_2}
    df_candidate = pd.DataFrame(d_candidate)
    df_c_sorted = df_candidate.sort_values(by=['groups'])

    count = 0
    clustering_groups_sublists = [[] for i in range(0, n_clusters)]
    for i in range(len(df_c_sorted)):
        if i == 0:
            clustering_groups_sublists[count].append(df_c_sorted.names.iloc[0])
        elif df_c_sorted.groups.iloc[i] == df_c_sorted.groups.iloc[i - 1]:
            clustering_groups_sublists[count].append(df_c_sorted.names.iloc[i])
        else:
            count = count + 1
            clustering_groups_sublists[count].append(df_c_sorted.names.iloc[i])
    while len(ground_truth) > 0:
        maxList = FindMaxLength(clustering_groups_sublists)
        # find best match between candidate and ground truth
        n_match = 0
        best_entry = 0
        for j in range(len(ground_truth)):
            best_match_i = sum(el in ground_truth[j] for el in maxList)
            if best_match_i > n_match:
                n_match = best_match_i
                best_entry = j
        match += n_match
        ground_truth.pop(best_entry)
        ind = clustering_groups_sublists.index(maxList)
        clustering_groups_sublists.pop(ind)
    return match

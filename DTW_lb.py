import math
import random
import numpy as np

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

def upper_envelope(series, sakoe_chiba):

    u_p = []
    for w in range(0, len(series)):
        index_1 = w - sakoe_chiba
        index_2 = w + sakoe_chiba
        if index_1 >= 0 and index_2 <= len(series):
            arr = []
            for c in range(index_1, index_2):
                arr.append(series[c])
            max_val = max(arr)
            u_p.append(max_val)
        elif index_1 >= sakoe_chiba:
            arr = []
            for c in range(index_1, len(series)):
                arr.append(series[c])
            max_val = max(arr)
            u_p.append(max_val)

    # fill in tails of envelope
    for w in range(0, sakoe_chiba):
        u_p.insert(w, u_p[0])
    return u_p

def lower_envelope(series, sakoe_chiba):

    l_p = []
    for w in range(0, len(series)):
        index_1 = w - sakoe_chiba
        index_2 = w + sakoe_chiba
        if index_1 >= 0 and index_2 <= len(series):
            arr = []
            for c in range(index_1, index_2):
                arr.append(series[c])
            max_val = min(arr)
            l_p.append(max_val)
        elif index_1 >= sakoe_chiba:
            arr = []
            for c in range(index_1, len(series)):
                arr.append(series[c])
            max_val = min(arr)
            l_p.append(max_val)

    # fill in tails of envelope
    for w in range(0, sakoe_chiba):
        l_p.insert(w, l_p[0])
    return l_p

def construct_lower_MBRs(series, N):
    n = len(series) // N
    entry = 0
    ls_i = []
    for i in range(1, N + 1):
        range_entries = n*i
        ls_j = []
        for j in range(entry, range_entries):
            ls_j.append(series[j])
        ls_i.append(ls_j)
        entry = range_entries
    l_a = []
    for w in range(0, len(ls_i)):
        min_val = min(ls_i[w])
        for z in range(len(ls_i[w])):
            l_a.append(min_val)
    return l_a

def construct_upper_MBRs(series, N):
    n = len(series) // N
    entry = 0
    ls_i = []
    for i in range(1, N + 1):
        range_entries = n*i
        ls_j = []
        for j in range(entry, range_entries):
            ls_j.append(series[j])
        ls_i.append(ls_j)
        entry = range_entries
    u_a = []
    for w in range(0, len(ls_i)):
        max_val = max(ls_i[w])
        for z in range(len(ls_i[w])):
            u_a.append(max_val)
    return u_a

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

sakoe_chiba = 1
N = 12

m = 12
Q = []
T = []
X = []
for i in range(0, m):
    Q.append(random.randint(1, 20))

for i in range(0, m):
    T.append(random.randint(1, 30))

u = upper_envelope(Q, sakoe_chiba)
l = lower_envelope(Q, sakoe_chiba)

T_u_r = construct_upper_MBRs(T, N)
T_l_r = construct_lower_MBRs(T, N)
Q_u_r = construct_upper_MBRs(Q, N)
Q_l_r = construct_lower_MBRs(Q, N)

lb1 = calc_min_dist(T_u_r, T_l_r, Q_u_r, Q_l_r, N)
dtw_d = dtw(T, Q)
print(T)
print(Q)
print(lb1)
print(dtw_d)
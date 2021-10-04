import random
import math
import statistics
import numpy as np
from matplotlib.pyplot import plot, show, grid

def normalize(list):
    mean = statistics.mean(list)
    std = np.std(list)
    for p in range(0, len(list)):
        list[p] = (list[p] - mean)/std
    return list


def dist_fun(a, b):
    return (a - b) ** 2

def upper_envelope(series, sakoe_chiba):

    u_p = []
    arr = []
    for w in range(0, len(series) - 1):
        index_1 = w - sakoe_chiba
        index_2 = w + sakoe_chiba
        if index_1 >= 0 and index_2 <= len(series) - 1:
            for c in range(index_1, index_2):
                arr.append(series[c])
            max_val = np.amax(arr)
        elif index_1 < 0:
            max_val = 0
        u_p.append(max_val)

    # fill initial values for which index_1 would be < 0
    for w in range(0, sakoe_chiba - 1):
        u_p[w] = u_p[sakoe_chiba]
    return u_p

def upper_envelope_paa(series, N):

    dataset_len = len(series)
    paa_env = []
    for w in range(0, N):
        lower = (w - 1) * math.ceil(dataset_len/N)
        upper = math.ceil(dataset_len/N) * w
        l = 0
        for j in range(lower, upper):
            if l < series[j]:
                l = series[j]
        paa_env.append(l)

    return paa_env

def lower_envelope(series, sakoe_chiba):
    l_p = []
    arr = []
    for w in range(0, len(series) - 1):
        index_1 = w - sakoe_chiba
        index_2 = w + sakoe_chiba
        if index_1 >= 0 and index_2 <= len(series) - 1:
            for c in range(index_1, index_2):
                arr.append(series[c])
            min_val = np.amax(arr)
        elif index_1 < 0:
            min_val = 0
        l_p.append(min_val)

    # fill initial values for which index_1 would be < 0
    for w in range(0, sakoe_chiba - 1):
        l_p[w] = l_p[sakoe_chiba]
    return l_p

def lower_envelope_paa(series, N):

    dataset_len = len(series)
    paa_env = []
    for w in range(0, N):
        lower = (w - 1) * math.ceil(dataset_len/N)
        upper = math.ceil(dataset_len/N) * w
        l = 0
        for j in range(lower, upper):
            if l > series[j]:
                l = series[j]
        paa_env.append(l)

    return paa_env

def calc_lb_paa(d_1, d_2, uo, lo, N):
    lb_cum = 0
    len_d = len(d_1)
    for p in range(0, len_d - 1):
        d = 0
        if d_2[p] > uo[p]:
            d = dist_fun(d_2[p], uo[p])
        elif d_1[p] < lo[p]:
            d = dist_fun(d_1[p], lo[p])
        lb_cum += (len_d / N) * d
    return math.sqrt(lb_cum)

#to change: edit code to avoid plagiarism
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

m = 10
Q = []
T = []
X = []
for i in range(0, 2*m):
    Q.append(random.randint(1, 2))

for i in range(0, m):
    T.append(random.randint(1, 2))
    X.append(0)
#Q = [1, 2, 3, 4, 5, 6, 7, 8]
#T = [1, 2, 3, 4, 5, 6, 7, 8]
print(Q)
print(T)

bsf = math.inf
count = 0
#Q = normalize(Q)
nn = 0
m = len(Q)
t = []
q = []
cb = []
sakoe_chiba = 2
u = upper_envelope(Q, sakoe_chiba)
l = lower_envelope(Q, sakoe_chiba)
N = 3
tz = []
var_1 = 0

uo = upper_envelope_paa(u, N)
lo = lower_envelope_paa(l, N)
T_paa_l = lower_envelope_paa(T, N)
T_paa_h = upper_envelope_paa(T, N)

for i in range(0, 2 * m):
    t.append(0)

for l in range(0, len(T) - 1):
        dist = 0
        lb1 = calc_lb_paa(T_paa_l, T_paa_h, uo, lo, 3)
        if lb1 < bsf:
            bsf = lb1
            r = sakoe_chiba
            dist = dtw(T, Q)
            if dist < bsf:
                bsf = dist
                # to change: i is the sequence index looping over many sequences
                #index_of_best_match = i

# plot series for visual comparison
print(bsf)
plot(T)
plot(Q)
grid(True)
show()







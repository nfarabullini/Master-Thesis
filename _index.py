import random
import math
import statistics
import numpy as np
import cmath
from numpy import array, sign, zeros
from scipy.interpolate import interp1d
from matplotlib.pyplot import plot, show, grid

def normalize(list):
    mean = statistics.mean(list)
    std = np.std(list)
    for p in range(0, m):
        list[p] = (list[p] - mean)/std
    return list


def dist_fun(a, b):
    return (a - b) ** 2

def upper_envelope(s, sakoe_chiba):

    #u_p = []
    #for w in range(0, len(series) - 1):
        #    index_1 = w - sakoe_chiba
        #    index_2 = w + sakoe_chiba
        #    max_val = max(series[index_1], series[index_1 + 1])
        #     for c in range(index_1, index_2 - 1):
            #        if max_val < max(series[c], series[c + 1]):
    #    max_val = max(series[c], series[c + 1])
        #    u_p.append(max_val)

    #return u_p

    q_u = zeros(len(s))

    u_x = [0, ]
    u_y = [s[0], ]

    for k in range(1, len(s) - 1):
        if (sign(s[k] - s[k - 1]) == 1) and (sign(s[k] - s[k + 1]) == 1):
            u_x.append(k)
            u_y.append(s[k])

    u_x.append(len(s) - 1)
    u_y.append(s[-1])

    u_p = interp1d(u_x, u_y, kind='cubic', bounds_error=False, fill_value=0.0)

    for k in range(0, len(s)):
        q_u[k] = u_p(k)

    return q_u

def lower_envelope(s, sakoe_chiba):

    #l_p = []
    #for w in range(0, len(series) - 1):
    #    index_1 = w - sakoe_chiba
        #    index_2 = w + sakoe_chiba
        #    min_val = min(series[index_1], series[index_1 + 1])
        #    for c in range(index_1, index_2 - 1):
    #        if min_val > max(series[c], series[c + 1]):
        #            min_val = max(series[c], series[c + 1])
        #    l_p.append(min_val)

    #return l_p

    q_l = zeros(len(s))

    l_x = [0, ]
    l_y = [s[0], ]

    for k in range(1, len(s) - 1):

        if (sign(s[k] - s[k - 1]) == -1) and ((sign(s[k] - s[k + 1])) == -1):
            l_x.append(k)
            l_y.append(s[k])

    l_x.append(len(s) - 1)
    l_y.append(s[-1])

    l_p = interp1d(l_x, l_y, kind='cubic', bounds_error=False, fill_value=0.0)

    for k in range(0, len(s)):
        q_l[k] = l_p(k)

    return q_l

def calc_lb(t, Q, j, m, mu, sigma, bsf):
    x = (t[j] - mu) / sigma
    y = (t[(m - 1 + j)] - mu) / sigma
    lb = dist_fun(x, Q[0]) + dist_fun(y, Q[m - 1])

    if (lb >= bsf):
        return lb

    x1 = (t[(j + 1)] - mu) / sigma
    d = min(dist_fun(x1, Q[0]), dist_fun(x, Q[1]))
    d = min(d, dist_fun(x1, Q[1]))
    lb += d

    if (lb >= bsf):
        return lb

    y1 = (t[m - 2 + j] - mu) / sigma
    d = min(dist_fun(y1, Q[m - 1]), dist_fun(y, Q[m - 2]))
    d = min(d, dist_fun(y1, Q[m - 2]))
    lb += d

    if (lb >= bsf):
        return lb

    x2 = (t[(j + 2)] - mu) / sigma
    d = min(dist_fun(x, Q[2]), dist_fun(x1, Q[2]))
    d = min(d, dist_fun(x2, Q[2]))
    d = min(d, dist_fun(x2, Q[1]))
    d = min(d, dist_fun(x2, Q[0]))
    lb += d

    if (lb >= bsf):
        return lb

    y2 = (t[(m - 3 + j)] - mu) / sigma
    d = min(dist_fun(y, Q[m - 3]), dist_fun(y1, Q[m - 3]))
    d = min(d, dist_fun(y2, Q[m - 3]))
    d = min(d, dist_fun(y2, Q[m - 2]))
    d = min(d, dist_fun(y2, Q[m - 1]))
    lb += d

    return lb

def calc_lb_cum(t, j, m, mu, sigma, bsf, order, uo, lo, cb1):
    lb_cum = 0
    for p in range(0, m - 1):
        if lb_cum < bsf:
            x = (t[(order[p] + j)] - mu) / sigma
            d = 0
            if x > uo[p]:
                d = dist_fun(x, uo[p])
            elif x < lo[p]:
                d = dist_fun(x, lo[p])
            lb_cum += d
            cb1[order[p]] = d
    return lb_cum


def calc_lb_data_cum(m, mu, sigma, bsf, order, u, l, qo, cb2):
    lb_data_cum = 0

    for p in range(0, m - 1):
        if lb_data_cum < bsf:
            uu = (u[order[p]] - mu) / sigma
            ll = (l[order[p]] - mu) / sigma
            d = 0
            if qo[p] > uu:
                d = dist_fun(qo[p], uu)
            elif qo[p] < ll:
                d = dist_fun(qo[p], ll)

            lb_data_cum += d
            cb2[order[p]] = d
    return lb_data_cum


def dtw(tz, Q, cb, m, r, bsf):

# classic DTW algorithm
#     dtw_arr = []
#     for p in range(0, r - 1):
#         for s in range(0, m - 1):
#             dtw_arr[p, s] = math.inf
#     dtw_arr[0, 0] = 0
#     for p in range(1, r - 1):
#         for s in range(1, m - 1):
#             cost = dist(tz[p], Q[s])
#             min_1 = min(dtw_arr[p - 1, s])
#             min_2 = min(dtw_arr[p, s - 1])
#             min_3 = min(dtw_arr[p - 1, s - 1])
#             dtw_arr[p, s] = cost + min(min_1, min_2, min_3)
#     return dtw_arr[p, s]

    cost = []
    cost_prev = []

    for l in range(0, 2 * r + 1):
        cost.append(math.inf)
        cost_prev.append(math.inf)

    for p in range(0, m - 1):
        n_max = max(0, r - p)
        cost_min = math.inf
        lower_bound_h = max(0, p - r)
        upper_bound_h = min(m - 1, p + r)
        for h in range(lower_bound_h, upper_bound_h):
            if p == 0 and h == 0:
                cost[n_max] = dist_fun(tz[0], Q[0])
                cost_min = cost[n_max]
            else:
                y = cost[n_max - 1]
                z = cost_prev[n_max]
                if (n_max + 1) > 2*r:
                    x = math.inf
                else:
                    x = cost_prev[n_max + 1]
                min_1 = min(x, y)
                cost[n_max] = min(min_1, z) + dist_fun(tz[p], Q[h])
                if cost[n_max] < cost_min:
                    cost_min = cost[n_max]
            n_max += 1
        if (p + r) < (m - 1) and (cost_min + cb[p + r + 1]) >= bsf:
            return cost_min + cb[p + r + 1]

        cost_tmp = cost
        cost = cost_prev
        cost_prev = cost_tmp
    n_max -= 1
    final_dtw = cost_prev[n_max]
    return final_dtw


m = 10
Q = []
T = []
X = []
for i in range(0, m):
    Q.append(random.randint(1, 30))

for i in range(0, 2*m):
    T.append(random.randint(1, 30))
    X.append(0)
print(Q)
print(T)

# to change
sakoe_chiba = 0

bsf = math.inf
count = 0
Q = normalize(Q)
ex = 0
ex2 = 0
nn = 0
m = len(Q)
# to change r = Sakoe-Chiba band
r = len(T)
t = []
q = []
cb = []
cb1 = []
cb2 = []
order = []
u = upper_envelope(Q, sakoe_chiba)
l = lower_envelope(Q, sakoe_chiba)
u_buff = upper_envelope(T, sakoe_chiba)
l_buff = lower_envelope(T, sakoe_chiba)
tz = []
var_1 = 0
var_2 = 0
var_3 = 0

for i in range(0, m):
    cb.append(0)
    cb1.append(0)
    cb2.append(0)

# find indexes of sorted values corresponding to positions in original array
indexes_sorted = sorted(range(len(Q)), key=lambda k: Q[k])
order = indexes_sorted
qo = []
uo = []
lo = []
for n in range(0, m -1):
    o = order[n]
    qo.append(Q[o])
    uo.append(u[o])
    lo.append(l[o])

for i in range(0, 2 * m):
    t.append(0)

for l in range(0, len(T) - 1):
    i = count % m
    X[i] = T[l]
    ex += T[l]
    ex2 += T[l]**2
    t[l % m] = T[l]
    t[(l % m) + m] = T[l]
    if l >= m - 1:
        mu = ex/m
        sigma = cmath.sqrt(ex2/m - mu**2)
        if (ex2/m - mu**2) < 0:
            #sigma = cmath.sqrt(ex2 / m - mu ** 2)
            sigma = -sigma.imag
        else:
            sigma = math.sqrt(ex2 / m - mu ** 2)
        j = (l + 1) % m
        I = l - (m - 1)
        dist = 0
        lb = calc_lb(t, Q, j, m, mu, sigma, bsf)
        if lb < bsf:
            lb1 = calc_lb_cum(t, j, m, mu, sigma, bsf, order, uo, lo, cb1)
            if lb1 < bsf:
                for k in range(0, m - 1):
                    tz.append((t[(k + j)] - mu) / sigma)
                    # to change
                    #u_buff + I
                    #l_buff + I
                lb2 = calc_lb_data_cum(m, mu, sigma, bsf, order, u_buff, l_buff, qo, cb2)
                if lb2 < bsf:
                    if lb2 < lb1:
                        cb[m - 1] = cb1[m - 1]
                        k = m - 2
                        for k in range(m - 2, 0, -1):
                            cb[k] = cb[k + 1] + cb1[k]
                    else:
                        cb[m - 1] = cb2[m - 1]
                        for k in range(m - 2, 0, -1):
                            cb[k] = cb[k + 1] + cb2[k]
                    dist = dtw(tz, Q, cb, m, r, bsf)
                    if dist < bsf:
                        bsf = dist
                else:
                    var_3 += 1
            else:
                var_2 += 1
        else:
            var_1 += 1
            ex -= t[j]
            ex2 -= t[j] ** 2
    count += 1

DTW_cals = 100 - (var_1 + var_2 + var_3)/len(T)*100
print(DTW_cals)

# plot series for visual comparison
plot(T)
plot(Q)
grid(True)
show()







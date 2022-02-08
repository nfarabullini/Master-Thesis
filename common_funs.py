from metrics_msproject import compute_angle_vector
import pandas as pd
import os
import math
import numpy as np
import json

#count number of steps in a DTW path
def dtw_steps(dtw_matrix, n, m):
    dtw_path_ls = [[0, 0]]
    i = n - 1
    j = m - 1
    while i > 0 and j > 0:
        if i == 0:
            j = j - 1
        elif j == 0:
            i = i - 1
        else:
            if dtw_matrix[i - 1, j] == min(dtw_matrix[i - 1, j - 1], dtw_matrix[i - 1, j],
                                           dtw_matrix[i, j - 1]):
                i = i - 1
            elif dtw_matrix[i, j - 1] == min(dtw_matrix[i - 1, j - 1], dtw_matrix[i - 1, j],
                                             dtw_matrix[i, j - 1]):
                j = j - 1
            else:
                i = i - 1
                j = j - 1
        dtw_path_ls.append([n - i - 1, m - j - 1])
    return len(dtw_path_ls)

# DTW horizontal function
def dtw_horizontal(s, t):
    n, m = len(s), len(t)
    comp_vals = 0
    for i in range(n):
        dtw_matrix = np.zeros((len(s.iloc[i]) + 1, len(t.iloc[i]) + 1))
        for j in range(len(s.iloc[i]) + 1):
            for k in range(len(t.iloc[i]) + 1):
                dtw_matrix[j, k] = np.inf
        dtw_matrix[0, 0] = 0
        vec_vals = [0] * (len(t.iloc[i]) + 1)
        for j in range(1, len(s.iloc[i]) + 1):
            for k in range(1, len(t.iloc[i]) + 1):
                # multi-dimensional case
                count = 0
                if not (math.isnan((s.iloc[i][j - 1] - t.iloc[i][k - 1]))):
                    diff_entries = abs(s.iloc[i][j - 1] - t.iloc[i][k - 1])
                    count += 1
                if count > 0:
                    cost = diff_entries
                    # take last min from a square box
                    last_min = np.min([dtw_matrix[j - 1, k], dtw_matrix[j, k - 1], dtw_matrix[j - 1, k - 1]])
                    dtw_matrix[j, k] = cost + last_min
                    vec_vals[k] = cost + last_min
                else:
                    dtw_matrix[j, k] = vec_vals[k]
        # divide by length of DTW path, aka the number of steps
        n_steps = dtw_steps(dtw_matrix, len(s.iloc[i]), len(t.iloc[i]))
        dtw_final = dtw_matrix[len(s.iloc[i]), len(t.iloc[i])] / n_steps
        comp_vals += dtw_final
    return comp_vals

# DTW vertical function
def dtw_vertical(s, t):
    # number of columns in each df, corresponding to number of frames
    n, m = len(s.columns), len(t.columns)
    dtw_matrix = np.zeros((n + 1, m + 1))
    vec_vals = [0] * (m + 1)
    for i in range(n + 1):
        for j in range(m + 1):
            dtw_matrix[i, j] = np.inf
    dtw_matrix[0, 0] = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            sum_entries = 0
            # multi-dimensional case
            count = 0
            for k in range(0, len(s[i - 1])):
                if not (math.isnan((s[i - 1][k] - t[j - 1][k]))):
                    sum_entries += pow((s[i - 1][k] - t[j - 1][k]), 2)
                    count += 1
            if count > 0:
                cost = math.sqrt(sum_entries)/count
                # take last min from a square box
                last_min = np.min([dtw_matrix[i - 1, j], dtw_matrix[i, j - 1], dtw_matrix[i - 1, j - 1]])
                dtw_matrix[i, j] = cost + last_min
                vec_vals[j] = cost + last_min
            else:
                dtw_matrix[i, j] = vec_vals[j]

    # divide by length of DTW path, aka the number of steps
    n_steps = dtw_steps(dtw_matrix, n, m)
    dtw_final = dtw_matrix[n, m]/n_steps
    return dtw_final

# vertical DTW cosSim
def dtw_cosSim_vertical(s, t):
    # number of columns in each df, corresponding to number of frames
    n, m = len(s.columns), len(t.columns)
    dtw_matrix = np.zeros((n + 1, m + 1))
    for i in range(n + 1):
        for j in range(m + 1):
            dtw_matrix[i, j] = np.inf
    dtw_matrix[0, 0] = 0
    vec_vals = [0] * (m + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s_squared_sum = 0
            t_squared_sum = 0
            sum_entries = 0
            count = 0
            # multi-dimensional case
            for k in range(0, len(s[i - 1])):
                if not (math.isnan((s[i - 1][k] * t[j - 1][k]))):
                    sum_entries += (s[i - 1][k] * t[j - 1][k])
                    s_squared_sum += pow(s[i - 1][k], 2)
                    t_squared_sum += pow(t[j - 1][k], 2)
                    count += 1

            if count > 0:
                cost = sum_entries/(math.sqrt(s_squared_sum)*math.sqrt(t_squared_sum))
                # adjust cost with subtracting 1
                cost = 1 - round(cost, 5)
                # take last min from a square box
                last_min = np.min([dtw_matrix[i - 1, j], dtw_matrix[i, j - 1], dtw_matrix[i - 1, j - 1]])
                dtw_matrix[i, j] = cost + last_min
                vec_vals[j] = cost + last_min
            else:
                dtw_matrix[i, j] = vec_vals[j]
    # divide by length of DTW path, aka the number of steps
    n_steps = dtw_steps(dtw_matrix, n, m)
    dtw_final = dtw_matrix[n, m]/n_steps
    return dtw_final

# compute df for query
def compute_df(path, files_ls, index):
    newDF_AR = pd.DataFrame(index=range(29))
    i = 0
    for data in files_ls[index]:
        f = open(os.path.join(path, data), 'r')
        data = json.load(f)
        bodyvector1 = compute_angle_vector(data)
        new_bodyvector = pd.DataFrame(bodyvector1)

        newDF_AR[i] = new_bodyvector
        i += 1
        f.close()
    return newDF_AR

# compute files list
def compute_files_ls(path):
    n = 0
    m = 0
    files_ls = [[] for i in range(0, 52)]
    for file in sorted(os.listdir(path))[1:]:
        file_name_new = str(file)
        if m == 0:
            files_ls[n].append(file)
            m = m + 1
        elif file_name_new[0] == file_name[0] and file_name_new[1] == file_name[1] and \
                file_name_new[2] == file_name[2] and file_name_new[3] == file_name[3] and file_name_new[4] == file_name[4] \
                and file_name_new[5] == file_name[5] and file_name_new[6] == file_name[6] and file_name_new[7] == file_name[7]\
                and file_name_new[8] == file_name[8] and file_name_new[9] == file_name[9] and file_name_new[10] == file_name[10]:
            files_ls[n].append(file)
        else:
            n = n + 1
            files_ls[n].append(file)
        file_name = str(file)
    return files_ls

def vector_vertical(s, t, n_frames):
    n_cols, m_cols = len(s.columns), len(t.columns)
    # vectors are of different lengths, take the shortest and loop over values for both videos for that range
    min_cols = min(n_cols, m_cols)
    sim_ls = []
    # general case
    for i in range(min_cols):
        sim = 0
        ls_vec_s = []
        ls_vec_t = []
        if i >= n_frames and i <= (min_cols - n_frames):
            j = i - n_frames
            l = i + n_frames
            for k in range(j, l):
                ls_vec_s.append(s[k])
                ls_vec_t.append(t[k])
            for h in range(len(ls_vec_s)):
                for z in range(len(ls_vec_s[h])):
                    if not (math.isnan(ls_vec_s[h][z] - ls_vec_t[h][z])):
                        sim_tmp = abs(ls_vec_s[h][z] - ls_vec_t[h][z])
                    sim += sim_tmp
        # # corner case 1
        # elif i < 6:
        #     l = i + 6
        #     for k in range(i, l):
        #         ls_vec_s.append(s[k])
        #         ls_vec_t.append(t[k])
        #     for h in range(len(ls_vec_s)):
        #         for z in range(len(ls_vec_s[h])):
        #             if not (math.isnan(ls_vec_s[h][z] - ls_vec_t[h][z])):
        #                 sim_tmp = abs(ls_vec_s[h][z] - ls_vec_t[h][z])
        #             sim += sim_tmp
        # # corner case 2
        # elif i > (min_cols - 6):
        #     j = i - 6
        #     for k in range(j, i):
        #         ls_vec_s.append(s[k])
        #         ls_vec_t.append(t[k])
        #     for h in range(len(ls_vec_s)):
        #         for z in range(len(ls_vec_s[h])):
        #             if not (math.isnan(ls_vec_s[h][z] - ls_vec_t[h][z])):
        #                 sim_tmp = abs(ls_vec_s[h][z] - ls_vec_t[h][z])
        #             sim += sim_tmp
        sim_ls.append(sim)
    sim_final = sum(sim_ls)/min_cols
    return sim_final


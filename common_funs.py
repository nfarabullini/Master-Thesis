from metrics_msproject import compute_angle_vector
import pandas as pd
import os
import json

#count number of steps in a DTW path
def dtw_steps(dtw_matrix, n, m):
    dtw_path_ls = [[n - 1, m - 1]]
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
        dtw_path_ls.append([i, j])
    return len(dtw_path_ls)

# compute df for query
def compute_df_query(path, files_ls):
    newDF_AR = pd.DataFrame(index=range(29))
    i = 0
    for data in files_ls[0]:
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
    files_ls = [[] for i in range(0, 85)]

    for file in sorted(os.listdir(path)):
        file_name_new = str(file)
        if m == 0:
            files_ls[n].append(file)
            #files_AR.append(file)
            m = m + 1
        elif file_name_new[0] == file_name[0] and file_name_new[1] == file_name[1] and \
                file_name_new[2] == file_name[2] and file_name_new[3] == file_name[3] and file_name_new[4] == file_name[4] \
                and file_name_new[5] == file_name[5]:
            files_ls[n].append(file)
        else:
            n = n + 1
            files_ls[n].append(file)
        file_name = str(file)
    return files_ls

# compute file for query (AR, the first file in this case)
def compute_query_ls(path):
    files_AR = []
    file = sorted(os.listdir(path))[0]
    files_AR.append(file)
    return files_AR

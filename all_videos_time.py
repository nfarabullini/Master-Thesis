import os
import time
import json
import pandas as pd
import numpy as np
from settings import DATA_PATH
from metrics.keypoint_frames import compute_angle_vector as compute_angle_vector_new
from sklearn.metrics.pairwise import cosine_similarity
from tslearn.metrics import dtw_path

path = DATA_PATH
files_AR = []
start = time.time()

# extract json files corresponding to videos
n = 0
m = 0
files_ls = [[] for i in range(0, 85)]

for file in sorted(os.listdir(DATA_PATH)):
    file_name_new = str(file)
    if m == 0:
        files_ls[n].append(file)
        files_AR.append(file)
        m = m + 1
    elif file_name_new[0] == file_name[0] and file_name_new[1] == file_name[1] and \
            file_name_new[2] == file_name[2] and file_name_new[3] == file_name[3] and file_name_new[4] == file_name[4]\
            and file_name_new[5] == file_name[5]:
        files_ls[n].append(file)
    else:
        n = n + 1
        files_ls[n].append(file)
    file_name = str(file)

# compute angle vectors for videos with first one as query
newDF_AR = pd.DataFrame(index=range(29))
i = 0
for data in files_ls[0]:
    f = open(os.path.join(DATA_PATH, data), 'r')
    data = json.load(f)
    bodyvector1 = compute_angle_vector_new(data)
    new_bodyvector = pd.DataFrame(bodyvector1)

    newDF_AR[i] = new_bodyvector
    i += 1
    f.close()

for g in range(1, 85):
    i = 0
    if g == 81 or g == 82 or g == 83 or g == 84 or g == 85:
        continue
    newDF = pd.DataFrame(index=range(29))
    for data in files_ls[g]:
        f = open(os.path.join(DATA_PATH, data), 'r')
        d = json.load(f)
        if g == 36 and i == 62:
            continue
        bodyvector1 = compute_angle_vector_new(d)
        new_bodyvector = pd.DataFrame(bodyvector1)

        newDF[i] = new_bodyvector
        i += 1
        f.close()
    # compute similarity
    similar_num = 0
    cos_vector = np.array([])
    path = dtw_path(newDF_AR.T, newDF.T)[0]
    path_dict = dict()
    for f1, f2 in path:
        path_dict.setdefault(f1, []).append(f2)
    i = 0
    for i, j in path:
        skip_it = False
        for k in range(0, len(newDF_AR[i])):
            if str(newDF_AR[i][k]) == "nan":
                skip_it = True
        for k in range(0, len(newDF[j])):
            if str(newDF[j][k]) == "nan":
                skip_it = True
        if skip_it:
            continue
        a = cosine_similarity(newDF_AR[i].values.reshape(1, -1), newDF[j].values.reshape(1, -1))
        if a != (np.array([0])):
            cos_vector = np.append(cos_vector, a)
    similar_num = round(np.mean(cos_vector), 3)

end = time.time()
print(end - start)



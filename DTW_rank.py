from common_funs import compute_df_query, compute_files_ls, dtw_horizontal

import warnings
import time

warnings.filterwarnings('ignore')
# initial values to be set by the user
index_query = 5
th = 200

path = "./files_dances"

start = time.time()
# group files belonging to each video in a different sublist, combine all sublist into one list
files_ls = compute_files_ls(path)
actual_dtw_ls = []

# compute angle vectors for query video
newDF_query = compute_df_query(path, files_ls, index_query)

# loop over all other videos to be compared with query
for g in range(0, 52):
    if g != index_query:
        newDF = compute_df_query(path, files_ls, g)
        actual_dtw = dtw_horizontal(newDF, newDF_query)
        if actual_dtw <= th:
            actual_dtw_ls.append([g, actual_dtw])
        print(g)

end = time.time()
tot_time = end - start
print(actual_dtw_ls, tot_time)



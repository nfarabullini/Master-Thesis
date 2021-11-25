from common_funs import compute_files_ls
import numpy as np

path = "./files_dances"
files_ls = compute_files_ls(path)
ls = []
for i in range(len(files_ls)):
    ls.append(len(files_ls[i]))

print(min(ls))
print(max(ls))
std = np.std(ls)
print(std)

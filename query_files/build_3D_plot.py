import matplotlib.pyplot as plt
import pandas as pd

read_file = pd.read_csv (r'DTW_lb_times - DTW_lb_times.csv')
fig = plt.figure()
ax = plt.axes(projection ='3d')
ax.scatter3D(read_file["Sakoe_Chiba"], read_file["N"], read_file["Time (s)"])
#ax.plot3D(read_file["Sakoe_Chiba"], read_file["N"], read_file["Time (s)"])
#ax.set_title('3D line plot geeks for geeks')
plt.show()

print(read_file)
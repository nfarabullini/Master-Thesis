'''Script to build plots for time measurements from LB_Keough and DTW combination given a query'''

import matplotlib.pyplot as plt
import pandas as pd

# 3D plot
read_file = pd.read_csv (r'DTW_lb_times - DTW_lb_times.csv')
fig = plt.figure()
ax = plt.axes(projection ='3d')
ax.scatter3D(read_file["Sakoe_Chiba"], read_file["N"], read_file["Time (s)"])

# 2D plots
sc_1 = 10
sc_2 = 15
sc_3 = 19
sc_4 = 5
plt.figure()
plt.plot(read_file["N"][read_file["Sakoe_Chiba"].isin([sc_4])], read_file["Time (s)"][read_file['Sakoe_Chiba'].isin([sc_4])], label = "Sakoe-Chiba = 5")
plt.plot(read_file["N"][read_file["Sakoe_Chiba"].isin([sc_1])], read_file["Time (s)"][read_file['Sakoe_Chiba'].isin([sc_1])], label = "Sakoe-Chiba = 10")
plt.plot(read_file["N"][read_file["Sakoe_Chiba"].isin([sc_2])], read_file["Time (s)"][read_file['Sakoe_Chiba'].isin([sc_2])], label = "Sakoe-Chiba = 15")
plt.plot(read_file["N"][read_file["Sakoe_Chiba"].isin([sc_3])], read_file["Time (s)"][read_file['Sakoe_Chiba'].isin([sc_3])], label = "Sakoe-Chiba = 19")
plt.legend()
plt.ylabel('Time (s)')
plt.xlabel('MBRs')
plt.title("Time VS MBRs")

N_1 = 10
N_2 = 15
N_3 = 19
N_4 = 5
plt.figure()
plt.plot(read_file["Sakoe_Chiba"][read_file["N"].isin([N_4])], read_file["Time (s)"][read_file['N'].isin([N_4])], label = "N = 5")
plt.plot(read_file["Sakoe_Chiba"][read_file["N"].isin([N_1])], read_file["Time (s)"][read_file['N'].isin([N_1])], label = "N = 10")
plt.plot(read_file["Sakoe_Chiba"][read_file["N"].isin([N_2])], read_file["Time (s)"][read_file['N'].isin([N_2])], label = "N = 15")
plt.plot(read_file["Sakoe_Chiba"][read_file["N"].isin([N_3])], read_file["Time (s)"][read_file['N'].isin([N_3])], label = "N = 19")
plt.legend()
plt.ylabel('Time (s)')
plt.xlabel('Sakoe-Chiba lengths')
plt.title("Time VS Sakoe-Chiba lengths")
plt.show()

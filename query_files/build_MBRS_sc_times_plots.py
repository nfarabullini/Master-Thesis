'''Script to build plots for time measurements from LB_Keough and DTW combination given a query'''

import matplotlib.pyplot as plt
import pandas as pd

# 3D plot
read_file = pd.read_csv (r'DTW_lb_times.csv')
fig = plt.figure()
ax = plt.axes(projection ='3d')
ax.scatter3D(read_file["Sakoe_Chiba"], read_file["N"], read_file["Time (s)"])
plt.savefig('./plots/3D_MBRs_sc.png', format='png', bbox_inches='tight')

# 2D plots
sc_1 = 7
sc_2 = 13
sc_3 = 19
sc_4 = 3
plt.figure()
plt.plot(read_file["N"][read_file["Sakoe_Chiba"].isin([sc_4])], read_file["Time (s)"][read_file['Sakoe_Chiba'].isin([sc_4])], label = "Sakoe-Chiba = 3")
plt.plot(read_file["N"][read_file["Sakoe_Chiba"].isin([sc_1])], read_file["Time (s)"][read_file['Sakoe_Chiba'].isin([sc_1])], label = "Sakoe-Chiba = 7")
plt.plot(read_file["N"][read_file["Sakoe_Chiba"].isin([sc_2])], read_file["Time (s)"][read_file['Sakoe_Chiba'].isin([sc_2])], label = "Sakoe-Chiba = 13")
plt.plot(read_file["N"][read_file["Sakoe_Chiba"].isin([sc_3])], read_file["Time (s)"][read_file['Sakoe_Chiba'].isin([sc_3])], label = "Sakoe-Chiba = 19")
plt.legend()
plt.ylabel('Time (s)')
plt.xlabel('MBRs')
plt.title("Time VS MBRs")
plt.savefig('./plots/MBRs_with_set_sc.png', format='png', bbox_inches='tight')

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
plt.savefig('./plots/sc_with_set_MBRs.png', format='png', bbox_inches='tight')
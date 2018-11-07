import matplotlib
matplotlib.use('Agg') #avoids ssh problems, but can not use .show()
import matplotlib.pyplot as plt
import numpy as np

filename = "parse_ads.out"
poav = np.genfromtxt(filename, delimiter="", comments="#",usecols = (1))
asa = np.genfromtxt(filename, delimiter="", comments="#",usecols = (2))
h = np.genfromtxt(filename, delimiter="", comments="#",usecols = (3))
up = np.genfromtxt(filename, delimiter="", comments="#",usecols = (5,6,7,8,9))
up_err = np.genfromtxt(filename, delimiter="", comments="#",usecols = (10,11,12,13,14))

p=[0.01, 0.05, 0.1, 0.15, 0.2] #bar

fig, ax = plt.subplots()
ax.set(
       xlabel="Pressure (bar)",
       ylabel="Uptake (cm$^3$/g)",
       )

for i in range(len(up)):
    poav_arr=[poav[i]]*5
    scatter1 = ax.errorbar(p,up[i],yerr=up_err[i],c="blue",marker='o',markersize=5,capsize=5,capthick=1)

ax.grid()
fig.savefig("parse_ads_plot3.png",dpi=600)
plt.close(fig)

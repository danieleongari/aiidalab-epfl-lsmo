import matplotlib
matplotlib.use('Agg') #avoids ssh problems, but can not use .show()
import matplotlib.pyplot as plt
import numpy as np

filename = "parse_ads.out"
poav = np.genfromtxt(filename, delimiter="", comments="#",usecols = (1))
asa = np.genfromtxt(filename, delimiter="", comments="#",usecols = (2))
up = np.genfromtxt(filename, delimiter="", comments="#",usecols = (9))
up_err = np.genfromtxt(filename, delimiter="", comments="#",usecols = (14))

fig, ax = plt.subplots()
ax.set(
       ylabel="Uptake @ 0.2bar (cm$^3$/g)",
       xlabel="Accessible surface area (m$^2$/g)",
       )

scatter1 = ax.scatter(asa,up,s=40,c=poav)
ax.grid()
#ax.set_yscale('log')

cbar = plt.colorbar(scatter1)
cbar.set_label("Accessible pore volume (cm$^3$/g)")
fig.savefig("parse_ads_plot1.png",dpi=600)
plt.close(fig)

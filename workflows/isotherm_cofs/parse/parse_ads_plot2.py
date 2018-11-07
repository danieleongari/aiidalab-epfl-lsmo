import matplotlib
matplotlib.use('Agg') #avoids ssh problems, but can not use .show()
import matplotlib.pyplot as plt
import numpy as np

filename = "parse_ads.out"
poav = np.genfromtxt(filename, delimiter="", comments="#",usecols = (1))
asa = np.genfromtxt(filename, delimiter="", comments="#",usecols = (2))
h = np.genfromtxt(filename, delimiter="", comments="#",usecols = (3))
up = np.genfromtxt(filename, delimiter="", comments="#",usecols = (9))
up_err = np.genfromtxt(filename, delimiter="", comments="#",usecols = (14))

fig, ax = plt.subplots()
ax.set(
       ylabel="Henry's coefficient (mol/kg/Pa)",
       xlabel="Uptake @ 0.2bar (cm$^3$/g)",
       yscale='log',
       ylim=[1e-6, 1e-3],
       )

scatter1 = ax.scatter(up,h,s=40,c=poav)
ax.grid()
#ax.set_yscale('log')

cbar = plt.colorbar(scatter1)
cbar.set_label("Accessible pore volume (cm$^3$/g)")
fig.savefig("parse_ads_plot2.png",dpi=600)
plt.close(fig)

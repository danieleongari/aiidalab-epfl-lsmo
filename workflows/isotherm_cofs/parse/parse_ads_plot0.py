import matplotlib
matplotlib.use('Agg') #avoids ssh problems, but can not use .show()
import matplotlib.pyplot as plt
import numpy as np

filename = "parse_ads.out"
poav = np.genfromtxt(filename, delimiter="", comments="#",usecols = (1))
asa = np.genfromtxt(filename, delimiter="", comments="#",usecols = (2))
h = np.genfromtxt(filename, delimiter="", comments="#",usecols = (3))
h_err = np.genfromtxt(filename, delimiter="", comments="#",usecols = (4))

fig, ax = plt.subplots()
ax.set(
       ylabel="Henry's coefficient (mol/kg/Pa)",
       xlabel="Accessible surface area (m$^2$/g)",
       yscale='log',
       ylim=[1e-6, 1e-3],
       )

scatter1 = ax.scatter(asa,h,s=40,c=poav)
ax.grid()
#ax.set_yscale('log')

cbar = plt.colorbar(scatter1)
cbar.set_label("Accessible pore volume (cm$^3$/g)")
fig.savefig("parse_ads_plot0.png",dpi=600)
plt.close(fig)

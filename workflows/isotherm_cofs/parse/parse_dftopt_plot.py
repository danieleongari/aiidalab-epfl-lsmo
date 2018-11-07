import matplotlib
matplotlib.use('Agg') #avoids ssh problems, but can not use .show()
import matplotlib.pyplot as plt
import numpy as np

with open('cif_list.txt') as finp:
    labels=finp.read().splitlines()

for label in labels:
    filename = "parse_dftopt_"+label+".out"
    steps = np.genfromtxt(filename, delimiter="", comments="#",usecols = (0))
    energy = np.genfromtxt(filename, delimiter="", comments="#",usecols = (1))

    fig, ax = plt.subplots()
    ax.set(ylabel='Energy (Hartree)', 
           xlabel='Steps',
           title='Robust cell optimization of: '+label)

    #make coloured background
    nstep=[0,0,0] #for md, geo_opt, cell_opt
    for i in range(2,len(steps)): #skip energy and first 0 md step
      if steps[i]==0:
         if nstep[0]==0:
            nstep[0]=i-1
         else:
            nstep[1]=i-1-nstep[0]
            break

    nstep[2]=len(steps)-1-nstep[0]-nstep[1]
    print(nstep)

    ax.axvspan(1, nstep[0], ymin=0, ymax=1, color='red', alpha=0.2)
    ax.axvspan(nstep[0]+1, nstep[0]+nstep[1]+1, ymin=0, ymax=1, color='yellow', alpha=0.2)
    ax.axvspan(nstep[0]+nstep[1]+2, len(steps), ymin=0, ymax=1, color='green', alpha=0.2)

    #print energy profile
    ax.plot(energy,color='blue',marker='o',markersize=3,linewidth=1)
    ax.grid()

    fig.savefig("parse_dftopt_"+label+".png")
    plt.close(fig)

### Imports
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import reac_samp

n = input('Please type the number of samples in your scheme: ');

reac_samp.make_dirs(n),reac_samp.make_var_rates(n)

fig = plt.figure()

# median rate dsitrubtion from STARLIB
med_data = (np.loadtxt('starlib_raw_rates/r_c12_ag_o16.txt',dtype=float, usecols=(0, 1,2)))
t9=(med_data[:,0])
rr=(med_data[:,1])
fu=(med_data[:,2])

# plot median for comparison
lines = plt.plot(t9,rr,linewidth=3.0,marker='o',markeredgewidth=1.0,ms=2.0,zorder=10,color='k')

#plot sampled rate distributions for c12(a,g)o16
for i in range(1,n+1):
    data=(np.loadtxt('example_grid/'+str(i)+'/rate_tables/r_c12_ag_o16.txt',dtype=float,skiprows=3))
    t9=(data[:,0]/10.)
    rr=(data[:,1])
    plt.hold(True)
    lines = plt.plot(t9,rr,linewidth=0.5,marker='o',markeredgewidth=1.0,ms=1.0)
    
plt.ylabel(r'$\rm{Reaction \ Rate}$',fontsize=24)
plt.xlabel(r'$T \ (\rm{GK})$',fontsize=24)    
plt.annotate(r'$^{12}\rm{C}(\alpha,\gamma)^{16}O$',xy=(0.075, 0.8),xycoords='axes fraction',fontsize=20)
plt.tight_layout()
plt.savefig("reac_samp_example.pdf")
plt.show()




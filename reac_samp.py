# Copyright (c) 2016, Carl Fields cef@asu.edu

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


# This program creates NxM indepently sampled nuclear reaction rate
# distributions where N is the number of rates in #the scheme and
# M is the number of samples.


### Imports
import numpy as np
import shutil,subprocess,os
from os import remove, close
from tempfile import mkstemp
from shutil import move
from shutil import copyfile


# EDIT THIS TO CHANGE WHICH RATES ARE IN YOUR SCHEME
# THIS EXAMPLE ONLY SAMPLES THE C12(A,G)O16 REACTION
'''
rates_list = [
'r_c12_ag_o16',\
]
'''

rates_list = []
subprocess.call(['./get_rate_labels.sh']) 
with open("rate_labels.txt") as f:
    rates_list = [line.rstrip() for line in f]    
os.remove('rate_labels.txt')
    
"""
# SAMPLING SCHEME USED IN FIELDS ET AL. 2016, APJ - http://arxiv.org/abs/1603.06666
rates_list = [
'r_h1_pg_h2',\
'r_h2_pg_he3',\
'r_he3_ag_be7',\
'r_li7_pn_be7',\
'r_be7_pg_b8',\
'r_c12_pg_n13',\
'r_c13_pg_n14',\
'r_n13_pg_o14',\
'r_n14_pg_o15',\
'r_n15_pa_c12',\
'r_n15_pg_o16',\
'r_o14_ap_f17',\
'r_o15_ag_ne19',\
'r_o16_pg_f17',\
'r_o17_pa_n14',\
'r_o17_pg_f18',\
'r_o18_pa_n15',\
'r_o18_pg_f19',\
'r_f17_pg_ne18',\
'r_f18_pa_o15',\
'r_f19_pa_o16',\
'r_o16_ag_ne20',\
'r_n14_ag_f18',\
'r_o18_ag_ne22',\
'r_c12_ag_o16',\
'r_he4_he4_he4_to_c12'\
]
"""


t9 = []
rr = []
fu = []
mu, sigma = 0., 1.0 # mean and standard deviation

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

# copy default directory and number it according to i'th variant
def make_dirs(N_var):
        copyfile('./starlib_raw_rates/rates_list.txt','./default_work_dir/rate_tables/rates_list.txt' )
	for i in range(1,N_var+1):
        	shutil.copytree('default_work_dir','example_grid/'+str(i))
	return

# create array of p_i for sampling
def make_var_vec(N_var):
	mu, sigma = 0., 1.0
	var_vec = []
	for i in range(len(rates_list)):
		var_vec.append(np.random.normal(mu,sigma,N_var))
	return var_vec

#use p_i to construct sampled rate distributions/place into i'th work directory
def make_var_rates(N_var):
	t9 = []
	rr = []
	fu = []
	var = np.array(make_var_vec(N_var))
	rec = []
	samp_ind = []
	for i in range(1,N_var+1):
		for j in range(len(rates_list)):
			data=(np.loadtxt('starlib_raw_rates/'+str(rates_list[j])+'.txt',dtype=float, usecols=(0, 1,2),skiprows=1))
			t9=(10.*data[:,0])
			rr=(data[:,1])
			fu=(data[:,2])
			samp = var[j][i-1]
			rate_var = (rr* (fu**(samp)) )
		        f = open('example_grid/'+str(i)+'/rate_tables/'+str(rates_list[j])+'.txt','w')
        		f.write('#  '+str(rates_list[j])+' modified with var: '+str(samp)+'\n')
        		f.write('# T8            RATE      \n')
        		f.write('60\n')
        		f.close()
        		with open('example_grid/'+str(i)+'/rate_tables/'+str(rates_list[j])+'.txt','a') as f_handle:
                		np.savetxt(f_handle, np.column_stack([t9, rate_var]),fmt=[' %1.2f\t','       %1.3E\t'])
			rec.append(samp),samp_ind.append(j)
	np.savetxt('rate_varitation_factors.txt', np.column_stack([samp_ind, rec]),fmt=['%i',' %1.8f\t'])
	return

make_dirs(50),make_var_rates(50)


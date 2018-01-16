import rpy2
import readline #what is this? seems to fix robjects problem
from rpy2 import robjects 

#OR
import os
import subprocess

def plot(bkpt_name):
    """r = robjects.r
    r.source("plot_bcs_across_bkpts.R")
    r.Rplot_bcs(bkpt_name)
    #r.rfunc(bkpt_name)"""

#OR
    #args = ['R','plot_bcs_across_bkpts.R', '1']
    #process = subprocess.Popen(args) #, stdout = sys.stdout)
    
    #subprocess.call('plot_bcs_across_bkpts.R')
    #subprocess.call(["R", "plot_bcs_across_bkpts.R", "1"])#, "arg1", "arg2"])
    
    subprocess.call("R plot_bcs_across_bkpts.R --1", shell=True)

import rpy2
import readline #what is this? seems to fix robjects problem
from rpy2 import robjects 

def plot(bkpt_name):
    r = robjects.r
    r.source("plot_bcs_across_bkpts.R")
    r.rfunc(bkpt_name)

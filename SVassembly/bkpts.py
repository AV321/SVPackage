import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
from scipy.stats import mode
import math as m 

def plot_bkpts(bkpt_name):

  file_1 = bkpt_name + "_1.bc_windows.txt"
  file_2 = bkpt_name + "_2.bc_windows.txt"
  file_hap =  bkpt_name + "_hap_bcs.txt"
  
  
  
  #sort barcodes by where they map (lowest coordinate to highest)
  
  #generating 2 figures - 1 for each breakpoint
  
  
  
  
  path = bkpt_name + "_bkpt_region.pdf"
  plt.savefig(path)

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
from scipy.stats import mode
import math as m 

#set working directory
os.chdir(/mnt/ix1/Projects/M002_131217_gastric/P00526/P00526_WG10_150722_gastric/A20_170516_hmw_maps/metr)

def plot_bkpts(bkpt_name):

  file_1 = bkpt_name + "_1.bc_windows.txt"
  file_2 = bkpt_name + "_2.bc_windows.txt"
  file_hap =  bkpt_name + "_hap_bcs.txt"
  
  
  
  #sort barcodes by where they map (lowest coordinate to highest)
  
  #generating 2 figures - 1 for each breakpoint
  
  
   # read in data frames
  '''df_1 <- read.table(file_1,header=T)
  df_2 <- read.table(file_2,header=T)

  chrom_1<-tail(names(sort(table(df_1$chrom))), 1)
  chrom_2<-tail(names(sort(table(df_2$chrom))), 1)


  # read in haplotyped bc data frame
  hap_bcs <- read.table(file_hap,header=T)

  # obtain names of barcode columns
  bc_cols<-tail(colnames(df_1),-3)

  # make a vector of the first position
  first_pos <- vector("numeric")
  counter=3
  for(i in bc_cols){
    counter = counter+1
    result<-min((df_1$window_start)[df_1[[paste(i)]]>0])
    first_pos[counter]=result
    }'''
  
  
  path = bkpt_name + "_bkpt_region.pdf"
  plt.savefig(path)

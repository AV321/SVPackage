import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import csv
    from scipy.stats import mode
    import math as m #have to install in testing environment

def map_to_genome(infile, out_folder):
    #%matplotlib inline
    
    
    df = pd.read_table(infile) #"/mnt/ix2/avitko/170621_SV_phasing/A04_plotting/out_metr_192.merge.txt"
    df = df.loc[df['chr_x'] <= 23]
    
    #find mode 
    mode_array = mode(df['chr_x'])
    chr_mode = int(mode_array[0])
    max_freq = int(mode_array[1])
    
    grouped = df.groupby("chr_x")
    counts = grouped.size()
    chr_arr = [] #list of chromosomes to map to
   
    for i in range(1,24):
        if counts[i] > 0.3*max_freq:
            chr_arr.append(i)
   
    for i in chr_arr:
        map_to_chr(i, grouped, out_folder)





#given a chromosome, plots contig to that chromosome. Returns plot
def map_to_chr(chrm, grouped, out_folder):
    group = grouped.get_group(chrm)
  
    #get max value in pos_x and pos_y to determine scale
    xcol = group["pos_x"]
    mode_array = mode(xcol)
    max_x = int(mode_array[0])

    ycol = group["pos_y"]
    mode_array = mode(ycol)
    max_y = int(mode_array[0])


    x_col_pow = int(round(m.log10(float(max_x)/1000)))  #5
    y_col_pow = int(round(m.log10(float(max_y)/1000)))  #1 -- was getting 2 in R?

    x_axis = ycol/(10.**y_col_pow)

    y_axis = xcol/(10.**x_col_pow)

    plt.scatter(x_axis, y_axis, marker = ".")
   
    plt.xlabel("contig coordinate (10^%d)" % y_col_pow)
    plt.ylabel("chr %d coordinate (10^%d)" % (chrm, x_col_pow))
  
    #plt.show()
  
    #saving to a folder
    path = out_folder + ("/Chr_%d" %chrm)
    plt.savefig(path)

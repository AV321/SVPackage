import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.colors

import csv
from scipy.stats import mode
import math as m
import os
import collections

#set working directory
os.chdir("/mnt/ix1/Projects/M002_131217_gastric/P00526/P00526_WG10_150722_gastric/A20_170516_hmw_maps/metr")

bkpt_name = "1"

file_1 = bkpt_name + "_1.bc_windows.txt"
file_2 = bkpt_name + "_2.bc_windows.txt"
file_hap =  bkpt_name + "_hap_bcs.txt"

df_1 = pd.read_table(file_1)
df_2 = pd.read_table(file_2)
hap_bcs = pd.read_table(file_hap)

bkpt_name = "1"

file_1 = bkpt_name + "_1.bc_windows.txt"
file_2 = bkpt_name + "_2.bc_windows.txt"
file_hap =  bkpt_name + "_hap_bcs.txt"

#sort barcodes by where they map (lowest coordinate to highest)
#read in data frames
df_1 = pd.read_table(file_1)
df_2 = pd.read_table(file_2)
hap_bcs = pd.read_table(file_hap)

hap_bcs = hap_bcs.transpose()




bcs_hap_dict = {}
for key in df_1.keys():
    if key != "chrom" and key != "window_start" and key != "window_end":
        key = key[:-2]
        bcs_hap_dict[key] = 'unassigned'


for key, values in hap_bcs.iteritems():
    if values[0] != 'bcs':
        hap = values[1]
        bcs_hap_dict[values[0]] = hap


df_1 = df_1.sort_values('window_start')
df_2 = df_2.sort_values('window_start')

chrom_1 = df_1.at[0, 'chrom']
chrom_2 = df_2.at[0, 'chrom']

x_values_1_1 = []
x_values_1_2 = []
x_values_1_unassigned = []
y_values_1_1 = []
y_values_1_2 = []
y_values_1_unassigned = []

x_values_2_1 = []
x_values_2_2 = []
x_values_2_unassigned = []
y_values_2_1 = []
y_values_2_2 = []
y_values_2_unassigned = []


i1 = 0
window_start_arr1 = df_1['window_start']


for name, values in df_1.iteritems(): #go through columns (so each barcode)
    if name != "chrom" and name != "window_start" and name != "window_end":
        i1 += 1
        name = name[:-2]
        hap = bcs_hap_dict[name]
        for indx, window in values.iteritems():
            if window != 0:
                if hap == '1':
                    y_values_1_1.append(i1)
                    x_values_1_1.append(window_start_arr1[indx])
                elif hap == '2':
                    y_values_1_2.append(i1)
                    x_values_1_2.append(window_start_arr1[indx])
                else:
                    y_values_1_unassigned.append(i1)
                    x_values_1_unassigned.append(window_start_arr1[indx])
i2 = 0
window_start_arr2 = df_2['window_start']
for name, values in df_2.iteritems():
    if name != "chrom" and name != "window_start" and name != "window_end":
        i2 += 1
        name = name[:-2]
        hap = bcs_hap_dict[name]
        for indx, window in values.iteritems():
            if window != 0:
                if hap == '1':
                    y_values_2_1.append(i2)
                    x_values_2_1.append(window_start_arr2[indx])
                elif hap == '2':
                    y_values_2_2.append(i2)
                    x_values_2_2.append(window_start_arr2[indx])
                elif hap == 'unassigned':
                    y_values_2_unassigned.append(i2)
                    x_values_2_unassigned.append(window_start_arr2[indx])

brkpt1 = min(df_1['window_start']) + ((max(df_1['window_end']) - min(df_1['window_start']))/2)
brkpt2 = min(df_2['window_start']) + ((max(df_2['window_end']) - min(df_2['window_start']))/2)

fig, ax = plt.subplots(1, 2)

ax[0].scatter(x_values_1_1, y_values_1_1, s=0.2, color='b')
ax[0].scatter(x_values_1_2, y_values_1_1, s=0.2, color='r', ax = ax)
ax[0].scatter(x_values_1_unassigned, y_values_1_unassigned, s=0.2, color='g')

ax[0].axvline(x=brkpt1, linewidth=1, color = 'black')
ax[0].set_title("")
ax[0].set_xlabel("chr %d (Mb)" %chrom_1)
ax[0].set_ylabel("SV-specific barcode")


ax[1].scatter(x_values_2_1, y_values_2_1, s=0.2, color='b')
ax[1].scatter(x_values_2_2, y_values_2_1, s=0.2, color='r')
ax[1].scatter(x_values_2_unassigned, y_values_2_unassigned, s=0.2, color='g')

ax[1].axvline(x=brkpt2, linewidth=1, color = 'black')
ax[1].set_title("")
ax[1].set_xlabel("chr %d (Mb)" %chrom_2)
ax[1].set_ylabel("")

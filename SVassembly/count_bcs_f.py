#!/usr/bin/env python

#From Stephanie Greer's github

"""

:Author: Ji Research Group/Stanford Genome Technology Center
:Contact: sgreer2@stanford.edu
:Creation date: 24.11.2016
:Description: 

This script counts the number of unique barcodes in windows around the SV breakpoints

This script requires:
- all of the python packages listed (imported) below

Revisions:
None to date

CURRENT VERSION: 1.0

"""

cur_version = 1.0

### LOAD THE NECESSARY PACKAGES ###

import sys
import os
import __main__ as main
import argparse
import ast

import sys
import pandas as pd
import pysam
import numpy as np


MIN_MAPQ = 0
PERF_CIGAR = False

#################################################################
################                                 ################
################        PARSE THE ARGUMENTS      ################
################                                 ################
#################################################################

## DEFINE FUNCTION TO CREATE WINDOWS AROUND BREAKPOINTS

def make_window(s,e,w):
	cur_size = e-s
	adj_val = (w-cur_size)/2
	adj_val = int(round(adj_val,0))
	new_start = s - adj_val
	new_end = e + adj_val
	return [new_start,new_end]

## DEFINE FUNCTION TO OBTAIN BARCODES FROM BAM FILE FOR SPECIFIC REGIONS

def get_barcode_ids(bam_in, chrom, start, end, min_mapq, perf_cigar):
	bcs = []
	for r in bam_in.fetch(chrom, start, end):
	  if r.mapq >= min_mapq and (not(perf_cigar) or (not(r.cigar is None) and len(r.cigar) == 1)):
		  if r.has_tag("BX"):
			  bc_id=r.get_tag("BX")
			  bcs.append(bc_id)
	return list(bcs)

#def count_bcs(sv_in, bam_file, full_w_size, small_w_size):
def count_bcs(outpre='out',out_window=500000, in_window=1000,**kwargs):
	
	print kwargs
	
	if 'sv' in kwargs:
		sv_input = kwargs['sv']
	if 'bam' in kwargs:
		bam_input = kwargs['bam']
	if 'out_window' in kwargs:
		full_w_size = kwargs['out_window']
	if 'in_window' in kwargs:
		small_w_size = kwargs['in_window']
	if 'out' in kwargs:
		outpre = kwargs['out']
	
	print sv_input
	print outpre
	print full_w_size
	print small_w_size
	
	global full_w_size
	full_w_size = int(full_w_size)  # -l #500000
	global small_w_size
	small_w_size = int(small_w_size)
	
	sv_df = sv_input

	sv_df1 = sv_df[['name1','chrom1','start1','stop1','bc_overlap_id']]
	sv_df2 = sv_df[['name2','chrom2','start2','stop2','bc_overlap_id']]
	full_names = ['name','chrom','start','stop','bc_overlap_id']
	sv_df1.columns = full_names
	sv_df2.columns = full_names
	sv_df_full = pd.concat([sv_df1,sv_df2])
	print sv_df_full


	w_start_list = [x[0] for x in sv_df_full.apply(lambda row: make_window(row['start'],row['stop'], full_w_size), axis=1)]
	w_stop_list = [x[1] for x in sv_df_full.apply(lambda row: make_window(row['start'],row['stop'], full_w_size), axis=1)]
	sv_df_full['w_start'] = w_start_list
	sv_df_full['w_stop'] = w_stop_list
	sv_df_full


	bam_open = pysam.Samfile(bam_input)

	for index,row in sv_df_full.iterrows():

		# Create data frame of 1kb windows
		start = int(row['w_start'])
		stop = int(row['w_stop'])
		window_start = np.arange(start, start+full_w_size, small_w_size+1)
		window_end = window_start+small_w_size
		df = pd.DataFrame([window_start, window_end]).transpose()
		df.columns = ['window_start','window_end']
		df['chrom'] = str(row['chrom'])
		df = df[['chrom','window_start','window_end']]

		# Make a list of barcodes in each of the 1kb windows
		region_bcs = []
		for i,r in df.iterrows():  
			region_bc_list = get_barcode_ids(bam_open, r['chrom'], r['window_start'], r['window_end'], MIN_MAPQ, PERF_CIGAR)
			region_bcs.append(region_bc_list)

		# Make list of SV-specific barcodes
		bc_list = row['bc_overlap_id']
		#bc_list = ast.literal_eval(row['bc_overlap_id'])

		# For each SV-specific barcode, count the number of times it occurs in each region
		for bc in bc_list:
			df[bc] = [x.count(bc) for x in region_bcs]

		# Write output to file
		cur_name = str(row['name'])
		df.to_csv(cur_name + ".bc_windows.txt", sep="\t", index=False)

		return df


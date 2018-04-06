#!/usr/bin/env python

import csv
import pysam
#import distance
#import editdistance
from itertools import izip_longest, islice
import gzip
import sys
import time

import io



def extract_readsv2_1(r1, r2, i1, bcs, out_r1, out_r2, out_i1):
	
	start_time = time.time()
	
	bcs_list = []
	out_r1_file = gzip.open(out_r1,'w')
	out_r2_file = gzip.open(out_r2,'w')
	out_si_file = gzip.open(out_i1,'w')


	with open(bcs,'r') as f:
		for line in csv.reader(f,delimiter='\t'):
			bcs_list.append(line[0])

	bcs_set = set(bcs_list)

	n = 0
	i = 0

	with gzip.open(r1, 'r') as f1, gzip.open(r2, 'r') as f2, gzip.open(i1,'r') as ind:
		cur_time = time.time()
		#don't use grouper -- it's slow
		#for (lines,lines_index) in zip(grouper(f, 8, ""),grouper(ind,8,"")):
		while True:
			lines_r1 = list(islice(f1,3))
			lines_r2 = list(islice(f2,4))
			lines_index = list(islice(ind,4))

			if not lines_r1:
				break

			n = n + 1
			if (n % 1000000 == 0):
				print >>sys.stderr, "%d reads processed, %d records matched bcs in a %d second chunk" % (n, i, time.time() - cur_time)
				cur_time = time.time()

			if (lines_r1[1][0:16] in bcs_set):
				i = i + 1

				for line in lines_r1:
					out_r1_file.write(line)
				for line in lines_r2:
					out_r2_file.write(line)
				for line in lines_index:
					out_si_file.write(line)
				
	end_time = time.time()
        total_time = end_time - start_time
        print >>sys.stderr, "Total run time was %d" % (total_time)

#phasing.py in A05_package
#NOT DONE

import pandas as pd
import numpy as np

df = pd.read_table(input_file, sep="\t")  # out_metl.sv_haps.txt   
df = df.sort_values('name')

def makeNewColumns():
    df["hap1_overlap_bcs_bp_new"] = df["hap1_overlap_bcs_bp"]
    df["hap2_overlap_bcs_bp_new"] = df["hap2_overlap_bcs_bp"]
    df["hap1_overlap_count_bp_new"] = df["hap1_overlap_count_bp"]
    df["hap2_overlap_count_bp_new"] = df["hap2_overlap_count_bp"]

    df["haplotype_assignment_original"] = df["haplotype_assignment_final"] = np.nan

    df["bcs_list"] = np.nan

    df["able_to_assign"] = False

def flipPhaseBlock(phaseToFlip): #save 1, make 1 be 2, make 2 be saved value of 1. Repeat for other flip
  a = df.ix[df.phase_id_norm == phaseToFlip, 'hap1_overlap_count_bp_new']
  df.ix[df.phase_id_norm == phaseToFlip, 'hap1_overlap_count_bp_new'] = df.ix[df.phase_id_norm == phaseToFlip, 'hap2_overlap_count_bp_new']
  df.ix[df.phase_id_norm == phaseToFlip, 'hap2_overlap_count_bp_new'] = a

  b = df.ix[df.phase_id_norm == phaseToFlip, 'hap1_overlap_bcs_bp_new']
  df.ix[df.phase_id_norm == phaseToFlip, 'hap1_overlap_bcs_bp_new'] = df.ix[df.phase_id_norm == phaseToFlip, 'hap2_overlap_bcs_bp_new']
  df.ix[df.phase_id_norm == phaseToFlip, 'hap2_overlap_bcs_bp_new'] = b


#returns number of variants with break points not assigned to the same haplotype
def notUniformlyAssigned():
    num = 0
    name_set = set(df["name"].tolist()) #set of variant names
    for this_name in name_set:
        setOfHapAssignments =(set(df.ix[df.name == this_name , "haplotype_assignment_final"].tolist()))
        if (len(setOfHapAssignments) != 1):
            print ("The following variant is not assigned uniformly " + str(this_name))
            num = num + 1
    return num

    #needs to be fixed 
def assignBreakpoints(column):

    size =(df.groupby('phase_id_norm').size()) #pd.DataFrame
    non_assignable = size[size < 2]


    for index, row in df.iterrows():
        #determines if break point is assignable
        cond1 = (row['hap1_overlap_count_bp_new'] + row['hap2_overlap_count_bp_new'] > 15)
        cond2 = ((row['hap1_overlap_count_bp_new'] < 8), (row['hap2_overlap_count_bp_new'] < 8))
        cond3 = ((row['hap1_overlap_count_bp_new'] > (3*row['hap2_overlap_count_bp_new'])),
                  (row['hap2_overlap_count_bp_new'] > (3*row['hap1_overlap_count_bp_new'])),
                  ((row['hap1_overlap_count_bp_new'] >= 8),(row['hap2_overlap_count_bp_new'] >= 8)))

        if(cond1,cond2,cond3):
            df.ix[index, 'able_to_assign'] = True
        else:
            df.ix[index, 'able_to_assign'] = False

#assign to 1, 2, or both
        if (df.ix[index,'able_to_assign'] == True):
            if ((row['hap1_overlap_count_bp_new'] > 8),(row['hap2_overlap_count_bp_new'] > 8)):
                df.ix[index, column] = 'both'
            if (row['hap1_overlap_count_bp_new'] > row['hap2_overlap_count_bp_new']):
                df.ix[index, column] = 1
            else:
                df.ix[index, column] = 2


    #special case if one of the bps of the variant is unassignable
    for index, row in df.iterrows():
        if(df.ix[index,'phase_id_norm'] in non_assignable):
            #check if other breakpoint was assignable

            a = df[df.name == row['name']] #--> will basically get group as dataframe vs. groupby object

            for ind, r in a.iterrows():
                if(a.ix[ind, 'phase_id_norm'] not in non_assignable):
                    hap_assignment = a.ix[ind, column]
                    df.ix[index, column] = hap_assignment

def phaseFlipRecWrap():
    numPhaseBlocks = len(set(df["phase_id_norm"].tolist()))
    return phaseFlipRec(0,0, numPhaseBlocks)


def phaseFlipRec(phaseToFlip, phaseBlocksFlipped, numPhaseBlocks):
    if(phaseToFlip != 0):
        flipPhaseBlock(phaseToFlip)
        assignBreakpoints("haplotype_assignment_final")

    if (notUniformlyAssigned() == 0):
        return ([df, 0])

    if (phaseBlocksFlipped == numPhaseBlocks):
        return ([df,notUniformlyAssigned()])

    else:
        for name, group in df.groupby(['name']):
            numDifIDs = (group["phase_id_norm"]).tolist()

            #if breakpoints are in different phase blocks,
            if (len(set(numDifIDs))>1):

                #check if they're assigned to different haplotypes
                haplotypes = (group["haplotype_assignment_final"]).tolist()
                if (haplotypes[0] != haplotypes[1]):

                    #in which case, try flipping both, and see which works better. Recursive call will be made here.
                    flip1 = phaseFlipRec(numDifIDs[0], phaseBlocksFlipped + 1, numPhaseBlocks)
                    flip2 = phaseFlipRec(numDifIDs[1], phaseBlocksFlipped + 1, numPhaseBlocks)

                    if (flip1[1] < flip2[1]):
                        return (flip1)
                    else:
                        return (flip2)
def bcs_list():

    #TO DO -- filter for breakpoints that have non-empty lists (as was the case in chol_4705_out.sv_haps.txt)

    for name, group in df.groupby(['name']):
        if ((group["able_to_assign"].tolist())[0] == True): #assumes uniform assignment for both breakpoints
            haplotype = (group["haplotype_assignment_final"].tolist())[0]
            if (haplotype == 1):
                bcsList = set((group["hap1_overlap_bcs_bp_new"]).tolist())
                df.ix[df.name == name, "bcs_list"] = bcsList
            elif (haplotype == 2):
                bcsList = set((group["hap2_overlap_bcs_bp_new"]).tolist())
                df.ix[df.name == name, "bcs_list"] = bcsList
            elif (haplotype == 'both'):
                bcsList = set((group["hap1_overlap_bcs_bp_new"]).tolist() + (group["hap2_overlap_bcs_bp_new"]).tolist())
                df.ix[df.name == name, "bcs_list"] = bcsList

def output_files():
    dfHap1bcs = df.query('(haplotype_assignment_final == [1]) | haplotype_assignment_final == "both"')
    dfHap2bcs = df.query('(haplotype_assignment_final == [2]) | haplotype_assignment_final == "both"')

    hap_bcs_list_1 = set()
    for entry in dfHap1bcs['bcs_list']:
        hap_bcs_list_1.update(entry)
    hap_bcs_list_2 = set()
    for entry in dfHap2bcs['bcs_list']:
        hap_bcs_list_2.update(entry)

    thefile = open('haplotype_1_bcs_list.txt', 'w')   #TO DO -- does this need to exist?
    for item in list(hap_bcs_list_1):
        thefile.write("%s\n" % item)

    thefile2 = open('haplotype_2_bcs_list.txt', 'w')
    for item in list(hap_bcs_list_2):
        thefile2.write("%s\n" % item)

def phase_haps(input_file):            
    makeNewColumns()
    assignBreakpoints("haplotype_assignment_original")
    assignBreakpoints("haplotype_assignment_final")
    df = phaseFlipRecWrap()[0]
    bcs_list()
    output_files() #this cant work without bcs_list working
    #df                        

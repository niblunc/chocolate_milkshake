import glob
import os
import pandas as pd
import argparse
import sys
import subprocess
import re
from multiprocessing import Pool
from IPython.core import display as ICD
from os import listdir
from shutil import rmtree
from subprocess import check_output


### Set paths and other variables

data_path='/projects/niblab/experiments/chocolate_milkshake/data'
#chunksize_input=sys.argv[1]
#pool_size_input=sys.argv[2]

data_dict={}
bad_subs=[]
     

### Helper Functions

def chunks(l,n):
    return [l[i:i+n] for i in range(0, len(l), n)]



def pull_timeseries(roi_list, bb300_path='/projects/niblab/parcellations/bigbrain300',roi_df='/projects/niblab/parcellations/bigbrain300/renaming.csv'):

    
    bad_subs=[]
    #ICD.display(roi_df)

    # load asymmetrical nifti roi files
    asym_niftis=glob.glob("/projects/niblab/parcellations/bigbrain300/MNI152Asymmetrical_3mm/*.nii.gz")

    # load roi list
    out_dir = os.path.join(data_path, 'rois/bigbrain300/funcs')
    #print('[INFO] output folder: \t%s \n'%out_dir)


    # loop through the roi file list
    #print(roi_list[:3])
    for nifti in sorted(roi_list):

        subj_id = nifti.split("/")[-1].split("_")[0]
        task_id = nifti.split("/")[-1].split("_")[2]
        #print('[INFO] roi: %s %s \n%s'%(subj_id, task_id, nifti))

        # loop through roi reference list
        for ref_nifti in sorted(asym_niftis):
            #print('[INFO] reference roi: %s'%ref_nifti)
            roi = ref_nifti.split('/')[-1].split(".")[0]
            out_path = os.path.join(out_dir, "{}_{}_{}_{}.txt".format(subj_id, "ses-1", task_id, roi))
            #print(roi, out_path)
            cmd='fslmeants -i {} -o {} -m {}'.format(nifti, out_path, ref_nifti)
            try:
                #cmd='fslmeants -i {} -o {} -m {}'.format(nifti, out_path, ref_nifti)
                #print("Running shell command: {}".format(cmd))
                os.system(cmd)
            except:
                bad_subs.append((subj_id, task_id))
        
        #print('[INFO] finished processing for %s'%subj_id)
        

    return "%s"%bad_subs

   

"""  
# Timeseries Pull Main Program
"""


# load roi
print("[INFO] loading roi and reference file....")

#subject_ids=[x.split("/")[-2] for x in glob.glob(os.path.join(data_path, 'preprocessed/sub-*/ses-1'))]
# get functionals 
funcs_3mm =glob.glob(os.path.join(data_path, "preprocessed/sub-*/ses-1/func/*milkshake*brain_3mm.nii.gz"))
print("Functional nifti files found: {}".format(len(funcs_3mm)))
chunksize=20
print("[INFO] chunksize: {}".format(chunksize))
chunk_list=chunks(funcs_3mm, chunksize)
#roi_df['network']
# pull timeseries by rois --fslmeants command
#print(chunk_list)
def run_process(pool_size):
    print("[INFO] starting multiprocess...")
    with Pool(pool_size) as p:
        error_subjects=p.map(pull_timeseries, chunk_list)
    print("[INFO] process complete. \n[INFO] bad subjects: \t\t%s"%error_subjects)
    
pool_size=20
run_process(pool_size)



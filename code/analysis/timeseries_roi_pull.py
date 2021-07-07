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

subject_folders=sorted(glob.glob('/projects/niblab/experiments/chocolate_milkshake/data/bids/derivatives/preprocessed/sub-*'))
beta_path='/projects/niblab/experiments/chocolate_milkshake/data/betaseries'
concat_path="/projects/niblab/experiments/chocolate_milkshake/data/betaseries/niftis_concat"
stim=sys.argv[1]#'HS_plus_h20'
data_dict={}
bad_subs=[]
task_rois=sorted(glob.glob(os.path.join(concat_path,stim,'*sub-*_3mm.nii.gz')))

                

### Helper Functions

def chunks(l,n):
    return [l[i:i+n] for i in range(0, len(l), n)]



def pull_timeseries(roi_list, bb300_path='/projects/niblab/parcellations/bigbrain300',roi_df='/projects/niblab/parcellations/bigbrain300/renaming.csv',stim=stim):

    
    bad_subs=[]
    #ICD.display(roi_df)

    # load asymmetrical nifti roi files
    asym_niftis=glob.glob("/projects/niblab/parcellations/bigbrain300/MNI152Asymmetrical_3mm/*.nii.gz")

    # load roi list
    out_dir = os.path.join(beta_path, 'rois/big300/%s'%stim)
    #print('[INFO] OUT DIRECTORY: %s \n'%out_dir)

    #roi_df.set_index("final order name", inplace=True)
    #ICD.display(roi_df)#.head())

    # run parallel job pools
    for nifti in sorted(roi_list):
        #print('[INFO] loop1')
        subj_id = nifti.split("/")[-1].split("_")[0]
        subj_condition=nifti.split("/")[-1].split(".")[0].replace("_3mm", "")
        #print('[INFO] roi: %s %s'%(subj_id, subj_condition))

        # loop through roi reference list
        for ref_nifti in sorted(asym_niftis):
            #print('[INFO] reference roi: %s'%ref_nifti)
            roi = ref_nifti.split('/')[-1].split(".")[0]
            out_path = os.path.join(out_dir, "{}_{}.txt".format(subj_condition, roi))
            #print(roi, out_path)
            cmd='fslmeants -i {} -o {} -m {}'.format(nifti, out_path, ref_nifti)
            try:
                #cmd='fslmeants -i {} -o {} -m {}'.format(nifti, out_path, ref_nifti)
                #print("Running shell command: {}".format(cmd))
                os.system(cmd)
            except:
                bad_subs.append((subj_id, subj_condition))
        
        print('[INFO] finished processing for %s'%subj_id)


    return "%s"%bad_subs

   
### Timeseries Pull Main Program
# load roi
print("[INFO] loading roi and reference file....")
print("[INFO] {} task roi nifti files being processed.".format(len(task_rois)))
chunksize=15
print("[INFO] chunksize: {}".format(chunksize))
chunk_list=chunks(task_rois, chunksize)
#roi_df['network']
# pull timeseries by rois --fslmeants command

def run_process(pool_size):
    print("[INFO] starting multiprocess...")
    with Pool(pool_size) as p:
        error_subjects=p.map(pull_timeseries, chunk_list)
    print("[INFO] process complete. \n[INFO] bad subjects: \t\t%s"%error_subjects)
    
pool_size=15
run_process(pool_size)
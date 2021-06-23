# Nichollette Acosta | Heuristic phantom converter for phantom-1
# 9/4/2017#

# Phantom heurisitc converter
# Very simple ~ can be upgraded/modified
# Searches for T1w files and dwi files

import os

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    # create directories

    # anat/
    t1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w')


    # fmap/
    fmap_phase = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_phasediff')
    fmap_magnitude = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_magnitude')


    # func/

    milkA = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-milkshakeA_bold' )
    milkB = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-milkshakeB_bold')
    milkC = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-milkshakeC_bold')
    milkD = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-milkshakeD_bold')
    #noGo1 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-GoNoGo1_bold')
    #noGo2 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-GoNoGo2_bold')
    imagine = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-imagine_bold')

    milkA_moco = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-milkshakeA_physio' )
    milkB_moco = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-milkshakeB_physio')
    milkC_moco = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-milkshakeC_physio')
    milkD_moco = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-milkshakeD_physio')
    #noGo1_moco = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-GoNoGo1_physio')
    #noGo2_moco = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-GoNoGo2_physio')
    imagine_moco = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-imagine_physio')

    info = {t1: [],  fmap_phase: [], fmap_magnitude: [], milkA: [], milkB: [], milkC: [], milkD: [],  imagine: [],
            milkA_moco: [], milkB_moco: [], milkC_moco: [], milkD_moco: [],  imagine_moco: [] }
    for s in seqinfo:
        print(s)

        if ('t1' in s.protocol_name):
            info[t1].append(s.series_id)  ## append if multiple series meet criteria

        if (s.dim3 == 54) and ('field_map' in s.protocol_name):
            info[fmap_magnitude].append(s.series_id)  ## append if multiple series meet criteria


        if (s.dim3 == 27) and ('field_map' in s.protocol_name):
            info[fmap_phase].append(s.series_id)  # append if multiple series meet criteria


        if ('milkshake_A' in s.protocol_name):
            if (s.is_motion_corrected == False):
                info[milkA].append(s.series_id)  # append if multiple series meet criteria
            if (s.is_motion_corrected == True):
                info[milkA_moco].append(s.series_id)  # append if multiple series meet criteria

        if ('milkshake_B' in s.protocol_name):
            if (s.is_motion_corrected == False):
                info[milkB].append(s.series_id)  # append if multiple series meet criteria
            if (s.is_motion_corrected == True):
                info[milkB_moco].append(s.series_id)  # append if multiple series meet criteria

        if ('milkshake_C' in s.protocol_name):
            if (s.is_motion_corrected == False):
                info[milkC].append(s.series_id)  # append if multiple series meet criteria
            if (s.is_motion_corrected == True):
                info[milkC_moco].append(s.series_id)  # append if multiple series meet criteria

        if ('milkshake_D' in s.protocol_name):
            if (s.is_motion_corrected == False):
                info[milkD].append(s.series_id)  # append if multiple series meet criteria
            if (s.is_motion_corrected == True):
                info[milkD_moco].append(s.series_id)  # append if multiple series meet criteria

        if ('imagine' in s.protocol_name):
            if (s.dim4 == 475) and (s.is_motion_corrected == False):
                info[imagine].append(s.series_id)  # append if multiple series meet criteria
            if (s.dim4 == 475) and (s.is_motion_corrected == True):
                info[imagine_moco].append(s.series_id)  # append if multiple series meet criteria

       # if ('NoGo1' in s.protocol_name):
        #    if (s.dim4 == 195) and (s.is_motion_corrected == False):
         #       info[noGo1].append(s.series_id)  # append if multiple series meet criteria
          #  if (s.dim4 == 195) and (s.is_motion_corrected == True):
           #     info[noGo1_moco].append(s.series_id)  # append if multiple series meet criteria

        #if ('NoGo2' in s.protocol_name):
         #   if (s.dim4 == 195) and (s.is_motion_corrected == False):
          #      info[noGo2].append(s.series_id)  # append if multiple series meet criteria
           # if (s.dim4 == 195) and (s.is_motion_corrected == True):
            #    info[noGo2_moco].append(s.series_id)  # append if multiple series meet criteria

    return info

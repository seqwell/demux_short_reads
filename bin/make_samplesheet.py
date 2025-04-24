#!/usr/bin/env python3
import datetime as dt
import sys
import pandas as pd
import numpy as np
import os


# write_samplesheets save the samplesheets after correcting index length for mixed
def write_samplesheet(full_sheet, samplesheet_path, read_length):
    date = dt.date.today()
    header = ['[Header],,,,,,,,,',
              'IEMFileVersion,4,,,,,,,,',
              'Investigator Name,seqWell,,,,,,,,',
              'Experiment Name,plexwell,,,,,,,,',
              'Date,' + str(date) + ',,,,,,,,',
              'Workflow,GenerateFASTQ,,,,,,,,',
              'Application,MiSeq FASTQ Only,,,,,,,,',
              'Assay,Nextera XT,,,,,,,,',
              'Description,,,,,,,,,',
              'Chemistry,Amplicon,,,,,,,,',
              read_length,
              read_length,
              '[Reads],,,,,,,,,',
              '[Settings],,,,,,,,,',
              '[Data],,,,,,,,,',
              'Sample_ID,Sample_Name,Sample_Plate,Sample_Well,I7_Index_ID,index,I5_Index_ID,index2,Sample_Project,Description']

    f = open(samplesheet_path, 'wt')

    for line in header:
        f.write(line + '\n')

  
    full_sheet.to_csv(f, index=False, header=False)
    f.close()
    return samplesheet_path







# make_custom return the samplesheet for a customized index input
def make_custom(plate_path):
    # import samplesheet
    ss = pd.read_csv(plate_path)

    # check for missing index
    groups = ss.groupby('Sample_Plate').count()
    for i in groups.index:
        n = groups.loc[i].Sample_Well
        for j in groups.loc[i].values:
            if j != 0 and j != n:
                raise ValueError('library ' + i + ' missing index')

    # fill in i5 or i7 with empty string
    if 'i7' not in ss.columns:
        ss['i7'] = ''
        ss['I7_Index_ID'] = ''
        ss['I5_Index_ID'] = ss['Sample_Well']
    elif 'i5' not in ss.columns:
        ss['i5'] = ''
        ss['I5_Index_ID'] = ''
        ss['I7_Index_ID'] = ss['Sample_Well']
    else:
        ss['I7_Index_ID'] = ss['Sample_Well']
        ss['I5_Index_ID'] = ss['Sample_Well']

    

    # check for illegal characters in sample name
    # name_check = len(ss) - ss.Sample_Plate.str.match("^[0-9]{6}-[a-zA-Z0-9-]*$").sum()
    name_check = len(ss) - ss.Sample_Plate.str.match("^[a-zA-Z0-9][a-zA-Z0-9-_]*$").sum()
    if name_check:
        raise ValueError('Sample_Plate value not accepted')

    # check for illegal characters in sample well
    name_check = len(ss) - ss.Sample_Well.str.match("^[a-zA-Z0-9]*$").sum()
    if name_check:
        raise ValueError('Sample_Well value not accepted')

    # check for duplicated index
    if ss.duplicated(subset=['i5', 'i7']).any():
        raise ValueError('i7/i5 index pair duplicated')

    

    # Sample_ID and Sample_Name will have the same value and identical for each sample
    ss['Sample_ID'] = ss['Sample_Plate'] + '_' + ss['Sample_Well']
    ss['Sample_Name'] = ss['Sample_Plate'] + '_' + ss['Sample_Well']
    if ss.Sample_Name.duplicated().any():
        raise ValueError('Sample_Name duplicate, check for Sample_Plate and Sample_Well duplications')

    ss['Sample_Project'] = ss['Sample_Plate'] + '_FASTQ'
    ss['Description'] = 'Custom'

    ss = ss[['Sample_ID', 'Sample_Name', 'Sample_Plate', 'Sample_Well', 'I7_Index_ID', 'i7', 'I5_Index_ID',
             'i5', 'Sample_Project', 'Description']]
    ss.columns = ['Sample_ID', 'Sample_Name', 'Sample_Plate', 'Sample_Well', 'I7_Index_ID', 'index', 'I5_Index_ID',
                  'index2', 'Sample_Project', 'Description']
    return ss

# parameter setting
plate = sys.argv[1]

out_path = os.path.basename(plate).split('.')[0] + '_samplesheet.csv'
length = '100'


# run make_custom if the input is a custom csv file
if plate.endswith('.csv'):
    sheet = make_custom(plate_path=plate)
    write_samplesheet(full_sheet=sheet, samplesheet_path=out_path, read_length=length)

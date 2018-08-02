from sub.excel2csv import excel2csv
import os
import parse_coding
import csv
import logging

# Script to preprocess data into standard format for analysis of looking time parameter
# impact.

baseDir = os.path.dirname(__file__)
# Keep record of any warnings about preprocessing
logging.basicConfig(filename=os.path.join(baseDir, 'Data', 'preprocess_data.log'), level=logging.INFO) 


# ******************** CSIBRA DATA ******************************************************
#    (expect to find Data/Csibra/Original/effhelp_PRF.xlsx with one sheet per child)

# Turn Csibra xlsx sheets into individual CSVs, named by sheetname 
csibra_csv_path = os.path.join(baseDir, 'Data', 'Csibra', 'csv')
csibra_xlsx = os.path.join(baseDir, 'Data', 'Csibra', 'Original', 'effhelp_PRF.xlsx')
sheets = excel2csv.get_all_sheets(csibra_xlsx)
sheets = [sh for sh in sheets if 'excl' not in sh and sh not in ['Data', 'Coding Template', 'Sheet1']]
excel2csv.csv_from_excel(csibra_xlsx, sheets, csibra_csv_path)

# Parse individual Csibra CSVs and  make a combined file for all kids
dataAllKids = []
for csv_fname in os.listdir(csibra_csv_path):
    (childCode, ext) = os.path.splitext(csv_fname)
    if ext == '.csv':
        markings = parse_coding.read_csibra_data(os.path.join(csibra_csv_path, csv_fname))
        addlMarks = {'Child': childCode, 'Coder': '', 'comment': '(null)'}
        fullMarks = [{**addlMarks, **m} for m in markings]
        dataAllKids += fullMarks
# Export all data to CSV
ofile = open(os.path.join(baseDir, 'Data', 'Csibra', 'combined_csibra.csv'), "w")
writer = csv.DictWriter(ofile, fieldnames=['Child', 'Coder', 'Time', 'Duration', 'TrackName', 'comment'], restval='')
writer.writeheader()
writer.writerows(dataAllKids)
ofile.close()
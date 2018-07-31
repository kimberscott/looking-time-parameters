from sub.excel2csv import excel2csv
import os
import parse_coding



baseDir = os.path.dirname(__file__)

# Turn Csibra xlsx sheets into individual CSVs, named by sheetname
def csibra_xlsx_to_csvs():
    csibra_xlsx = os.path.join(baseDir, 'Data', 'Csibra', 'Original', 'effhelp_PRF.xlsx')
    csibra_csv_path = os.path.join(baseDir, 'Data', 'Csibra', 'csv')
    sheets = excel2csv.get_all_sheets(csibra_xlsx)
    sheets = [sh for sh in sheets if 'excl' not in sh and sh not in ['Data', 'Coding Template', 'Sheet1']]
    excel2csv.csv_from_excel(csibra_xlsx, sheets, csibra_csv_path)



# csibra_xlsx_to_csvs()
parse_coding.read_csibra_data(os.path.join(baseDir, 'Data', 'Csibra', 'csv', '0108171630.csv'))
parse_coding.read_csibra_data(os.path.join(baseDir, 'Data', 'Csibra', 'csv', '0510171430.csv'))

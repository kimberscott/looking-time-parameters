from sub.excel2csv import excel2csv
import os

# Turn Csibra xlsx sheets into individual CSVs, named by sheetname

baseDir = os.path.dirname(__file__)
csibra_xlsx = os.path.join(baseDir, 'Data', 'Csibra', 'Original', 'effhelp_PRF.xlsx')
csibra_csv_path = os.path.join(baseDir, 'Data', 'Csibra', 'csv')
sheets = excel2csv.get_all_sheets(csibra_xlsx)
excel2csv.csv_from_excel(csibra_xlsx, sheets, csibra_csv_path)


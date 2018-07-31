import csv

# TODO: code >= 1 file manually and write tests

def read_csibra_data(csv_path):
    # Grab all data into lists
    with open(csv_path) as csvfile:
        reader = csv.reader(csvfile)
        alldata = [row for row in reader]
    # Headers for trials are in first column
    firstCol = [row[0].lower().strip() for row in alldata]
    trial1Row = firstCol.index('test trial 1')
    trial2Row = firstCol.index('test trial 2')
    recodingRow = firstCol.index('recoding') if 'recoding' in firstCol else 0
    # Make sure the trial rows we've gotten are for original coding, not recoding
    assert (not recodingRow) or (trial1Row < recodingRow and trial2Row < recodingRow)
    print((trial1Row, trial2Row))
    
    # TODO: fetch Begins/Ends time sequences for test trial 1, after trial end, between-trials; test trial 2, after trial end. 
    # (assert we see Begins, Ends in appropriate columns, MIN SEC FRAME headers under them)
    # TODO: fetch timing of attention-getter start from note
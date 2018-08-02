import csv, os, math, re

def read_csibra_data(csv_path):

    def getTime(msf): # sequence of minute, second, frame (30fps) -> time in ms
        if all([c.isnumeric() for c in msf]):
            return 1000 * (float(msf[0])*60 + float(msf[1]) + float(msf[2])/30)
        else:
            return float('nan')
            
    def getBeginEnd(row): # Columns A-C are begin, cols F-H are end
        return (getTime(row[0:3]), getTime(row[5:8]))
        
    # Grab all data into lists. Using simple csv reader instead of pandas because
    # data types are all mixed up anyway and easier to deal with by hand..
    with open(csv_path) as csvfile:
        reader = csv.reader(csvfile)
        alldata = [row for row in reader]
    # Headers for trials are in first column
    firstCol = [row[0].lower().strip() for row in alldata]
    
    # Get row inds for important separators
    trial1Row = firstCol.index('test trial 1')
    trial2Row = firstCol.index('test trial 2')
    trialEndRow = firstCol.index('% looked at test')
    recodingRow = firstCol.index('recoding') if 'recoding' in firstCol else 0
    
    # Make sure the trial rows are in expected order and do not include recoding
    assert trial1Row < trial2Row, "trial 2 before trial 1"
    assert trial2Row < trialEndRow, "trial end before trial 2"
    assert (not recodingRow) or (trialEndRow < recodingRow), "recoding before trials 1 and 2 found"
    
    # Get all the looking begins/ends throughout test trials & attention getter
    looking1 = [getBeginEnd(alldata[i]) for i in range(trial1Row, trial2Row)]
    looking2 = [getBeginEnd(alldata[i]) for i in range(trial2Row, trialEndRow)]
    looking = looking1 + looking2
    looking = [t for t in looking if not(math.isnan(t[0])) or not(math.isnan(t[1]))]
    
    # Fetch timing of attention-getter start, from note. Expect to find something like:
    #    attention-getter starts playing at 3:59,14
    notesCol =[row[12].lower().strip() for row in alldata]
    attNote = next(note for note in notesCol if 'attention-getter' in note)
    m = re.match(r'^.*(?P<min>[0-9]+):(?P<sex>[0-9]{2}),(?P<frame>[0-9]+)$', attNote)
    assert m, "No attention-getter timing note"
    attentionStart = getTime(m.groups())
    
    # Fetch timing of video end, from note. Expect to find something like:
    #    video ends at 4:23,22
    vidEndNote = next(note for note in notesCol if 'video ends' in note)
    m = re.match(r'^.*(?P<min>[0-9]+):(?P<sex>[0-9]{2}),(?P<frame>[0-9]+)$', vidEndNote)
    assert m, "No video end timing note"
    videoEnd = getTime(m.groups())
    
    # Get begin/end times of trials
    trials = [(looking[0][0], attentionStart), # first trial: first "begin" look, attention-getter start
              (next(begin for (begin, end) in looking2 if not math.isnan(begin)), videoEnd)] # second trial
              
    # Check that the last "begins" code is actually trial end, w/ missing "ends" value, & remove
    assert looking[-1][0] == videoEnd, "video end note does not line up with last coded value"
    assert math.isnan(looking[-1][1]), "coding does not end with begin / no end value"
    looking.pop()
    
    # Build the return object - starts/durations/labels.
    events = [{'TrackName': 'trial', 'Time': t1, 'Duration': t2-t1} for (t1, t2) in trials] + \
             [{'TrackName': 'looking', 'Time': t1, 'Duration': t2-t1} for (t1, t2) in looking]
    
    return events
    
read_csibra_data(os.path.join(os.path.dirname(__file__), 'Data', 'Csibra', 'csv', '2509171200.csv'))
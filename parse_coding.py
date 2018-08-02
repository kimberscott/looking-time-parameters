import csv, os, math, re
from warnings import warn
import logging


def read_csibra_data(csv_path):
    '''Read a coding file from Csibra dataset.
    
    See notes below for expected input format. Returns list of dicts with keys:
    TrackName: either 'trial' or 'looking'
    Time: onset of trial or look, in ms
    Duration: duration of trial or look, in ms
    comment: either '(null)' for looking times or trial number for trials.
    
    Child is assumed to be looking at start of Trial 1, so first look start and
    first trial start are the same. Trials are not continous (there's an attention-getter
    in between). 
    
    Explanation of input format from Laura Schlingloff:

    for clarification, I’m attaching a video of what a test sequence would look like 
    (unfortunately I can’t share one with an actual baby so easily, so you’ll have to 
    make do with an imaginary baby…). 
    Here, I would have coded the beginning of TEST TRIAL 1 (“Begins”) when the video starts
    (at 00:03:14); “Ends" when the video ends (so, after the ringing sound) (00:18:16), 
    “After trial end - Begins” at the next frame (00:18:17) and until the baby looks away 
    (“Ends”). Let’s say the fictional baby here starts looking away from the screen at 
    00:28:10 and then the attention gets drawn back to the screen a second after the 
    attention-getter starts. So the “Between-trials” coding would start (“Begins”) with 
    this look-back to the screen during the attention-getter, let’s say at 00:31:19, and 
    “Ends" when the second trial video starts (00:34:12). Then, same for TEST TRIAL 2: 
    “Begins” as the video starts (00:34:12), “Ends” as the video ends (00:49:14), “After 
    trial end - Begins” at the next frame (00:49:15) and until the baby looks away 
    (let’s say, fictional baby starts looking away at 00:57:00). Here, the recording ends 
    at 00:59:13, which would be the last number I put in the coding sheet.
    Basically, for each trial, the first coding is for when the action is still happening 
    (mainly I coded this to check for attention), and the second one (“After trial end”) is
    the looking time to the paused scene where nothing happens anymore. But they are 
    back-to-back: there is generally no look-away between these two codings!
    So answer your question 2: not entirely - “ends” for the first of the two codings 
    (so, looking during the video) can mean just the end of the video playing, as you can 
    see because the looking continues seamlessly in the “After trial end” section 
    afterwards. Here, the baby watched the entire video playing from 03:17:23 until 
    03:33:01, then continued looking until 03:37:16, looked away for .72 s, looked back at 
    03:38:09, and again away at 03:45:10. Then, the baby looked back at 03:48:01 while the 
    attention-getter was playing and continued to attend as the second trial started at
    03:51:11. The baby again watched the whole video until it ended at 04:06:14 and 
    continued watching the still frame until 04:08:09.

    TEST TRIAL 1												
                                                
    Begins 					Ends							
    MIN 	SEC	FRAME	TOT		MIN 	SEC	FRAME	TOT	TOT AWAY	Dif Looking		
    3	26	15	206.6		3	41	18	221.72		15.12		
                                            Sum Look		
                                            15.12		
    After trial end												
    Begins 					Ends							
    MIN 	SEC	FRAME	TOT		MIN 	SEC	FRAME	TOT	TOT AWAY	Dif Looking		
    3	41	19	221.76		3	59	4	239.16	0.8	17.4		
    3	59	24	239.96		4	6	10	246.4	1.88	6.44		
    4	8	7	248.28		4	11	6	251.24	#REF!	2.96		
                                            Sum Look		
                                            26.8		
                                                
    Between-trials (attention-getter)												
    Begins 					Ends							
    MIN 	SEC	FRAME	TOT		MIN 	SEC	FRAME	TOT	TOT AWAY	Dif Looking		
    4	14	2	254.08		4	16	6	256.24	-256.24	2.16		attention-getter starts playing at 4:13,18
                0					0	0	0		
                0					0	0	0		
                0					0	0	0		
                                            Sum Look		
                                            #REF!		

                                                
    TEST TRIAL 2												
                                                
    Begins 					Ends							
    MIN 	SEC	FRAME	TOT		MIN 	SEC	FRAME	TOT	TOT AWAY	Dif Looking		
    4	16	6	256.24		4	31	9	271.36		15.12		
                                            Sum Look		
                                            15.12		
    After trial end												
    Begins 					Ends							
    MIN 	SEC	FRAME	TOT		MIN 	SEC	FRAME	TOT	TOT AWAY	Dif Looking		
    4	31	10	271.4		4	39	21	279.84	1.6	8.44		
    4	41	11	281.44		4	50	18	290.72	0.96	9.28		
    4	51	17	291.68		5	5	11	305.44	1.32	13.76		
    5	6	19	306.76		5	9	10	309.4	2.52	2.64		
    5	11	23	311.92					0	0	-311.92		video ends at 5:11,23
                                            Sum Look		
                                            34.12		
    
    '''
    logging.info('Reading {}'.format(csv_path))

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
    m = re.match(r'^.*(?P<min>[0-9]+):(?P<sex>[0-9]+),(?P<frame>[0-9]+)$', attNote)
    assert m, "No attention-getter timing note"
    attentionStart = getTime(m.groups())
    
    # Fetch timing of video end, from note. Expect to find something like:
    #    video ends at 4:23,22
    vidEndNote = next(note for note in notesCol if 'video ends' in note)
    m = re.match(r'^.*(?P<min>[0-9]+):(?P<sex>[0-9]+),(?P<frame>[0-9]+)$', vidEndNote)
    assert m, "No video end timing note"
    videoEnd = getTime(m.groups())

    # Check that last code has no "end" mark, just "begin"
    if not math.isnan(looking[-1][1]):
        logging.warn("coding does not end with an unmatched begin value. Noted trial end: {}, last coding begin / end: {} / {}".format(videoEnd, looking[-1][0], looking[-1][1]))
    else: # If no last "end", check that "begins" is actually trial end, & remove
        if looking[-1][0] != videoEnd:
            logging.warn("video end note {} does not line up with singleton last coded value {}; using earlier one".format(videoEnd, looking[-1][0]))
            videoEnd = min(looking[-1][0], videoEnd)
        looking.pop()
    
    # Combine any looks where look 1 ends at the same time look 2 starts. Already in 
    # order so we can just loop through checking from the end
    for iLook in range(len(looking)-2, -1, -1):
        if looking[iLook][1] >= looking[iLook+1][0]:
            looking[iLook] = (looking[iLook][0], max(looking[iLook][1], looking[iLook+1][1]))
            looking.pop(iLook+1)
    
    # Get begin/end times of trials
    trials = [(looking[0][0], attentionStart, 1), # first trial: first "begin" look, attention-getter start
              (next(begin for (begin, end) in looking2 if not math.isnan(begin)), videoEnd, 2)] # second trial

    # Build the return object - starts/durations/labels.
    events = [{'TrackName': 'trial', 'Time': t1, 'Duration': t2-t1, 'comment': trialNum} for (t1, t2, trialNum) in trials] + \
             [{'TrackName': 'looking', 'Time': t1, 'Duration': t2-t1} for (t1, t2) in looking]
    
    return events
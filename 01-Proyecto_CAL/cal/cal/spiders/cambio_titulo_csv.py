import csv
import os

inputFileName = "horario1718.csv"
outputFileName = os.path.splitext(inputFileName)[0] + "_modified.csv"

with open(inputFileName, 'rb') as inFile, open(outputFileName, 'wb') as outfile:
    r = csv.reader(inFile)
    w = csv.writer(outfile)

    next(r, None)  # skip the first row from the reader, the old header
    # write new header
    w.writerow(['Subject','Start Date','Start Time','End Date','End Time','Location','All Day Event'])

    # copy the rest
    for row in r:
        w.writerow(row)
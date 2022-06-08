from pymarc import MARCReader,MARCWriter
from pymarc.field import Field
import csv
import re

def main():
    fname = input ("Enter the MARC filename: ")
    """Get each 773$w in each record and looks it up in the dictionary, removes the old Aleph ID and inserts the new MMS ID when it can.

    Additionally writes the update marc records to a new file and outputs as csv and mrc files records that
    recieved partial updates or no updates
    """
    alephs = open('773dictionary.csv', newline='', encoding='utf-8')
    alephlines = alephs.readlines()
    reader = csv.reader(alephlines, delimiter=',')
    dict773 = {}
    for row in reader:
        dict773[row[0]] = row[1]

    reader = MARCReader(open(fname, 'rb'), to_unicode=True, force_utf8=True)
    writer = MARCWriter(open('773updates.mrc', 'wb'))
    nochangewriter = MARCWriter(open('checkmanually.mrc', 'wb'))

    for record in reader:
        for f in record.get_fields('773'):
            if f.get_subfields('w'):
                for w in f.get_subfields('w'):
                    if 'Aleph' in w:
                        mmsid = dict773.get(w)
                        if mmsid is not None:
                            f.delete_subfield('w')
                            f.add_subfield('w', mmsid)
                        else:
                            with open('nochanges.csv', 'a', newline='') as csvfile:
                                output = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                                field001 = record['001']
                                f001 = re.sub("=001  ", "", str(field001))
                                output.writerow([w, f001])
        if mmsid is not None:
            writer.write(record)
        else:
            nochangewriter.write(record)

main()

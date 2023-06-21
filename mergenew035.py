from pymarc import MARCReader,MARCWriter
from pymarc.field import Field
import csv
import re

def main():
    fname = input ("Enter the primary record set MARC filename: ")
    """Get each 773$w in each record and looks it up in the dictionary, removes the old Aleph ID and inserts the new MMS ID when it can.

    Additionally writes the update marc records to a new file and outputs as csv and mrc files records that
    recieved partial updates or no updates
    """
    xrefs = open('xrefs.txt', newline='', encoding='utf-8')
    xreflines = xrefs.readlines()
    reader = csv.reader(xreflines, delimiter=',')
    dictxref = {}
    for row in reader:
        dictxref[row[0]] = row[1]

    reader = MARCReader(open(fname, 'rb'), to_unicode=True, force_utf8=True)
    writer = MARCWriter(open('xrefmerged.mrc', 'wb'))
    nochangewriter = MARCWriter(open('checkmanually.mrc', 'wb'))

    for record in reader:
        my_record = deepcopy(record)
        new_035_field = Field(
               tag = '035'
               subfields = ['a', ]
        )
        zerozeroone = record.get_fields('001')
        mmsid = '{}'.format(zerozeroone)
        new35 = dictxref.get(mmsid)

        new_035_field = Field(
               tag = '035',
               indicators = ['\','\'],
               subfields = ['a', new35 ]
        )

        my_record.add_ordered_field(new_035_field)
        if mmsid is not None:
            writer.write(record)
        else:
            nochangewriter.write(record)

main()

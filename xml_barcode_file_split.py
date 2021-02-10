import pymarc as pymarc
from pymarc import MARCReader,MARCWriter
from pymarc.field import Field
import re

def listToString(list):
    str1 = " "
    return (str1.join(list))

fname = input("MARC filename: ")

reader = MARCReader(open(fname, 'rb'), to_unicode=True, force_utf8=True)

for record in reader:
    for b in record.get_fields('954'):
        if b.get_subfields('5'):
            barcode = b.get_subfields('5')
            outName = listToString(barcode)
            outNameClean = re.sub(r'\[\]', "", str(outName))
            #print(outNameClean)
            with open(outNameClean + '.xml', 'wb') as processed:
                xml_record = pymarc.record_to_xml(record)
                processed.write(xml_record)

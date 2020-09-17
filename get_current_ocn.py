import urllib
from urllib import request
from urllib.request import urlopen
import csv
import re
from tqdm import tqdm
from lxml import etree
import xml.etree.ElementTree as ET

def main():
    wskey = input("Enter your WorldCat Search API wskey for this session: ")
    fname = input ("Enter the spreadsheet filename: ")
    run = input ("Which file run are you on?: ") #helps with quota issues
    report_name = 'ocn_ht_oclc_lookup_report.csv'
    with open(fname) as csv_file:
        reader = csv.reader(csv_file, delimiter='\t')
        header = next(reader)
        if header != None:
            for row in tqdm(reader, desc="Progress", unit=" rows"):
                ocn = row[0]
                if ocn.isdigit():
                    lookupUrl = "http://www.worldcat.org/webservices/catalog/content/" + ocn + "?wskey=" + wskey
                    query_wc = urlopen(lookupUrl)
                    record_data = ET.parse(query_wc)
                    root = record_data.getroot()
                    oclc = root[1].text

                    with open(report_name, 'a', newline='') as outfile:
                        output = csv.writer(outfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        if oclc:
                            output.writerow([ocn, oclc])
                        else:
                            nothing = "No Items" #change this to your preference
                            output.writerow([ocn, oclc])

main()

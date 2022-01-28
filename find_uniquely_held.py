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
    report_name = 'titles_with_holdings_count.csv'
    with open(fname) as csv_file:
        reader = csv.reader(csv_file, delimiter='\t')
        header = next(reader)
        if header != None:
            for row in tqdm(reader, desc="Progress", unit=" rows"):
                ocn = row[0]
                if ocn.isdigit():
                    memberCount = 0
                    lookupUrl = "http://www.worldcat.org/webservices/catalog/content/libraries/" + ocn + "?maximumLibraries=100" + "?wskey=" + wskey
                    query_wc = urlopen(lookupUrl)
                    record_data = ET.parse(query_wc)
                    root = record_data.getroot()
                    holdings = root.findall('holding')
                    for holding in holdings:
                        memberCount += 1

                    with open(report_name, 'a', newline='') as outfile:
                        output = csv.writer(outfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        if memberCount:
                            output.writerow([ocn, memberCount])
                        else:
                            nothing = "No Items" #change this to your preference
                            output.writerow([ocn, memberCount])

main()

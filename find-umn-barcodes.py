import json
import urllib
from urllib import request
from urllib.request import urlopen
import csv
import re
from tqdm import tqdm

def get_items(record_data):
    list_items = []
    regexp = re.compile(r'^umn*') #change this to your prefix
    for item in record_data['items']:
        htid = item.get('htid')
        if regexp.search(htid):
            list_items.append(htid)
    return(list_items)

def main():
    fname = input ("Enter the spreadsheet filename: ")
    run = input ("Which file run are you on?: ") #helps with quota issues
    report_name = 'itemreport' + run + '.csv'
    with open(fname) as csv_file:
        reader = csv.reader(csv_file, delimiter='\t')
        header = next(reader)
        if header != None:
            for row in tqdm(reader, desc="Progress", unit=" rows"):
                ocn = row[0]
                mms = row[1]
                if ocn.isdigit():
                    lookupUrl = "https://catalog.hathitrust.org/api/volumes/brief/oclc/"
                    url_full = lookupUrl + ocn + ".json"
                    query_ht = urlopen(url_full)
                    record_data = json.loads(query_ht.read())
                    #ht_record_id = get_record_id(record_data)
                    list_items = get_items(record_data)
                    umn_items = ' '.join([str(x) for x in list_items])
                    with open(report_name, 'a', newline='') as outfile:
                        output = csv.writer(outfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        if umn_items:
                            output.writerow([ocn, mms, umn_items])
                        else:
                            nothing = "No UMN Items" #change this to your preference
                            output.writerow([ocn, mms, nothing])

if __name__ == "__main__":
    main()

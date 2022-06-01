
'''This script updates OCLC numbers in Alma bibliographic records based on the OCLC
Datasync cross-reference report *xrefrpt.txt. Based on that file, the script fetches
each record via the Alma bib API, adds or changes the OCLC number in the MARCXML record, 
and replaces the Alma bib record with the updated record. It can be used instead of the 
datasync_xref.py script, which produces files for manual Alma jobs that accomplish the same
thing.'''

import csv
import re
import os
import requests
import pyaml
from lxml import etree


def get_apikey():
    config = pyaml.yaml.safe_load(open('config.yml'))
    apikey = config.get('apikey')
    return apikey


def create_xref_dict(xref_file):
	f = open(xref_file, 'r')
	reader = f.read()
	lines = reader.split('\n')	
	xref_dict = {}
	for line in lines:
		try:
			xref = line.split('\t')
			xref_dict[xref[0]] = xref[1]
		except IndexError:
			next
	return xref_dict


def get_bib_record(mmsid, apikey):
		urlroot = "https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs"
		get_headers = {'Accept': 'application/xml', 'Authorization': 'apikey ' + apikey}
		get_url = urlroot + '?mms_id=' + mmsid + '&view=full&expand=None'
		get_bib_response = requests.get(get_url, headers=get_headers)
		if get_bib_response.status_code != 200:
			return 0
		else:
			return get_bib_response


def update_bib_ocn(get_bib_response, upd_ocn):
	full_tree = etree.fromstring(get_bib_response.content)
	bib_tree = full_tree.find('.bib')
	if bib_tree is not None:
		rec_tree = bib_tree.find('.record')

		def add_oclc035(rec_tree):
			#Function to add a new 035 field when conditions are met
			new035 = etree.Element('datafield', ind1=' ', ind2=' ', tag='035')
			rec_tree.append(new035)
			for field in [field for field in rec_tree.xpath(".//datafield[@tag='035']")]:
				subfields = field.getchildren()
				if len(subfields) == 0:
					new035a = etree.SubElement(field, 'subfield', code='a')
					new035a.text = '(OCoLC)' + upd_ocn
			return rec_tree

		oclc = re.compile('.*OCoLC.*')
		fields = rec_tree.xpath(".//datafield[@tag='035']")
		if len(fields) == 1:
			#Check for existing OCLC 035 in a record with 1 035 field and update if exists
			for subfield_a in [subfield_a for subfield_a in rec_tree.xpath(".//datafield[@tag='035']/subfield[@code='a']") if subfield_a is not None]:
				if oclc.match(subfield_a.text):
					subfield_a.text = '(OCoLC)' + upd_ocn
				else:
					add_oclc035(rec_tree)
		elif len(fields) > 1:
			#Check for existing OCLC 035 in a record with >1 035 field and update if exists
			for subfield_a in [subfield_a for subfield_a in rec_tree.xpath(".//datafield[@tag='035']/subfield[@code='a']") if oclc.match(subfield_a.text) is not None]:
				subfield_a.text = '(OCoLC)' + upd_ocn
			#Get content of all 035a subfields and add new OCLC 035 if none exists
			subfields = rec_tree.xpath(".//datafield[@tag='035']/subfield[@code='a']")
			oclc_check_list = []
			for subfield in subfields:
				oclc_check_list.append(subfield.text)
			oclc_check = ' '.join(oclc_check_list)
			if oclc.match(oclc_check) is None:
				add_oclc035(rec_tree)
		else:
			#Add new OCLC 035 when no 035 exists
			add_oclc035(rec_tree)

		updated_record = etree.tostring(bib_tree, encoding='utf-8')
		return updated_record
	else:
		return 0


def put_updated_bib(updated_record, mmsid, apikey):
	put_headers = {'Content-Type': 'application/xml', 'Authorization': 'apikey ' + apikey}
	urlroot = "https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs"
	put_url = urlroot + '/' + mmsid
	put_response = requests.put(url=put_url, data=updated_record, headers=put_headers)
	if put_response.status_code != 200:
		return 0
	else:
		return 1


def main():
	#flist = [f for f in os.listdir() if re.match('.*[0-9]\x2Exrefrpt.*', f)]
	fname = input("Enter file name of MMS Ids and OCNS: ")
	try:
		#fname = str(flist[0])
		xref_dict = create_xref_dict(fname)
		apikey = get_apikey()
		success_count = 0
		failed_count = 0
		total_count = 0
		with open('ocn_update_error_log.txt', 'w+') as error_log:
			for mmsid, upd_ocn in xref_dict.items():
				get_bib_response = get_bib_record(mmsid, apikey)
				total_count += 1
				if get_bib_response != 0:
					updated_record = update_bib_ocn(get_bib_response, upd_ocn)
					if updated_record != 0:
						put_response = put_updated_bib(updated_record, mmsid, apikey)
						if put_response == 0:
							error_log.write(mmsid + '\t' + upd_ocn + '\t' + 'Put record failed' + '\n')
							failed_count += 1
						else:
							print(mmsid + ' OK')
							success_count += 1
					else:
						error_log.write(mmsid + '\t' + upd_ocn + '\t' + 'Record not found' + '\n')
						failed_count += 1
				else:
					error_log.write(mmsid + '\t' + upd_ocn + '\t' + 'Get record failed' + '\n')
					failed_count += 1
		print(str(total_count) + ' updates attempted.')
		print(str(success_count) + ' records updated successfully.')
		print(str(failed_count) + ' records failed.')
		
	except IndexError:
		print('xrefrpt file not found. Exiting.')
		exit()

if __name__ == '__main__':
	main()
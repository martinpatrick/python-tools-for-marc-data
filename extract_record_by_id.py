import pymarc
from pymarc import MARCReader, MARCWriter, Field
import re
import csv


identifier = input("001 or 035?")
marcname = input("Enter the source MARC filename: ")
new_marcname = re.sub(".mrc", "", str(marcname))
csvname = input("Enter the CSV or txt filename of identifiers: ")
kind = input("Do you want to extract records on your list or not on your list? (enter ON or NOT): ")


if kind == "NOT":
	with open(csvname, newline='') as f:
		reader = csv.reader(f)
		vList = list(reader)

		read_records = MARCReader(open(marcname, 'rb'), to_unicode=True, force_utf8=True)
		write_records = MARCWriter(open('recs_extracted_from_' + new_marcname + '.mrc', 'wb'))
		if identifier == "001":
			for rec in read_records:
				field001 = rec['001']
				f001 = re.sub("=001	 ", "", str(field001))
				try:
					found = vList.index([f001])
					write_records.write(rec)
				except ValueError:
					continue

		else: #elif identifier == "035":
			for rec in marcreader:
				field035 = rec.get_fields("035")
				for field in field035:
					suba035 = field.get_subfields("a")
					for suba in suba035:
						try:
							found = vList.index([suba])
							write_records.write(rec)
						except ValueError:
							continue


else:
	with open(csvname, newline='') as f:
		reader = csv.reader(f)
		vList = list(reader)

		read_records = MARCReader(open(marcname, 'rb'), to_unicode=True, force_utf8=True)
		write_records = MARCWriter(open('recs_extracted_from_' + new_marcname + '.mrc', 'wb'))
		if identifier == "001":
			for rec in read_records:
				field001 = rec['001']
				f001 = re.sub("=001  ", "", str(field001))
				try:
					found = vList.index([f001])
					write_records.write(rec)
				except ValueError:
					continue


		elif identifier == "035":
			for rec in marcreader:
				field035 = rec.get_fields("035")
				for field in field035:
					suba035 = field.get_subfields("a")
					for suba in suba035:
						try:
							found = vList.index([suba])
							write_records.write(rec)
						except ValueError:
							continue
		elif identifier == "020":
			for rec in marcreader:
				field020 = rec.get_fields("020")
				for field in field020:
					suba020 = field.get_subfields("a")
					#regex here to only look at the actual numbers
					for suba in suba020:
						try:
							found = vList.index([suba])
							write_records.write(rec)
						except ValueError:
							continue



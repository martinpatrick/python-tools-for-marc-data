import os
import re
import pymarc
from pymarc import MARCReader, MARCWriter, Record
from datetime import date

today = str(date.today())

MARCfile = input("Enter the source MARC filename: ")
fname_str = str(MARCfile)
fpref, fsuf = fname_str.split('.')
yourId = input("Enter your ID for 909: ")
marc930 = input("Enter 930 phrase (enter none if leaving empty): ")
marc931 = input("Enter 931 phrase (enter none if leaving empty): ")
marc035 = input("Build identifier from 001 yes or no? ")

with open(MARCfile,'rb') as f:
	reader = MARCReader(f)
	
	writer_edits = MARCWriter(open(fpref + '_edits.mrc', 'wb'))
	
	for rec in reader:
	#evaluate 006/007 situation
	#evaluate 300 field
	#evaluate identifier situation
	#evaluate 4xx/8xx 

	#add 9xx fields
        field_909 = pymarc.Field(
        	tag = '909',
            indicators = [' ',' '],
            subfields = ['a', 'bcat', 'b', 'MNU', 'c', today, 'd', yourId])

        rec.add_ordered_field(field_909)
        
        if marc930 =! 'none':
        	field_930 = pymarc.Field(
        		tag = '930',
            	indicators = [' ',' '],
            	subfields = ['a', 'marc930])

        	rec.add_ordered_field(field_930)
        
        if marc931 =! 'none':
        	field_931 = pymarc.Field(
        		tag = '931',
            	indicators = [' ',' '],
            	subfields = ['a', 'marc931])

	        rec.add_ordered_field(field_930)
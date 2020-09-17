# python_marc_extractors
 Various python scripts and notebooks to extract MARC data

**extract_record_by_id.py** will extract records from a given mrc file based on a list of identifiers for 001 or 035 to a new mrc file. I got frustrated with the relative clunk of MarcEdit's implementation of the file search feature in the extract records function, so I wrote a little script to do it for me for identifiers. This could someday be expanded to include ISBNs or ISSNs. The list you feed it should be one column only with each identifier on its own line.

**issn extractor.ipynb** will extract to a csv and pkl file the issns present in the records in the file.

**oclc extractor.ipynb** will extract to a csv and pkl file the OCLC#s present in the records in the file. This file lets you choose whether the OCLC numbers are stored in the 001 (that is, you just downloaded these files directly from OCLC or another vendor who supplies OCLC#s in the 001 field) or the 035, such as directly from Alma.

**id_marc_problem.py** script has been copied from https://github.umn.edu/trail001. The jupyter notebooks here will fail if they encounter an unicode character in the indicators of a field in a record. This script allows you to find the record that is problematic. Please read the comments at the head of the file closely. I have occasionally run into problems when using the MARC Edit OCLC bib file reader plugin to extract large amounts of records from OCLC with this problem and needed to use this script to clean them up.

**get_current_ocn.py** this script takes a file of just oclc numbers and looks that up against worldcat search api to get the oclc current primary record number. you'll need a production wskey from oclc for this to work properly. i haven't built in anything to handle timeouts.
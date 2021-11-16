import pandas as pd

file_name = input('Copy and paste the full filename: ')
file = pd.read_csv(file_name, sep='\t')
title_count = len(file)
missing_count = len(file[file['oclc_number'] == ''])
print(str(missing_count) + " out of " + str(title_count) + " lack OCLC Numbers")

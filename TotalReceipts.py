#!/usr/bin/env python3
import os
import glob
import re
from decimal import *

# set the cwd to the same folder the file is run in 
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Check paths and files
mboxPath = dname + '/Emails/'
if(not os.path.isdir(mboxPath)):
	raise NotADirectoryError('mboxPath of ' + mboxPath + ' not found')

mboxFiles = glob.glob(mboxPath + '*.mbox')

# Open the mbox file and loop over each email, checking for totals
for mboxFile in mboxFiles:
	if(not os.path.isfile(mboxFile)):
		raise FileNotFoundError('Could not open file ' + mboxFile)
	
	with open(mboxFile) as f:
		fileName = os.path.basename(mboxFile)
		
		print('TOTALS FOR ' + fileName)
		
		totalUSD = []
		totalYEN = []
		
		contents = f.read()
		
		emails = contents.split('From ')
		# First element is empty so we can discard
		del emails[0]
		
		print('Email count (' + str(len(emails)) + ')')
		
		for email in emails:
			readable = email.split('quoted-printable')[1].replace('=\n', '')
			try:
				# If this is successful it means it was either US or converted to USD
				totalAfter = readable.split('Total')[1]
				totalIsolated = re.search(r'\d+\.\d+', totalAfter).group()
				
				# Add total to list
				totalUSD.append(Decimal(totalIsolated))
				# print(str(totalIsolated) + ' (' + str(sum(totalUSD)) + ')')
			except:
				# Going to have to put an exception for yen here :)
				try:
					totalAfter = readable.split('Total')[1].split('JP=C2=A5')[1]
					# print('YEN SPLIT SUCCESSFUL')
					totalIsolated = re.search(r'\d+(\,\d+)?', totalAfter).group()
					
					# Add total to list
					totalYEN.append(int(totalIsolated.replace(',', '')))
					
					# print(str(totalIsolated) + ' (' + str(sum(totalYEN)) + ')')
				except:
					# Email was not formatted in a way that was expected
					print('Printing readable')
					print(readable)
					raise Exception('Could not split successfully')
		
		print('-- Purchases --')
		print('Total USD: ' + str(sum(totalUSD)))
		print('USD Purchase Count: ' + str(len(totalUSD)))
		print('Total YEN: ' + str(sum(totalYEN)))
		print('YEN Purchase Count: ' + str(len(totalYEN)))
		print('---------------------------------\n')
import MySQLdb
from collections import defaultdict
import re
import operator
import itertools



escape_dict={'\a':r'\a',
           '\b':r'\b',
           '\c':r'\c',
           '\f':r'\f',
           '\n':r'\n',
           '\r':r'\r',
           '\t':r'\t',
           '\v':r'\v',
           '\'':r'\'',
           '\"':r'\"',
           '\0':r'\0',
           '\1':r'\1',
           '\2':r'\2',
           '\3':r'\3',
           '\4':r'\4',
           '\5':r'\5',
           '\6':r'\6',
           '\7':r'\7',
           '\8':r'\8',
           '\9':r'\9'}

def raw(text):
    """Returns a raw string representation of text"""
    new_string=''
    for char in text:
        try: new_string+=escape_dict[char]
        except KeyError: new_string+=char
    return new_string



db = MySQLdb.connect(host="10.0.0.125", # your host, usually localhost
						 user="Lydia", # your username
						  passwd="voxpop", # your password
						  db="voxpop") # name of the data base       
						  
cur = db.cursor()

query ="SELECT itemText FROM newsitems WHERE sourceType = 2 or sourceType = 4 or sourceType = 5 LIMIT 1000"

cur.execute(query)
expr1 = re.compile("Mark Rutte")
expr2 = re.compile("M. Rutte")
regex = '\b(Mark|M\.)\s+Rutte\b'
expr3 = re.compile(regex)
expr4 = re.compile(raw(regex))

freqRutte = 0
freqRutteReg = 0
freqRutteReg2 = 0

for item in cur.fetchall():
	text = item[0]	
	result1 = re.search(expr1, text)
	result2 = re.search(expr2, text)
	result3 = re.search(expr3, text)
	result4 = re.search(expr4, text)
	
	if result1 != None or result2 != None:
		freqRutte+=1
	if result3 != None:
		freqRutteReg += 1
	if result4 != None:
		freqRutteReg2 += 1
	
	
print "frequentie Mark Rutte = ", freqRutte, "frequentie met regex =", freqRutteReg, "en", freqRutteReg2


		

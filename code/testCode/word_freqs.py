import MySQLdb
import nltk
import string
from nltk.corpus import stopwords
from collections import defaultdict
import re

def get_counts():
	db = MySQLdb.connect(host="10.0.0.125", # your host, usually localhost
						 user="Lydia", # your username
						  passwd="voxpop", # your password
						  db="voxpop") # name of the data base       
						  
	# you must create a Cursor object. It will let
	#  you execute all the queries you need
	cur = db.cursor()

	# Columns: 5 = itemText
	# Use all the SQL you like
	# Sourcetypes: 1 = algemeen, 2 = politiek, 3 = business

	print "Get items from database"
	cur.execute("SELECT itemText FROM newsitems WHERE sourceType = 2 LIMIT 5000")
	#cur.execute("SELECT itemText FROM newsitems WHERE sourceType = 2")
	print "selection made"

	stop_words = stopwords.words('dutch')
	has_digits = re.compile('\d')
	
	# init dictionary
	freq = defaultdict(int)

	nr_docs = 0
	nr_words = 0
	nr_functional_words = 0
	for count, row in enumerate(cur.fetchall()):
		nr_docs += 1
		if len(row) == 1:
			text = nltk.word_tokenize(row[0])	
			
			for w in text:
				nr_words +=1
				if w not in string.punctuation and w not in stop_words and (not bool(has_digits.search(w))  ):
					
					w2 = w.translate(string.maketrans("",""), string.punctuation)
					w2 = w2.lower()	
						
					# Update count and if necessary add to dict
					if w2 != "":				
						freq[w2] += 1
						nr_functional_words +=1
			
		else:
			print "lengte is niet goed"
			print len(row)
		if count%1000 == 0:
			print count, "files processed"
			
	# Counts and list of words to file
	
	print "data processed, read to file"
	f = open('wordFrequencies.txt', 'w')
	count = 0
	for key, value in freq.iteritems():
		count += 1
		f.write( key + " " + str(value) + "\n")

	print "nr of documents", nr_docs
	print "total nr of words", nr_words
	print "nr of functional words", nr_functional_words 
	print "nr of unique words", count

if __name__ == "__main__":
	get_counts()
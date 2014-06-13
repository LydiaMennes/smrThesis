from __future__ import division
import MySQLdb
import datetime
from collections import defaultdict
import string

def read_landscape(landscape_file):
	# return grid with words and 
	# defaultdict with true values for landscape words and false as default
	return None
	
def get_frequencies(landscape, word_dict):

	db = MySQLdb.connect(host="10.0.0.125", # your host, usually localhost
						 user="Lydia", # your username
						  passwd="voxpop", # your password
						  db="voxpop") # name of the data base       
						  
	cur = db.cursor()

	# Sourcetypes: 1 = algemeen, 2 = politiek, 3 = business

	print "Get items from database"	
	query = "SELECT itemText, pubDate FROM newsitems WHERE sourceType = 2"
	cur.execute(query)
	print "selection made"	
	silly_words = ["image", "afbeelding", "reageer"]
	
	# init dictionary
	freqs = defaultdict(lambda: defaultdict(int))
	
	for row in enumerate(cur.fetchall()):
		s = row[1][0]
		s = unicodedata.normalize('NFKD', s.decode('unicode-escape')).encode('ascii', 'ignore')
		s = s.replace("\n", "")
		s = s.translate(None, string.punctuation)
		text = s.split(" ")
		date = row[1][1].date()
				
		for word in text:	
			if len(word)!=1 and word != "" and word not in stop_words and not bool(has_digits.search(word)) and word not in silly_words:				
				word = word.lower()
				if word_dict[word]:
					freqs[word][date] += 1
		
	return freqs

def calc_correlations(freqs):
	return None

def evaluate_sem(landscape_file):
	landscape, word_dict = read_landscape(landscape_file)
	freqs = get_frequencies(landscape, word_dict)
	del word_dict
	corr = get_correlations(freqs):
	
	
if __name__ == "__main__":
	folder = r"D:\Users\Lydia\results puzzle"

	data_case = r"limit1000_nolog"
	evaluate_sem(folder+data_case)
from __future__ import division
import MySQLdb
import datetime
from collections import defaultdict
import string
from thesis_utilities import *
import numpy as np
import unicodedata

folder = r"D:\Users\Lydia\results puzzle"

def read_landscape(landscape_file):
	# return grid with words and 
	# defaultdict with true values for landscape words and false as default
	grid = grid_from_file(landscape_file)
	
	word_dict = defaultdict(lambda: False)
	for x, grid_d in grid.iteritems():
		for y, elem in grid_d.iteritems():
			word_dict[elem.name] = True
	return grid, word_dict
	
def get_frequencies(landscape, word_dict):

	db = MySQLdb.connect(host="10.0.0.125", # your host, usually localhost
						 user="Lydia", # your username
						  passwd="voxpop", # your password
						  db="voxpop") # name of the data base       
						  
	cur = db.cursor()

	# Sourcetypes: 1 = algemeen, 2 = politiek, 3 = business
	stop_words = get_parabots_stopwords()
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
			if len(word)!=1 and word != "" and word not in stop_words and not has_digits(word) and word not in silly_words:				
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
	corr = calc_correlations(freqs)
	
	
if __name__ == "__main__":	
	data_case = r"\test3"
	landscape_name = r"\grid_stats_init3_tr201_itLAST.txt"
	input = folder + data_case
	evaluate_sem(folder+data_case+ landscape_name)
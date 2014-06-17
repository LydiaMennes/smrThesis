from __future__ import division
import MySQLdb
import datetime
from collections import defaultdict
import string
from thesis_utilities import *
import numpy as np
import unicodedata
import argparse

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
	# query = "SELECT itemText, pubDate FROM newsitems WHERE sourceType = 2"
	query = "SELECT itemText, pubDate FROM newsitems WHERE sourceType = 2 LIMIT 100"
	cur.execute(query)
	print "selection made"	
	silly_words = ["image", "afbeelding", "reageer"]
	# no_date = datetime.date(0,0,0)
	
	# init dictionary
	freqs = defaultdict(lambda: defaultdict(int))
	min_date,max_date = 0,0
	first = True
	for row in enumerate(cur.fetchall()):
		s = row[1][0]
		s = unicodedata.normalize('NFKD', s.decode('unicode-escape')).encode('ascii', 'ignore')
		s = s.replace("\n", "")
		s = s.translate(None, string.punctuation)
		text = s.split(" ")
		date = row[1][1].date()
		if first:
			first = False
			min_date = date
			max_date = date
		if date > max_date:
			max_date = date
		if date < min_date:
			min_date = date
		for word in text:	
			if len(word)!=1 and word != "" and word not in stop_words and not has_digits(word) and word not in silly_words:				
				word = word.lower()
				if word_dict[word]:
					freqs[word][date] += 1
		
	return freqs, min_date, max_date

def calc_correlations(freqs, min_date, max_date):
	dt = datetime.timedelta(1)
	
	return None
	
def to_file(corr):
	print "NOT YET IMPLEMENTED"

def evaluate_sem(folder, landscape_file):
	landscape, word_dict = read_landscape(folder+landscape_file)
	freqs, mindate, maxdate = get_frequencies(landscape, word_dict)
	del word_dict
	corr = calc_correlations(freqs, min_date, max_date)
	to_file(folder)
	
	
if __name__ == "__main__":	

	parser = argparse.ArgumentParser(description='Run puzzle algorithm')
	# '''parser.add_argument(<naam>, type=<type>, default=<default>, help=<help message>)'''
	parser.add_argument("case_name", help="Name of the data case that you want to process")
	parser.add_argument("landscape", help="The number of words in the data case")
	
	args = parser.parse_args()
	kwargs = vars(args)	
	
	print "\n\n\n"
	print kwargs
	
	data_case = "\\" + kwargs["case_name"]
	landscape_name = "\\"+kwargs["landscape"]	
	
	
	evaluate_sem(folder+data_case, landscape_name)
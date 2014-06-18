from __future__ import division
import MySQLdb
import datetime
from collections import defaultdict
import string
from thesis_utilities import *
import numpy as np
import unicodedata
import argparse
import math

folder = r"D:\Users\Lydia\results puzzle"
no_date = datetime.date(1,1,1)

def read_landscape(landscape_file):
	# return grid with words and 
	# defaultdict with true values for landscape words and false as default
	grid = grid_from_file(landscape_file)
	
	word_dict = defaultdict(lambda: False)
	for x, grid_d in grid.iteritems():
		for y, elem in grid_d.iteritems():
			word_dict[elem.name] = True
	return grid, word_dict
	
def get_frequencies(word_dict):

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
	
	# init dictionary
	freqs = defaultdict(lambda: defaultdict(int))
	min_date,max_date = 0,0
	first = True
	for row in enumerate(cur.fetchall()):
		date = row[1][1].date()
		if date != no_date:
			s = row[1][0]
			s = unicodedata.normalize('NFKD', s.decode('unicode-escape')).encode('ascii', 'ignore')
			s = s.replace("\n", "")
			s = s.translate(None, string.punctuation)
			text = s.split(" ")
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

def build_freq_vect(f, min_date, max_date):
	dt = datetime.timedelta(1)
	if f != None:		
		vec_len = (max_dat-min_date).days
		vect = np.zeros(vec_len)
		cur_date = copy.deepcopy(min_date)
		index = 0
		while cur_date <= max_date:
			vect[index] = f[cur_date]
			if f[cur_date] == 0:
				del f[cur_date]
			cur_date=cur_date+dt
			index+=1
		return vect
			
	return None
		
	
def calc_correlations(freqs, min_date, max_date, landscape, grid_size):
	freqs[None] = None
	neighs = [[0,1],[1,1],[1,0]]	
	# correlations = [sum corr coeff, nr_neighbors]
	correlations = defaultdict(lambda: np.array([0,0]))
	avg_corr = 0
	nr_words = 0
	repr = defaultdict(defaultdict(lambda: None))
	for i in range(grid_size-1):
		repr[0][0] = build_freq_vect(freqs[landscape[i][0]], min_date, max_date)
		repr[1][0] = build_freq_vect(freqs[landscape[i+1][0]], min_date, max_date)
		for j in range(grid_size-1):
			repr[0][1] = build_freq_vect(freqs[landscape[i][j+1]], min_date, max_date)
			repr[1][1] = build_freq_vect(freqs[landscape[i+1][j+1]], min_date, max_date)
			if landscape[i][j]!=None:
				nr_words+=1
				for [ni, nj] in neighs:
					# calc correlations if neighbor niet = None
					if repr[ni][nj]!= None:
						result = np.array([0,1])
						result[0] = np.corr_coef(repr[0][0], y = repr[ni][nj])[0,1]
						correlations[landscape[i][j]] += result
						correlations[landscape[i+ni][j+nj]] += result
				correlations[landscape[i][j]] = correlations[landscape[i][j]][0]/correlations[landscape[i][j]][1] 
				avg_corr += correlations[landscape[i][j]]
			repr[0][0] = repr[0][1]
			repr[1][0] = repr[1][1]
	#process edges!!!!
	for i in range(grid_size):
		if landscape[i][grid_size-1]!= None:
			nr_words+=1
			correlations[landscape[i][grid_size-1]] = correlations[landscape[i][grid_size-1]][0]/correlations[landscape[i][grid_size-1]][1] 
			avg_corr += correlations[landscape[i][grid_size-1]]
		if landscape[grid_size-1][i]!= None and i!=grid_size-1:
			nr_words+=1
			correlations[landscape[grid_size-1][i]] = correlations[landscape[grid_size-1][i]][0]/correlations[landscape[grid_size-1][i]][1] 
			avg_corr += correlations[landscape[grid_size-1][i]]
	return correlations, avg_corr/nr_words
	
def to_file(corr):
	print "NOT YET IMPLEMENTED"

def evaluate_sem(folder, landscape_file):
	landscape, word_dict = read_landscape(folder+landscape_file)
	freqs, mindate, maxdate = get_frequencies(word_dict)	
	del word_dict
	corr = calc_correlations(freqs, min_date, max_date, landscape)
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
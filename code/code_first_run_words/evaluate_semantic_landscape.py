from __future__ import division
import oursql
import datetime
from collections import defaultdict
import string
from thesis_utilities import *
import numpy as np
import unicodedata
import argparse
import math
import matplotlib.pyplot as plt
import copy
import sys
import os

input_folder = r"D:\Users\Lydia\results puzzle"
output_folder = r"D:\Users\Lydia\results_freqs"
no_date = datetime.date(1,1,1)
query = "SELECT itemText, pubDate FROM newsitems WHERE sourceType = 2"
log_day_freqs = False
figure_size = 8

def read_landscape(landscape_file):
	# return grid with words and 
	# defaultdict with true values for landscape words and false as default
	grid = grid_from_file(landscape_file)

	word_dict = defaultdict(lambda: (False,-1,-1))
	grid_size = 0
	for x, grid_d in grid.items():
		grid_size+=1
		for y, elem in grid_d.items():
			if elem != None:
				word_dict[elem] = (True, x, y)
	return grid, word_dict, grid_size

def get_frequencies(word_dict):

	conn = oursql.connect(host="10.0.0.125", # your host, usually localhost
						 user="Lydia", # your username
						  passwd="voxpop", # your password
						  db="voxpop",
						  use_unicode=False)
	curs = conn.cursor(oursql.DictCursor)
	# result = curs.execute('SELECT * FROM `some_table` WHERE `col1` = ? AND `col2` = ?',(42, -3))

	# Sourcetypes: 1 = algemeen, 2 = politiek, 3 = business
	stop_words = get_parabots_stopwords()
	print("Get items from database"	)
	# query = "SELECT itemText, pubDate FROM newsitems WHERE sourceType = 2"
	# query = "SELECT itemText, pubDate FROM newsitems WHERE sourceType = 2 LIMIT 1000"
	curs.execute(query)

	print( "selection made"	)
	silly_words = get_silly_words()

	# init dictionary
	freqs = defaultdict(lambda: defaultdict(int))
	freqs_per_day = defaultdict(lambda: defaultdict(int))
	min_date,max_date = 0,0
	first = True
	punc_map = str.maketrans("","",string.punctuation)
	for row in curs:
		date = row['pubDate'].date()
		if date != no_date:
			s = row['itemText']
			s = unicodedata.normalize('NFKD', s.decode('unicode-escape')).encode('ascii', 'ignore')
			s = str(s)
			s = esc_chars(s)
			s = s.translate(punc_map)
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
					if word_dict[word][0]:
						freqs[word][date] += 1
						freqs_per_day[date][word]+=1

	return freqs, freqs_per_day, min_date, max_date

def build_freq_vect(f, min_date, max_date):
	dt = datetime.timedelta(1)
	if f != None:		
		vec_len = (max_date-min_date).days+1
		if (max_date-min_date).seconds > 0:
			vec_len+=1
		vect = np.zeros(vec_len)
		cur_date = copy.deepcopy(min_date)
		# print (vec_len, max_date, min_date, (max_date-min_date).days)
		index = 0
		while cur_date <= max_date and index<vec_len:
			if math.isnan(f[cur_date]):
				print( "nan found")
				sys.exit()
			vect[index] = f[cur_date]
			if f[cur_date] == 0:
				del f[cur_date]
			cur_date=cur_date+dt
			index+=1
		if any([math.isnan(x) for x in vect]):
			print( "vect contains nan")
			sys.exit()
		if np.sum(vect)== 0.0:
			# print("vector with only zeros")
			vect[0]=0.1
			return vect
		return vect

	return None


def calc_correlations(freqs, min_date, max_date, landscape, grid_size):
	freqs[None] = None
	neighs = [[0,1],[1,1],[1,0]]	
	# correlations = [sum corr coeff, nr_neighbors]
	correlations = defaultdict(lambda: np.array([0,0]))
	avg_corr = 0
	nr_words = 0
	repr = defaultdict(lambda: defaultdict(lambda: None))
	for i in range(grid_size-1):
		# print( landscape[i][0])
		repr[0][0] = build_freq_vect(freqs[landscape[i][0]], min_date, max_date)
		# print( landscape[i+1][0])
		repr[1][0] = build_freq_vect(freqs[landscape[i+1][0]], min_date, max_date)
		for j in range(grid_size-1):
			# print( landscape[i][j+1])
			repr[0][1] = build_freq_vect(freqs[landscape[i][j+1]], min_date, max_date)
			# print( landscape[i+1][j+1])
			repr[1][1] = build_freq_vect(freqs[landscape[i+1][j+1]], min_date, max_date)
			if landscape[i][j]!=None:
				nr_words+=1
				for [ni, nj] in neighs:
					# calc correlations if neighbor niet = None
					if repr[ni][nj]!= None:
						result = np.array([0,1])
						# print("indices", ni, nj)
						# print(repr[0][0])
						# print(repr[ni][nj])
						temp = np.corrcoef(repr[0][0], y = repr[ni][nj])[0,1]
						if math.isnan(temp):
							result[0] = 0.0
							print("has nan")
						else:
							result[0] = temp
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

def to_file(corr, avg_corr, word_dict, grid_size):
	f = open(output_folder + r"\correlations.txt", "w")
	f.write("average correlation,"+str(avg_corr)+"\n")
	# grid_size = int(np.ceil(np.sqrt(len(corr))))
	figv = np.zeros((grid_size,grid_size))
	for k, v in corr.items():
		f.write(k+","+str(v)+"\n")
		figv[word_dict[k][1],word_dict[k][2]] = v
	f.close()

	fig = plt.figure()	
	cmap_v = "RdYlGn"
	xp, yp = np.mgrid[slice(0, grid_size, 1), slice(0, grid_size, 1)]	
	# zmin, zmax = 0, stress_cutoff
	# plt.pcolor(xp, yp, figv, cmap=cmap_v, vmin=zmin, vmax=zmax)
	plt.pcolor(xp, yp, figv, cmap=cmap_v)
	plt.title("Resulting average correlations with neighbors")
	plt.axis([0, grid_size-1, 0, grid_size-1])
	plt.colorbar()
	image_name = output_folder + r"\Avg_corr_neighs.pdf"
	fig.savefig(image_name, bbox_inches='tight')
	plt.close()

def check_freqs(freqs, freqs_per_day):
	f =open(output_folder+r"\check_freq_words.txt", "w")
	keys = list(freqs.keys())
	keys.sort()
	for k in keys:
		f.write(k+" "+str(freqs[k])+"\n")
	f.close()
	
	f =open(output_folder+r"\check_daily_freq.txt", "w")
	keys = list(freqs_per_day.keys())
	keys.sort()
	for k in keys:
		f.write(str(k)+" "+ str(len(freqs_per_day[k]))+" "+str(freqs_per_day[k])+"\n")
	f.close()
	
def log_daily_freqs(freqs_per_day, landscape, grid_size):

	log_folder = output_folder + r"\daily_freqs"
	if not os.path.exists(log_folder):
		os.makedirs(log_folder)
	cmap_v = "RdYlGn"
	fig_nr = 0
	empty_value = -0.01
		
	keys = list(freqs_per_day.keys())
	keys.sort()
	for date in keys:
		f_dict = freqs_per_day[date]
		f = open(log_folder+r"\day"+str(date)+".txt","w")
		values = np.zeros((grid_size, grid_size))
		for i in range(grid_size):
			for j in range(grid_size):
				elem = landscape[i][j]
				if elem != None:
					f.write(str(f_dict[elem])+" ; ")
					values[grid_size-1-i,j]=f_dict[elem]					
				else:
					f.write(str(empty_value)+" ; ")
					values[grid_size-1-i,j]=empty_value
			f.write("\n")
		f.close()
		
		
		values = (values/np.sum(values))*10
		fig = plt.figure(figsize=(figure_size, figure_size))
		xp, yp = np.mgrid[slice(0, grid_size, 1), slice(0, grid_size, 1)]
		plt.pcolor(xp, yp, values, cmap=cmap_v, vmin=empty_value, vmax=0.05)
		plt.title("Frequencies in grid" + str(date))
		plt.axis([0, grid_size-1, 0, grid_size-1])
		plt.colorbar()	
		fig_name = log_folder + r"\day" + four_digit_string(fig_nr) + ".png"
		fig.savefig(fig_name)
		plt.close()
		fig_nr+=1
		

def evaluate_sem(landscape_file):
	landscape, word_dict, grid_size = read_landscape(landscape_file)
	freqs, freqs_per_day, min_date, max_date = get_frequencies(word_dict)
	if log_day_freqs:
		check_freqs(freqs, freqs_per_day)
		log_daily_freqs(freqs_per_day, landscape, grid_size)
	corr, avg_corr = calc_correlations(freqs, min_date, max_date, landscape, grid_size)
	to_file(corr, avg_corr, word_dict, grid_size)

if __name__ == "__main__":	

	# wd=defaultdict(lambda: False)
	# wd['de'] = True
	# wd['het'] = True
	# freq, mind, maxd = get_frequencies(wd)
	# print(mind, "\n", maxd)
	# for key, indict in freq.items():
		# for key2, value in indict.items():
			# print(key, key2, value)

	parser = argparse.ArgumentParser(description='Run puzzle algorithm')
	# '''parser.add_argument(<naam>, type=<type>, default=<default>, help=<help message>)'''
	parser.add_argument("case_name", help="Name of the data case that you want to process")
	parser.add_argument("landscape", help="The number of words in the data case")
	parser.add_argument("--doc_limit", default=None, help="The number of words in the data case")
	parser.add_argument("--log_day_freqs", default=None, help="The number of words in the data case")
	parser.add_argument("--dif_output_dir", default=None, help="The number of words in the data case")

	args = parser.parse_args()
	kwargs = vars(args)	

	print( "\n\n\n")
	print( kwargs)

	data_case = "\\" + kwargs["case_name"]
	landscape_name = input_folder+data_case+ "\\grids\\"+kwargs["landscape"]	
	if kwargs["doc_limit"]!=None:
		query = query +  " LIMIT " + kwargs["doc_limit"]
	if kwargs["log_day_freqs"]=="yes":
		log_day_freqs = True
	if kwargs["dif_output_dir"]==None:
		output_folder = output_folder+data_case
	else:
		output_folder = output_folder+kwargs["dif_output_dir"]
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)
	 

	evaluate_sem(landscape_name)
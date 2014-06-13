from __future__ import division
import sys
lib_path = r"K:\Lydia\code\tsne_python"
print lib_path
sys.path.append(lib_path)
import tsne
import random
import pca_large
import space_to_grid as stg
import numpy as np
from collections import defaultdict
import visualizeGrid as viz
import os
import datetime

input_folder = r"D:\Users\Lydia\results word cooc"
result_folder = r"D:\Users\Lydia\results semantic landscape"
input_path = r"default"
result_path = "default"
red_k = 30

def data_2d_to_file(data):
	size = data.shape
	file = open(result_path + r"\tsne_result_2d.txt",'w')
	for i in range(size[0]):
		for j in range(size[1]):
			file.write(str(data[i,j]) + " ")
		file.write("\n")
	file.close()

def grid_to_file(grid, grid_size, sampled_words):
	print "gridsize = ", grid_size
	grid_w = []
	for i in range(grid_size):
		grid_w.append([])		
		for j in range(grid_size):
			grid_w[i].append("-EMPTY-")
		
	for elem in grid:		
		grid_w[elem[0]][elem[1]] = sampled_words[elem[2]]
	
	file = open(result_path + r"\semantic_landscape.txt",'w')
	for i in range(grid_size):		
		for j in range(grid_size):
			file.write(grid_w[i][j] + " ; ")
		file.write("\n")
	file.close()	


def get_word_list(nr_words, nr_words_sample):
	word_file = input_path+r"\complete_cooc\wordlist.txt"
	f = open(word_file, 'r')
	lst = []
	xtra = []
	p_add = nr_words_sample/nr_words
	print "P(add)=", p_add
	added = 0
	for line in f:
		if random.random() <= p_add:
			lst.append( line.replace(" \n", "").replace("\n", "") )
			added+=1
		elif random.random() < p_add*3:
			xtra.append((line.replace("\n", "")).split(" ")[0] )
	if len(lst) < nr_words_sample:
		while len(lst)<nr_words_sample:
			ind = random.randrange(len(xtra))
			lst.append(xtra[ind])
			del xtra[ind]
	while len(lst) > nr_words_sample:
		del lst[ random.randrange(len(lst)) ]
	lst.sort()
	f_out = open(result_path + r"\sampled_words.txt", "w")
	for w in lst:
		f_out.write(w + "\n")
	f_out.close()
	return lst

	
def nse(data, nr_words):
	return tsne.tsne(data, 2, nr_words, already_reduced=True)
	
def space_to_grid(reduced_2):
	return stg.space_to_grid_iterative(reduced_2, result_path)

def build_cooc_file(sampled_words):
	# only selected words
	# normalize and to log
	sums = defaultdict(int)
	input_letter = "a"
	input_file_temp = input_path + r"\complete_cooc\_"
	f = open(input_file_temp + input_letter + ".txt", 'r')
	f_output = open(result_path + r"\sampled_coocs.txt", 'w')
	
	word = 	sampled_words[0]
	print "current word", word
	nr_found = 0
	while nr_found < len(sampled_words):
		if word[0] > input_letter and word[0] <= "z":		
			f.close()
			input_letter = word[0]
			# print "input letter now: ", input_letter
			f = open(input_file_temp + input_letter + ".txt", 'r')
		items = f.readline().replace(";\n", "").split(";")
		if word == items[0]:
			f_output.write(word)
			#process			
			del items[0]			
			for entry in items:	
				entry = entry.split(" ")
				sums[entry[0]] += float(entry[1])
				f_output.write(";" + entry[0] + " " + entry[1])			
			f_output.write("\n")
			nr_found+=1		
			if nr_found < len(sampled_words):
				word = sampled_words[nr_found]
	f.close()
	f_output.close()
	f_output = open(result_path + r"\avgs_nonzero_columns.txt", 'w')
	for w in sums.iterkeys():
		f_output.write(w + " " + str(sums[w]/len(sampled_words)) + "\n" )
	f_output.close()
	print "\n\nnumber of nonzero columns:", len(sums)
	
def read_reduced_data(nr_words_sample):	
	data_file = open(result_path+ r"\reduced_data_30.txt", "r")	
	data = np.zeros((nr_words_sample, red_k))
	i = 0
	for l in data_file:
		l = l.replace(" \n","")
		l = l.split(" ")
		data[i,:] = np.array(map(float,l))
		i+=1		
	return data	
		
	
def read_sampled_words_from_file():
	data_file = open(result_path + r"\sampled_words.txt", "r")
	w_list = []
	for l in data_file:
		l = l.replace("\n", "")
		w_list.append(l)
	return w_list
	
	
def get_reduced_data(nr_words_sample):
	input = result_path + r"\sampled_coocs.txt"
	input_sums = result_path + r"\avgs_nonzero_columns.txt"
	output = result_path + r"\reduced_data_30.txt"
	pca = pca_large.PCA_ext(input, output)
	pca.add_averages(input_sums)
	return pca.pca_large(nr_words_sample, red_k)
	
def get_semantic_landscape(nr_words, nr_words_sample, build_coocs, create_reduced):
	
	print "Begin process building/reading coocs ", datetime.datetime.now()
	if create_reduced:		
		if build_coocs:
			print "get sampled words and build cooc file"
			sampled_words = get_word_list(nr_words, nr_words_sample)
			build_cooc_file(sampled_words)
			
		#TODO: Hier inbouwen dat je ook reduced data van file kan inlezen als het al eerder gedaan is!!
		print "Begin dimensionality reduction", datetime.datetime.now()
		get_reduced_data(nr_words_sample)
	if not build_coocs and not create_reduced:
		sampled_words = read_sampled_words_from_file()
	reduced_30 = read_reduced_data(nr_words_sample)
	print "run nse at", datetime.datetime.now()
	reduced_2 = nse(reduced_30, nr_words)
	print "data 2 file at", datetime.datetime.now()
	data_2d_to_file(reduced_2)
	print "make grid from space at", datetime.datetime.now()
	(assignment, grid_size) = space_to_grid(reduced_2)
	print "results to file at", datetime.datetime.now()
	grid_to_file(assignment, grid_size, sampled_words)
	# viz.visualize_grid(grid_size, assignment, result_path)
	print "+++++++++ DONE +++++++++++\n", datetime.datetime.now()
	
if __name__ == "__main__":
	# print "test data set"
	# build_coocs = True
	# create_reduced = True	
	# nr_words = 11756
	# nr_words_sample = 3000
	# input_directory = r"\limit1000_freq1"
	# data_directory = r"\limit1000_freq1"
	
	# input_path = input_folder + input_directory
	# result_path = result_folder + data_directory
	# if not os.path.exists(result_path):
		# os.makedirs(result_path)	
		# print "directory made"		
	
	# get_semantic_landscape(nr_words, nr_words_sample, build_coocs, create_reduced)

	#==============================================================
	
	# print "==============test data set no log=============="
	# build_coocs = True
	# create_reduced = True	
	# nr_words = 11756
	# nr_words_sample = 100
	# input_directory = r"\limit1000_nolog"
	# data_directory = r"\limit1000_nolog"
	
	# input_path = input_folder + input_directory
	# result_path = result_folder + data_directory
	# if not os.path.exists(result_path):
		# os.makedirs(result_path)	
		# print "directory made"		
	
	# get_semantic_landscape(nr_words, nr_words_sample, build_coocs, create_reduced)
	
	#==============================================================
	
	# print "==============cutoff 10 dataset=============="
	# build_coocs = True
	# create_reduced = True
	# nr_words = 30348
	# nr_words_sample = 2500
	# input_directory = r"\cutoff_10_nolog"	
	# data_directory = r"\cutoff_10_nolog"	
	
	# input_path = input_folder + input_directory
	# result_path = result_folder + data_directory
	# if not os.path.exists(result_path):
		# os.makedirs(result_path)	
		# print "directory made"		
	
	# get_semantic_landscape(nr_words, nr_words_sample, build_coocs, create_reduced)
	
	#==============================================================
	
	# print "==============cutoff 3 dataset=============="
	# build_coocs = True
	# create_reduced = True
	# nr_words = 57457
	# nr_words_sample = 5000
	# input_directory = r"\cutoff_3_nolog"	
	# data_directory = r"\cutoff_3_nolog"	
	
	# input_path = input_folder + input_directory
	# result_path = result_folder + data_directory
	# if not os.path.exists(result_path):
		# os.makedirs(result_path)	
		# print "directory made"		
	
	# get_semantic_landscape(nr_words, nr_words_sample, build_coocs, create_reduced)
	
	
		
	#==============================================================
	
	
	# input_directory = r"\test"
	# data_directory = r"\test"
	
	# input_path = input_folder + input_directory
	# result_path = result_folder + data_directory
	# if not os.path.exists(result_path):
		# os.makedirs(result_path)	
		# print "directory made"
	# build_cooc_file(["blaat", "blub", "hoi", "jam"])
	
	#==============================================================
	
	print "test 3 dataset"
	build_coocs = True
	create_reduced = True
	nr_words = 40
	nr_words_sample = 20
	input_directory = r"\test3"
	data_directory = r"\test3"	
	red_k = 3
	
	input_path = input_folder + input_directory
	result_path = result_folder + data_directory
	if not os.path.exists(result_path):
		os.makedirs(result_path)	
		print "directory made"		
	
	get_semantic_landscape(nr_words, nr_words_sample, build_coocs, create_reduced)

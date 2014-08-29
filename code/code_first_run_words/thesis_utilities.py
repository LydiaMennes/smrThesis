from collections import defaultdict
import numpy as np
import string
import re
from bisect import bisect_left
import random
import os
import datetime
from matplotlib import pyplot as plt
import pylab as P

empty = "-EMPTY-"

def distribution_daily_docs(case_name):
    file_name = r"D:\Users\Lydia\results_freqs\freqs_per_day"+"\\"+case_name+r"\info.txt"
    f = open(file_name,"r")
    f.readline()
    dates = []
    nr_docs = []
    for l in f:
        l = l.split(";")
        d = l[0].split("-")
        d = [int(x) for x in d]
        dates.append(datetime.date(d[0],d[1],d[2]))
        nr_docs.append(int(l[1]))
    f.close()
    
    file_name = r"D:\Users\Lydia\results_freqs\freqs_per_day"+"\\"+case_name+r"\\"
    fig = plt.figure()
    ax = plt.subplot(111)
    plt.plot(list(range(len(dates))), nr_docs, 'r.')
    plt.show()
    fig.savefig(file_name+"scatterplot_nr_docs_over_days.png")
        
    fig=plt.figure()
    plt.hist(nr_docs, bins=150)
    plt.title("Nr documents over days")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()
    fig.savefig(file_name+"histogram_nr_docs_over_days.png")
    

def has_digits (word):
	hd = re.compile('\d')
	return bool(hd.search(word))
    
def get_parabots_stopwords():
	filename = r"K:\Lydia\smrThesis\code\code_first_run_words\dutchStopwords.txt"
	return get_word_list(filename)
	
def get_english_stopwords():
	filename = r"K:\Lydia\smrThesis\code\code_first_run_words\english_stop_words.txt"
	return get_word_list(filename)
	

def four_digit_string(i):
	if i == 0:
		return "0000"
	elif i >=10000:
		return "TOO LARGE NUMBER"
	s = ""
	start = 1000
	while i/start < 1:
		s += "0"
		start = start / 10
	return s + str(i)
	
def grid_to_file(output_directory, grid_size, suffix, grid):
	f = open(output_directory + r"\grid_" + suffix +".txt", "w")	
	grid_size = int(grid_size)
	for i in range(grid_size):
		for j in range(grid_size):
			if grid[i][j]!= None:
				f.write(grid[i][j].name + " ; " )
			else:
				f.write(empty+" ; ")
		f.write("\n")
	f.close()
	
def get_colors():
	r = [[0,1,0],[1,1,0],[0,1,1],[0,0,1],[0,1,0.5],[1,0,0.5],[0.5,1,0],[0,0.5,1],[1,0,1], [1,0,0],[0.5,0,1],[1,0.5,0]]
	q = np.array(r)
	q = q*0.5
	r.extend(map(list,list(q)))
	return r
	
def space_to_file(data, filename):
	f = open(filename, "w")
	for i in range(data.shape[0]):
		f.write(str(data[i,0]) + "," + str(data[i,1])+"\n")
	f.close()

def space_from_file(filename):
	print(filename)
	f = open(filename, "r")
	d = []
	for line in f:
		line = line.replace("\n","")
		line = line.split(",")
		d.append([float(line[0]), float(line[1])])
	f.close()
	print("d", len(d))
	return np.array(d)
	
def grid_from_file(landscape_file):
	grid = defaultdict(lambda: defaultdict(lambda: None) )
	f = open(landscape_file)
	row = 0
	column = 0
	for line in f:
		line = line.replace(" ; \n", "")
		line = line.split(" ; ")
		for w in line:
			if w != empty:
				grid[row][column] = w	
			column += 1
		column = 0
		row+= 1	
	f.close()
	
	return grid
	
def esc_chars(s):
	s = s.replace(r"\a"," ")
	s = s.replace(r"\b"," ")
	s = s.replace(r"\f"," ")
	s = s.replace(r"\n"," ")
	s = s.replace(r"\x"," ")
	s = s.replace(r"\v"," ")
	s = s.replace(r"\r"," ")
	s = s.replace(r"\t"," ") 
	return s
	
def get_silly_words():
	f = open("silly_words.txt","r")
	words = []
	for line in f:
		line = line.replace("\n", "")
		words.append(line)
	f.close()
	return words
	
def get_word_list(file):
	f = open(file,"r")
	words = []
	for l in f:
		l = l.replace("\n","")
		words.append(l)
	f.close()
	return words

def build_random_grid(words, output_dir):
	print("nr words:", len(words))
	grid_size = int(np.ceil(np.sqrt(len(words))))
	print("grid_size", grid_size)
	nr_items = grid_size*grid_size
		
	if not os.path.exists(output_dir+r"\grids"):
		os.makedirs(output_dir+r"\grids")
	f = open(output_dir+r"\grids\random_grid.txt", "w")
	f2 = open(output_dir+r"\grid_initial.txt", "w")	
	for i in range(grid_size):
		for j in range(grid_size):
			ind = random.randrange(nr_items)
			if ind<len(words):
				f.write(words[ind]+" ; ")
				f2.write(words[ind]+" ; ")
				del words[ind]
			else:
				f.write(empty + " ; ")
				f2.write(empty + " ; ")
			nr_items-=1
		f.write("\n")
		f2.write("\n")
	f.close()
	f2.close()

def get_nr_words_from_stats(file_folder):
	f = open(file_folder+r"\stats.txt","r")
	for line in f:
		if "number of included words: " in line:
			line = line.replace("number of included words: ", "")
			line = line.replace("\n", "")
			included_words = int(line)
			break
	f.close()
	return included_words
	
def build_random_puzzle_result(landscape_file, out_folder):
	if not os.path.exists(out_folder):
		os.makedirs(out_folder)
	landscape = grid_from_file(landscape_file)
	grid_size = len(landscape)
	blob_size = grid_size//2
	blob_nr = 0
	freq = 0
	first = True
	word_list = []
	f = open(out_folder+r"\blob_file.txt","w")
	for i in range(grid_size):
		for j in range(grid_size):
			elem = landscape[i][j]
			if elem != None:
				if elem == "strontrace":
					print("ENCOUNTERED")
				word_list.append(elem)
				if freq==blob_size or first:
					if not first:
						f.write("\n")
					first = False
					f.write(str(blob_nr) + " " + elem + " " + str(000) )
					freq = 0
					blob_nr+=1
				else:
					f.write(" " + elem)
					freq+=1
	f.close()
	build_random_grid(word_list, out_folder)
	
def get_related_colors(c, n):
	colors = np.array([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[0,1,1],[1,0,1]])
	dif = 0.6/c
	if n > 6:
		print("too many colors")
	result = []
	for i in range(n):
		result.append([])
		for j in range(c):
			# print(result, i)
			result[i].append( list(colors[i,:]*(0.4+dif*j)))
	return result
	
	
	
if __name__ == "__main__":
    distribution_daily_docs("politics_merged")

	# data_cases = ["football_limit1000_no_stem","football_limit1000_stem","politics_limit1000_no_stem","politics_limit1000_stem"]
	# output_naes = ["football_limit1000_no_stem","football_limit1000_stem","politics_limit1000_no_stem","politics_limit1000_stem"]
	# data_cases = ["politics_big_stem"]
	# output_names = ["politics_big_stem_random"]
	
	# for i in range(len(data_cases)):
		# data_case = data_cases[i]
		# output_name = output_names[i]
		# landscape = r"D:\Users\Lydia\results puzzle"+"\\"+data_case+r"\grid_initial.txt"
		# destination = r"D:\Users\Lydia\results puzzle"+"\\"+output_name
		# build_random_puzzle_result(landscape, destination)
		
	# print("==============\nDONE\n==============")
	
	
	# stat_file = r"D:\Users\Lydia\results word cooc\football_limit1000_no_stem"
	# print(get_nr_words_from_stats(stat_file))
	
	
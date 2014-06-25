from collections import defaultdict
import numpy as np
import string
import re
from bisect import bisect_left
import random
import os

def has_digits (word):
	hd = re.compile('\d')
	return bool(hd.search(word))

def get_parabots_stopwords():
	file = open(r"D:\Users\Lydia\code stuff\dutchStopwords.txt", 'r')
	stopwords = []
	for line in file:
		line = line.replace("\n", "")
		stopwords.append(line)
	return stopwords

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
				f.write("-EMPTY- ; ")
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
			if w != "-EMPTY-":
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

def build_random_grid(word_file, output_dir):
	empty = "-EMPTY-"
	words = get_word_list(word_file)
	print("nr words:", len(words))
	grid_size = int(np.ceil(np.sqrt(len(words))))
	print("grid_size", grid_size)
	nr_items = grid_size*grid_size
		
	if not os.path.exists(output_dir+r"\grids"):
		os.makedirs(output_dir+r"\grids")
	f = open(output_dir+r"\grids\random_grid.txt", "w")
		
	for i in range(grid_size):
		for j in range(grid_size):
			ind = random.randrange(nr_items)
			if ind<len(words):
				f.write(words[ind]+" ; ")
				del words[ind]
			else:
				f.write(empty + " ; ")
			nr_items-=1
		f.write("\n")
	f.close()
		
	
	
	
	
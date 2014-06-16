from __future__ import division
import math
import numpy as np
import random
import space_to_grid as stg
import bisect as bis
import datetime
import os
from collections import defaultdict
import matplotlib.pyplot as plt
from sets import Set
from operator import methodcaller
import sys
import copy
from matplotlib import cm
import prettyplotlib as ppl
import semantic_distance
import argparse
from thesis_utilities import *

input_directory_landscape = r"D:\Users\Lydia\results semantic landscape"
input_directory_cooc = r"D:\Users\Lydia\results word cooc"
output_directory = r"D:\Users\Lydia\results puzzle"
data_case_name = ""
max_closest = 0
nr_trials_check = 0
nr_trials_reinit = 0
neighbor_range_swap = [0,0]
block_ratio = 0
grid_f = defaultdict(lambda: defaultdict(lambda: None) )
data_portion = 0
nr_words_to_follow = 0
to_file_trials = 0
global_index = {}
stop_nr_trials = 0
blob_neighbors = []
init_type = "probabilistic" # can be probabilistic or deterministic
log_file_n = ""

stress_cutoff = 1.2
figure_size = 8

class GridElem:

	def __init__(self, i, pos, name, blob_color, blob_nr=None):
		self.id = i
		self.pos = np.array(pos)
		self.closest = []
		self.dists = []
		self.followers = {}
		self.name = name
		self.blob_nr = blob_nr
		self.nr_swaps = 0
		self.followers2 = {}
		self.closest_copy = []
		self.sem_rep = None
	
	# n = [dist, id, x pos, y pos]
	def check_neighbor(self, n):
		if self.id == n[1]:
			"compared to self"
					
		if len(self.dists) == 0:
			self.dists.append(n[0])
			self.closest.append([n[1], np.array(n[2:len(n)])] )
		if len(self.dists)!= 0 and (len(self.dists) < max_closest or n[0] < self.dists[-1]):
			i = bis.bisect(self.dists, n[0])
			self.dists.insert(i, n[0])
			self.closest.insert( i, [n[1], np.array(n[2:len(n)])] )
			if grid_f[n[2]][n[3]].id != n[1]:
				print "WRONG CLOSEST ADDED"
				sys.exit()
			if np.array(n[2:len(n)])[0]  == self.pos[0] and np.array(n[2:len(n)])[1]==self.pos[1]:
				"closest added with own position", self.name, self.pos, "id to be added" ,n[0]
				sys.exit()
			if len(self.dists) > max_closest:
				del self.dists[-1]
				del self.closest[-1]
			
	def get_closest(self):
		return self.closest
		
	def get_followers(self):
		return self.followers
	
	def get_optimal(self):
		return np.mean(np.array(self.dists))
	
	def add_follower(self, id_f, pos_f):
		# if id_f == self.id:
			# print "self added as follower"
			# print closest
			# sys.exit()
		# if grid_f[pos_f[0]][pos_f[1]].id != id_f:
			# print "WRONG FOLLOWER ADDED"
			# sys.exit()
		self.followers[id_f] = pos_f
		self.followers2[id_f] = pos_f
	
	def add_cooc(self, sem):
		self.sem_rep = sem
	
	def init_as_follower(self):
		for c in self.closest:
			self.closest_copy.append(copy.deepcopy(c))		
		for (x, c) in self.closest:		
			grid_f[int(c[0])][int(c[1])].add_follower(self.id, self.pos)
		
	def follower_pos_update(self, id_f, pos_f):
		# if grid_f[pos_f[0]][pos_f[1]] == None:
			# print "Hier wordt een None positie follower doorgegeven", id_f, pos_f
			# sys.exit()
		# elif grid_f[pos_f[0]][pos_f[1]].id != id_f:
			# print "Hier wordt een verkeerde follower positie doorgegeven", id_f, pos_f
			# sys.exit()
		# if id_f == self.id:
			# print "adds itself as follower in update function", self.name
			# sys.exit()
		self.followers[id_f] = pos_f
		
	def closest_pos_update(self, id_c, pos_c):
		found = False
		# print "closest pos update" 
		for c in self.closest:
			if c[0]==id_c:				
				c[1] = pos_c
				found = True
		if not found:
			print "closest not found: searched", id_c, "at", self.name			
			sys.exit()
	
	def get_improvement(self, new_x, new_y):
		# bereken improvement als je naar deze positie gaat
		new_pos = np.array([new_x,new_y])
		old = 0
		new = 0
		for c in self.closest:	 
			old += np.dot(self.pos-c[1], self.pos-c[1])
			new += np.dot(new_pos-c[1], new_pos-c[1])
		return old-new
		
	def change_pos(self, pos_x, pos_y):
		self.nr_swaps +=1		
		old_pos = np.array(self.pos)
		self.pos = np.array([pos_x, pos_y])
		for idX, posX in self.closest:
			# if idX == self.id:
				# print "found itself in list with closest"
			# if grid_f[posX[0]][posX[1]].id == self.id and grid_f[old_pos[0]][old_pos[1]].id != idX:
				# print "ID position combination does not make sense"
				# print self.pos, self.name, global_index[idX]			
			global_index[idX].follower_pos_update(self.id, self.pos)
		for idX, posX in self.followers.iteritems():
			# if idX != grid_f[posX[0]][posX[1]].id and grid_f[old_pos[0]][old_pos[1]].id != idX:
				# print self.name, ":WRONG ID, name at position: ", grid_f[posX[0]][posX[1]].name
				# print "name at old position: " , grid_f[old_pos[0]][old_pos[1]].name
				# print "expected name: ", global_index[idX].name 
			# if idX == self.id:
				# print "HAS ITSELF AS FOLLOWER"
				# print self.followers.keys()
				# print self.followers2.keys()
			# if grid_f[posX[0]][posX[1]].id == self.id:
				# "Position of follower equals own position"
			global_index[idX].closest_pos_update(self.id, self.pos)
			
	def reset(self):
		self.closest = []
		self.dists = []
		self.followers = {}

def print_all_lists(x):
	f = open(output_directory+r"\lists of closest.txt","a")
	f.write("=========" + str(x) + "========\n\n")
	for i in range(len(grid_f)):
		for j in range(len(grid_f)):
			if grid_f[i][j] != None:
				f.write(grid_f[i][j].name + " at position "+str(i)+" "+str(j)+" thinks at position "+str(grid_f[i][j].pos)+ ":\nClosest:")
				for id1, pos1 in grid_f[i][j].get_closest():
					f.write(" " + grid_f[pos1[0]][pos1[1]].name + "(" + str(pos1) + ")")
				f.write("\nFollowers:")
				for id2, pos2 in grid_f[i][j].get_followers().iteritems():
					f.write(" " + grid_f[pos2[0]][pos2[1]].name + "(" + str(pos2) + ")")
				f.write("\n")
	f.write("\n\n")
	f.close()

def grid_and_blob_from_file():
	f = open(output_directory+r"\blob_file.txt")
	blob_nrs = {}
	for line in f:
		line = line.replace("\n", "")
		line = line.split(" ")
		blob_nr = int(line[0])
		del line[2]
		del line[0]
		for w in line:
			blob_nrs[w] = blob_nr
	f.close()
	
	colors = get_colors()

	landscape_file = output_directory+r"\grid_initial.txt"
	grid = grid_from_file(landscape_file)
	id = 0
	nr_words = 0
	for x, inDict in grid.iteritems():
		for y, elem in inDict.iteritems():
			# if elem.pos[0] != x or elem.pos[1]!=y:
				# print "x", x, elem.pos[0], "y", y, elem.pos[1]
			if elem != None:
				# i, pos, name, blob_color, blob_nr=None
				grid_f[x][y] = GridElem(id, [x,y], elem, colors[id%len(colors)], blob_nrs[elem])				
				global_index[id] = grid_f[x][y]
				id+=1
				nr_words+=1
	print "\n====\nFile read\n===="
	grid_to_file(output_directory, x+1, "test", grid_f)
	return x+1, nr_words
	
# Requires semantic representation as a list of lists of the non-zeros entries: [[name, value],[name,value]]
def distance(sem_w1, sem_w2):
	# Je kan hier ook andere afstands maten gebruiken
	return semantic_distance.cosine_distance(sem_w1, sem_w2)
	# return semantic_distance.cosine_distance_log(sem_w1, sem_w2)	


	
def stats_to_file(iter, trial, to_follow, nr_inits, grid_size, png_nr):
	# followers
	image_name = output_directory + r"\follow_points_init" +str(nr_inits)+  "_tr" +str(trial)+"_it"+ str(iter)+".pdf"
	fig = plt.figure(figsize=(figure_size, figure_size))	
	colors = get_colors()
	points = []
	for i,ind in enumerate(to_follow):
		pos = global_index[ind].pos
		prop_plot = plt.scatter(pos[1], (grid_size-pos[0]-1), c=colors[i%len(colors)], marker='s')
		prop_plot.set_edgecolor("none")
		points.append((pos[0],pos[1]))
		cs = global_index[ind].get_closest()
		# print "nr closests: ", len(cs)
		for c in cs:
			# print indexes[c[0]][0],
			pos = c[1]
			fx = 1.0
			fy = 1.0
			if random.random() > 0.5:
				fx = -1.0
			if random.random() < 0.5:
				fy = -1.0
			prop_plot = plt.scatter(pos[1]+ fx*(random.random()/5+0.05), grid_size-1-(pos[0]+ fy*(random.random()/5+0.05)), c=colors[i%len(colors)], marker='.')
			prop_plot.set_edgecolor("none")
			points.append((pos[0],pos[1]))
		# print ""
	plt.title("Follow words and their most similar words trial " +str(trial) )	
	plt.axis([-1, grid_size+1, -1, grid_size+1])
	fig.savefig(image_name, bbox_inches='tight')		
	fig.savefig(output_directory+r"\points_"+ four_digit_string(png_nr) +".png")	
	plt.close()
	# grid to file 
	grid_to_file(output_directory, grid_size, "stats_init" +str(nr_inits)+  "_tr" +str(trial)+"_it"+ str(iter), grid_f)
	
	# stress measure figure
	# Make plot with vertical (default) colorbar
	fig = plt.figure(figsize=(figure_size, figure_size))
	# print "get stress values"
	stress_values = get_stress_values()
	# cmap_v = "PuRd"
	cmap_v = "RdYlGn"
	# print "make figure"
	xp, yp = np.mgrid[slice(0, grid_size, 1), slice(0, grid_size, 1)]
	if data_case_name=="test3":
		plt.pcolor(xp, yp, stress_values, cmap=cmap_v)
	else:
		zmin, zmax = 0, stress_cutoff
		plt.pcolor(xp, yp, stress_values, cmap="PuRd", vmin=zmin, vmax=zmax)
	plt.title("Stress values at trial " + str(trial))
	plt.axis([0, grid_size-1, 0, grid_size-1])
	plt.colorbar()
	image_name = output_directory + r"\heat_map_stress_values_init" +str(nr_inits)+  "_tr" +str(trial)+"_it"+ str(iter)+".pdf"
	fig.savefig(image_name, bbox_inches='tight')
	fig.savefig(output_directory+r"\heat_map_stress_" + four_digit_string(png_nr) +".png")
	plt.close()
	# print "figure done"
	
	# fig, ax = ppl.subplots(1)
	# ppl.pcolormesh(fig, ax, np.abs(np.random.randn(10,10)))
	# fig.savefig('pcolormesh_prettyplotlib_positive.png')
	# plt.close()
	
	# marker='o'
	# image_name = output_directory + r"\stg_init_plot_blobColoring.pdf"
	# fig = plt.figure()
	# plt.scatter( data_space[:,0], data_space[:,1], c=coloring)
	# fig.savefig(image_name, bbox_inches='tight')	
	# plt.close()
	
def get_stress_values():	
	# dit kan je nog faseren bij grotere dataset
	gs = len(grid_f)
	# print "get data"
	words = [x.name for x in global_index.itervalues()]
	words.sort()
	data = get_data_sample(words)
	# print "process data"
	values = np.zeros((gs,gs))
	values.fill(0.0)
	nr_elems = 0
	for i in range(gs):
		for j in range(gs):
			nr_n = 0
			sum_dif = 0
			elem = grid_f[i][j]
			if elem != None:
				nr_elems +=1
				for k in range(-1,2):
					for l in range(-1,2):
						if i+k>=0 and i+k<gs and j+l>=0 and j+l<gs:
							n = grid_f[i+k][j+l]
							if not k ==0 and l == 0 and n!= None:
								nr_n+=1
								sum_dif += distance(data[elem.name], data[n.name])
				xg = gs-i-1
				if sum_dif != 0:
					values[xg,j] = elem.get_optimal() / (sum_dif/float(nr_n))
					if values[xg,j] > stress_cutoff:
						values[xg,j] = stress_cutoff
				if nr_n==0:
					values[xg,j]=0.0
	# print values	
	# print "nr_elems", nr_elems
	return values

def add_all_cooc_data():
	template = input_directory_cooc + r"\complete_cooc\_"
	letters = "abcdefghijklmnopqrstuvwqyz"
	for l in letters:
		try:
			f = open(template+l+".txt", 'r')
			for line in f:
				# PROCESS LINE
				line = line.replace(";\n", "")
				line = line.split(";")
				repr = []
				word = line[0]
				del line[0]
				if len(line)>0:
					for elem in line:
						elem = elem.split(" ")
						repr.append([elem[0], float(elem[1])])
					try:
						global_index[word].add_cooc(repr)					
					except KeyError:
						print "word not found when adding cooc"
		except IOError:
			print "file for letter", l, "not found!!!"
	
def get_sem_data():
	file = open(input_directory_landscape +  r"\semantic_landscape.txt",'r')
	grid = [[],[],[],[]]
	i = 0
	j = 0
	grid_size = -1
	for line in file:
		line = line.replace("\n", "")
		instance = line.split(" ; ")		
		for elem in instance:
			if grid_size == -1:
				grid_size = len(instance)					
			if elem != "-EMPTY-" and elem != "":
				grid[0].append(i)
				grid[1].append(j)
				grid[2].append(elem)				
				grid[3].append([])			
			j+=1
		i+=1
		j=0
	file.close()
	# data = lees alle sampled dingen in
	data = {}
	f = open(input_directory_landscape + r"\sampled_coocs.txt")
	for line in f:
		line = line.replace("\n","")
		line = line.split(";")
		w = line[0]
		del line[0]
		data[w] = []
		for elem in line:
			elem = elem.split(" ")
			data[w].append( (elem[0] , float(elem[1])) )	
	return grid_size, data, grid

	
def add_to_sim_word(w1, sem_w1, data_sample, grid):	
	k = data_sample.keys()
	k.sort()
	best_index = -1
	if init_type == "deterministic":
		best_dis = float("inf")
		sem_w1 = map( methodcaller( "split"," "), sem_w1)
		sem_w1 = [[x, float(y)] for [x,y] in sem_w1]
		for index, w2 in enumerate(k):		
			sem_w2 = data_sample[w2]
			dis = distance(sem_w1, sem_w2)
			if dis < best_dis:
				best_dis = dis
				best_index = index
	elif init_type == "probabilistic":		
		best = []
		for i in range(10):
			best.append([float("inf"),-1])
		sem_w1 = map( methodcaller( "split"," "), sem_w1)
		sem_w1 = [[x, float(y)] for [x,y] in sem_w1]
		for index, w2 in enumerate(k):		
			sem_w2 = data_sample[w2]
			dis = distance(sem_w1, sem_w2)
			if dis < best[len(best)-1][0]:
				del best[-1]
				best.append( [dis,index])
				best.sort()
		sum_len = 0
		sum_dist = 0
		prev = 0
		prob = random.random()
		for cand in best:
			sum_len += 1/max(len(grid[3][cand[1]]), 0.01)
			sum_dist+= 1/cand[0]
		for cand in best:
			cumulative = ((1/cand[0])/sum_dist)*0.4 + ((1/max(0.01,len(grid[3][cand[1]])))/sum_len * 0.6) + prev
			prev = cumulative
			if prob <= cumulative:
				best_index = cand[1]
				break
	else:
		print "The initialization type for adding to similar word does not exist"
	return best_index
	
def get_grid(grid_size, data_sample, grid, nr_words):
	input_template = input_directory_cooc + r"\complete_cooc\_"
	
	if data_case_name == r"\limit1000_freq1_small_sample":
		input_template = r"D:\Users\Lydia\results word cooc\limit1000_freq1\complete_cooc\_"
	
	print "at file",
	for letter in "abcdefghijklmnopqrstuvwxyz":
		try:
			print letter,
			f = open(input_template+letter+".txt",'r')		
			line_nr = 0
			for line in f:
				line = line.replace(";\n", "")
				line = line.split(";")
				word = line[0]
				if word not in grid[2]:
					del line[0]
					if len(line) == 0:
						print word, "at line", line_nr, "in file", letter
						nr_words -= 1
					else:
						best_index = add_to_sim_word(word, line, data_sample, grid)		
						grid[3][best_index].append(word)
			f.close()
		except IOError:
			print letter, 
	print "\n New nr words:", nr_words
	del data_sample
		
		
	new_grid_size = math.ceil(math.sqrt(nr_words))
	ratio = new_grid_size/float(grid_size)	
	ratio_resize = ratio/1.2
	shift_resize_x = (new_grid_size - grid_size*ratio_resize)/2 + ratio_resize
	shift_resize_y = (new_grid_size - grid_size*ratio_resize)/2 + ratio_resize
	data_space = np.zeros((nr_words,2))
	index = 0
	blob_file = open(output_directory + r"\blob_file.txt", "w")
	for i in range(len(grid[0])):
		new_pos = np.array([ round(grid[0][i] * ratio_resize + shift_resize_x),round(grid[1][i] * ratio_resize + shift_resize_y)])
		data_space[index,:] = new_pos
		global_index[index] = [grid[2][i],i]
		index+=1		
		assigned = len(grid[3][i])
		data_space[index:index+assigned,0].fill(new_pos[0])
		data_space[index:index+assigned,1].fill(new_pos[1])
		random_dist = np.random.rand(assigned,2)
		data_space[index:index+assigned,:] = (random_dist-0.5)*ratio_resize + data_space[index:index+assigned,:]
		blob_file.write(str(i) + " " + grid[2][i] + " " + str(len(grid[3][i]))) 
		for elem in grid[3][i]:
			global_index[index] = [elem, i]
			index+=1
			blob_file.write(" " + elem)
		blob_file.write("\n")
	blob_file.close()		
	
	print "data space shape", data_space.shape
	print "last index = ", index-1 
	used_marker = "o"
	if nr_words > 1000:
		used_marker = "."	
	colors = get_colors()		
	coloring = []
	color_index = {}
	for i in range(nr_words):
		coloring.append( colors[global_index[i][1]%len(colors)] )	
		color_index[i] = colors[global_index[i][1]%len(colors)]
		
	image_name = output_directory + r"\stg_init_plot_blobColoring.pdf"	
	fig = plt.figure(figsize=(figure_size, figure_size))
	# fig = plt.figure(figsize=(figure_size, figure_size), dpi=figure_dpi)
	prop_plot = plt.scatter( data_space[:,1], new_grid_size-1-data_space[:,0], c=coloring, marker=used_marker)
	if nr_words > 1000:
		prop_plot.set_edgecolor("none")
	plt.axis([-1,new_grid_size+1, -1, new_grid_size+1])
	plt.title("Initial blob coloring")
	fig.savefig(image_name, bbox_inches='tight')
	plt.close()
	
	print "new grid size", new_grid_size
	intermediate_grids = output_directory + "\intermediate_grids" 
	if not os.path.exists(intermediate_grids):
		os.makedirs(intermediate_grids)	
		print "directory made"
	assignment, gz = stg.space_to_grid_iterative(data_space, intermediate_grids, with_figures=False, blob_nr_keeper=stg.TypeKeeper(color_index))
	del data_space
	
	print "init final grid and make figure of grid"
	image_name = output_directory + r"\stg_result_plot_blobColoring.pdf"
	# fig = plt.figure(figsize=(figure_size, figure_size), dpi=figure_dpi)
	fig = plt.figure(figsize=(figure_size, figure_size))
	for elem in assignment:
		grid_f[elem[0]][elem[1]] =  GridElem(elem[2], elem[0:2], global_index[elem[2]][0], color_index[elem[2]], global_index[elem[2]][1] )
		global_index[elem[2]] = grid_f[elem[0]][elem[1]]
		prop_plot = plt.scatter(elem[1], new_grid_size-1-elem[0], c=color_index[elem[2]] , marker=used_marker)
		if nr_words > 1000:
			prop_plot.set_edgecolor("none")
	plt.axis([-1,new_grid_size, -1, new_grid_size])
	plt.title("Resulting blob coloring")
	fig.savefig(image_name, bbox_inches='tight')	
	plt.close()
	
	return new_grid_size, nr_words

def stop_condition(trial_nr):	
	# print "stop_condition not  implemented yet"
	return trial_nr > stop_nr_trials

def get_data_sample(sampled_words):
	input_letter = "a"
	input_file_temp = input_directory_cooc + r"\complete_cooc\_"
	filename = input_file_temp + input_letter + ".txt"
	f = open(filename, 'r')
	data = {}
	
	word = 	sampled_words[0]
	nr_found = 0
	while nr_found < len(sampled_words):
		if word[0] > input_letter and word[0] <= "z":		
			f.close()
			input_letter = word[0]
			f = open(input_file_temp + input_letter + ".txt", 'r')
		l = f.readline()
		items = l.replace(";\n", "")
		items = items.split(";")
		if word == items[0]:
			data[word] = []
			#process			
			del items[0]			
			for entry in items:	
				entry = entry.split(" ")
				data[word].append( [entry[0] ,float(entry[1]) ] )
			nr_found+=1		
			if nr_found < len(sampled_words):
				word = sampled_words[nr_found]
	f.close()
	return data
	
def init_closest(grid_size, old_grid_size, first):
	# als je een grotere area wil kan je de blob_size groter zetten zonder 
	# al deze shit opnieuw te doen
	blob_size = math.ceil( (grid_size*1.5)/float(old_grid_size))
	nr_blobs = int(math.floor(grid_size/blob_size))
	data_size = int(math.ceil(nr_blobs/float(data_portion)))
	grid_size = int(grid_size)
	print "grid size", grid_size, "old_grid_size", old_grid_size
	print "calculated blob size", blob_size, "nr_blobs", nr_blobs, "data_size", data_size,"data_portion", data_portion,  "grid_size", grid_size
	if not first:
		for i in range(grid_size):
			for j in range(grid_size):
				if grid_f[i][j] != None:
					grid_f[i][j].reset()
	
	blobs = defaultdict(lambda: defaultdict(lambda: [[],[]]))
	r_b = 0
	c_b = 0
	data_names = []
	# print "\n"
	# for r in range(grid_size):
		# for c in range(grid_size):
			# if grid_f[r][c]!= None:
				# print grid_f[r][c].name,
			# else:
				# print "xx",
		# print "\n"
	
	# print "grid_size", grid_size
	for r in range(grid_size):
		if r%blob_size == 0 and r+blob_size <= grid_size and r!=0:
			r_b += 1
		for c in range(grid_size):
			if c%blob_size == 0 and c+blob_size <= grid_size and c!=0:
				c_b += 1
			if grid_f[r][c] != None:			
				blobs[r_b][c_b][0].append( grid_f[r][c].name )
				blobs[r_b][c_b][1].append( (r, c, grid_f[r][c].id) )	
		c_b = 0
		
	# print "\n\nnr of blobs per side: ", len(blobs), nr_blobs
	# print "blobs:"
	# for i1, d in blobs.iteritems():
		# for i2, v in d.iteritems():
			# print "blob", i1, i2, ":",
			# for n in v[0]:
				# print n,
			# print ""
	# print "==============\n\n"
	d_beg = 0
	d_end = 1		
	for r_b in range(nr_blobs):
		for c_b in range(nr_blobs):
			# print "pairwise distances blob", r_b, c_b
			if r_b == d_end-1 or d_end == 1:
				d_beg = d_end-1
				d_end = min(d_end+data_size, nr_blobs)				
				# print "new data slice pairwise distances", datetime.datetime.now(), r_b, d_beg, d_end
				words = []
				# print d_beg, d_end
				for rb_i in range(d_beg, d_end):
					for cb_i in range(nr_blobs):
						words.extend(blobs[rb_i][cb_i][0])
				words.sort()
				if len(words) > 0:
					data = get_data_sample(words) 
				else:
					print "data of 0 words requested\n!!!!!!!!!!!!!!!"
				k = data.keys()
				k.sort()
				# print "got data" , datetime.datetime.now(), "\ndata\n", k
			# inside blob
			# print "blob", r_b, c_b, "\n within"
			for i in range(len(blobs[r_b][c_b][0])-1):
				for j in range(i+1, len(blobs[r_b][c_b][0])):
					d = distance(data[blobs[r_b][c_b][0][i]], data[blobs[r_b][c_b][0][j]] )
					# print "comp", blobs[r_b][c_b][0][i], "id" ,blobs[r_b][c_b][1][i][2], blobs[r_b][c_b][0][j], d
					(r1,c1, id1) = blobs[r_b][c_b][1][i]
					(r2,c2, id2) = blobs[r_b][c_b][1][j]
					grid_f[r1][c1].check_neighbor([d, id2, r2, c2])
					grid_f[r2][c2].check_neighbor([d, id1, r1, c1])
			# print "pairwise distances with neighboring blob"		
			# other blobs
			# print "\nwith other blobs\n"
			for n in blob_neighbors:
				r_b2 = n[0]+r_b
				c_b2 = n[1]+c_b
				# print "with blob", r_b2, c_b2
				if r_b2 > 0 and r_b2 < nr_blobs and c_b2 < nr_blobs:
					for i in range(len(blobs[r_b][c_b][0])):
						for j in range(len(blobs[r_b2][c_b2][0])):
							# print r_b, c_b, i, r_b2, c_b2, j
							# print blobs[r_b][c_b][0][i]
							# print blobs[r_b2][c_b2][0][j]
							d = distance(data[blobs[r_b][c_b][0][i]], data[blobs[r_b2][c_b2][0][j]] )
							# print "comp", blobs[r_b][c_b][0][i], "id" ,blobs[r_b][c_b][1][i][2], blobs[r_b2][c_b2][0][j], d					
							(r1,c1, id1) = blobs[r_b][c_b][1][i]
							(r2,c2, id2) = blobs[r_b2][c_b2][1][j]
							grid_f[r1][c1].check_neighbor([d, id2, r2, c2])
							grid_f[r2][c2].check_neighbor([d, id1, r1, c1])
			
						
			# if c_b == 1:
				# sys.exit()
				
	# let all elements set themselves as followers
	for i in range(grid_size):
		for j in range(grid_size):
			if grid_f[i][j]!= None:
				grid_f[i][j].init_as_follower()		

	
def puzzle(grid_size, old_grid_size, nr_words):
	print "NR WORDS", nr_words
	iter = 0
	png_nr = 0
	# log_file = open(output_directory + r"\log.txt", "w")
	#sample words to follow
	follow_inds = Set()
	while len(follow_inds) < nr_words_to_follow:
		follow_inds.add(random.randrange(nr_words))
	follow_inds = list(follow_inds)
	
	# log_file.write("Indexes:")
	# for key, value in global_index.iteritems():
		# log_file.write(str(key)+" " + value.name + " " + str(value.id) + "\n")
		
	
	print "\n========\nSTART PUZZLING\n===========\n"
	log_file = open(log_file_n, 'a')
	log_file.write("\n\n========\nSTART PUZZLING\n===========\n\n")	
	log_file.close()
	trial_nr = 0
	nr_inits = 0
	elem_indexes = range(nr_words)
	grid_size = int(grid_size)
	while not stop_condition(trial_nr):
		for i in range(nr_trials_check):
			if trial_nr%5 == 0:
				print "\nTRIAL", trial_nr, datetime.datetime.now()
				log_file = open(log_file_n, 'a')
				log_file.write("TRIAL " + str(trial_nr) + " " + str(datetime.datetime.now()) +"\n")
				log_file.close()
			# check if you need to reinitialize
			if iter%(nr_words*nr_trials_re_init)==0 or iter ==0:
				nr_inits+=1
				print "\ninit closest trial", trial_nr ,"     start:", datetime.datetime.now()
				log_file = open(log_file_n, 'a')
				log_file.write("init closest at "+str(datetime.datetime.now())+"\n")
				log_file.close()
				init_closest(grid_size, old_grid_size, iter==0)
				print "init closest stop:", datetime.datetime.now()
				log_file = open(log_file_n, 'a')
				log_file.write("stop init closest at "+str(datetime.datetime.now())+"\n")
				log_file.close()
				# log_file.write("INITIALIZED\n\n")
				# print_all_lists(str(trial_nr))
			if iter == 0:
				stats_to_file("FIRST", trial_nr , follow_inds, nr_inits, grid_size, png_nr)
				png_nr+=1
			# pick random element
			random.shuffle(elem_indexes)
			for elem_i in elem_indexes:
				[x,y] = list(global_index[elem_i].pos)
								
				if iter%5000 == 0:
					print "iter", iter,
				
							
				swap_value = float("-inf")
				# check with which neighbor it wants to swap
				for dx in range(neighbor_range_swap[0],neighbor_range_swap[1]):
					for dy in range(neighbor_range_swap[0],neighbor_range_swap[1]):
						# print x, dx, y, dy
						if x+dx >= 0 and x+dx < grid_size and y+dy >= 0 and y+dy < grid_size:
							# check grid elem != none
							# print "in check"
							if grid_f[x+dx][y+dy] != None:
								v = grid_f[x][y].get_improvement(x+dx, y+dy) + grid_f[x+dx][y+dy].get_improvement(x, y)
							else:
								v = grid_f[x][y].get_improvement(x+dx, y+dy)
							if v > swap_value:
								# process swap value
								swap_value = v
								swap_x = x+dx
								swap_y = y+dy
								
				if swap_value > 0:
					xy = grid_f[x][y]
					xy_swap = grid_f[swap_x][swap_y]
					grid_f[x][y] = xy_swap
					grid_f[swap_x][swap_y] = xy
					xy.change_pos(swap_x,swap_y)
					if xy_swap!=None:
						xy_swap.change_pos(x,y)						
				elif swap_value == float("-inf"):
					print "-inf"
					
						
				iter+=1
					
			# figures and stats to file
			if trial_nr%to_file_trials == 0 and trial_nr != 0:
				stats_to_file(iter, trial_nr, follow_inds, nr_inits, grid_size, png_nr)
				png_nr+=1
			trial_nr+=1
	stats_to_file("LAST", trial_nr, follow_inds, nr_inits, grid_size, png_nr)
	
def build_final_grid(nr_words, process, old_grid_size = -1):
	if process == "all" or process == "initial_grid":
		log_file = open(log_file_n, 'a')
		print "get data", datetime.datetime.now()
		log_file.write("get data " + str(datetime.datetime.now()) + "\n")
		log_file.close()
		(old_grid_size, data_sample, grid_sample) = get_sem_data()
		print "get initial grid", datetime.datetime.now()
		log_file = open(log_file_n, 'a')
		log_file.write("get initial grid " + str(datetime.datetime.now()) + "\n")
		log_file.close()
		(new_grid_size, nr_words) = get_grid(old_grid_size, data_sample, grid_sample, nr_words)
		log_file = open(log_file_n, 'a')		
		log_file.write("initial grid finished " + str(datetime.datetime.now()) + "\n")
		log_file.close()
		grid_to_file(output_directory, new_grid_size, "initial", grid_f)
	elif process == "only_puzzle":
		(new_grid_size, nr_words) = grid_and_blob_from_file()
		print "nr words grid from file", nr_words
		grid_to_file(output_directory, new_grid_size, "as_from_file", grid_f)
	else:
		print "unrecognized process type"
		log_file = open(log_file_n, 'a')
		log_file.write("unrecognized process type\n")
		log_file.close()
	if process == "all" or process == "only_puzzle":
		puzzle(new_grid_size, old_grid_size, nr_words)
			
			
if __name__ == "__main__":


	neighbor_range_swap = [-1,2]
	blob_neighbors = [(0,1),(1,-1),(1,0),(1,1)]
	
	parser = argparse.ArgumentParser(description='Run puzzle algorithm')
	# '''parser.add_argument(<naam>, type=<type>, default=<default>, help=<help message>)'''
	parser.add_argument("case_name", help="Name of the data case that you want to process")
	parser.add_argument("nr_words", type=int ,help="The number of words in the data case")
	parser.add_argument("--process", default=["all"] , nargs='*',help="What parts of the algorithm you want to execute")
	parser.add_argument("--max_closest", type=int , nargs='*',default=[8] ,help="number of closest words taken into account")
	parser.add_argument("--nr_trials_check", type=int ,nargs='*',default=[1] ,help="bla")
	parser.add_argument("--nr_trials_re_init", type=int ,nargs='*',default=[250] ,help="bla")
	parser.add_argument("--stop_nr_trials", type=int ,nargs='*',default=[500] ,help="bla")
	parser.add_argument("--block_ratio", type=int ,default=[2] ,nargs='*',help="bla")
	parser.add_argument("--data_portion", type=int ,default=[5] ,nargs='*',help="bla")
	parser.add_argument("--nr_words_to_follow", type=int ,default=[20] ,nargs='*',help="bla")
	parser.add_argument("--to_file_trials", type=int ,default=[20] ,nargs='*',help="bla")
	parser.add_argument("--old_grid_size", type=int , nargs='*',default=[-1] , help = "If you do only puzzle you have to provide the grid_size of the sample input")
	parser.add_argument("--dif_output_dir", nargs='*', default=[None])
	
	args = parser.parse_args()
	kwargs = vars(args)	
	
	print kwargs
	
	data_case_name = "\\" + kwargs["case_name"]
	nr_words = kwargs["nr_words"]
	
	process = kwargs["process"][0]
	max_closest = kwargs["max_closest"][0]
	nr_trials_check = kwargs["nr_trials_check"][0]
	nr_trials_re_init = kwargs["nr_trials_re_init"][0]
	stop_nr_trials = kwargs["stop_nr_trials"][0]
	block_ratio = kwargs["block_ratio"][0]
	data_portion = kwargs["data_portion"][0]
	nr_words_to_follow = kwargs["nr_words_to_follow"][0]
	to_file_trials = kwargs["to_file_trials"][0]
	old_grid_size = kwargs["old_grid_size"][0]
	dif_output_dir = kwargs["dif_output_dir"][0]
	
	input_directory_landscape = input_directory_landscape + data_case_name
	input_directory_cooc = input_directory_cooc + data_case_name
	print dif_output_dir
	if dif_output_dir == None:
		output_directory = output_directory + data_case_name
	else:
		output_directory = output_directory +  "\\" + dif_output_dir  		
	if not os.path.exists(output_directory):
		os.makedirs(output_directory)	
		print "directory made"
	
	log_file_n = output_directory+r"\log_file.txt"
	log_file = open(log_file_n, 'w')
	log_file.write("=====START SETTINGS=====\n")
	for key, value in kwargs.iteritems():		
		log_file.write(key+ ": " + str(value) +"\n")
	log_file.write("=====END  SETTINGS=====\n\n")
	log_file.write("START\n")
	log_file.close()
	
	f = open(output_directory+r"\lists of closest.txt","w")
	f.close()	
	build_final_grid(nr_words, process, old_grid_size)
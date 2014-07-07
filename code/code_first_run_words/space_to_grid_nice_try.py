from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pylab
import math
import datetime
from thesis_utilities import *
import sys
import copy
import random
from pympler import summary
from pympler import muppy
import gc
import calc_angle

figure_size = 8
update_neighborhood = 300
prev_steps = defaultdict(lambda: np.zeros(2))
grid_size_global = []

class TypeKeeper:	
	def __init__(self, indexes):
		self.indexes = indexes
		
	def get_color(self, x):
		return self.indexes[x]

class GridPoint:
	
	stepsize = 0.6 # before: 0.4
	
	def __init__(self, x, y, grid):
		self.pos = np.array([float(x), float(y)])
		self.assignments = []
		self.lonely_points = []
		self.steps = {}
		self.providers = []
		self.prev_providers = []
		self.grid = grid
		self.arrivals = []
				
	def reset(self):
		self.assignments=[]
		self.lonely_points=[]
		self.steps = {}	
		self.prev_providers = self.providers
		self.providers = []
		
	# assignment 0 = numpy array with position, 1 = index of point, 2 = orig_pos
	def add_assignment(self, assignment):			
		self.assignments.append(assignment)
		if assignment[1] not in self.arrivals:
			self.arrivals.append(assignment[1])
		
	def add_provider(self, prov):
		self.providers.append(prov)
		
	def get_prev_providers(self):
		return self.prev_providers
		
	def add_lonely_gridpoint(self, x, y):
		# implement processing of grid points
		g_pos = np.array([float(x), float(y)])		
		dist = np.sqrt(np.inner(g_pos-self.pos, g_pos-self.pos))
		self.lonely_points.append([dist, g_pos])
		
	def get_movement(self, i):
		if len(self.assignments) < 2:	
			return np.array([0.0,0.0])
		elif self.steps == {}:
			self.calc_assignments()
			if not i in self.steps.keys():
				return np.array([0.0,0.0])
			return self.steps[i]
		else:
			if not i in self.steps.keys():
				return np.array([0.0,0.0])				
			return self.steps[i]
	
	## p = point, p0 = first point of line, p1 = other point of line
	# def dist_to_line(p, p0, p1):
		# gamma_q = np.sum(np.multiply(p1-p0, p-p0)) / np.sum(np.power(p1-p0,2))
		# return np.sqrt(np.sum(p-p0- gamma_q*np.power(p1-p0,2)))
	
	def get_step(self, min_max, lt_min):
		# Next part makes direction slightly more random		
		# q = np.array([p[0]+(random.random()-0.5)/3, p[1]+(random.random()-0.5)/3])
		# d1 = np.sqrt(np.dot(q-gp, q-gp))
		if lt_min:
			min_a = math.floor(min_max[0]*100)/100
			max_a = math.ceil(min_max[1]*100)/100
			alpha = random.uniform(min_a, max_a)
		else:
			min_a = math.ceil(min_max[0]*100)/100
			max_a = math.floor(min_max[1]*100)/100
			alpha = random.uniform(0, min_a + 2*math.pi-max_a)
			alpha = min_a - alpha
			if alpha < 0:
				alpha = 2*math.pi+alpha
		return np.array([math.sin(alpha), math.cos(alpha)]) * self.stepsize
	
	def get_stepXXX(self, gp, p, d):
		# Next part makes direction slightly more random		
		# q = np.array([p[0]+(random.random()-0.5)/3, p[1]+(random.random()-0.5)/3])
		# d1 = np.sqrt(np.dot(q-gp, q-gp))
		alpha = math.asin( abs(gp[0]-p[0]) / d )
		step = np.array([math.sin(alpha), math.cos(alpha)]) * self.stepsize
		if gp[0] < p[0]:
			step[0] *= -1.0
		if gp[1] < p[1]:
			step[1]*=-1.0
		return step
	
	# ZORGEN DAT DEZE NIET BUITEN HET GRID WANDELEN!!!
	def calc_assignments(self):	
		# print(self.assignments[0])
		# Original position kan verwijderd worden!! als je het op basis van arrival doet
		grid_size = grid_size_global[0]
		if grid_size == -1:
			print("shizzle with grid_size")
			sys.exit()
		
		assignment_ids = [y for (x,y,z) in self.assignments]
		for i in reversed(range(len(self.arrivals))):
			if self.arrivals[i] not in assignment_ids:
				del self.arrivals[i]			
		
		for index in range(len(self.assignments)):
			if len(self.lonely_points)>2:
				min_max, lt_min = calc_angle.calc(self.pos, np.array([y for [x,y] in self.lonely_points]))
				ass_id = self.assignments[index][1]
				if ass_id != self.arrivals[-1]:		
					found = False
					if not np.array_equal(prev_steps[ass_id] , np.zeros(2)):
						angle = calc_angle.angle(np.array([0,0]), prev_steps[ass_id])
						if (lt_min and angle>min_max[0] and angle<min_max[1]) or (not lt_min and (angle<min_max[0] or angle>min_max[1])):
							step = prev_steps[ass_id]
							newpos = step+self.assignments[index][0]
							if not (newpos[0] < 0 or newpos[0] > grid_size or newpos[1]<0 or newpos[1]>grid_size):
								self.steps[ass_id] = step
								found = True
								# if newpos[0] < 0 or newpos[0] > grid_size or newpos[1]<0 or newpos[1]>grid_size:
									# print( "walking out of grid")
					if not found:
						step = self.get_step(min_max, lt_min)						
						newpos = step+self.assignments[index][0]						
						if not (newpos[0] < 0 or newpos[0] > grid_size or newpos[1]<0 or newpos[1]>grid_size):						
							self.steps[ass_id] = step	
						# if newpos[0] < 0 or newpos[0] > grid_size or newpos[1]<0 or newpos[1]>grid_size:
							# print( "walking out of grid")
			elif len(self.lonely_points)==1:
				alpha = calc_angle.angle(self.pos, self.assignments[index][0])
				step = np.array([math.cos(alpha), math.sin(alpha)])	
				newpos = step+self.assignments[index][0]
				# newpos[0] = max(min(grid_size, newpos[0]),0)
				# newpos[1] = max(min(grid_size, newpos[1]),0)
				# if newpos[0] < 0 or newpos[0] > grid_size or newpos[1]<0 or newpos[1]>grid_size:
					# print( "walking out of grid")
				if not (newpos[0] < 0 or newpos[0] > grid_size or newpos[1]<0 or newpos[1]>grid_size):						
					self.steps[self.assignments[index][1]] = step
		
	
	def calc_assignments2(self):		
		max_dist_orig = 0.0
		max_ind = -1			
		for index in range(len(self.assignments)):
			[pos, ind, orig_pos] = self.assignments[index]			
			dist_orig = np.sqrt(np.dot(orig_pos-pos, orig_pos-pos))
			if dist_orig > max_dist_orig:
				max_dist_orig = dist_orig
				max_ind = index

		if len(self.lonely_points) > 1:
			min_max, lt_min = calc_angle.calc(self.pos, np.array([y for [x,y] in self.lonely_points]))
		
			for index in range(len(self.assignments)):
				if index != max_ind:		
					ass_id = self.assignments[index][1]
					found = False
					if not np.array_equal(prev_steps[ass_id] , np.zeros(2)):
						angle = calc_angle.angle(np.array([0,0]), prev_steps[ass_id])
						if lt_min and angle>min_max[0] and angle<min_max[1]:
							self.steps[ass_id] = prev_steps[ass_id]
							found = True
							# print("previous step")
						elif not lt_min and (angle<min_max[0] or angle>min_max[1]):
							self.steps[ass_id] = prev_steps[ass_id]
							found = True
							# print("previous step")
					if not found:
						step = self.get_step(min_max, lt_min)
						self.steps[ass_id] = step
						# print("new step", step)
						
		
		
	def calc_assignmentsXXX(self):
		self.lonely_points.sort(key=lambda x: x[0])	
		# make point move with smallest distance to 'movement line' from grid point to lonely gridpoint
		
		for i in range(len(self.assignments)-1):
			if i < len(self.lonely_points):
				min_dist_lgp = float("inf")
				min_dist_orig = float("inf")
				min_ind = -1
				p = self.lonely_points[i]			
				for index in range(len(self.assignments)):
					[pos, ind, orig_pos] = self.assignments[index]
					if not ind in self.steps.keys():
						dist_orig = np.sqrt(np.dot(orig_pos-pos, orig_pos-pos))
						if dist_orig < min_dist_orig:
							min_dist_lgp = np.sqrt(np.dot(p[1]-pos, p[1]-pos))
							min_dist_orig = dist_orig
							min_ind = index
						if dist_orig == min_dist_orig:
							dist_lgp = np.sqrt(np.dot(p[1]-pos, p[1]-pos))
							if dist_lgp < min_dist_lgp:
								min_dist_lgp=dist_lgp
								min_ind = index	
				self.steps[self.assignments[min_ind][1] ] = self.get_step(p[1], self.assignments[min_ind][0], min_dist_lgp)


	
def restart(data_folder, log_memory, last_iter_nr, last_fig_nr):
	blob_colors = {}
	colors = get_colors()
	f = open(data_folder+r"\color_file.txt")
	for line in f:
		line = line.replace("\n", "")
		line = line.split(";")
		color = line[1]
		color = color.replace("]","")
		color = color.replace("[","")
		color = color.split(", ")
		color = [float(color[0]), float(color[1]), float(color[2])]
		blob_colors[int(line[0])] = color
	f.close()
	blob_colors = TypeKeeper(blob_colors)
	
	data = space_from_file(data_folder+r"\intermediate_grids\data_"+str(last_fig_nr)+"_it"+str(last_iter_nr)+".txt")
	print("data shape",data.shape[0])
	nr_items = data.shape[0]
	grid_size_global.append( int(math.ceil(math.sqrt(nr_items))))
	grid_size = grid_size_global[0]
	grid = []
	for i in range(grid_size):
		grid.append([])
		for j in range(grid_size):
			grid[i].append(GridPoint(i,j, grid))
	
	orig_data = space_from_file(data_folder + r"\intermediate_grids\data_orig.txt")
	
	iter_nr, assignment = iterate(data, orig_data, grid, last_fig_nr+1, nr_items, data_folder+r"\intermediate_grids", log_memory, last_iter_nr+1, blob_colors) 
	
	f = open(data_folder+r"\init_grid_assignment.txt", "w")
	for elem in assignment:
		f.write(str(elem[0]) +";"+ str(elem[1]) +";"+ str(elem[2]) + "\n") 
	f.close()

def iterate(data, orig_data, grid, fig_nr, nr_items, result_path,  log_memory, iternr, blob_nr_keeper=None):
	grid_size = grid_size_global[0]
	print("grid size in iterate =", grid_size)
	#iteratively move to grid points
	assigned = set()
	assignment = []
	sufficient_gradient =True
	neighborhood_size = 5
	first = True
	print("start conversion to grid", datetime.datetime.now())
	neighborhood_size_changed = True
	
	#find intial lonely gridpoints 
	lonely_points = []
	assigned = set()	
	assignment = []
	for i in range(nr_items):			
		nearest = [min(max(int(round(data[i,0])),0),grid_size-1), min(max(int(round(data[i,1])),0),grid_size-1)]
		grid[nearest[0]][nearest[1]].add_assignment( (data[i,:], i, orig_data[i,:]) )
		assigned.add((nearest[0], nearest[1]))
		assignment.append((nearest[0], nearest[1], i))
	for i in range(grid_size):
		for j in range(grid_size):
			if len(grid[i][j].assignments) == 0:
				lonely_points.append(grid[i][j])
	
	print("\n\nNr lonely points at start:", len(lonely_points), "with grid size", grid_size, "and", nr_items, "elems")
	while len(assigned)<nr_items:
		
		iternr+=1
		if not first:
			assigned = set()	
			assignment = []
			
			# Assign each data point to the nearest grid point
			for i in range(nr_items):			
				nearest = [min(max(int(round(data[i,0])),0),grid_size-1), min(max(int(round(data[i,1])),0),grid_size-1)]				
				grid[nearest[0]][nearest[1]].add_assignment( (data[i,:], i, orig_data[i,:]) )
				assigned.add((nearest[0], nearest[1]))
				assignment.append((nearest[0], nearest[1], i))
		if first:
			first = False
				
		if len(assigned)<nr_items:	
			# VERVANG DIT MET DOOR LONELY POINTS HEEN LOPEN
			for lpi in reversed(range(len(lonely_points))) :
				lonely_p = lonely_points[lpi]
				if len(lonely_p.assignments)==0:
					i = int(lonely_p.pos[0])
					j = int(lonely_p.pos[1])
					if sufficient_gradient:
						no_providers = True
						if not neighborhood_size_changed:
							# DOOR VORIGE PUNTEN HEEN LOPEN
							prev_providers = lonely_p.get_prev_providers()
							no_providers = len(prev_providers)==0
							nr_additions = 0
							checked = set()
							for [px,py] in prev_providers:
								from_pi, to_pi = max(0, px-2), min(grid_size, px+4)
								from_pj, to_pj = max(0, py-2), min(grid_size, py+4)
								for ii in range(from_pi,to_pi):
									for jj in range(from_pj,to_pj):
										if (ii,jj) not in checked and len(grid[ii][jj].assignments) > 1:
											grid[ii][jj].add_lonely_gridpoint(i,j)
											lonely_p.add_provider([ii,jj])
											nr_additions +=1
											checked.add((ii,jj))
						else:
							from_i, to_i = max(0, i-neighborhood_size), min(grid_size, i+neighborhood_size+1)
							from_j, to_j = max(0, j-neighborhood_size), min(grid_size, j+neighborhood_size+1)
							for ii in range(from_i,to_i):
								for jj in range(from_j,to_j):
									if len(grid[ii][jj].assignments) > 1:
											grid[ii][jj].add_lonely_gridpoint(i,j)
											lonely_p.add_provider([ii,jj])
					else:
						for elem in assigned:
							if len(grid[elem[0]][elem[1]].assignments) > 0:
								grid[elem[0]][elem[1]].add_lonely_gridpoint(i,j)
				else:
					del lonely_points[lpi]
			
			nr_movements = 0
			for i in range(nr_items):
								
				nearest = [min(max(int(round(data[i,0])),0),grid_size-1), min(max(int(round(data[i,1])),0),grid_size-1)]
				m = grid[nearest[0]][nearest[1]].get_movement(i)
				if m[0] != 0 or m[1] != 0:
					nr_movements+=1
					prev_steps[i] = m
				data[i,:] = np.add(data[i,:] , m)
			for i in range(grid_size):
				for j in range(grid_size):
					grid[i][j].reset()
		
		
		neighborhood_size_changed = False
		if iternr%5 == 0:
			sufficient_gradient = True
			sufficient_gradient = nr_movements > 50 or len(assigned)+nr_movements==nr_items
			# sufficient_gradient = nr_movements > 50 or len(assigned)+nr_movements==nr_items
			if not sufficient_gradient:
				print("insuf grad")			
			print("i:",iternr,"ass",len(assigned), "mo:", nr_movements, "nr lonely points:", len(lonely_points))
		
			if nr_movements < update_neighborhood and len(assigned)+nr_movements!=nr_items:
			# if nr_movements < update_neighborhood:
				neighborhood_size_changed = True
				neighborhood_size += 5
				print("neigh size upgraded", neighborhood_size)
			
			gc.collect()
				
		
		if iternr%10 == 0 and len(assigned)+nr_movements!=nr_items:
			neighborhood_size_changed = True
		
		if iternr%15 == 0 or len(assigned) == nr_items:
			print("\n\n")
			if blob_nr_keeper!=None:
				used_marker = "o"
				if nr_items > 1000:
					used_marker = "."
				print( "im" +  str(fig_nr))
				space_to_file(data, result_path + r"\data_"+str(fig_nr)+"_it"+str(iternr)+".txt")
				image_name = result_path + r"\intermediate_grid_formed_"+str(fig_nr)+".pdf"
				fig = plt.figure(figsize=(figure_size, figure_size))
				for i in range(nr_items):
					prop_plot=plt.scatter(data[i,0],  data[i,1], c=blob_nr_keeper.get_color(i), marker=used_marker)
					if nr_items > 1000:
						prop_plot.set_edgecolor("none")
				# for i in range(grid_size):
					# for j in range(grid_size):
						# if len(grid[i][j].assignments) == 0:
							# prop_plot = plt.scatter(j, grid_size-1-i, c = "k", marker = used_marker)
							# if nr_items > 1000:
								# prop_plot.set_edgecolor("none")
				plt.axis([-1, grid_size, -1, grid_size])
				plt.title("Result at iteration " + str(iternr))
				fig.savefig(image_name, bbox_inches='tight')
				fig.savefig(result_path + r"\intermediate_grid_"+four_digit_string(fig_nr)+".png")
				plt.close()		
				fig_nr+=1
				print( "iter", iternr, "nr assigned", len(assigned), "from", nr_items, "mo:", nr_movements, "at", datetime.datetime.now())

			
			if log_memory:
				all_objects = muppy.get_objects()
				sum1 = summary.summarize(all_objects)
				summary.print_(sum1, limit=15, sort='size')
				print("printed at", datetime.datetime.now())
		# if iternr == 26:
			# sys.exit()
		
	return iternr, assignment

	
def space_to_grid_iterative(data, result_path, log_memory, with_figures=True, blob_nr_keeper = None, scale = True):
	
	nr_items = data.shape[0]
	grid_size_global.append( int(np.ceil(np.sqrt(nr_items))))
	grid_size = grid_size_global[0]
	space_to_file(data, result_path + r"\data_orig.txt")	
	orig_data = np.copy(data)
	# Prepare grid
	grid = []
	for i in range(grid_size):
		grid.append([])
		for j in range(grid_size):
			grid[i].append(GridPoint(i,j, grid))
	

	# Rescale and move data
	if(scale):
		print("scale data")	
		move = 0.9
		move_scale = np.array([move , move])
		if data.min(axis=0)[0] < 0:
			move_scale[0] = 2-move
		if data.min(axis=0)[1] < 0:
			move_scale[1] = 2-move
		data = data - (data.min(axis=0) * move_scale)
		scaling = (float(grid_size)-1)/ (data.max(axis=0) * 1.2)
		data = np.multiply(data, np.tile(scaling, (nr_items, 1) ) )	
	
	colors = get_colors()	
	
	# Show initial data
	if with_figures:
		x = list(data[:,0])		
		xi = np.tile(np.arange(grid_size), (grid_size, 1))
		y = list(data[:,1])
		yi = np.tile( np.array([np.arange(grid_size)]).T, (1,grid_size))
		image_name = result_path + r"\space_to_grid_init_plot.pdf"
		fig = plt.figure()
		plt.plot(np.ndarray.flatten(xi), np.ndarray.flatten(yi), 'b.')
		plt.scatter( x, y, c=colors)
		fig.savefig(image_name, bbox_inches='tight')
		plt.close()
		
		image_name = result_path + r"\space_to_grid_init_plot2.pdf"
		fig = plt.figure()
		plt.scatter( x, y, c=colors)
		fig.savefig(image_name, bbox_inches='tight')
		plt.close()
	
	fig_nr = 1
	
	iternr = 0
	iternr, assignment = iterate(data, orig_data, grid, fig_nr, nr_items, result_path, log_memory, iternr, blob_nr_keeper)
	
	print("needed ", iternr, "iterations for", len(assignment), "points")
	print("\n=============\nDONE\n=============\n")

	
	# plt.plot(np.ndarray.flatten(xi), np.ndarray.flatten(yi), 'b.')
	# plt.scatter( x, y, c=colors)
	# plt.show()
	
	if with_figures:
		for i in range(nr_items):
			data[assignment[i][2],:] = np.array([assignment[i][0], assignment[i][1]])
		x = list(data[:,0])		
		y = list(data[:,1])
		image_name = result_path + r"\grid_result_plot.pdf"
		fig = plt.figure(figsize=(figure_size, figure_size))
		plt.scatter( x, y, c=colors)
		plt.title("Result of forming a grid from a space")
		plt.axis([-1, grid_size+1, -1, grid_size+1])
		# fig.savefig(image_name, bbox_inches='tight')
		fig.savefig(image_name)
		plt.close()
	
	# return result
	return assignment, grid_size	
		
def get_minst_data(file):
	f = open(file, 'r')
	data = []
	labels = []
	for line in f:		
		line = line.replace("\n", "")
		instance = line.split(" ")
		data.append([float(instance[0]), float(instance[1])])
		labels.append(float(instance[2]))
	return data,labels
	
if __name__ == "__main__":
	# random_data = (np.random.random((2500, 2)) * 6) -3
	# random_data[0:100,:] = (np.random.random((500, 2)) * 3) + 0.5 
	# random_data[500:2500,:] = (np.random.random((2000, 2)) * 6) -3
	# ass, grid_size = space_to_grid_iterative(random_data)	
	
	
	# file = r"K:\Lydia\code\tsne_python\minst_data_reduced.txt"
	# (data, labels) = get_minst_data(file)
	# data = np.array(data)
	# plt.scatter(data[:,0], data[:,1], c=labels)
	# plt.show()
	# print("shape:", data.shape)
	# (assignment, grid_size) = space_to_grid_iterative(data )
	# index = 0
	# x=[]
	# y=[]
	# l=[]
	# for elem in assignment:
		# x.append(elem[0])
		# y.append(elem[1])
		# l.append(labels[elem[2]])	
	# plt.scatter(x, y, c=l);
	# plt.show()
	
	# update_neighborhood = 500
	# data_case = "\cutoff_10_nolog"
	# iter = 120
	# fig = 6
	# restart(r"D:\Users\Lydia\results puzzle" + data_case, False, iter, fig)
	
	update_neighborhood = 5
	data_case = "\test3"
	iter = 20
	fig = 1
	restart(r"D:\Users\Lydia\results puzzle" + data_case, False, iter, fig)
	
	
	
	
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pylab
import math
import datetime
from thesis_utilities import *

figure_size = 8

class TypeKeeper:	
	def __init__(self, indexes):
		self.indexes = indexes
		
	def get_color(self, x):
		return self.indexes[x]

class GridPoint:
	
	stepsize = 0.6 # before: 0.4
	
	def __init__(self, x, y):
		self.pos = np.array([float(x), float(y)])
		self.assignments = []
		self.lonely_points = []
		self.steps = {}
				
	def reset(self):
		self.assignments = []
		self.lonely_points = []
		self.steps = {}
		
	# assignment 0 = numpy array with position, 1 = index of point
	def add_assignment(self, assignment):			
		self.assignments.append(assignment)
		
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
	
	def get_step(self, gp, p, d):
		alpha = math.asin( abs(gp[0]-p[0]) / d )
		step = np.array([math.sin(alpha), math.cos(alpha)]) * self.stepsize
		# print "step", step, "for point", p, "and gridpoint", gp, "\n"
		if gp[0] < p[0]:
			step[0] *= -1.0
		if gp[1] < p[1]:
			step[1]*=-1.0
		return step
	
	
	def calc_assignments(self):
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
	
	def calc_assignments_old(self):
		self.lonely_points.sort(key=lambda x: x[0])	
		for i in range(len(self.assignments)-1):
			if i < len(self.lonely_points):
				min_dist = float("inf")
				min_ind = -1
				p = self.lonely_points[i]			
				for index in range(len(self.assignments)):
					a = self.assignments[index]
					if not a[1] in self.steps.keys():
						dist = np.sqrt(np.inner(p[1]-a[0], p[1]-a[0]))
						if dist< min_dist:
							min_dist = dist
							min_ind = index
				self.steps[self.assignments[min_ind][1] ] = self.get_step(p[1], self.assignments[min_ind][0], min_dist)
			
	
def getColors(data):
	nr_items = data.shape[0]
	max_y = data.max(axis=0)[1] * 1.2
	max_x = data.max(axis=0)[0] * 1.2
	colors = []
	for i in range(nr_items):
		colors.append( (data[i,0]/max_x, 0.1, data[i,1]/max_y) )	
		if colors[-1][0] <0 or  colors[-1][0] > 1:
			print "wrong", data[i,0], max_x
		if colors[-1][1] <0 or  colors[-1][1] > 1:
			print "wrong", data[i,1], max_y
	return colors

	
def space_to_grid_iterative(data, result_path, with_figures=True, blob_nr_keeper = None):
	
	nr_items = data.shape[0]
	grid_size = int(np.ceil(np.sqrt(nr_items)))
	
	# Prepare grid
	grid = []
	for i in range(grid_size):
		grid.append([])
		for j in range(grid_size):
			grid[i].append(GridPoint(i,j))
			
	# Rescale and move data
	print "scale data"
	move_scale = np.array([0.9 , 0.9])
	if data.min(axis=0)[0] < 0:
		move_scale[0] = 1.1
	if data.min(axis=0)[1] < 0:
		move_scale[1] = 1.1
	data = data - (data.min(axis=0) * move_scale)
	scaling = (float(grid_size)-1)/ (data.max(axis=0) * 1.2 )
	data = np.multiply(data, np.tile(scaling, (nr_items, 1) ) )	
	colors = getColors(data)	
	
	# Show initial data
	# print "INITIAL DATA"
	if with_figures:
		x = list(data[:,0])		
		xi = np.tile(np.arange(grid_size), (grid_size, 1))
		y = list(data[:,1])
		yi = np.tile( np.array([np.arange(grid_size)]).T, (1,grid_size))
		image_name = result_path + r"\space_to_grid_init_plot.pdf"
		# print "Image name: ", image_name
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
	
	#iteratively move to grid points
	orig_data = np.copy(data)
	assigned = set()
	assignment = []	
	iternr = 0
	old_len = 0
	sufficient_gradient =True
	fig_nr = 1
	neighborhood_size = 10
	print "start conversion to grid", datetime.datetime.now()
	while len(assigned)<nr_items:
		
		iternr+=1
		assigned = set()	
		assignment = []
		
		# Assign each data point to the nearest grid point
		for i in range(nr_items):			
			nearest = [int(round(data[i,0])), int(round(data[i,1]))]
			grid[nearest[0]][nearest[1]].add_assignment( (data[i,:], i, orig_data[i,:]) )
			assigned.add((nearest[0], nearest[1]))
			assignment.append((nearest[0], nearest[1], i))
				
		# if not sufficient_gradient:
			# print "insufficient gradient"
		if len(assigned)<nr_items:	
			for i in range(grid_size):
				for j in range(grid_size):
											
					# if has no assignments
					if len(grid[i][j].assignments)==0:
						
						if sufficient_gradient:
							from_i, to_i = max(0, i-neighborhood_size), min(grid_size, i+neighborhood_size+1)
							from_j, to_j = max(0, j-neighborhood_size), min(grid_size, j+neighborhood_size+1)
							for ii in range(from_i,to_i):
								for jj in range(from_j,to_j):
									if grid[ii][jj].assignments > 0:
											grid[ii][jj].add_lonely_gridpoint(i,j)
						else:
							for elem in assigned:
								if grid[elem[0]][elem[1]].assignments > 0:
									grid[elem[0]][elem[1]].add_lonely_gridpoint(i,j)
														
			nr_movements = 0
			for i in range(nr_items):
				nearest = [int(round(data[i,0])), int(round(data[i,1]))]
				m = grid[nearest[0]][nearest[1]].get_movement(i)
				if m[0] != 0 or m[1] != 0:
					nr_movements+=1
				data[i,:] = np.add(data[i,:] , m)
				
			for i in range(grid_size):
				for j in range(grid_size):
					grid[i][j].reset()
		
		
		
		if iternr%5 == 0:
			# xx = list(data[:,0])		
			# yy = list(data[:,1])
			# fig = plt.figure()
			# plt.scatter( xx, yy, c=colors)
			# plt.show()
			# plt.close()
		
			sufficient_gradient = nr_movements > 50

			if not sufficient_gradient and iternr%20!=0:
				print "insuf grad",
			
			print "i:",iternr,"ass",len(assigned), "mo:", nr_movements
		
			if nr_movements < 300:
				neighborhood_size += 5
				print "neigh size upgraded"
		
		if iternr%20 == 0:
			print
			if blob_nr_keeper!=None:
				used_marker = "o"
				if nr_items > 1000:
					used_marker = "."
				print "im" +  str(fig_nr),
				image_name = result_path + r"\intermediate_grid_formed_"+str(fig_nr)+".pdf"
				fig = plt.figure(figsize=(figure_size, figure_size))
				fig_nr+=1
				for i in range(nr_items):
					prop_plot=plt.scatter( data[i,1], grid_size-1-data[i,0], c=blob_nr_keeper.get_color(i), marker=used_marker)
					if nr_items > 1000:
						prop_plot.set_edgecolor("none")
				for i in range(grid_size):
					for j in range(grid_size):
						if grid[i][j].assignments == 0:
							prop_plot = plt.scatter(j, grid_size-1-i, c = "k", marker = used_marker)
							if nr_items > 1000:
								prop_plot.set_edgecolor("none")
				plt.axis([-1, grid_size, -1, grid_size])
				plt.title("Result at iteration " + str(iternr))
				fig.savefig(image_name, bbox_inches='tight')
				fig.savefig(result_path + r"\intermediate_grid_"+four_digit_string(fig_nr)+".png")
				plt.close()		
				print "iter", iternr, "nr assigned", len(assigned), "from", nr_items, "at", datetime.datetime.now()
				
		old_len = len(assigned)
				
						
	
	# print result
	print "needed ", iternr, "iterations for", len(assignment), "points"
	print "\n=============\nDONE\n=============\n"	

	
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
	
	
	file = r"K:\Lydia\code\tsne_python\minst_data_reduced.txt"
	(data, labels) = get_minst_data(file)
	data = np.array(data)
	plt.scatter(data[:,0], data[:,1], c=labels)
	plt.show()
	print "shape:", data.shape
	(assignment, grid_size) = space_to_grid_iterative(data )
	index = 0
	x=[]
	y=[]
	l=[]
	for elem in assignment:
		x.append(elem[0])
		y.append(elem[1])
		l.append(labels[elem[2]])	
	plt.scatter(x, y, c=l);
	plt.show()
	
	
	
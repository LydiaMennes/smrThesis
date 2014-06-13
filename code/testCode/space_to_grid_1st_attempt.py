import numpy as NP
import matplotlib.pyplot as plt
import pylab

S_NEIGH = 4
step_rate = 0.5
pointValue = 10
blow_time = 5

class GridPoint:
	
	d_min = 0.1
	v_bonus = 2.0	
	closeness = 0.75
	
	def __init__(self):
		self.dist_assigned = self.v_bonus
		self.assigned = 0
		self.d_clo = 1000
		self.close_one = False
				
	def reset(self):
		self.assigned = 0
		self.dist_assigned = self.v_bonus
		self.d_clo = 1000
		self.close_one = False
		
	def add_assignment(self, d):
		if d<self.closeness:
			self.close_one = True			
		if d<self.d_clo:			
			self.d_clo = d			
		if d > self.d_min:
			self.dist_assigned += 1.0/d
		else:
			self.dist_assigned += 1.0/self.d_min			
		
	def get_value(self, d):	
		p = 0
		print("dist: %.2f , d_clo: %.2f" % (d, self.d_clo) )
		if d > self.d_min:			
			if d == self.d_clo:
				if d < 0.5:
					p = ((1.0/d)+self.v_bonus) / self.dist_assigned
					print "bonus", 
				else:
					p = ((1.0/d)+(self.v_bonus*2)) / self.dist_assigned
					print "big bonus", 
			else:
				p = (1.0/d) / self.dist_assigned
		else:
			p = (1.0/self.d_min) / self.dist_assigned
		if self.close_one:
			return pointValue * p
		print "xtra",
		return pointValue * 5 * p

def surrounding_points():
	s = NP.array([[-1,0,1,2]])	
	# s = NP.array([[0,1]])	
	if s.shape != (1,S_NEIGH):
		print "adjust indexes"
	x = NP.tile(s, (2,S_NEIGH,1))
	y = NP.tile(s.T, (1,S_NEIGH))
	x[1,:,:]=y
	return x
	
def getColors(data):
	nr_items = data.shape[0]
	max_y = data.max(axis=0)[1] * 1.2
	max_x = data.max(axis=0)[0] * 1.2
	colors = []
	for i in range(nr_items):
		colors.append( (data[i,0]/max_x, data[i,1]/max_y  ,0.1) )
	# colorBins = int(NP.ceil(nr_items**(1/float(3))))
	# colors = []
	# v = 1.0/ (colorBins+1)
	# c = 0
	# for i in range(1,colorBins+1):
		# for j in range(1,colorBins+1):
			# for k in range(1,colorBins+1):
				# c+=1
				# if c<=nr_items:
					# colors.append( (i*v, j*v, k*v) )
	return colors
	
def space_to_grid_iterative(data):
	
	nr_items = data.shape[0]
	grid_size = int(NP.ceil(NP.sqrt(nr_items)))
	print "grid size:", grid_size
	# colors_g = [(1,1,1)]*(grid_size*grid_size)
	
	# Prepare grid
	grid = []
	for i in range(grid_size):
		grid.append([])
		for j in range(grid_size):
			grid[i].append(GridPoint())
			
	# Rescale and move data
	data = data - data.min(axis=0) 
	scaling = (float(grid_size)-1)/ data.max(axis=0)
	data = NP.multiply(data, NP.tile(scaling, (nr_items, 1) ) )	
	colors = getColors(data)
	# print data	
	# print
	
	# Show initial data
	print "INITIAL DATA"
	x = list(data[:,0])		
	xi = NP.tile(NP.arange(grid_size), (grid_size, 1))
	y = list(data[:,1])
	yi = NP.tile( NP.array([NP.arange(grid_size)]).T, (1,grid_size))
	plt.scatter( x, y, c=colors)
	plt.plot(NP.ndarray.flatten(xi), NP.ndarray.flatten(yi), 'b.')
	plt.show()
	
	#iteratively move to grid points
	layer = surrounding_points()
	
	assigned = set()
	assignment = []
	
	iternr = 0
	while len(assigned)<nr_items:
		iternr+=1
		if iternr%50 == 0:
			print iternr
			
		# if iternr%blow_time == 0:
			# data = data * 1.3
			
		assigned = set()	
		assignment = []
		
		for i in range(nr_items):
			p = NP.array([[[NP.floor(data[i,0])]], [[NP.floor(data[i,1])]]])
			neighbors = NP.add(layer, NP.tile(p, (1,S_NEIGH,S_NEIGH)))
			q = NP.array([[[data[i,0]]], [[data[i,1]]]])
			dist = NP.subtract(neighbors, NP.tile(q, (1,S_NEIGH,S_NEIGH)))
			dist = NP.sqrt(NP.sum(NP.power(dist,2), 0))
			for i in range(S_NEIGH):
				for j in range(S_NEIGH):
					ix = int(neighbors[0,i,j])
					iy = int(neighbors[1,i,j])
					if ix >= 0 and iy >= 0 and ix <grid_size and iy < grid_size:
						grid[ix][iy].add_assignment(dist[i,j])
					
		for i in range(nr_items):
			p = NP.array([[[NP.floor(data[i,0])]], [[NP.floor(data[i,1])]]])
			neighbors = NP.add(layer, NP.tile(p, (1,S_NEIGH,S_NEIGH)))
					
					
			q = NP.array([[[data[i,0]]], [[data[i,1]]]])
			dist = NP.subtract(neighbors, NP.tile(q, (1,S_NEIGH,S_NEIGH)))
			dist = NP.sqrt(NP.sum(NP.power(dist,2), 0))
			max_ind = (-1,-1)
			max_v = -1
			for j in range(S_NEIGH):
				for k in range(S_NEIGH):
					if neighbors[0,j,k] >= 0 and neighbors[1,j,k] >= 0 and neighbors[0,j,k] < grid_size and neighbors[1,j,k]<grid_size:
						# print neighbors[0,j,k], neighbors[1,j,k]
						print "neigh", int(neighbors[0,j,k]), int(neighbors[1,j,k]), ":",
						v = grid[int(neighbors[0,j,k])][int(neighbors[1,j,k])].get_value(dist[j,k]) 						
						print("value %.2f" % v)
						if v > max_v:
							max_v = v
							max_ind = (j,k)								
			# direct = NP.subtract(neighbors, NP.tile(q, (1,S_NEIGH,S_NEIGH)))	
			print("p: %.2f %.2f n: %.2f %.2f max v: %.2f" % (q[0,0,0],  q[1,0,0], neighbors[0,max_ind[0],max_ind[1]], neighbors[1,max_ind[0],max_ind[1]], max_v)  )			
			print "----------"
			data[i,0] += (neighbors[0,max_ind[0],max_ind[1]]- q[0,0,0]) * step_rate
			data[i,1] += (neighbors[1,max_ind[0],max_ind[1]]- q[1,0,0]) * step_rate
			
			q = NP.array([[[data[i,0]]], [[data[i,1]]]])
			dist = NP.subtract(neighbors, NP.tile(q, (1,S_NEIGH,S_NEIGH)))
			dist = NP.sqrt(NP.sum(NP.power(dist,2), 0))
			min_index = dist.argmin()
			grid_x = int(neighbors[0, min_index/S_NEIGH, min_index%S_NEIGH])
			grid_y = int(neighbors[1, min_index/S_NEIGH, min_index%S_NEIGH])
			grid[grid_x][grid_y].assigned +=1
			assigned.add( ( grid_x, grid_y) ) 
			assignment.append( ( grid_x, grid_y, i))
			
		for i in range(grid_size):
			for j in range(grid_size):
				grid[i][j].reset()
		
		print "nr assigned: ", len(assigned), "from", nr_items
		# plot result
		x = list(data[:,0])		
		xi = NP.tile(NP.arange(grid_size), (grid_size, 1))
		y = list(data[:,1])
		yi = NP.tile( NP.array([NP.arange(grid_size)]).T, (1,grid_size))
		plt.plot(NP.ndarray.flatten(xi), NP.ndarray.flatten(yi), 'b.')
		plt.scatter( x, y, c=colors)
		plt.show()
		
	# return result
	print assignment
	print "DONE"
	
	x = list(data[:,0])		
	xi = NP.tile(NP.arange(grid_size), (grid_size, 1))
	y = list(data[:,1])
	yi = NP.tile( NP.array([NP.arange(grid_size)]).T, (1,grid_size))
	plt.plot(NP.ndarray.flatten(xi), NP.ndarray.flatten(yi), 'b.')
	plt.scatter( x, y, c=colors)
	plt.show()
	
	return assignment, grid_size	
		
	
	
if __name__ == "__main__":
	# print surrounding_points(NP.array([2,1]))
	
	random_data = (NP.random.random((60, 2)) * 6) -3
	random_data[0:30,:] = (NP.random.random((30, 2)) * 3) + 0.5 
	random_data[30:60,:] = (NP.random.random((30, 2)) * 6) -3
	ass, grid_size = space_to_grid_iterative(random_data)
	
	
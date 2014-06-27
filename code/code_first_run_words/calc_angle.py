import numpy as np
import math
import random
import matplotlib.pyplot as plt

# def min_angle_lines(point, p1, p2):
	# alpha = angle_lines(point, p1, p2)
	# return min(alpha, 2*math.pi-alpha)
	

# def angle_lines(point,p1, p2):
	# angle_1 = angle(point, p1)
	# angle_2 = angle(point, p2)
	# return abs(angle_1-angle_2)
	
def angle(point, p1):
	a = math.atan2(p1[1]-point[1], p1[0]-point[0])
	if a < 0:
		return 2*math.pi + a
	return a

	
def calc(point, others, axis=None):
	a1 = angle(point, others[0,:])
	a2 = angle(point, others[1,:])
	if a1 > a2:
		min_max = [a2,a1]
		mm_id = [1,0]
	else:
		min_max = [a1,a2]
		mm_id = [0,1]
	# print(others)
		
	# plt.plot(point[0], point[1], '.g')
	# plt.plot(others[0:2,0], others[0:2,1], '.r')
	# plt.plot(others[2:others.shape[0],0], others[2:others.shape[0],1], '.b')
	# plt.xlim(axis[0])
	# plt.ylim(axis[1])
	# plt.show()
	
	# plt.plot([point[0], math.cos(min_max[0])*0.3+point[0]], [point[1], math.sin(min_max[0])*0.3+point[1]], 'b-')
	# plt.plot([point[0], math.cos(min_max[1])*0.3+point[0]], [point[1], math.sin(min_max[1])*0.3+point[1]], 'r-')
		
	plt.plot([point[0], math.cos(min_max[1])], [point[1], math.sin(min_max[1])], 'r-')
	# plt.xlim(axis[0])
	# plt.ylim(axis[1])
	# plt.show()
			
	lt_min = abs(min_max[0] - min_max[1])<math.pi
	for i in range(2,others.shape[0]):
		# print("point", i)
		# print("have to be larger than minimum to be in the area", lt_min)
		replace_min, alpha = replace(point, min_max, others[i,:], lt_min)
		if replace_min!=None:
			if replace_min:
				# print("min change: old", min_max[0], "new",alpha)
				min_max[0] = alpha
				mm_id[0] = i
			else:
				# print("max change: old", min_max[1], "new",alpha )
				min_max[1] = alpha
				mm_id[1] = i
			if min_max[1] < min_max[0]:
				# print("reverse")
				lt_min = not lt_min
				min_max.append(min_max[0])
				del min_max[0]
				mm_id.append(mm_id[0])
				del mm_id[0]
		# else:
			# print("no change")
			
		# fig = plt.figure()
		# print("min angle",min_max[0],"max angle", min_max[1])
		# for j in range(i+1):
			# plt.plot(others[j,0], others[j,1], 'g.')
		# plt.plot([point[0], math.cos(min_max[0])*0.3+point[0]], [point[1], math.sin(min_max[0])*0.3+point[1]], 'b-')
		# plt.plot([point[0], math.cos(min_max[1])*0.3+point[0]], [point[1], math.sin(min_max[1])*0.3+point[1]], 'r-')
		# plt.xlim(axis[0])
		# plt.ylim(axis[1])
		# plt.show()
	return min_max, lt_min

def replace(c, min_max, p, lt_min):
	min_a = min_max[0]
	max_a = min_max[1]
	alpha = angle(c,p)
	if lt_min:
		if min_a<alpha and max_a>alpha:
			return None, None		
	else:
		if min_a>alpha or max_a<alpha:
			return None, None
	# return replace minimal angle (if false replace maximum angle, if none replace nothing)
	# return min_angle_lines(c, min_a, p) < min_angle_lines(c, max_a, p), alpha	
	min_dif, max_dif = abs(min_a-alpha), abs(max_a-alpha)
	return min(min_dif, 2*math.pi-min_dif) < min(max_dif, 2*math.pi-max_dif), alpha	
	
if __name__ == "__main__":
	blaat = np.random.random((10,2))
	axis = [[np.min(blaat[:,0])*0.8,np.max(blaat[:,0])*1.2],[np.min(blaat[:,1])*0.8,np.max(blaat[:,1])*1.2]]
	point = blaat[0,:]
	others = blaat[1:-1,:]
	mm, b = calc(point, others, axis)
	print("END")
	
	
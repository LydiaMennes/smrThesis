import numpy as np
import scipy.linalg as sl
import datetime

class PCA_ext:

	f = ""
	processed = 0
	d = -1

	def __init__(self, filename, filename_out, retrieval_type="words"):
		self.filename = filename
		self.d_type = retrieval_type		
		self.file_out = filename_out
	
	
	def pca_large(self, n, k):
		i = 2
		l = k+2
		q = (i+1)*l
		d = self.d
		self.n = n
		print( "n=",n, "d=", d, "k=",k, "l=", l, "q=",q, "i=", i, "\n")
		
		#step 1
		print( "step 1")
		# initialize
		
		G = np.random.normal(size=(d, l))
		
		H = np.zeros((n, q))
		# create H(0)
		print( "create H(0)")
		self.new_round_data()		
		while self.processed != n:
			(s, p) = self.get_portion_A()
			H[ self.processed:self.processed+s, :l ] = np.dot(p, G)
			del p			
			self.processed += s
		self.new_round_data()
		del G
		
		# fill in remainder of H
		for iter in range(1,i+1):
			H_t = np.zeros((d, l))
			while self.processed != n:
				(s, p) = self.get_portion_A()
				for row in range(d):
					for column in range(l):
						H_t[ row, column ] += np.dot( p[:,row] , H[self.processed:self.processed+s , column+ l*(iter-1) ])
				del p			
				self.processed += s
			self.new_round_data()
			print( "H",iter, "transpose" )
			
			while self.processed != n:
				(s, p) = self.get_portion_A()
				
				H[self.processed:self.processed+s, iter*l:(iter+1)*l ] = np.dot(p, H_t)
				del p			
				self.processed += s
			self.new_round_data()
			print( "H",iter, "final")
		print( "size H", H.shape)
		
		# step 2
		print( "step 2")
		# Q, R, P = sl.qr(H, pivoting=True)
		Q, R, P = sl.qr(H, pivoting=True, mode='economic')
		print( "Q", Q.shape)
		del H
		del R
		
		# step 3
		print( "step 3")
		T = np.zeros((d, q))
		print( "T size", T.shape)
		while self.processed != n:
			(s, p) = self.get_portion_A()
			for row in range(d):
				for column in range(q):
					T[ row, column ] += np.dot( p[:,row] , Q[self.processed:self.processed+s , column])
			del p			
			self.processed += s
		self.new_round_data()
		
		# step 4
		print( "step 4")
		print( "begin SVD", datetime.datetime.now())
		V, S, W = sl.svd(T)
		print( "end SVD", datetime.datetime.now() ,"\nV",V.shape, "S", S.shape, "W", W.shape)
		del T		
		del V
		del S
		
		# step 5
		"step 5"
		U = np.dot(Q,W.T)
		del Q
		del W
		
		# step 6
		print( "step 6")
		# reconstruction = np.dot( np.dot(U[:n, :k], S[:k, :k] ), V[:d, :k].T) 	
		out = open(self.file_out, 'w')
		for i in range(n):
			for j in range(k):
				out.write(str(U[i,j])+" ")
			out.write("\n")
		out.close()
		print( "\nPCA done!!!\n")
		
	def portion_size_A(self):
		#Dit moet afhankelijk van remaining geheugen de grootte terug geven
		return min(200, self.n-self.processed)

	def get_portion_A(self):
		s = self.portion_size_A()
		
		if self.d_type == "words":
			return s, self.get_coocs_portion(s)
		elif self.d_type == "test":
			return s, self.get_test_portion(s)
		print( "unknown retrieval type PCA for large datasets")
	
	def new_round_data(self):		
		if self.f != "":
			self.f.close()		
		self.f = open(self.filename, 'r')
		self.processed = 0

	def get_coocs_portion(self, s):
		p = np.zeros((s, self.d))
		for i in range(s):
			line = self.f.readline().replace("\n", "")
			line = line.split(";")
			index = 0
			for instance in line:
				if index == 0:
					index += 1
				else:
					instance = instance.split(" ")
					p[i, self.avgs[instance[0]][0] ] = float(instance[1]) - self.avgs[instance[0]][1]
		return p
	
	def get_test_portion(self, s):
		p = np.zeros((s, self.d))
		for i in range(s):
			line = self.f.readline().replace(" \n", "")
			# p[i,:] = map(float, line.split(" "))
			p[i,:] = [float(x) for x in line.split(" ")]
			p[i,:] -= self.avgs
		return p
		
	def add_average_test(self, name):
		f = open(name, 'r')
		lst = []
		self.d = 0
		for l in f:
			lst.append(float(l.replace("\n", "")))
			self.d+=1
		self.avgs = np.array(lst)
		
	def add_averages(self, file):
		self.avgs = {}
		f = open(file, "r")
		index = 0
		for l in f:
			l = l.replace("\n", "").split(" ")
			self.avgs[l[0]] = (index, float(l[1]))
			index+=1
		self.d = index
		f.close()
	
if __name__ == "__main__":
	# n = 14
	# d = 5
	# k = 2
	# a = [[1, 1, 1, 0, 0],[3, 3, 3, 0, 0],[4, 4, 4, 0, 0],[5, 5, 5, 0, 0],[0, 2, 0, 4, 4],[0, 0, 0, 5, 5],[0, 1, 0, 2, 2], [1, 1, 1, 0, 0],[3, 3, 3, 0, 0],[4, 4, 4, 0, 0],[5, 5, 5, 0, 0],[0, 2, 0, 4, 4],[0, 0, 0, 5, 5],[0, 1, 0, 2, 2]] 
	# data = np.array(a)
	# print( "original data\n", data.shape, "\n", data-np.mean(data,axis=0), "\n")
	# name = "blaat_tiny.txt"
	# name_sum = "sum_blaat_tiny.txt"
	# f = open(name, 'w')
	# sums = np.zeros(d)
	# print( "n = ", n, "d=", d, "q=", 3*(k+2)	)
	# sums += np.sum(data, axis = 0)
	# for r in range(data.shape[0]):
		# for c in range(data.shape[1]):
			# f.write(str(data[r,c]) + " ")
		# f.write("\n") 
	# f.close()
	
	print( "large test set")
	n = 5000
	d = 60000
	k = 30
	p_gen = 200
	name = "blaat.txt"
	name_sum = "sum_blaat.txt"
	
	# print( "small test set")
	# n = 1000
	# d = 100
	# k = 30
	# p_gen = 200
	# name = "blaat_s.txt"
	# name_sum = "sum_blaat_s.txt"
	
	f = open(name, 'w')
	sums = np.zeros(d)
	print( "create data")
	for i in range(n/p_gen):
		print( i)
		data = np.round(np.random.rand(p_gen, d)*10)
		sums += np.sum(data, axis = 0)
		for r in range(data.shape[0]):
			for c in range(data.shape[1]):
				f.write(str(data[r,c]) + " ")
			f.write("\n") 
		del data
	f.close()
	
	sums = sums / float(n)
	f = open(name_sum, 'w')
	for i in sums:
		f.write(str(i) + "\n")
	f.close()
	del sums
	
	print( "start pca large")
	p = PCA_ext(name, r"D:\Users\Lydia\results semantic landscape\test.txt" ,retrieval_type="test")
	p.add_average_test(name_sum)
	p.pca_large(n,k)

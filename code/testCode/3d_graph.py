from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as PLT
import numpy as NP
import itertools

a = [1,	1,	1,	1,	2,	2,	2	,2	,3	,3	,3	,3	,4	,4	,4	,4]
b = [1	,2	,3	,4	,1	,2	,3	,4	,1	,2	,3	,4	,1	,2	,3	,4]
c = [2	,6	,2	,3	,1	,4	,3	,1	,3	,6	,9	,3	,2	,1	,7	,5]

fig = PLT.figure()
ax1 = fig.add_subplot(111, projection='3d')

n = 10
nr_elems = n*n
xpos = []
ypos = []
for x in itertools.permutations(range(n), 2):
	xpos.append(x[0])
	ypos.append(x[1])
for x in range(n):
	xpos.append(x)
	ypos.append(x)
zpos = NP.zeros(nr_elems)
dx = NP.ones(nr_elems)*0.3
dy = NP.ones(nr_elems)*0.3
dz = NP.random.randint(1, 5, nr_elems)

# xpos = NP.random.randint(1, 10, 10)
# ypos = NP.random.randint(1, 10, 10)
# num_elements = 20
# zpos = NP.zeros(num_elements)
# dx = NP.ones(10)*0.2
# dy = NP.ones(10)*0.2
# dz = NP.random.randint(1, 5, 10)

print len(xpos)
print len(dz)
print len(dx)

ax1.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b')
PLT.show()
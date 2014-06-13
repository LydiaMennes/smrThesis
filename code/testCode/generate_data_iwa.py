import random


f = open("data_iwa.txt", "w")


sal = [0.1,0.65,0.25]
auto_sal = [[0.9,0.1,0.1],[0.15,0.8,0.2],[0.05,0.1,0.7]]
kin=[0.2,0.7,0.1]
gel_sal_kin = [[[0.1,0.2,0.1],[0.5,0.15,0.3],[0.8,0.1,0.1]],[[0.3,0.6,0.6],[0.3,0.15,0.6],[0.1,0.8,0.6]],[[0.6,0.2,0.3],[0.2,0.7,0.1],[0.1,0.1,0.3]]]

for i in range(20):
	
	r = random.random()
	if r < sal[0]:
		sal_v = 0
	elif r < sal[0]+sal[1]:
		sal_v = 1
	else:
		sal_v = 2
		
	r = random.random()
	if r < kin[0]:
		kin_v = 0
	elif r < kin[0]+kin[1]:
		kin_v = 1
	else:
		kin_v = 2
		
	r = random.random()
	if r < auto_sal[sal_v][0]:
		auto_v = 0
	elif r < auto_sal[sal_v][1]:
		auto_v = 1
	else:
		auto_v = 2
		
	r = random.random()	
	if r < gel_sal_kin[sal_v][kin_v][0]:
		gel_v = 0
	elif r < gel_sal_kin[sal_v][kin_v][1]:
		gel_v = 1
	else:
		gel_v = 2
		
	f.write(str(sal_v) + " & " + str(auto_v) + " & " + str(kin_v) + " & " + str(gel_v) + r" \\" +"\n")
		

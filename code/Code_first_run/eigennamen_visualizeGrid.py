import MySQLdb
from collections import defaultdict
import re
import operator
import itertools
import matplotlib.pyplot as plt


def get_data(suffix, grid_size):
	file = open(r"results\semantic_landscape_"+ suffix+ ".txt",'r')
	data = [[],[],[]]
	i = 1
	j = 0
	nr_empty_entries = 0
	for line in file:
		line = line.replace("\n", "")
		line = line.replace("; ", ";")
		instance = line.split(";")		
		for elem in instance:
			if elem != "-EMPTY-" and elem != "":
				data[0].append(j)
				data[1].append(grid_size-i)
				data[2].append(elem)
			else:
				nr_empty_entries+=1
			j+=1
		i+=1
		j=0
	file.close()
	print "nr empty entries:", nr_empty_entries
	
	file = open(r"results\tsne_result_2d_"+ suffix+ ".txt",'r')
	data2d = [[],[],[]]
	for line in file:
		line = line.replace("\n", "")
		instance = line.split(" ")
		data2d[0].append(float(instance[-3]))
		data2d[1].append(float(instance[-2]))
		data2d[2].append(" ".join(instance[0:-3]))
	file.close()
	
	return data, data2d	
	
def visualize_grid(suffix, grid_size):
	db = MySQLdb.connect(host="10.0.0.125", # your host, usually localhost
							 user="Lydia", # your username
							  passwd="voxpop", # your password
							  db="voxpop") # name of the data base       
							  
	cur = db.cursor()

	# cur.execute("SELECT * FROM people JOIN x_monitoredentities_categories ON people.monitoredEntityId = x_monitoredentities_categories.monitoredEntityId where categoryId = 3 or categoryId = 2 or categoryId = 1")

	data, data2d = get_data(suffix, grid_size)
	datascatter=[[[],[]],[[],[]],[[],[]]]
	index=0
	#For each name
	for name in data[2]:
		name = name.split("**")
		cur.execute("SELECT categoryId  FROM people JOIN x_monitoredentities_categories ON people.monitoredEntityId = x_monitoredentities_categories.monitoredEntityId join monitoredentities ON monitoredentities.id = people.id where (categoryId = 3 or categoryId = 2 or categoryId = 1) and surname = '" + name[0] + "' and firstname = '"+ name[1] + "'")
		result = cur.fetchall()[0][0]
		#Sla category erbij op
		if result == 1 or result ==2 or result == 3:
			datascatter[result-1][0].append(data[0][index])			
			datascatter[result-1][1].append(data[1][index])			
		else:
			print "unexpected category"
		index+=1
		
	# visualiseer
	fig = plt.figure(1)
	ax = fig.add_subplot(111)
	ax.scatter(datascatter[0][0], datascatter[0][1], c='r', marker='o', label='Politicians')
	ax.scatter(datascatter[1][0], datascatter[1][1], c='b', marker='D', label='Soccer players')
	ax.scatter(datascatter[2][0], datascatter[2][1], c='g', marker='s', label='Celebrities')
	handles, labels = ax.get_legend_handles_labels()
	lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,-0.1))
	image_name = r"results\eigennamen_grid_" + suffix + ".png"
	fig.savefig(image_name, bbox_extra_artists=(lgd,), bbox_inches='tight')
	
	
	
	# plt.scatter( datascatter[0][0], datascatter[0][1], c='r', marker='o')
	# plt.scatter( datascatter[1][0], datascatter[1][1], c='b', marker='D')
	# plt.scatter( datascatter[2][0], datascatter[2][1], c='g', marker='s')
	# plt.legend(("Politicians","Celebrities","Soccer players"))
	# image_name = r"results\eigennamen_grid_" + suffix + ".png"
	# plt.savefig(image_name, bbox_inches='tight')
	# plt.show()
	
	datascatter=[[[],[]],[[],[]],[[],[]]]
	index=0
	#For each name
	for name in data2d[2]:
		name = name.split("**")
		cur.execute("SELECT categoryId  FROM people JOIN x_monitoredentities_categories ON people.monitoredEntityId = x_monitoredentities_categories.monitoredEntityId join monitoredentities ON monitoredentities.id = people.id where (categoryId = 3 or categoryId = 2 or categoryId = 1) and surname = '" + name[0] + "' and firstname = '"+ name[1] + "'")
		result = cur.fetchall()[0][0]
		#Sla category erbij op
		if result== 1 or result ==2 or result == 3:
			datascatter[result-1][0].append(data2d[0][index])			
			datascatter[result-1][1].append(data2d[1][index])			
		else:
			print "unexpected category"
		index+=1
		
	# visualiseer
	fig = plt.figure(2)
	ax = fig.add_subplot(111)
	ax.scatter(datascatter[0][0], datascatter[0][1], c='r', marker='o', label='Politicians')
	ax.scatter(datascatter[1][0], datascatter[1][1], c='b', marker='D', label='Soccer players')
	ax.scatter(datascatter[2][0], datascatter[2][1], c='g', marker='s', label='Celebrities')
	handles, labels = ax.get_legend_handles_labels()
	lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,-0.1))
	image_name = r"results\eigennamen_space_" + suffix + ".png"
	fig.savefig(image_name, bbox_extra_artists=(lgd,), bbox_inches='tight')
		
	# plt.scatter( datascatter[0][0], datascatter[0][1], c='r', marker='o')
	# plt.scatter( datascatter[1][0], datascatter[1][1], c='b', marker='D')
	# plt.scatter( datascatter[2][0], datascatter[2][1], c='g', marker='s')
	# plt.legend(("Politicians","Soccer players","Celebrities"), loc="upper center")
	# image_name = r"results\eigennamen_space_" + suffix + ".png"
	# plt.savefig(image_name, bbox_inches='tight')
	# plt.show()	

if __name__ == "__main__":

	visualize_grid()
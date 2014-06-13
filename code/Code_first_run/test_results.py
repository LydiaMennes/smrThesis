import MySQLdb
	
def test_names_frequency_file(word_file):	
	names = []
	words = open(word_file, 'r')
	line_nr = 1
	for line in words:
		line_nr+=1
		instance = line.split(",")
		names.append(instance[0].split("**"))
	
	db = MySQLdb.connect(host="10.0.0.125", # your host, usually localhost
							user="Lydia", # your username
							passwd="voxpop", # your password
							db="voxpop") # name of the data base       
							  
	cur = db.cursor()
	
	countPol = 0
	countCel = 0
	countSpo = 0
	for name in names:
		cur.execute("SELECT categoryId  FROM people JOIN x_monitoredentities_categories ON people.monitoredEntityId = x_monitoredentities_categories.monitoredEntityId join monitoredentities ON monitoredentities.id = people.id where (categoryId = 3 or categoryId = 2 or categoryId = 1) and surname = '" + name[0] + "' and firstname = '"+ name[1] + "'")
		result = cur.fetchall()[0][0]
		name.append(result)
		#Sla category erbij op
		if result == 1:
			countPol +=1		
		elif result == 2:
			countSpo+=1
		elif result == 3:
			countCel +=1
	
		print name, result
		
	print "nr politicians:", countPol
	print "nr celebrities:", countCel
	print "nr voetballers:", countSpo
	
	
if __name__ == "__main__":
	# word_doc = r"results\person_frequencies_6000docs.txt"
	word_doc = r"results\person_frequencies_all.txt"
	test_names_frequency_file(word_doc)
	
		
	
	
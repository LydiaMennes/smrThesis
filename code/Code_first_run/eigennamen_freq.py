import MySQLdb
from collections import defaultdict
import re
import operator
import itertools


escape_dict={'\a':r'\a',
           '\b':r'\b',
           '\c':r'\c',
           '\f':r'\f',
           '\n':r'\n',
           '\r':r'\r',
           '\t':r'\t',
           '\v':r'\v',
           '\'':r'\'',
           '\"':r'\"',
           '\0':r'\0',
           '\1':r'\1',
           '\2':r'\2',
           '\3':r'\3',
           '\4':r'\4',
           '\5':r'\5',
           '\6':r'\6',
           '\7':r'\7',
           '\8':r'\8',
           '\9':r'\9'}

def raw(text):
    """Returns a raw string representation of text"""
    new_string=''
    for char in text:
        try: new_string+=escape_dict[char]
        except KeyError: new_string+=char
    return new_string

def get_freqs(nr_people, output_per_docs, suffix, docs_max = -1):
	
	db = MySQLdb.connect(host="10.0.0.125", # your host, usually localhost
							 user="Lydia", # your username
							  passwd="voxpop", # your password
							  db="voxpop") # name of the data base       
							  
	cur = db.cursor()

	# cur.execute("SELECT * FROM people JOIN x_monitoredentities_categories ON people.monitoredEntityId = x_monitoredentities_categories.monitoredEntityId where categoryId = 3 or categoryId = 2 or categoryId = 1")

	print "get names"
	countsCel = defaultdict(int)
	countsPol = defaultdict(int)
	countsSpo = defaultdict(int)
	cur.execute("SELECT surname, firstname, strictRegex, categoryId  FROM people JOIN x_monitoredentities_categories ON people.monitoredEntityId = x_monitoredentities_categories.monitoredEntityId join monitoredentities ON monitoredentities.id = people.id where categoryId = 3 or categoryId = 2 or categoryId = 1")

	names = cur.fetchall()
	print "names fetched"	

	queries = []	
	if docs_max == -1:
		queries=["SELECT itemText FROM newsitems WHERE sourceType = 2 or sourceType = 4 or sourceType = 5 "]
	else:
		queries = []
		queries.append("SELECT itemText FROM newsitems WHERE sourceType = 2 LIMIT " + str(docs_max))
		queries.append("SELECT itemText FROM newsitems WHERE sourceType = 4 LIMIT " + str(docs_max))
		queries.append("SELECT itemText FROM newsitems WHERE sourceType = 5 LIMIT " + str(docs_max))

	nr_docs = 0
	co_ocs = defaultdict(lambda: defaultdict(int))

	for query in queries:
		print "get docs"
		cur.execute(query)
		print "docs fetched"
		for row in cur.fetchall():
			nr_docs+=1
			if nr_docs%output_per_docs == 0:
				print nr_docs, "docs processed"
			txt = row[0]
			mentioned_persons = []
			for person in names:		
				expr = re.compile(raw(person[2]))
				result = re.search(expr, txt)
				if result != None:
					personName = person[0]+"**" +person[1]
					if person[3] == 1:
						countsPol[personName]+=1
					elif person[3] == 2:
						countsSpo[personName]+=1
					elif person[3] == 3:
						countsCel[personName]+=1
						
					mentioned_persons.append(personName)
			for c in itertools.combinations(mentioned_persons, 2):
				if c[0] > c[1]:
					co_ocs[c[1]][c[0]] += 1
				else:
					co_ocs[c[0]][c[1]] += 1
				
				
	print "All docs processed, to file"
	if nr_people > len(countsPol):
		nr_people = len(countsPol)
		print "nr of people encountered in politicians: ", len(countsPol)
	if nr_people > len(countsSpo):
		nr_people = len(countsSpo)
		print "nr of people encountered in sports people: ", len(countsSpo)
	if nr_people > len(countsCel):
		nr_people = len(countsCel)
		print "nr of people encountered in celebrities: ", len(countsCel)
					
	freq_file = open(r"results\person_frequencies_all_"+suffix+".txt", 'w')
	freq_names = []
	for (name, count) in countsPol.iteritems():
		freq_file.write(name + ',' + str(count) + '\n')
	for (name, count) in countsSpo.iteritems():
		freq_file.write(name + ',' + str(count) + '\n')
	for (name, count) in countsCel.iteritems():
		freq_file.write(name + ',' + str(count) + '\n')
	freq_file.close()
		
	cooc_file = open(r"results\person_coocs_all_"+suffix+".txt", 'w')
	for name1 in co_ocs.iterkeys():
		d = co_ocs[name1]
		for name2 in d.iterkeys():
			count = d[name2]			
			cooc_file.write(name1 + ',' + name2 + ',' + str(count) + '\n')
			if count == 0:
				print "something weird...."
	cooc_file.close()
	
	sorted_Pol = sorted(countsPol.iteritems(), key=operator.itemgetter(1))[-nr_people:]
	sorted_Spo = sorted(countsSpo.iteritems(), key=operator.itemgetter(1))[-nr_people:]
	sorted_Cel = sorted(countsCel.iteritems(), key=operator.itemgetter(1))[-nr_people:]
	
	all = []
	all.extend(sorted_Pol)
	all.extend(sorted_Spo)
	all.extend(sorted_Cel)

	freq_file = open(r"results\person_frequencies_"+suffix+".txt", 'w')
	freq_names = []
	for (name, count) in all:
		freq_file.write(name + ',' + str(count) + '\n')
		freq_names.append(name)
	freq_file.close()
		
	cooc_file = open(r"results\person_coocs_"+suffix+".txt", 'w')
	for name1 in co_ocs.iterkeys():
		d = co_ocs[name1]
		for name2 in d.iterkeys():
			count = d[name2]
			if name1 in freq_names and name2 in freq_names:
				cooc_file.write(name1 + ',' + name2 + ',' + str(count) + '\n')
			if count == 0:
				print "something weird...."
	cooc_file.close()	

	print "nr documents:", nr_docs
	print "nr people:", nr_people
	
if __name__ == "__main__":
	# print "FIRST RUN"
	# get_freqs(50, 50, "test", docs_max = 100)
	print "SECOND RUN"
	get_freqs(50, 1000, "all", docs_max = -1)
	






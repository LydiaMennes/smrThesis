import os
from collections import defaultdict
import MySQLdb
import datetime
import re

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


def sem_to_file(sem_words, data_path, date):
	f = open(data_path + r"\file"+str(date)+".txt", 'w')
	encountered_names = 0
	for k, v in sem_words.iteritems():
		if v[2]!=0:
			encountered_names+=1
			f.write(k +";"+str(v[0])+";"+str(v[1])+";"+str(v[2])+"\n")
	f.close()
	return encountered_names
	
def reset_sem(sem_words):
	for k in sem_words.iterkeys():
		sem_words[k][2] = 0
	
def update_semantic_landscape(text, sem_words):
	for k, v in sem_words.iteritems():
		expr = re.compile(v[3])
		found = len(re.findall(expr, text))
		sem_words[k][2] += found
		
	
def	generate_time_series(data_path, sem_words, cur):
	# generate files containing semantic landscapes
	query = "SELECT itemText, pubDate FROM newsitems WHERE year(pubDate)>2012 and (sourceType = 2 or sourceType = 4 or sourceType = 5)  ORDER BY pubDate asc"
	cur.execute(query)
	current_date = datetime.date(100,1,1)
	first = True
	doc_nr = 0
	nr_people_enc = []
	for (txt, pub_date) in iter(cur.fetchall()):
		doc_nr+=1
		# print date, type(date)
		if first:
			current_date = pub_date.date()
			first = False
		if pub_date.date() != current_date:
			nr_people_enc.append((current_date,sem_to_file(sem_words, data_path, current_date)))
			# new landscape
			reset_sem(sem_words)
			current_date = pub_date.date()
			
		# update semantic landscape
		update_semantic_landscape(txt, sem_words)
		if doc_nr%5000 == 0:
			print doc_nr, "docs processed"

	#last landscape to file
	f = open(data_path+r"\stats.txt", 'w')
	for i in nr_people_enc:
		f.write(str(i[0]) + ";" +str(i[1])+"\n")
	f.close()
	
# read semantic landscape from file
def get_semantic_landscape(file_name, cur):
	
	empty_string = "-EMPTY-"
	f = open(file_name, 'r')
	i = 0
	j = 0
	sem = defaultdict(lambda: [-1,-1,0])
	for line in f:
		line = line.replace("\n", "")
		instances = line.split("; ")
		for inst in instances:
			if inst != empty_string and inst != "":
				sem[inst][0] = j
				sem[inst][1] = i
			i+=1
		j+=1
		i = 0
		
	for name in sem.iterkeys():
		q_name = name.split("**")
		# q_name = "'" + q_name[1] + " " + q_name[0] + "'"
		# print "-"+ q_name+ "-"
		# q = "SELECT strictRegex FROM monitoredentities WHERE name = " + q_name
		q = "SELECT strictRegex FROM people join monitoredentities ON monitoredentities.id = people.id WHERE surname='" + q_name[0] + "' and firstname='" + q_name[1] + "'"
		cur.execute(q)
		regex = raw(cur.fetchall()[0][0])
		# print "regex",regex 
		sem[name].append(regex)
	
	# for key, value in sem.iteritems():
		# print key, value
	
	return sem	
	


	
if __name__ == "__main__":		
	data_directory = r"\timeseries_1day_alldocs_withStats"
	data_path = "temporal_data" + data_directory	
	file_sl = r"results\semantic_landscape_eigennamen_all.txt"

	try:
		os.makedirs(data_path)	
	except WindowsError:
		print "folder already exists"
		
	db = MySQLdb.connect(host="10.0.0.125", # your host, usually localhost
						 user="Lydia", # your username
						  passwd="voxpop", # your password
						  db="voxpop") # name of the data base       
							  
	cur = db.cursor()
		
	semantic_landscape = get_semantic_landscape(file_sl, cur)
	generate_time_series(data_path, semantic_landscape, cur)
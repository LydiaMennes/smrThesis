from __future__ import division
import MySQLdb
import datetime
import string

	
def get_frequencies():

	db = MySQLdb.connect(host="10.0.0.125", # your host, usually localhost
						 user="Lydia", # your username
						  passwd="voxpop", # your password
						  db="voxpop") # name of the data base       
						  
	# you must create a Cursor object. It will let
	#  you execute all the queries you need
	cur = db.cursor()

	# Columns: 5 = itemText
	# Use all the SQL you like
	# Sourcetypes: 1 = algemeen, 2 = politiek, 3 = business

	print "Get items from database"	
	query = "SELECT itemText, pubDate FROM newsitems WHERE sourceType = 2 LIMIT 100"
	cur.execute(query)
	print "selection made"
		
	# init dictionary
	
	for row in enumerate(cur.fetchall()):
		s = row[1][0]
		s = s.replace("\n", "")
		s = s.translate(None, string.punctuation)
		text = s.split(" ")
		
		print text[1:10]
		print row[1][1].date(), type(row[1][1])
		print row[0]
		
	return None

	
if __name__ == "__main__":
	get_frequencies()
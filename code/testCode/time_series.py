import MySQLdb
from collections import defaultdict

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
#cur.execute("SELECT pubDate FROM newsitems WHERE sourceType = 2 LIMIT 50")
cur.execute("SELECT pubDate FROM newsitems WHERE sourceType = 2")
print "selection made"

article_frequency = defaultdict(int)

for count, row in enumerate(cur.fetchall()):
	pub_date = row[0]
	article_frequency[(pub_date.year, pub_date.month, pub_date.day)] +=1
		
dates = article_frequency.keys()
dates.sort()

sum = 0
nr_zeros = 0
nr_little = 0
prev = None
sequential = True

article_freq = open("article_frequencies.txt", 'w')

for d in dates:
	#print d[0], "-", d[1], "-", d[2], "freq", article_frequency[d]
	if prev != None:
		if not (d[0]==prev[0] and d[1]==prev[1] and d[2]== prev[2]+1):
			if not (d[0]==prev[0] and d[1]==prev[1]+1 and d[2]== 1):
				if not (d[0]==prev[0]+1 and d[1]==1 and d[2]== 1):
					sequential = False
					
	sum += article_frequency[d]
	article_freq.write(str(article_frequency[d]) + " ")
	if article_frequency[d] < 10:
		nr_little += 1
		if article_frequency[d] == 0:
			nr_zeros +=1

article_freq.close()			
print "from", dates[0][0], "-", dates[0][1], "-", dates[0][2], "to", dates[-1][0], "-", dates[-1][1], "-", dates[-1][2]
print "nr of days available", len(dates)
print "nr of days without articles", nr_zeros
print "nr of days with very little articles", nr_little
print "Average nr of articles", sum / float(len(dates))
print "The data is sequential", sequential

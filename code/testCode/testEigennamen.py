import MySQLdb

db = MySQLdb.connect(host="10.0.0.125", # your host, usually localhost
						 user="Lydia", # your username
						  passwd="voxpop", # your password
						  db="voxpop") # name of the data base       
						  
# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

cur.execute("SELECT * FROM people JOIN x_monitoredentities_categories ON people.monitoredEntityId = x_monitoredentities_categories.monitoredEntityId where categoryId = 3")
celebs = cur.fetchall()
cur.execute("SELECT * FROM people JOIN x_monitoredentities_categories ON people.monitoredEntityId = x_monitoredentities_categories.monitoredEntityId where categoryId = 2")
footbal = cur.fetchall()
cur.execute("SELECT * FROM people JOIN x_monitoredentities_categories ON people.monitoredEntityId = x_monitoredentities_categories.monitoredEntityId where categoryId = 1")
politicians = cur.fetchall()

print "nr celebs: ", len(celebs)
print "nr football players: ", len(footbal)
print "nr politicians: ", len(politicians)

print "total:", len(celebs) + len(footbal) + len(politicians)


print "get docs"
cur.execute("SELECT itemText FROM newsitems WHERE sourceType = 2 or sourceType = 4 or sourceType = 5 ")
# cur.execute("SELECT itemText FROM newsitems WHERE sourceType = 2 LIMIT 5000")
print "docs fetched"

print "nr_docs: ", len(cur.fetchall())
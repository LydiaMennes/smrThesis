#!/usr/bin/python
import MySQLdb
import nltk
import string
from nltk.corpus import stopwords
from collections import defaultdict

print "start"
db = MySQLdb.connect(host="10.0.0.125", # your host, usually localhost
                     user="Lydia", # your username
                      passwd="voxpop", # your password
                      db="voxpop") # name of the data base

print "connected to database"          
                      
# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

print "cursor"


stopwords = stopwords.words('english')

# Columns: 5 = itemText
# Use all the SQL you like
# Sourcetypes: 1 = algemeen, 2 = politiek, 3 = business

#cur.execute("SELECT category, itemText FROM newsitems LIMIT 1000")
cur.execute("SELECT * FROM newsitems WHERE sourceType = 2 LIMIT 100")

print "selection made"

# print all the first cell of all the rows
tokenizer = nltk.tokenize.api.StringTokenizer

for count, row in enumerate(cur.fetchall()) :
    if len(row) == 1:
        text = row[0]
        words = [i for i in nltk.word_tokenize(text) if i not in string.punctuation]
        
    else:
        print "lengte is niet goed"
        print len(row)
    	
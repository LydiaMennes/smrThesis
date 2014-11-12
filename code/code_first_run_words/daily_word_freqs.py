import argparse
import datetime
import oursql
import os
from collections import defaultdict
import unicodedata
from thesis_utilities import *
import gc

output_path = r"D:\Users\Lydia\results_freqs\freqs_per_day"
database = ""

def check_date_nr_docs(article_type, lim=None):
    conn = get_connection_old()
    curs = conn.cursor(oursql.DictCursor)
    
    mindate = datetime.datetime(2014,12,1)
    maxdate = datetime.datetime(2007,1,1)
    
    curquery = "SELECT pubDate FROM newsitems where sourceType = "+ str(article_type)
    if lim != None:
        curquery+= " LIMIT " + str(lim)
    curs.execute(curquery)
    nr_docs = 0
        
    for row in curs:
        nr_docs +=1
        x = row['pubDate']
        if x !=None:
            if x < mindate:
                mindate=x
            if x > maxdate:
                maxdate = x
                
    print("nr docs", nr_docs)
    print("mindate", mindate)
    print("maxdate", maxdate)
    

# connection data as received in beginnig
def get_connection_old():
    conn = oursql.connect(host="10.0.0.125", # your host, usually localhost
                         user="Lydia", # your username
                          passwd="voxpop", # your password
                          db="voxpop",
                          use_unicode=False)
    return conn
    
# connection merged items !!!! tabel is mergednewsitems instead of newsitems!!!!
def get_connection_afterjan2011():
    conn = oursql.connect(host="10.0.0.124", # your host, usually localhost
                         user="lydia", # your username
                          passwd="voxpop", # your password
                          db="vp_exps",
                          use_unicode=False)
    return conn

# connection items before jan 5 2011
def get_connection_beforerjan2011():
    conn = oursql.connect(host="10.0.0.124", # your host, usually localhost
                         user="lydia", # your username
                          passwd="voxpop", # your password
                          db="voxpop",
                          use_unicode=False)
    return conn
    
def append_info_to_file(info, date, output_path):
    f = open(output_path+r"\info.txt","a")
    f.write(str(date) + ";" + str(info[0])+ ";" + str(info[1]) + "\n")
    f.close()

def word_freqs_to_file(curdate, output_path, words):
    f = open(output_path+r"\words"+str(curdate)+".txt", "w")
    keys = list(words.keys())
    keys.sort()
    for k in keys:
        f.write(str(k) + ";" + str(words[k]) + "\n")
    f.close()

def run_freqs(article_type, output_path, curdate, maxdate):
    oneday = datetime.timedelta(1)
    
    # change tabelname is newsitems voor tot 5 jan of oude versie en voor merged is het mergednewsitems
    query = "SELECT itemText FROM mergednewsitems where sourceType = "+article_type+" and date(pubDate) = \"PD\" ;"
    if database == "old":
        query = "SELECT itemText FROM newsitems where sourceType = "+article_type+" and date(pubDate) = \"PD\" ;"
    stop_words = get_parabots_stopwords()
    silly_words = get_silly_words()
    punc_map = str.maketrans("","",string.punctuation)
    
    if database == "new":
        conn = get_connection_afterjan2011()
    if database == "old":
        conn = get_connection_beforerjan2011()
    curs = conn.cursor(oursql.DictCursor)
    first = True
    
    while curdate <= maxdate:
    
        words = defaultdict(int)
        nr_docs = 0
        exceptions = 0
        curquery = query.replace("PD", str(curdate))
        if curdate.day%10 == 0 or first:
            print("requesting", str(curdate), "time", datetime.datetime.now(), article_type)
            first = False
        curs.execute(curquery)
        if curdate.day%10 == 0 or first:
            print("processing\t\t", datetime.datetime.now())
            first = False
        
        for row in curs:
            nr_docs +=1
            s = row['itemText']
            try: 
                s = unicodedata.normalize('NFKD', s.decode('unicode-escape')).encode('ascii', 'ignore')
                s = str(s)
                s = esc_chars(s)
                s = s.translate(punc_map)
                text = s.split(" ")                
                for word in text:    
                    word = word.lower()
                    if len(word)!=1 and word != "" and word not in stop_words and not has_digits(word) and word not in silly_words:
                        words[word]+=1
            except UnicodeDecodeError:
                exceptions+=1
        append_info_to_file((nr_docs, exceptions), curdate, output_path)
        if nr_docs > 0:
            word_freqs_to_file(curdate, output_path, words)
        curdate += oneday
        gc.collect()

if __name__ == "__main__":

    # print("lim = 1 mil")
    # check_date_nr_docs(2, 1000000)
    # print("no lim")    
    # check_date_nr_docs(2)

    parser = argparse.ArgumentParser(description='Run puzzle algorithm')
    # '''parser.add_argument(<naam>, type=<type>, default=<default>, help=<help message>)'''
    parser.add_argument("article_type", help="Types: politics or football")
    parser.add_argument("output_folder", help="Types: politics or football")
    parser.add_argument("min_day", type=int)
    parser.add_argument("min_month", type=int)
    parser.add_argument("min_year", type=int)
    parser.add_argument("max_day", type=int)
    parser.add_argument("max_month", type=int)
    parser.add_argument("max_year", type=int)
    parser.add_argument("--database", default="new", help="options are old or new")
    
    args = parser.parse_args()
    kwargs = vars(args)    
    
    mindate = datetime.date(kwargs["min_year"], kwargs["min_month"], kwargs["min_day"])
    maxdate = datetime.date(kwargs["max_year"], kwargs["max_month"], kwargs["max_day"])
    
    output_path = output_path+"\\"+kwargs["output_folder"]
    if not os.path.exists(output_path):
        os.makedirs(output_path)    
    print( "directory made"    )  
    f = open(output_path+r"\info.txt","w")   
    f.write("date;nr docs;word exceptions\n")    
    f.close()
    
    if kwargs["article_type"]=="politics": 
        article_type = "2"
    elif kwargs["article_type"]=="football":
        article_type = "5"
    else:
        print("Unrecognized article type")
        sys.exit()
       
    
    if kwargs["database"]== "old": 
        database = "old"
        run_freqs(article_type, output_path, mindate, maxdate)
    elif kwargs["database"]== "new": 
        database = "new"
        run_freqs(article_type, output_path, mindate, maxdate)        
    else:
        print("invalid database type")
        sys.exit()
        
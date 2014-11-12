import oursql
from collections import defaultdict
import re
import datetime
import os
import unicodedata
import sys


politieke_partijen = ["vvd", "pvda", "sp", "cda", "d66", "pvv", "christenunie", "groenlinks", "sgp", "pvdd", "50plus"]
voetbal_clubs = ["psv", "ajax", "feyenoord", "twente", "zwolle", "groningen", "heerenveen", "willem", "utrecht", "vitesse", "az", "ado", "nac", "heracles"]

def get_connection():
    conn = oursql.connect(  host="10.0.0.125", 
                            user="Lydia", 
                            passwd="voxpop",
                            db="voxpop",
                            use_unicode = False)
    return conn

def translate_string(s):
    s = s.decode('unicode-escape')
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore')
    s = s.decode('ascii')        
    s = s.lower()
    return s

def get_tha_peepz(sourceType):
    query_peepz ="select name, looseRegex, strictRegex, people.surname from monitoredentities join people on monitoredentities.id=people.id join x_monitoredentities_categories on people.monitoredEntityId=x_monitoredentities_categories.monitoredEntityId join x_categories_sourcetypes on x_categories_sourcetypes.categoryId=x_monitoredentities_categories.categoryId where SourceTypeId ="+str(sourceType)+";"

    conn = get_connection()   
                          
    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    curs = conn.cursor(oursql.DictCursor)
    
    # Sourcetypes: 1 = algemeen, 2 = politiek, 3 = business, 4 = celebs, 5 = Sport, Tech = 6, 7 = Cultuur

    print( "Get items from database")
    curs.execute(query_peepz)
    print("selection made")
        
    nr_peepz = 0
    names = {}
    remove_names = [b"Ernst Cramer",b"Jan Jacob van Dijk",b"Jules Kortenhorst",b"Rikus Jager"]
        
    for row in curs: 
        name = translate_string(row["name"])
        name = name.replace(" ", "_")
        if sourceType == 5:
            names[name]=[re.compile(row["strictRegex"]), 0]
            nr_peepz+=1
        elif sourceType == 2:
            if not row["name"] in remove_names:
                names[name]=[re.compile(b"\\b"+row["surname"]+b"\\b"), 0]
                nr_peepz+=1
            # sys.exit()
    print("nr peepz", nr_peepz)
        
    return names
    
def coocs_to_file(names, cooc, cooc_path):    
    print("coocs to file", datetime.datetime.now())
    current_letter = "a"
    cooc_path+=r"\complete_cooc"
    if not os.path.exists(cooc_path):
        os.makedirs(cooc_path)
    filename_out = cooc_path + r"\_"+current_letter+".txt" 
    f = open(filename_out, 'w')
    for w in names:     
        begin_letter = w[0]
        if  begin_letter> current_letter and begin_letter <= "z":            
            f.close()
            current_letter = begin_letter
            print( "letter", current_letter)
            filename_out = cooc_path + r"\_"+current_letter+".txt" 
            f = open(filename_out, 'w')
        
        sum=0
            
        f.write(w + ";")        
        for w2 in names:
            if cooc[w][w2] == 0:                    
                del cooc[w][w2]                    
            else:
                sum += cooc[w][w2]
        for w2 in names:            
            if cooc[w2][w] == 0:
                del cooc[w2][w]                
            else:
                normfreq = cooc[w2][w]/sum
                f.write(w2 + " " + str(normfreq)+";")
        f.write("\n")
    f.close()
    
def freqs_to_file(names, namelist, cooc_path):
    f = open(cooc_path+"\\names_freqs.txt","w")
    for n in names:
        f.write(str(n[1])+";"+str(n[0])+"\n")
    f.close()    
    
    f = open(cooc_path+"\\wordlist.txt","w")
    for n in namelist:
        f.write(str(n)+"\n")
    f.close()    
    
    f = open(cooc_path+"\\stats.txt","w")
    f.write("number of included words: "+str(len(namelist))+"\n")
    f.close()
    
def get_tha_freqs(names, sourceType, cooc_path, nr_names, limit=None):
    
    if sourceType ==5:        
        name_list_clubs = voetbal_clubs
    if sourceType ==2:        
        name_list_clubs = politieke_partijen
    bytez_list_clubs=[]
    for n in name_list_clubs:
        regex_str = ""
        for c in n:
            regex_str+="("+c.lower()+"|"+c.upper()+")"
        regex_str = ("\\b"+regex_str+"\\b").encode("utf-8")
        bytez_list_clubs.append(re.compile(regex_str))
    
    conn = get_connection()
    query_docs = "SELECT itemText, pubDate FROM newsitems WHERE sourceType = " + str(sourceType)
    if limit!=None:
        query_docs+= " LIMIT " + str(limit)
    query_docs+=";"
    
    curs = conn.cursor(oursql.DictCursor)
    
    # Sourcetypes: 1 = algemeen, 2 = politiek, 3 = business, 4 = celebs, 5 = Sport, Tech = 6, 7 = Cultuur

    print( "Get items from database")
    curs.execute(query_docs)
    print("selection made")    
        
    dates = []  
    coocs = defaultdict(lambda: defaultdict(int))
    club_name_freq = defaultdict(int)
    
    doc_nr = 0
    for row in curs:
        encounter = []
        doc_nr+=1
        txt = row["itemText"]
        dates.append(row["pubDate"])
        for name, regex_freq in names.items():
            if regex_freq[0].search(txt) != None:
                regex_freq[1]+=1
                encounter.append(name)
        for i in range(len(bytez_list_clubs)):        
            if bytez_list_clubs[i].search(txt) != None:
                name = name_list_clubs[i]
                if name == None:
                    print("none name encountered freqs" )
                    sys.exit()
                club_name_freq[name]+=1
                encounter.append(name)
        if doc_nr%100000==0:
            print("doc", doc_nr, datetime.datetime.now())
        for n1 in encounter:
            for n2 in encounter:
                if n1 != n2:
                    coocs[n1][n2]+=1
    
    dates.sort()
    print(dates[0], dates[-1])
    
    result = []  
    for name,value in names.items():
        result.append([value[1], name])
        if name == None:
            print("none name encountered result append 1" )
            sys.exit()
    result.sort()
    result = result[-nr_names:]
    for name, freq in club_name_freq.items():
        result.append([freq,name])
        if name == None:
            print("none name encountered result append 1" )
            sys.exit()
    
    namelist = []
    for r in result:
        namelist.append(r[1])
    namelist.sort()
    
    
    # print(namelist[1:5], "\n", result[1:5], "\n")
    
    freqs_to_file(result, namelist, cooc_path)
    coocs_to_file(namelist, coocs, cooc_path)
    
if __name__ == "__main__":


    nr_names = 100
    # limit = 1000000    

    sourceType = 2
    case_name = "politics_names_allDocs"
    
    cooc_path = r"D:\Users\Lydia\results word cooc"+"\\"+case_name
    if not os.path.exists(cooc_path):
            os.makedirs(cooc_path)    
            
    # get_tha_freqs(get_tha_peepz(sourceType), sourceType, cooc_path, nr_names, limit)
    get_tha_freqs(get_tha_peepz(sourceType), sourceType, cooc_path, nr_names)
    
    
    # sourceType = 5
    # case_name = "football_names"       
    
    # cooc_path = r"D:\Users\Lydia\results word cooc"+"\\"+case_name+r"\complete_cooc"
    # if not os.path.exists(cooc_path):
            # os.makedirs(cooc_path)    
            
    # get_tha_freqs(get_tha_peepz(sourceType), sourceType, cooc_path, nr_names, limit)
    
    
    
        
    
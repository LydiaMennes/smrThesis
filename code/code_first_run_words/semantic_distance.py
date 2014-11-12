import math
import numpy as np
import sys

def log_addition(a,b, subtraction=False):
    if subtraction:
        x = math.fabs(math.exp(a) - math.exp(b))
    else:
        x = math.exp(a) + math.exp(b)
    if x == 0.0:
        return 0.0
    return math.log( x )
    
def euclid_distance(sem_w1, sem_w2):
    dis = 0    
    i_e1 = 1
    e1 = sem_w1[0]
    for e2 in sem_w2:
        while e1[0] < e2[0] and i_e1 <= len(sem_w1):
            # iterate over sem_w1 until no longer e1 > e2
            dis +=  e1[1]**2 
            if i_e1 < len(sem_w1):
                e1 = sem_w1[i_e1]
            i_e1 += 1
        if e1[0] > e2[0]:
            # next e2
            dis += e2[1]**2
        elif e1[0] == e2[0] and i_e1 <= len(sem_w1):
            dis += (e1[1]-e2[1])**2
            if i_e1 < len(sem_w1):
                e1 = sem_w1[i_e1]
            i_e1 += 1
        elif i_e1 > len(sem_w1) :
            dis += e2[1]**2
        else:
            print("something wrong", e1[0], e2[0])
    while i_e1 <= len(sem_w1):
        dis += e1[1]**2
        if i_e1 < len(sem_w1):
            e1 = sem_w1[i_e1]
        i_e1 += 1
    return dis
    
def euclid_distance_log(sem_w1, sem_w2):
    dis = 0    
    i_e1 = 1
    e1 = sem_w1[0]
    for e2 in sem_w2:
        while e1[0] < e2[0] and i_e1 <= len(sem_w1):
            # iterate over sem_w1 until no longer e1 > e2
            dis = log_addition(dis, e1[1]*2) # + e1^2
            if i_e1 < len(sem_w1):
                e1 = sem_w1[i_e1]
            i_e1 += 1
        if e1[0] > e2[0]:
            # next e2
            dis = log_addition(dis, e2[1]*2) # + e2^2
        elif e1[0] == e2[0] and i_e1 <= len(sem_w1):
            dis = log_addition(dis, log_addition(e1[1],e2[1], subtraction=True)*2 ) # + (e1-e2)^2            
            if i_e1 < len(sem_w1):
                e1 = sem_w1[i_e1]
            i_e1 += 1
        elif i_e1 > len(sem_w1) :
            dis = log_addition(dis, e2[1]*2) # + e2^2
        else:
            print("something wrong", e1[0], e2[0])
    while i_e1 <= len(sem_w1):
        dis = log_addition(dis, e1[1]*2) # + e1^2
        if i_e1 < len(sem_w1):
            e1 = sem_w1[i_e1]
        i_e1 += 1
    if dis == 0.0:
        return 0.0
    return math.exp(dis)-1

def cosine_distance(sem_w1, sem_w2):
    if sem_w1 == None or sem_w2 == None or sem_w1==[] or sem_w2==[]:
        return 1
        
    dot_product = 0
    len_1 = 0
    len_2 = 0
    i_e1 = 1
    e1 = sem_w1[0]
    for e2 in sem_w2:
        while e1[0] < e2[0] and i_e1 <= len(sem_w1):
            # iterate over sem_w1 until no longer e1 > e2
            len_1 += e1[1]**2
            if i_e1 < len(sem_w1):
                e1 = sem_w1[i_e1]
            i_e1 += 1
        if e1[0] > e2[0]:
            # next e2
            len_2 += e2[1]**2
        elif e1[0] == e2[0] and i_e1 <= len(sem_w1):
            dot_product += e1[1]*e2[1]
            len_1 += e1[1]**2
            len_2 += e2[1]**2
            if i_e1 < len(sem_w1):
                e1 = sem_w1[i_e1]
            i_e1 += 1
        elif i_e1 > len(sem_w1) :
            len_2 += e2[1]**2
        else:
            print("something wrong", e1[0], e2[0])
    while i_e1 <= len(sem_w1):
        len_1 += e1[1]**2
        if i_e1 < len(sem_w1):
            e1 = sem_w1[i_e1]
        i_e1 += 1
    len_1 = math.sqrt(len_1)
    len_2 = math.sqrt(len_2)
    
    return 1- (dot_product / (len_1 * len_2))
    
def cosine_distance_log(sem_w1, sem_w2):
    dot_product = 0
    len_1 = 0
    len_2 = 0
    i_e1 = 1
    e1 = sem_w1[0]
    for e2 in sem_w2:
        while e1[0] < e2[0] and i_e1 <= len(sem_w1):
            # iterate over sem_w1 until no longer e1 > e2
            len_1 += math.exp(e1[1])**2
            if i_e1 < len(sem_w1):
                e1 = sem_w1[i_e1]
            i_e1 += 1
        if e1[0] > e2[0]:
            # next e2
            len_2 += math.exp(e2[1])**2
        elif e1[0] == e2[0] and i_e1 <= len(sem_w1):
            dot_product += math.exp(e1[1])*math.exp(e2[1])
            len_1 += math.exp(e1[1])**2
            len_2 += math.exp(e2[1])**2
            if i_e1 < len(sem_w1):
                e1 = sem_w1[i_e1]
            i_e1 += 1
        elif i_e1 > len(sem_w1) :
            len_2 += math.exp(e2[1])**2
        else:
            print("something wrong", e1[0], e2[0])
    while i_e1 <= len(sem_w1):
        len_1 += math.exp(e1[1])**2
        if i_e1 < len(sem_w1):
            e1 = sem_w1[i_e1]
        i_e1 += 1
    return 1- (dot_product / (math.sqrt(len_1) * math.sqrt(len_2)))
    
def cosine_distance_log2(sem_w1, sem_w2):
    print("DO NOT USE, CONTAINS ERROR")
    dot_product = 0
    len_1 = 0
    len_2 = 0
    i_e1 = 1
    e1 = sem_w1[0]
    for e2 in sem_w2:
        while e1[0] < e2[0] and i_e1 <= len(sem_w1):
            # iterate over sem_w1 until no longer e1 > e2
            len_1 = log_addition(len_1, e1[1]*2) # + e1^2
            if i_e1 < len(sem_w1):
                e1 = sem_w1[i_e1]
            i_e1 += 1
        if e1[0] > e2[0]:
            # next e2
            len_2 = log_addition(len_2, e2[1]*2) # + e2^2
        elif e1[0] == e2[0] and i_e1 <= len(sem_w1):
            dot_product = log_addition(dot_product, e1[1]+e2[1]) # + e1*e2
            len_1 = log_addition(len_1, e1[1]*2) # + e1^2
            len_2 = log_addition(len_2, e2[1]*2) # + e2^2
            if i_e1 < len(sem_w1):
                e1 = sem_w1[i_e1]
            i_e1 += 1
        elif i_e1 > len(sem_w1) :
            len_2 = log_addition(len_2, e2[1]*2) # + e2^2
        else:
            print("something wrong", e1[0], e2[0])
    while i_e1 <= len(sem_w1):
        len_1 = log_addition(len_1, e1[1]*2) # + e1^2
        if i_e1 < len(sem_w1):
            e1 = sem_w1[i_e1]
        i_e1 += 1
    result = dot_product - (0.5*len_1) + (0.5*len_2)
    if result == 0.0:
        return 1.0
    return 1- math.exp(result)
    
    
if __name__ == "__main__":
    print("cosine")
    w1 = [["a", -6.45],["b", -6.19],["e", -2.1],["f", -1.8],["i", -2.2]]
    w2 = [["a", -3.55],["c", -6.14],["f", -2.15],["g", -1.8],["j", -2.14]]
    print( cosine_distance_log(w1,w2))
    print( cosine_distance_log2(w1,w2))
    print( "non log")
    print( cosine_distance( [ [w,math.exp(x)] for [w,x] in w1], [ [w,math.exp(x)] for [w,x] in w2]))
    
    print( "\neuclidean")
    print( euclid_distance_log(w1, w2))
    print( "non log")
    print( euclid_distance([ [w,math.exp(x)] for [w,x] in w1], [ [w,math.exp(x)] for [w,x] in w2]))
    
    w1_norm = [-6.45,-6.19, 0.0, -2.1, -1.8, 0.0, -2.2, 0.0]
    w2_norm = [-3.55,0.0, -6.14, 0.0, -2.15, -1.8, 0.0, -2.14]
    
    for i in range(len(w1_norm)):
        if w1_norm[i] != 0.0:
            w1_norm[i] = math.exp(w1_norm[i])
        if w2_norm[i] != 0.0:
            w2_norm[i] = math.exp(w2_norm[i])
        
    
    print( "\n\n normal:\n", w1_norm, "\n", w2_norm, "\n")
    w1_norm = np.array(w1_norm)
    w2_norm = np.array(w2_norm)
    
    print( "cosine = ", 1- ( np.dot(w1_norm, w2_norm) / (np.linalg.norm(w1_norm) * np.linalg.norm(w2_norm))))
    a = w1_norm-w2_norm
    print( "euclid = ", np.dot(a,a), "\n\n")
    
    x = 0.16
    y = 0.12
    print( x-y)
    z = log_addition(math.log(x), math.log(y), subtraction = True)
    print( z, math.exp(z) )
    
    
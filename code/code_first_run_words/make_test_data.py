import datetime
import os

def build2(nr_days):
    folder = r"D:\Users\Lydia\results_freqs\perfect_easy_data\daily_freqs\patches"
    date = datetime.date(2011,1,1)
    delta = datetime.timedelta(1)
    nr_patches = 5
    patch_size = 10
    elem = 0.0
    
    for i in range(nr_days):
        day_folder = folder+r"\day"+str(date)
        if not os.path.exists(day_folder):
                os.makedirs(day_folder) 
        for j in range(nr_patches):
            for k in range(nr_patches):
                f = open(day_folder+r"\patch_"+str(j)+"_"+str(k)+".txt","w")
                for l in range(patch_size):
                    for m in range(patch_size):
                        f.write(str(elem))
                        if m<patch_size-1:
                            f.write(",")
                    f.write("\n")
                f.close()
                
                if i == 0:
                    print("make info file", j, k)
                    f = open(folder+r"\patch_"+str(j)+"_"+str(k)+"_info.txt","w")
                    f.write("nr rows input:  ")
                    f.write(str(patch_size))
                    f.write("\nnr cols input:  ")
                    f.write(str(patch_size))
                    f.write("\nnr rows output: ")
                    f.write(str(patch_size-2))
                    f.write("\nnr cols output: ")
                    f.write(str(patch_size-2))
                    f.close()
        if elem == 0:
            elem = 1.0
        else:
            elem = 0.0
        date+=delta
    

def build():
    words = ["a","b","c","d", "e", "f", "g", "h", "i", "j"]
    date = datetime.date(2011,1,1)
    delta = datetime.timedelta(1)
    x = 1
    
    for i in range(60):
        f = open(r"D:\Users\Lydia\results_freqs\freqs_per_day\bullshizzle_freqs\words"+str(date)+".txt","w")
        for w1 in words:
            for w2 in words:
                f.write(w1+w2+";"+str(x)+"\n")
                x+=1
        f.close()
        date+=delta
        
    f = open(r"D:\Users\Lydia\results puzzle\test_freqs\grid_final.txt","w")
    for w1 in words:
        for w2 in words:
            f.write(w1+w2+" ; ")
        f.write("\n")
    f.close()
        
if __name__ == "__main__":
    # build2(500)
    build()
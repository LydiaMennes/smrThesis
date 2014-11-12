import random
from matplotlib import pyplot as plt
import math
from scipy import cluster as clust
import numpy as np
import os
from thesis_utilities import four_digit_string as fds

x = [1,2,3,4,5,6]

def get_samples(filename, total_nr_samples, nr_samples):
    f = open(filename, "r")
    samples = []
    for line in f:
        if random.random()< (nr_samples+3)/total_nr_samples and len(samples)<nr_samples:
            samples.append(get_sample(line))
            if len(samples)>0 and len(samples) <= 3:
                print( samples[-1])        
    f.close()  
    return samples

# def chi_squared_dist(a,b):
    # for i in range(a)
    
    
def get_sample(line):
    line = line.split(";")
    result = list(map(float, line[0].split(",")))
    result.append(float(line[1]))
    return result
    
def k_means_on_samples_output_range(filename, total_nr_samples, nr_samples, nr_centroids, out_folder, intervals):
    # get samples
    samples = get_samples(filename, total_nr_samples, nr_samples)
    
    # devide in intervals
    samples_per_interval = []
    for i in range(len(intervals)-1):
        samples_per_interval.append([])
    
    for s in samples:
        for i in range(len(intervals)-1):
            if s[-1] >= intervals[i] and s[-1]<=intervals[i+1]:
                samples_per_interval[i].append(s)
                break
    
    #run k_means_on_samples per interval
   
    if not os.path.exists( out_folder+"\\all_all_centroids"):
        os.makedirs( out_folder+"\\all_all_centroids")
        
    for i in range(len(intervals)-1):
        interval_name = "interval_"+str(intervals[i])+"_"+str( intervals[i+1])
        print("len" , interval_name, "=", len(samples_per_interval[i]))
        interval_folder = out_folder+"\\"+interval_name
        k_means_on_samples(samples_per_interval[i], nr_centroids, interval_folder, in_title=interval_name, all_centroids_folder = out_folder+"\\all_all_centroids\\all_centroids_no_scale"+fds(i))
    

def k_means_on_samples_all(filename, total_nr_samples, nr_samples, nr_centroids, out_folder):
     samples = get_samples(filename, total_nr_samples, nr_samples)
     k_means_on_samples(samples, nr_centroids, out_folder)
    
def k_means_on_samples(samples, nr_centroids, out_folder, in_title = "", all_centroids_folder=None):
   
    # print("samples first", len(samples), len(samples[0]))
    samples = np.array(samples)
    # print("samples shape", samples.shape)
    max_value = np.max(samples)
    
    # whiten obs
    scales = []
    for feature in range(samples.shape[1]):
        sd = np.std(samples[:,feature])
        # print(sd)
        scales.append(sd)
        # samples[:,feature]= samples[:,feature]/sd
    
    # scipy.cluster.vq.kmeans
    centroids = clust.vq.kmeans(clust.vq.whiten(samples), nr_centroids, 10) [0]
    
    # un whiten centroids
    for feature in range(samples.shape[1]):    
        for c in range(len(centroids)):
            centroids[c,feature]*=scales[feature]        
        
    assignment = []
    for i in range(samples.shape[0]):
        s = samples[i,:]
        best = -1
        best_dif = float("inf")
        count = 0
        for c in centroids:
            dif = s-c
            dif = np.sum(dif*dif)
            if dif<best_dif:
                best_dif = dif
                best = count
                
            count+=1
        if best == -1:
            print("WRONG")
        assignment.append(best)
    
    # print("assignments", assignment[0:30])
    
    centroid_coll_folder = out_folder+"\\clusters"
    if not os.path.exists(centroid_coll_folder):
        os.makedirs(centroid_coll_folder)
    else:
        for the_file in os.listdir(centroid_coll_folder):
            file_path = os.path.join(centroid_coll_folder, the_file)
            try:                
                os.unlink(file_path)
            except:
                print("exception clearing folder")

    centroids_distr = np.zeros([nr_centroids])
    for c in range(centroids.shape[0]):
        fig = plt.figure(figsize=(15,15))
        for i in range(samples.shape[0]):
            if assignment[i]==c:
                plt.plot(x, samples[i,:], c="r")
                # print("plotted", c)
                centroids_distr[c]+=1
        plt.plot(x, centroids[c], c="g", linewidth=2.0)
        plt.xlabel("timestep")
        plt.ylabel("value")
        plt.axis([x[0],x[-1],0, max_value*1.1])
        peek = np.argmax(centroids[c])+1
        maxval = np.max(centroids[c])
        image_name = centroid_coll_folder + r"\data_patterns_centroid"+str(c)+"_peek"+str(peek)+"_maxval"+str(maxval)+".pdf"
        fig.savefig(image_name, bbox_inches='tight')
        image_name = centroid_coll_folder + r"\data_patterns_centroid"+fds(c)+".png"
        fig.savefig(image_name)
        plt.close()

    print("centroids_distr",centroids_distr)
    plot_centroids(out_folder, nr_centroids, centroids,all_centroids_folder, title=in_title)
    if all_centroids_folder!=None:
        all_centroids_folder=all_centroids_folder.replace("no_scale", "scale")
        plot_centroids(out_folder, nr_centroids, centroids,all_centroids_folder, title=in_title, eq_max=True)
    
    f_stats = open(out_folder+"\\stats_centroids.txt","w")
    for i in range(nr_centroids):
        f_stats.write("centroid"+str(i)+": "+str(centroids_distr[i])+"\n")
    f_stats.close()

def plot_centroids(out_folder, nr_centroids, centroids,  png_output_folder,title="title", eq_max=False):
    fig = plt.figure(figsize=(15,15))
    for c in range(centroids.shape[0]):
        plt.plot(x, centroids[c], c="g")
    plt.xlabel("timestep")
    plt.ylabel("value")
    plt.title(title)
    image_name = out_folder + r"\all_centroids.pdf"
    fig.savefig(image_name, bbox_inches='tight')
    if png_output_folder!=None:
        if eq_max:
            plt.axis([1,6,0,1])
        fig.savefig(png_output_folder)        
    plt.close()
    
    
def show_random_set_samples(filename, total_nr_samples, nr_samples, out_folder):
    samples = get_samples(filename, total_nr_samples, nr_samples)      
    
    fig = plt.figure()
    x = [1,2,3,4,5,6]
    for sample in samples:
        plt.plot(x, sample, c='r')
       
    plt.xlabel("timestep")
    plt.ylabel("value")
    image_name = out_folder + r"\data_patterns.pdf"
    fig.savefig(image_name, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    folder_template = r"D:\Users\Lydia\results_freqs\nn_data"
    case_name = r"\politics_ad_lim_ns_whole_landscape_simpleSamples"
    filename = folder_template+case_name+"\\simple_data.txt"
    
    total_nr_samples = 981763
    
    output_name = r"\clusters_per_output_range"    
    out_folder = folder_template+case_name+output_name
    nr_samples = 25000
    nr_centroids = 15
    intervals = [0,0.005,0.02, 0.04, 0.06, 0.08,0.1,0.15,0.2,1]
    k_means_on_samples_output_range(filename, total_nr_samples, nr_samples, nr_centroids, out_folder, intervals)
    
    
    # output_name = r"\normal_clusters"    
    # out_folder = folder_template+case_name+output_name
    # nr_samples = 5000
    # nr_centroids = 50
    # k_means_on_samples_all(filename, total_nr_samples, nr_samples, nr_centroids, out_folder)
    
    # out_folder = folder_template+case_name
    # nr_samples = 100
    # show_random_set_samples(filename, total_nr_samples, nr_samples, out_folder)
    
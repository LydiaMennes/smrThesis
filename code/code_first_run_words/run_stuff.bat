REM c:\python34\python co_occurrences.py new_politics_lim30000 politics --freq_cutoff 10 --use_stemmer no --max_nr_docs 30000 > log_cooc1.txt
REM c:\python34\python co_occurrences.py new_football_lim60000 football --freq_cutoff 10 --use_stemmer no --max_nr_docs 60000 > log_cooc2.txt
c:\python34\python co_occurrences.py new_politics_all politics --freq_cutoff 10 --use_stemmer no > log_cooc3.txt
c:\python34\python co_occurrences.py new_football_all football --freq_cutoff 10 --use_stemmer no > log_cooc4.txt

D:\Users\Lydia\results_freqs\nn_data\patches_pol_ed_rand_ndp5_nrp5\train.bat > log_exp_ed1.txt
D:\Users\Lydia\results_freqs\nn_data\patches_pol_ed_norm_ndp5_nrp5\train.bat > log_exp_ed2.txt

java -jar "K:\Lydia\smrThesis\code\thesis_NN\dist\thesis_NN.jar" 



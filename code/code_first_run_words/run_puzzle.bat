puzzle.py limit1000_nolog 11756 --process all --max_closest 8 --nr_trials_re_init 100 --stop_nr_trials 200 --to_file_trials 5 --old_grid_size 10
puzzle.py cutoff_10_nolog 30888 --process all --max_closest 8 --nr_trials_re_init 100 --stop_nr_trials 200 --to_file_trials 5 --old_grid_size 50



puzzle.py limit1000_nolog 11756 --process only_puzzle --max_closest 8 --nr_trials_re_init 30 --stop_nr_trials 59 --to_file_trials 3 --old_grid_size 10 --dif_output_dir limit1000_new_stats3
puzzle.py test3 130 --process initial_grid --max_closest 8 --nr_trials_re_init 30 --stop_nr_trials 59 --to_file_trials 3 --old_grid_size 10 --dif_output_dir test3_TEST
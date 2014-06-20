puzzle.py limit1000_nolog 11756 --process initial_grid
puzzle.py limit1000_nolog 11756 --dif_output_dir limit1000_normEnc_withF --encounter_deep no --process only_puzzle --max_closest 8 --nr_trials_re_init 500 --stop_nr_trials 300 --to_file_trials 3 --old_grid_size 10
puzzle.py limit1000_nolog 11756 --dif_output_dir limit1000_normEnc_noF --encounter_deep no --use_followers no --process only_puzzle --max_closest 8 --nr_trials_re_init 500 --stop_nr_trials 300 --to_file_trials 3 --old_grid_size 10
puzzle.py limit1000_nolog 11756 --dif_output_dir limit1000_deepEnc_noF --use_followers no --process only_puzzle --max_closest 8 --nr_trials_re_init 500 --stop_nr_trials 300 --to_file_trials 3 --old_grid_size 10
puzzle.py limit1000_nolog 11756 --dif_output_dir limit1000_deepEnc_noF --process only_puzzle --max_closest 8 --nr_trials_re_init 500 --stop_nr_trials 300 --to_file_trials 3 --old_grid_size 10


puzzle.py cutoff_10_nolog 30888 --process initial_grid --max_closest 8 --nr_trials_re_init 100 --dif_output_dir cutoff_10_new_stg

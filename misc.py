'''common functions for reuse'''
import os
import sys
import math
import multiprocessing as mp
args, exists = sys.argv, os.path.exists

'''parallel for loop'''
def parfor(my_function,  # function to run in parallel
           my_inputs,  # inputs evaluated by worker pool
           n_thread=mp.cpu_count()): # cpu threads to use

    if n_thread == 1:  # don't use multiprocessing for 1-thread
        return [my_function(my_inputs[i])
                for i in range(len(my_inputs))]
    else:
        n_thread = (mp.cpu_count() if n_thread is None
                    else n_thread)
        return mp.Pool(n_thread).map(my_function, my_inputs)


'''Display error, hard exit'''
def err(m):
    print("Error: ", m)
    sys.exit(1)


'''Run a shell command and return the return-code'''
def run(c):
    print(c)
    return os.system(c)

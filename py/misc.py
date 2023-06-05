'''common functions for reuse'''
import os
import sys
import math
import multiprocessing as mp
args, exists, sep = sys.argv, os.path.exists, os.path.sep

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

'''yyyymmddhhmmss time stamp'''
def time_stamp():
    import datetime
    now = datetime.datetime.now()  # create timestamp
    [year, month, day, hour, minute, second] = [str(now.year).zfill(4),
                                                str(now.month).zfill(2),
                                                str(now.day).zfill(2),
                                                str(now.hour).zfill(2),
                                                str(now.minute).zfill(2),
                                                str(now.second).zfill(2)]
    ts = ''.join([year, month, day, hour, minute, second])  # time stamp
    return ts


'''transform a shapefile to the desired crs in EPSG format'''
def shapefile_to_EPSG(src_f, dst_f, dst_EPSG=3347): # or 3005 bc albers
    t_epsg = dst_EPSG

    # try to read EPSG from file:
    if os.path.exists(dst_EPSG) and os.path.isfile(dst_EPSG):
        try:
            lines = [x.strip() for x in os.popen('gdalsrsinfo ' + dst_EPSG).read().strip().split('\n')]
            t_epsg = int(lines[-1].split(',')[-1].strip(']').strip(']'))
        except:
            err('failed to read EPSG from file')
    try:
        if src_f[-4:] != '.shp':
            err("shapefile input req'd")
    except Exception:
        err("please check input file")

    if not exist(src_f):
        err("could not find input file: " + src_f)

    run(' '.join['ogr2ogr',
                 '-t_srs',
                 'EPSG:' + str(t_epsg),
                 dst_f,
                 fn,
                 "-lco ENCODING=UTF-8"]);

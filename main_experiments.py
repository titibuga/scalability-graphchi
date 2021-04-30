#!/usr/bin/env python3
import time
import os
import subprocess
import re
import numpy as np
import matplotlib.pyplot as plt
import random, string


#### File lists

### Edge density

# files_list = [ "gnp_n10000_p0_001.txt",
#                     "gnp_n10000_p0_01.txt",
#                     "gnp_n10000_p0_1.txt",
#                     "gnp_n10000_p1.txt",
#                     "gnp_n10000_p10.txt",
#                     "gnp_n10000_p20.txt",
#                     "gnp_n10000_p50.txt"
#                     ]
##################



###### GraphChi setup

### Compute canada APP_DIR
APP_DIR = "/home/victorsp/projects/def-mseltzer/victorsp/graphchi-cpp/bin/example_apps/"
DATASET_DIR = "/home/victorsp/scratch/datasets/"
os.environ["GRAPHCHI_ROOT"] = "/home/victorsp/projects/def-mseltzer/victorsp/graphchi-cpp"
##

# ## LOCAL CONFIG
# APP_DIR = "../bin/example_apps/"
# DATASET_DIR = "../datasets/"
# os.environ["GRAPHCHI_ROOT"] = "/home/victorsp/UBC/CPSC508/graphchi-cpp"

#APP = "pagerank"
NITERS = "10"
NTHREADS = "1"

WARMUP_ROUNDS = 1
N_EXPERIMENTS = 3

TEMPDIR_CREATION_ATTEMPTS = 3



######


def main():
    dataset_file_template = "gnp_n10000_p{}.txt"
    # files_list = [ "circle_n10000000_out2.txt",
    #                "circle_n1000000_out2.txt",
    #                 "grid_h10000_w1000.txt",
    #                 "grid_h1000_w1000.txt",
    #                 ]
    
    files_list = ["rmat_gradient_n100000_e8499915_coeff0.7.txt"]

    applist = ["trianglecounting"]
    #app = "trianglecounting"
    n_threads_list = [1,2,4,8]
    p_list = ["1"]
    
    
    for app in applist:
        print("=========== APP: {} ============".format(app))
        plt.clf()

    
        print("============== EXPERIMENTS =================")
        (all_avg_times, std_devs) = experimentOverFiles(app, files_list,
                        n_threads_list=n_threads_list)
        print("============== END =================")

        for (t_list,f_name) in zip(all_avg_times, files_list):
            plt.plot(n_threads_list, [t_list[0]/t for t in t_list], label=f_name)
            print(t_list)

        
        print("All avg times:")
        print(all_avg_times)
        plt.legend()
        plt.savefig("{}_cyclegrid_timeplot_21Apr".format(app))
        #plt.savefig("timeplot_{}_gnps_varyinshards".format(app))
        
    
    


def experimentOverFiles(app, files_list, n_threads_list=[1,2,4,8]):

    all_avg_times = []
    all_std_devs = []
    for dataset_file in files_list:
        print("====> Experiments for file {}".format(dataset_file))
        (p_average_times, std_devs) = getAvgRuntimes(app, dataset_file,
                       n_threads_list=n_threads_list)
        all_avg_times.append(p_average_times)
        all_std_devs.append(std_devs)
    
    return all_avg_times, std_devs


def getAvgRuntimes(app, dataset, n_threads_list = [1,2,4,8]):
    average_times = []
    std_dev_times = []

    ### Create temporary folder for dataset to avoid concurrency problems

    def randomStrGenerator(str_size):
        return ''.join(random.choice(string.ascii_letters) for x in range(str_size))

    temp_dir_name = randomStrGenerator(20)
    temp_dir_creation_attempts = 0
    fullpath_temp_dir = DATASET_DIR + temp_dir_name + "/"
    print("==[GETAVGRT]===> Trying to create temp dir {}".format(temp_dir_name))
    while temp_dir_creation_attempts < TEMPDIR_CREATION_ATTEMPTS:

        ret1 = os.system("mkdir {}".format(fullpath_temp_dir))
        ret2 = os.system("cp {} {}".format( DATASET_DIR + dataset ,fullpath_temp_dir + dataset))

        if (ret1 == 0) and (ret2 == 0):
            print("==[GETAVGRT]===> Attemp {} was sucessful!".format(temp_dir_creation_attempts + 1))
            break

        temp_dir_creation_attempts+=1
        print("==[GETAVGRT]===> Attemp {} failed! (mkdir: {} | cp: {})".format(temp_dir_creation_attempts, ret1, ret2))
        os.system("rm -rf {}".format(fullpath_temp_dir))

    if temp_dir_creation_attempts >= TEMPDIR_CREATION_ATTEMPTS:
        return ([-2],[-2])

    for nt in n_threads_list:
        print("==[GETAVGRT]===> Number of threads: {}".format(nt))
        print("==[GETAVGRT]===> WARM UP")

        for _ in range(WARMUP_ROUNDS):
            execGraphChiApp(app, fullpath_temp_dir + dataset,
                             n_threads = nt)
        
        times = []

        print("==[GETAVGRT]===> EXPERIMENTS")
        for _ in range(N_EXPERIMENTS):
            t = execGraphChiApp(app, fullpath_temp_dir + dataset, n_threads = nt)
            times.append(t)

        print("==[GETAVGRT]===> nt: {} || times: {}".format(nt, times))
        average_times.append(np.mean(times))
        std_dev_times.append(np.std(times))

    print("==[GETAVGRT]===> (!!) End of experiments! (!!) ===========")
    print("==[GETAVGRT]===> List of avg times: {}".format(average_times))


    ## Delete temp dir
    ret3 = os.system("rm -rf {}".format(fullpath_temp_dir))
    print("==[GETAVGRT]===> Tried to delete temp dir. Ret: {}".format(ret3))

    return average_times, std_dev_times



def execGraphChiApp(app_name, dataset, n_threads=NTHREADS, n_shards=0):

    print("==================== GRAPHCHI EXEC ===================")
    print("=====> Dataset: {}".format(dataset))
    cmd_list = []
    cmd_list.append( APP_DIR + app_name)
    cmd_list.extend(["file", dataset])
    cmd_list.extend(["niters", NITERS])
    cmd_list.extend(["execthreads", str(n_threads)])
    if n_shards > 0:
        cmd_list.extend(["--nshards={}".format(n_shards)])

    print("====> Command List: {}".format(cmd_list))

    subp = subprocess.run(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,  input='edgelist\n'.encode('UTF-8'))
    pattern = re.compile("execute-updates")


    runtime = -1
    for l in subp.stdout.splitlines():
        print(l)
        l_str = str(l, 'UTF-8')
        if pattern.match(l_str):
            runtime = float((l_str.split()[1]).replace('s',''))
            print("Runtime: {}".format(runtime))
            break

    print("=============== END OF GRAPHCHI EXEC ================")

    return runtime

# tic = time.perf_counter()
# os.system(cmd)
# toc = time.perf_counter()
# print("===== PYTHON SCRIPT ==> Time: {}".format(toc - tic))

if __name__ == "__main__":
    main()
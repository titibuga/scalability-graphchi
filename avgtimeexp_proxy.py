#!/usr/bin/env python3


import os
import sys
from main_experiments import getAvgRuntimes
from main_experiments import DATASET_DIR


def main():

    if len(sys.argv) < 4:
        print("Usage mode: ./{} app dataset_name nthreads".format(sys.argv[0]))
        sys.exit(1)

    app_name = sys.argv[1]
    dataset_name = sys.argv[2]
    nt = int(sys.argv[3])

    (avg_times, std_devs) = getAvgRuntimes(app_name, dataset_name, n_threads_list=[nt])

    print("===[PROXY]==> File = {} || App = {} || nt = {}".format(dataset_name, app_name, nt))
    print("===[PROXY]==> avg_times = {}".format(avg_times))
    print("===[PROXY]==> std_devs =  {}".format(std_devs))




if __name__ == "__main__":
    main()
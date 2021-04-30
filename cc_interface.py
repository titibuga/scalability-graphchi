import os
import time

## CC root
GRAPHCHI_ROOT='/home/victorsp/projects/def-mseltzer/victorsp/graphchi-cpp'
##
# GRAPHCHI_ROOT='/home/victorsp/graphchi-cpp'
DEFAULT_MEM = '4G'

rmat_list = ["rmat_gradient_n100000_e8499915_coeff0.0.txt", "rmat_gradient_n100000_e8499915_coeff0.4.txt",  "rmat_gradient_n100000_e8499915_coeff0.8.txt",
"rmat_gradient_n100000_e8499915_coeff0.1.txt",  "rmat_gradient_n100000_e8499915_coeff0.5.txt",  "rmat_gradient_n100000_e8499915_coeff0.9.txt",
"rmat_gradient_n100000_e8499915_coeff0.2.txt", "rmat_gradient_n100000_e8499915_coeff0.6.txt", "rmat_gradient_n100000_e8499915_coeff1.txt",
"rmat_gradient_n100000_e8499915_coeff0.3.txt",  "rmat_gradient_n100000_e8499915_coeff0.7.txt"]

circlegrid_list = ["circle_n10000000_out2.txt",  "circle_n1000000_out2.txt",  "grid_h10000_w1000.txt",  "grid_h1000_w1000.txt"]

density_list = ["new_gnp_n100000_p0.0001_new.txt", "new_gnp_n100000_p0.001_new.txt", "new_gnp_n100000_p0.005_new.txt", "new_gnp_n100000_p0.0005_new.txt", "new_gnp_n100000_p0.002_new.txt"]



def main():

    file_list = density_list
    thread_n_list = [1, 2, 4, 8, 16, 32]
    task_list = ["connectedcomponents", "trianglecounting"]

    for f in file_list:
        for nt in thread_n_list:
            for task in task_list:
                print("Task: {}, File: {}, nt: {}".format(task, f, nt, maxtime="00:10:00"))
                ccAvgTimeExperiment(task, f, nt)
                time.sleep(1)   


def runJob(command, script_name ,output_name=None, ncores=1, mem=DEFAULT_MEM, maxtime="01:00:00"):

    if output_name == None:
        output_name = script_name.split(".")[0] + ".out"


    f = open(script_name, "w")

    # SLURM information

    f.write("#!/bin/bash\n")
    f.write("#SBATCH --time={}\n".format(maxtime))
    f.write("#SBATCH --output={}\n".format(output_name))
    f.write("#SBATCH --constraint=skylake\n")
    f.write("#SBATCH -c {}\n".format(ncores))
    if mem != None:
        f.write("#SBATCH --mem={}\n".format(mem))

    # Set GraphChi root -- just in case
    f.write("export GRAPHCHI_ROOT='{}'\n".format(GRAPHCHI_ROOT))

    # Add command
    f.write(command+"\n")

    f.close()

    # Schedule job
    os.system("sbatch {}".format(script_name))


def ccAvgTimeExperiment(app, dataset, nthreads, mem=DEFAULT_MEM):


    command = "python3 avgtimeexp_proxy.py {} {} {}".format(app, dataset, nthreads)
    shscript_name = "{}_{}_nt{}.sh".format(app, dataset, nthreads)
    out_name = "{}_{}_nt{}.out".format(app, dataset, nthreads)
    runJob(command, shscript_name, output_name=out_name, ncores=nthreads)



if __name__ == '__main__':
    main()
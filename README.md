# Experiment scripts


In this repository we most of the scripts used to reproduce the experiments from the paper "Analysis of Scalability in GraphChi".

The packages needed to generate the graphs and run the scripts are:
- `snap-stanford` 6.0.0
- `numpy` (any recent version).

Quick description of the scripts:
- `cc_interface` and `avgtimeexp_proxy.py` were used to perform the experiments on compute canada and do not have much purpose out of compute canada servers;
- `erdos_renyi.py` generates graphs with edges uniformly distributed;
- `gen_cycle.py` generates 3-regular circular graphs as described in the paper;
- `grid_generator.py` generates grid graphs as described in the paper;
- `rmat_gradient.py` generates a range of different RMAT graphs, going from real-world like to uniformly distributed edges;
- `main_experiments.py` this files performs the experiments in the same 

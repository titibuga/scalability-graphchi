#!/usr/bin/env python3


import snap
import sys


if len(sys.argv) < 3:
    print("Usage mode: ./{} n_of_vertices edge_density".format(sys.argv[0]))
    sys.exit(1)

n = int(sys.argv[1])
p = float(sys.argv[2])
m = round(p*n*(n-1)/2)
# my_seed = 42
G = snap.GenRndGnm(snap.TNGraph, n, m)

file_name = "new_gnp_n{}_p{}_new.txt".format(n,round(p,6))
f = open(file_name, "w")
for e in G.Edges():
    (u,v) = (e.GetSrcNId(), e.GetDstNId())
    f.write("{}\t{}\n".format(u,v))

f.close()
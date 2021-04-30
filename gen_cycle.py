#!/usr/bin/env python3

import snap
import sys



if len(sys.argv) < 3:
    print("Usage mode: ./{} n_of_vertices out_degree".format(sys.argv[0]))
    sys.exit(1)

n = int(sys.argv[1])
out_d = int(sys.argv[2])
# = round(p*n*(n-1)/2)
# my_seed = 42
G = snap.GenCircle(snap.TUNGraph, n, out_d)

file_name = "circle_n{}_out{}.txt".format(n,out_d)
f = open(file_name, "w")
for e in G.Edges():
    (u,v) = (e.GetSrcNId(), e.GetDstNId())
    f.write("{}\t{}\n".format(u,v))

f.close()
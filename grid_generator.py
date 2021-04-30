#!/usr/bin/env python3

import snap
import sys


if len(sys.argv) < 3:
    print("Usage mode: ./{} height width".format(sys.argv[0]))
    sys.exit(1)

h = int(sys.argv[1])
w = int(sys.argv[2])

# my_seed = 42
G = snap.GenGrid(snap.TNGraph, h, w)

file_name = "grid_h{}_w{}.txt".format(h,w)
f = open(file_name, "w")
for e in G.Edges():
    (u,v) = (e.GetSrcNId(), e.GetDstNId())
    f.write("{}\t{}\n".format(u,v))

f.close()
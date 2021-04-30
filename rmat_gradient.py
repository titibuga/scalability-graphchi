#!/usr/bin/env python3

import snap
import sys

if len(sys.argv) < 3:
    print("Usage mode: ./{} n_of_vertices n_of_edges [step_size]".format(sys.argv[0]))
    sys.exit(1)



n = int(sys.argv[1])
m = int(sys.argv[2])
step = 0.1
if len(sys.argv) > 3:
    step = float(sys.argv[3])

# Real-world R-MAT parameters
a = 0.59
b = c = 0.19

# Transition coeff - start at Real-world R-MAT
coeff = 0.0
unif = 0.25

while True:
    print("==> Generating R-MAT, transition coefficient: {}".format(coeff))

    print("==> a: {}, b: {}, c: {}".format(a + coeff*(unif - a),
                           b + coeff*(unif - b),
                           c + coeff*(unif- c)))
    G = snap.GenRMat(n, m, a + coeff*(unif- a),
                           b + coeff*(unif- b),
                           c + coeff*(unif- c))
    
    # Write to file
    file_name = "rmat_gradient_n{}_e{}_coeff{}.txt".format(n,m,coeff)
    f = open(file_name, "w")
    for e in G.Edges():
        (u,v) = (e.GetSrcNId(), e.GetDstNId())
        f.write("{}\t{}\n".format(u,v))
    f.close()

    # Next coeff
    if coeff == 1:
        break
    coeff += step
    if coeff > 1:
        coeff = 1
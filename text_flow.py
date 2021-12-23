"""

Author: Mouad Boudina
From: https://zenodo.org/record/5039610


The flow file structure is the following:

Re Ur
(blank line)
Nt N_nodes (Nt = length of the timeline of the flow simulation)
(blank line)
t0
node0_x node0_y U(node0) V(node0) p(node0)
node1_x node1_y U(node1) V(node1) p(node1)
...
t1
node0_x node0_y U(node0) V(node0) p(node0)
node1_x node1_y U(node1) V(node1) p(node1)
...

"""
import time
import numpy as np
#==============================================================================

def floatIt(l):
    return np.array([float(e) for e in l])

def intIt(l):
    return np.array([int(e) for e in l])

def read_flow(infile):
    # we need the following data for the normalisation 
    D = 0.055
    rho = 1.146
    #=====================================================

    f = open(infile, 'r')

    t1 = time.time()

    print('Reading flow...')

    Re, Ur = floatIt(f.readline().strip().split())

    f.readline() # blank line

    Nt, N_nodes = intIt(f.readline().strip().split())

    f.readline()

    times = []

    nodes_X, nodes_Y = [], []
    Us, Vs, ps = [], [], []

    for n in range(Nt):
        tn = float(f.readline().strip())
        times.append(tn)

        print('%.3f' % tn)

        tmp_nodes_X, tmp_nodes_Y = [], []
        tmp_Us, tmp_Vs, tmp_ps = [], [], []

        for k in range(N_nodes):
            x, y, U, V, p = floatIt(f.readline().strip().split())

            tmp_nodes_X.append(x)
            tmp_nodes_Y.append(y)

            tmp_Us.append(U)
            tmp_Vs.append(V)
            tmp_ps.append(p)

        nodes_X.append(tmp_nodes_X)
        nodes_Y.append(tmp_nodes_Y)

        Us.append(tmp_Us)
        Vs.append(tmp_Vs)
        ps.append(tmp_ps)

    cpu_time = time.time() - t1
    print('Done!')
    print('CPU_TIME = %f seconds' % cpu_time)

    f.close()
    times, Us, Vs, ps = np.array(times), np.array(Us), np.array(Vs), np.array(ps)
    return Re, Ur, times/(Ur/D), \
           np.array(nodes_X)/D, np.array(nodes_Y)/D, \
           Us/Ur, Vs/Ur, ps/(rho*Ur**2)                   # normalize data

def write_flow(flow, outfile):
    f = open(outfile, 'w')

    t1 = time.clock()

    print('Writing flow...')

    f.write('%.0f %.1f\n' % (flow.Re, flow.Ur))
    f.write('\n') # blank line

    Nt, N_nodes = len(flow.times), len(flow.nodes_X[0])

    f.write('%d %d\n' % (Nt, N_nodes))
    f.write('\n')

    for n in range(Nt):
        tn = flow.times[n]

        print('%.6f' % tn)

        f.write('%.6f\n' % tn)

        for k in range(N_nodes):
            f.write('%13.9f %13.9f %13.9f %13.9f %13.9f\n' %\
                    (flow.nodes_X[n, k],
                     flow.nodes_Y[n, k],
                     flow.Us[n, k],
                     flow.Vs[n, k],
                     flow.ps[n, k]))

    cpu_time = time.clock() - t1
    print('Done!')
    print('CPU_TIME = %f seconds' % cpu_time)

    f.close()

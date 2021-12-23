# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 21:24:33 2021

@author: louis
"""
import sys
import matplotlib.pyplot as plt
import pickle
import NN_functions as nnf
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--SparseData',type = bool, default=False,help="Set to True if you used sparse data for the job and False otherwise")
parser.add_argument('--Location', type=str, default = 'all', help="specify the location. Options are 'all' (default), 'cylinder_pitot', 'cylinder_only','pitot_only' ")
parser.add_argument('--Ur', type = float, default = 1, help = 'entry speed of your job. Set by default to 1 (data paper)')
parser.add_argument('--TwoZones', type = str, default = 'True', help = 'Mesh type of the job. If set to False, it means you used a uniform sampling.')
parser.add_argument('--Rand', type = int, default = 0, help = 'random number associated with the job')

args = parser.parse_args()
Vitesse = [1, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1, 0.15, 0.2, 4, 8, 12, 16, 20, 24, 28, 32]


if args.Ur not in Vitesse:
    print('Error: you have entered a wrong wpeed, please do it again')
    sys.exit()

if args.Rand<0 or args.Rand>999 or not isinstance(args.Rand, int):
    print('Error: the random number you have entered in not correct, please enter it again')
    sys.exit()
    
if args.Location not in ['all', 'cylinder_pitot', 'cylinder_only','pitot_only']:
    print('Error: location is not correct, please enter it again')
    sys.exit()

if args.Ur == 1:
    repertoire = 'OutputPythonScript_Surrogates/Paper_data/'
    Re = '100'
else:
    repertoire = 'OutputPythonScript_Surrogates/Real_data/'
    if args.Ur ==  0.03:
        Re = str(9.969789e+01)
    if args.Ur ==  0.04:
        Re = str(1.329305e+02)
    if args.Ur ==  0.05:
        Re = str(1.661631e+02)
    if args.Ur ==  0.06:
        Re = str(1.993958e+02)
    if args.Ur ==  0.08:
        Re = str(2.658610e+02)
    if args.Ur ==  0.1:
        Re = str(3.323263e+02)
    if args.Ur ==  0.15:
        Re = str(4.984894e+02)
    if args.Ur ==  0.2:
        Re = str(6.646526e+02)
    if args.Ur ==  4:
        args.Ur = int(args.Ur)
        Re = str(1.329305e+04)
    if args.Ur ==  8:
        args.Ur = int(args.Ur)
        Re = str(2.658610e+04)
    if args.Ur ==  12:
        args.Ur = int(args.Ur)
        Re = str(3.987915e+04)
    if args.Ur ==  16:
        args.Ur = int(args.Ur)
        Re = str(5.317221e+04)
    if args.Ur ==  20:
        args.Ur = int(args.Ur)
        Re = str(6.646526e+04)
    if args.Ur ==  24:
        args.Ur = int(args.Ur)
        Re = str(7.975831e+04)
    if args.Ur ==  28:
        args.Ur = int(args.Ur)
        Re = str(9.305136e+04)
    if args.Ur ==  32:
        args.Ur = int(args.Ur)
        Re = str(1.063444e+05)
        
path1 = repertoire + 'ModalPINN_Ur_' + str(args.Ur) + '_Re_' + Re + '_loc_' + args.Location + '_twoZones_' + str(args.TwoZones) + '_sparse_' + str(args.SparseData) + '_' + str(args.Rand)
path = repertoire + 'ModalPINN_Ur_' + str(args.Ur) + '_Re_' + Re + '_loc_' + args.Location + '_twoZones_' + str(args.TwoZones) + '_sparse_' + str(args.SparseData) + '_' + str(args.Rand) + '/Comparison_history.pickle'

file = open(path,'rb')
Dict = pickle.load(file)
file.close()

X_comp_u, X_comp_v, X_comp_p, Y_comp_u, Y_comp_v, Y_comp_p, U_comp, V_comp, P_comp, fluid_u_comp, fluid_v_comp, fluid_p_comp, timesteps = Dict

print('\n Starting plots \n')
for ind, timestep in enumerate(timesteps):
    title = 'Ur = ' + str(args.Ur) + ' - Comparison with exact model at time ' + '{0:.2f}'.format(timestep)
    nnf.plot_compare_9plot(X_comp_u[ind], Y_comp_u[ind], U_comp[ind], fluid_u_comp[ind], 
                           X_comp_v[ind], Y_comp_v[ind], V_comp[ind], fluid_v_comp[ind],
                           X_comp_p[ind], Y_comp_p[ind], P_comp[ind], fluid_p_comp[ind],
                           title = title, title2 = 'Approx of u', title3 = 'Approx of v', title4 = "Approx of p")                       
    plt.savefig(path1 + '/Courbes/Comparison_to_ground_truth/' + str(args.Ur) + '_t_'+'{0:.2f}'.format(timestep)+'.png', dpi=200)
    plt.close()

print('\n End !\n')


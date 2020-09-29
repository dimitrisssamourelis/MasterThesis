import sys
sys.path.append("./delauney")

import argparse
from delauney.algorithm.DCEL import *
from numpy import genfromtxt



ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="input images folder")
ap.add_argument("-vtree", "--visualize_tree", required=False, default=False, help="True if triangle tree (Dtree) visualization is needed")
ap.add_argument("-vstep", "--visualize_steps", required=False, default=False, help="True if algorithm steps visualization is needed")
args = vars(ap.parse_args())

# Arguments
full_filename = args['input']
vtree = bool(args['visualize_tree'])
vstep = bool(args["visualize_steps"])

filename = full_filename.split(".")[0]

data = genfromtxt(filename + '.csv', delimiter=',')

dcel = DCEL(data)

delauney_trig = dcel.execute()

dcel.visualize_triangulization(filename + "_result.jpg")

if vtree:
    dcel.visualize_tree(filename + "_tree")

if vstep:
    dcel.visualize_algorithm(filename)

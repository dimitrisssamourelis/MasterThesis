import sys
import numpy as np 

import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-r", "--rows", required=True, help="#rows of generated data")
ap.add_argument("-m", "--maxnum", required=True, help="Max Number generated in set ")
ap.add_argument("-o", "--output", required=False, default="./data.csv", help="Output location of generated dataset")
args = vars(ap.parse_args())

# Arguments
rows = int(args['rows'])
maxnum = int(args['maxnum'])
savefile = args["output"]

points = np.random.rand(rows, 2)

points = points*maxnum

points = np.unique(points.astype(int), axis = 0)

np.savetxt(savefile, points, delimiter=',')

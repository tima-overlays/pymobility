# coding: utf-8
#
#  Copyright (C) 2008-2010 Istituto per l'Interscambio Scientifico I.S.I.
#  You can contact us by email (isi@isi.it) or write to:
#  ISI Foundation, Viale S. Severo 65, 10133 Torino, Italy.
#
#  This program was written by André Panisson <panisson@gmail.com>
#

'''
Created on Jan 24, 2012

@author: André Panisson
@contact: panisson@gmail.com
@organization: ISI Foundation, Torino, Italy
'''
from pymobility.models.mobility import truncated_levy_walk
import numpy as np
import logging
import sys
import argparse


logging.basicConfig(format='%(asctime)-15s - %(message)s', level=logging.INFO)
logger = logging.getLogger("simulation")

parser = argparse.ArgumentParser(description='Generate a mobility file using the Truncated-Levy-Walk model.')
parser.add_argument('--steps', dest='steps_per_second', type=int, default=15,
                    help='Steps per second')
parser.add_argument('--width', dest='map_width', type=int, default=100,
                    help='Map Width')
parser.add_argument('--height', dest='map_height', type=int, default=100,
                    help='Map Height')
parser.add_argument('--nodes', dest='nr_nodes', type=int, default=200,
                    help='Number Of Nodes')
parser.add_argument('--time', dest='simtime', type=int, default=60*100,
                    help='Simulation Time in Seconds')
parser.add_argument('--out', dest='filename', type=str, default="output.txt",
                    help='Output file')

args = parser.parse_args()

SPS = int(args.steps_per_second)
nr_nodes = args.nr_nodes

# simulation area (units)
MAX_X, MAX_Y = args.map_width, args.map_height

sim_time = int(args.simtime)

# number of steps to ignore before start plotting
STEPS_TO_IGNORE = 1000

np.random.seed(0xffff)

# Truncated Levy-Walk model
rw = truncated_levy_walk(nr_nodes, dimensions=(MAX_X, MAX_Y))

step_time = 1. / float(SPS)

with open(args.filename, 'w') as f:
    # warm-up steps
    for step in range(0, STEPS_TO_IGNORE):
        rw.next()

    # real steps
    for step in range(0, sim_time*SPS):
        xy = rw.next()
        if step % 1000 == 0:
            logger.info('Step %s' % step)

        for idx, (x, y) in enumerate(xy):
            f.write('hostR%d,%f,%f,%f\n' % (idx, step_time*step, x, y))

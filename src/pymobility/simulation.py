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
from pymobility.models.mobility import gauss_markov, reference_point_group, \
    tvc, truncated_levy_walk, random_direction, random_waypoint, random_walk
import numpy as np
import logging
from scipy.spatial.distance import cdist
import matplotlib.animation as manimation
import sys


logging.basicConfig(format='%(asctime)-15s - %(message)s', level=logging.INFO)
logger = logging.getLogger("simulation")

# set this to true if you want to plot node positions
DRAW = True

FPG=20

if DRAW:
    FFMpegWriter = manimation.writers['ffmpeg']
    metadata = dict(title='Movie Test', artist='Matplotlib', comment='Movie support!')
    writer = FFMpegWriter(fps=FPG, metadata=metadata)


# number of nodes
nr_nodes = 100

# simulation area (units)
MAX_X, MAX_Y = 100, 100

# max and min velocity
MIN_V, MAX_V = 0.1, 1.

# max waiting time
MAX_WT = 100.

# number of steps to ignore before start plotting
STEPS_TO_IGNORE = 1000

# set this to true if you want to calculate node contacts
CALCULATE_CONTACTS = False
# if calculating contacts, this is the range to be used
# (if a distance(a,b) < RANGE, then there is a contact betwen a and b)
RANGE = 1.

if DRAW:
    import matplotlib.pyplot as plt
    fig = plt.figure() # plt.ion()
    ax = plt.subplot(111)
    line, = ax.plot(range(MAX_X), range(MAX_X), linestyle='', marker='.')

step = 0
np.random.seed(0xffff)

# UNCOMMENT THE MODEL YOU WANT TO USE

## Random Walk model
#rw = random_walk(nr_nodes, dimensions=(MAX_X, MAX_Y))

## Truncated Levy Walk model
rw = tlw = truncated_levy_walk(nr_nodes, dimensions=(MAX_X, MAX_Y))

## Random Direction model
#rd = random_direction(nr_nodes, dimensions=(MAX_X, MAX_Y))

## Random Waypoint model
#rwp = random_waypoint(nr_nodes, dimensions=(MAX_X, MAX_Y), velocity=(MIN_V, MAX_V), wt_max=MAX_WT)

## Gauss-Markov model
#gm = gauss_markov(nr_nodes, dimensions=(MAX_X, MAX_Y), alpha=0.99)

## Reference Point Group model
#groups = [4 for _ in range(10)]
#nr_nodes = sum(groups)
#rpg = reference_point_group(groups, dimensions=(MAX_X, MAX_Y), aggregation=0.5)

## Time-variant Community Mobility Model
#groups = [4 for _ in range(10)]
#nr_nodes = sum(groups)
#tvcm = tvc(groups, dimensions=(MAX_X, MAX_Y), aggregation=[0.5,0.], epoch=[100,100])

with writer.saving(fig, "writer_test.mp4", 100):
    for xy in rw:

        step += 1
        if step % 1000 == 0:
            logger.info('Step %s' % step)



        if step >= STEPS_TO_IGNORE and DRAW:

            line.set_data(xy[:, 0], xy[:, 1])
            writer.grab_frame()
            plt.draw()

        if step == 10*60*FPG + STEPS_TO_IGNORE:
            sys.exit(0)

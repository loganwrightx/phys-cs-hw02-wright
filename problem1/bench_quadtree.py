"""
Author: Logan Wright
Description: Bench test of the quad tree data structure implmented prior.
"""

import random
import time
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from numpy import log2

from quadtree import QuadTree, Rectangle

# Simple linear model to fit to the log-log curve
linear_model = lambda x, m, b: m * x + b

Ns = [100, 200, 400, 800, 1600, 3200]
ts = []

for N in Ns:
    # Generate random points
    points = []
    for _ in range(N):
        points.append((random.uniform(-10.0, 10.0), random.uniform(-10.0, 10.0)))
    
    # Small debug statement to help with clarity
    print(f"Starting to build tree for N = {N}")

    # Record start time
    start = time.perf_counter()

    # Build the tree for each N
    tree = QuadTree(boundary=Rectangle(0.0, 0.0, 20.0, 20.0))

    for point in points:
        tree.insert(point)
    
    # And get stop time
    delta = time.perf_counter - start

    ts.append(delta)

# Get logs of both x and y axes
log_t = [log2(t) for t in ts]
log_n = [log2(n) for n in Ns]

fit_params, fit_uncertainties = curve_fit(linear_model, log_n, log_t)

print(f"slope = {fit_params[0]}, y-intercept = {fit_params[1]}")

plt.plot(log_n, log_t)
plt.savefig("log_log.png")
plt.show()

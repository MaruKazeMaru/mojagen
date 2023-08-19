#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from curve import curve
from curve_generator import moja_generator
from curve_twister import twist_curve 

if __name__ == "__main__":
    import sys
    moja = moja_generator(point_num=2000, tor_coef=float(sys.argv[1])).generate()
    moja = twist_curve(moja, freq=float(sys.argv[2]), radius=float(sys.argv[3]))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    x = moja.c[0, :]
    y = moja.c[1, :]
    z = moja.c[2, :]
    max_x = max(x)
    min_x = min(x)
    max_y = max(y)
    min_y = min(y)
    max_z = max(z)
    min_z = min(z)
    cen_x = (max_x + min_x) / 2.0
    cen_y = (max_y + min_y) / 2.0
    cen_z = (max_z + min_z) / 2.0
    ax_scale = max(max_x - min_x, max_y - min_y, max_z - min_z) / 2.0
    ax.set_xlim(cen_x - ax_scale, cen_x + ax_scale)
    ax.set_ylim(cen_y - ax_scale, cen_y + ax_scale)
    ax.set_zlim(cen_z - ax_scale, cen_z + ax_scale)
    ax.plot(x, y, z)
    plt.show()

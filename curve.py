#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2023 Kazemaru
# SPDX-License-Identifer: MIT

from numpy import ndarray

class curve:
    # arc length parameter
    s:ndarray
    # position
    c:ndarray
    # tangent Frenet-Serret frame
    t:ndarray
    # normal Frenet-Serret frame
    n:ndarray
    # normal Frenet-Serret frame
    b:ndarray

    def __init__(self, sol=None):
        if not sol is None:
            self.s = sol.t
            self.c = sol.y[3:6,:]
            self.t = sol.y[6:9,:]
            self.n = sol.y[9:12,:]
            self.b = sol.y[12:15,:]

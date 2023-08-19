#!/usr/bin/env python3

import numpy as np
from numpy import ndarray
from curve import curve

def twist_curve(original:curve, radius:float=1.0, freq:float=2.0) -> curve:
    twisted = curve()
    twisted.s = original.s
    twisted.c = original.c
    for i in range(1,4):
        rand = np.random.normal(loc=1.0, scale=0.3)
        twisted.c += radius * rand * float(1 / i) * np.sin(float(i) * freq * twisted.s) * original.n
        twisted.c += radius * rand * float(1 / i) * np.cos(float(i) * freq * twisted.s) * original.b
    return twisted
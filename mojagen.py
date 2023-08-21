#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from curve import curve
from curve_generator import moja_generator
from curve_twister import twist_curve
from plot import plot_curve
import argparse

def parse_argumets() -> dict:
    parser = argparse.ArgumentParser(description="moja generator")
    parser.add_argument("--length", type=float)
    parser.add_argument("--sample", type=int, help="sample point count")
    parser.add_argument("--torsion", type=float)
    parser.add_argument("--radius", type=float, help="twist radius")
    parser.add_argument("--freq", type=float, help="twist frequency")
    parser.add_argument("-p", "--plot", action="store_true", help="show graph")
    args = parser.parse_args()

    moja_kwargs = {}
    if not args.length is None:
        moja_kwargs["length"] = args.length
    if not args.sample is None:
        moja_kwargs["point_num"] = args.sample
    if not args.torsion is None:
        moja_kwargs["tor_coef"] = args.torsion

    twist_kwargs = {}
    if not args.radius is None:
        twist_kwargs["radius"] = args.radius
    if not args.freq is None:
        twist_kwargs["freq"] = args.freq

    return {"generate" : moja_kwargs, "twist" : twist_kwargs, "plot" : args.plot}


def generate_moja(args) -> curve:
    moja = moja_generator(**(args["generate"])).generate()
    moja = twist_curve(moja, **(args["twist"]))
    return moja


if __name__ == "__main__":
    args = parse_argumets()
    moja = generate_moja(args)

    if args["plot"]:
        plot_curve(moja)

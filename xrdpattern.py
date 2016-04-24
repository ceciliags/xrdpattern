#!/usr/bin/env python3
"""Plot XRD patterns."""

import argparse
from itertools import dropwhile

import docx2txt
from matplotlib import pyplot as plt
import numpy as np


def find_token(name, tokens):
    # With dropwhile(), all the items before name are dropped and
    # keeps what comes next
    tokens = dropwhile(lambda token: token != name, tokens)
    next(tokens)  # Skip first item
    return tokens


def parse_data(filename):
    txt = docx2txt.process(filename)
    # Split data into smaller pieces: tokens
    # split() is a method that separates text into words using
    # white-spaces when no argument is given
    tokens = txt.split()
    tokens = find_token("Sample", tokens)
    sample = next(tokens)
    tokens = find_token("FirstAngle", tokens)
    first_angle = float(next(tokens))
    tokens = find_token("ScanRange", tokens)
    scan_range = float(next(tokens))
    tokens = find_token("StepWidth", tokens)
    step_width = float(next(tokens))
    tokens = find_token("ScanData", tokens)
    scan_data = list(map(float, tokens))
    return (sample, first_angle, scan_range, step_width, scan_data)


def main():
    # Define parser for parsing the command line arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "datafiles",
        metavar="datafile",
        nargs="+",
        help="a MS Word file containing xrd data",
    )
    parser.add_argument(
        "-t", "--title",
        help="a title for the plot",
    )
    parser.add_argument(
        "-l", "--labels",
        help="non-default labels for the datafiles separated by commas",
    )
    parser.add_argument(
        "--no-show",
        dest="show",
        action="store_false",
        help="if given, the plots are not displayed",
    )
    parser.add_argument(
        "-s", "--save",
        metavar="NAME",
        help="saves the plot as the given NAME (extension honored)",
    )
    parser.add_argument(
        "--no-si",
        dest="si",
        action="store_false",
        help="hides Bragg reflections for Si in orinetation (100)",
    )
    parser.add_argument(
        "--no-zrc",
        dest="zrc",
        action="store_false",
        help="hides Bragg reflections for ZrC",
    )
    parser.add_argument(
        "--zr3c2",
        dest="zr3c2",
        action="store_true",
        help="shows Bragg reflections for delta-Zr3C2",
    )
    parser.add_argument(
        "--zr",
        dest="zr",
        action="store_true",
        help="shows most intense Bragg reflections for Zr",
    )
    args = parser.parse_args()

    if args.labels:
        labels = args.labels.split(",")
        if len(labels) != len(args.datafiles):
            raise RuntimeError(
                "Number of labels does not match number of datafiles"
            )
    else:
        labels = []

    for i, filename in enumerate(args.datafiles):
        sample, first_angle, scan_range, step_width, scan_data = \
            parse_data(filename)

        angle = np.linspace(
            first_angle,
            first_angle + scan_range,
            len(scan_data),
        )
        scan_data = np.array(scan_data) * 1000**i

        plt.text(angle[-1], scan_data[-1], sample, va="bottom")

        if labels:
            plt.text(angle[-1], scan_data[-1], labels[i], va="top")

        plt.semilogy(angle, scan_data)

    ymin, ymax = plt.ylim()

    if args.si:
        for a, p in [(32.959, "(200)"), (69.132, "(400)"), (117, "(600)")]:
            plt.plot((a, a), (ymin, ymax), "k--")
            plt.text(a, ymax / 2.5, "Si " + p, ha="right",
                     rotation="vertical", va="top")

    if args.zrc:
        for a, p in [(33.041, "(111)"), (38.338, "(200)"),
                     (55.325, "(220)"), (65.969, "(311)"),
                     (82.051, "(400)"), (91.340, "(331)"),
                     (94.455, "(420)"), (107.061, "(422)"),
                     (117.064, "(511)")]:
            plt.plot((a, a), (ymin, ymax), "k:")
            plt.text(a, ymax, "ZrC " + p, ha="left", rotation="vertical",
                     va="top")

    if args.zr3c2:
        for a, p in [(17.846, "(003)"), (35.966, "(102)"),
                     (36.145, "(006)"), (55.336, "(017)"),
                     (60.511, "(110)"), (60.753, "(108)")]:
            plt.plot((a, a), (ymin, ymax), "b-.")
            plt.text(a, ymax / 7.5, "$\delta-$Zr3C2 " + p, ha="left",
                     rotation="vertical", va="top")

    if args.zr:
        for a, p in [(31.958, "(100)"), (34.838, "(002)"),
                     (36.509, "(101)"), (47.993, "(102)"),
                     (56.932, "(110)"), (63.537, "(103)"),
                     (68.534, "(112)"), (69.578, "(201)")]:
            plt.plot((a, a), (ymin, ymax), "r-.")
            plt.text(a, ymax / 7.5, "Zr " + p, ha="left",
                     rotation="vertical", va="top")

    plt.xlabel("2$\Theta$ ($^{\circ}$)")
    plt.ylabel("Intensity")
    plt.gca().set_yticklabels([])

    if args.title:
        plt.title(args.title)

    if args.save:
        plt.savefig(args.save, dpi=300)

    if args.show:
        plt.show()


if __name__ == "__main__":
    main()

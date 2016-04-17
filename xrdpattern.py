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
    args = parser.parse_args()

    for i, filename in enumerate(args.datafiles):
        sample, first_angle, scan_range, step_width, scan_data = \
            parse_data(filename)

        angle = np.linspace(
            first_angle,
            first_angle + scan_range,
            len(scan_data),
        )
        scan_data = np.array(scan_data) * 1000**i

        plt.text(angle[-1], scan_data[-1], sample)

        plt.semilogy(angle, scan_data)

        ymin, ymax = plt.ylim()
        for a, p in [(33, "(200)"), (69.13, "(400)"), (117, "(600)")]:
            plt.plot((a, a), (ymin, ymax), "k--")
            plt.text(a, ymax / 2.5, "Si " + p, ha="right", rotation="vertical",
                     va="top")

        for a, p in [(33.5, "(111)"), (38, "(200)"), (55, "(220)"),
                     (65, "(311)"), (81, "(400)"), (93, "(420)"),
                     (108, "(422)")]:
            plt.plot((a, a), (ymin, ymax), "k:")
            plt.text(a + 0.5, ymax, "ZrC " + p, ha="left", rotation="vertical",
                     va="top")

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

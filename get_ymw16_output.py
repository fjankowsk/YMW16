#
#   2017 Fabian Jankowski
#   Get output from YMW16 model.
#

import logging
import argparse
import shlex
import subprocess
import numpy as np
from io import BytesIO


def get_ymw16_output(gl, gb, dm):
    """
    Call and parse output data from YMW16 model.
    """

    command = "ymw16 -o Gal {0} {1} {2} 1".format(gl, gb, dm)

    # split into correct tokens for Popen
    args = shlex.split(command)

    resultstr = subprocess.check_output(args)

    dtype = [
        ("mode", "|S8"),
        ("gl", "float"),
        ("gb", "float"),
        ("dm", "float"),
        ("dm_gal", "float"),
        ("dist", "float"),
        ("taus", "float"),
    ]

    f = BytesIO(resultstr)
    data = np.genfromtxt(f, delimiter=";", dtype=dtype)

    # convert to kpc
    data["dist"] = 1e-3 * data["dist"]

    # convert taus
    data["taus"] = 10 ** data["taus"]

    return data


#
# MAIN
#


def main():
    # set up logging
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    # handle command line arguments
    parser = argparse.ArgumentParser(description="Get output from YMW16 model.")
    parser.add_argument(
        "gl", type=float, help="Galactic latitude of object in degrees."
    )
    parser.add_argument(
        "gb", type=float, help="Galactic longitude of object in degrees."
    )
    parser.add_argument("dm", type=float, help="DM of object in pc/cm3.")

    args = parser.parse_args()

    data = get_ymw16_output(args.gl, args.gb, args.dm)

    for field in data.dtype.names:
        print("{0:10} {1:8}".format(field, data[field]))

    print("All done.")


if __name__ == "__main__":
    main()

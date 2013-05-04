import argparse
import numpy as np
from FAUSTPy import *

# set up command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--faustfloat',
                    dest="faustfloat",
                    default="float",
                    help="The value of FAUSTFLOAT.")
parser.add_argument('-p', '--path',
                    dest="faust_path",
                    default="",
                    help="The path of FAUSTFLOAT.")
parser.add_argument('-c', '--cflags',
                    dest="cflags",
                    default=[],
                    type=str.split,
                    help="Extra compiler flags")
parser.add_argument('-s', '--fs',
                    dest="fs",
                    default=48000,
                    type=int,
                    help="The sampling frequency")
args = parser.parse_args()

wrapper.FAUST_PATH = args.faust_path

dattorro = FAUST("dattorro_notch_cut_regalia.dsp", args.fs, args.faustfloat,
                 extra_compile_args=args.cflags)

audio = np.zeros((dattorro.dsp.num_in, args.fs), dtype=dattorro.dsp.dtype)
audio[:,0] = 1

out = dattorro.compute(audio)

print(audio)
print(out)

print("everything passes!")

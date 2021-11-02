import os
import glob
from sys import version_info
import argparse

import FAUSTPy


def find_faust_examples_directory():
    """Find and return the path to the faust examples directory"""

    # check for a "/usr/share/faust-<version>" directory
    fs_root = os.path.abspath(os.sep)
    usr_share_glob_results = glob.glob(os.path.join(fs_root, 'usr', 'share', 'faust-*'))
    if usr_share_glob_results:
        youngest_result = max(usr_share_glob_results, key=os.path.getctime)
        return os.path.join(youngest_result, 'examples')

    # if `faust` executable is in PATH, try using that to find the examples
    # note: shutil.which is only available in python 3.3+
    if version_info.major >= 3 and version_info.minor >= 3:
        from shutil import which
        from pathlib import Path
        faust_install_dir = Path(which('faust')).resolve().parents[1]
        return str(faust_install_dir / 'share' / 'faust' / 'examples')

    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path',
                        dest="examples_path",
                        default=find_faust_examples_directory(),
                        help="The path to the FAUST examples.")
    args = parser.parse_args()

    if args.examples_path is None:
        raise EnvironmentError(
            "Could not find path to faust examples directory "
            "automatically.  Please specify manually using the --path flag."
        )

    fs = 48e3
    examples = (
        glob.glob(os.path.join(args.examples_path, "*.dsp")) +
        glob.glob(os.path.join(args.examples_path, "*/*.dsp"))
    )
    for f in examples:
        print(f)
        dsp = FAUSTPy.FAUST(f, int(fs), "double")

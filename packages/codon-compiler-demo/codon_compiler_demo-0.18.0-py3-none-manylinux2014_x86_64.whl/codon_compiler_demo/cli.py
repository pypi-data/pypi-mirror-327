from codon_compiler_demo import CODON_BIN
from codon_compiler_demo.find_shared_lib import find_python_shared_library
import sys, os, subprocess

import sys
def main():
    if CODON_PYTHON := find_python_shared_library(not_found_ok=True):
        env = dict(os.environ, CODON_PYTHON=CODON_PYTHON)
    else:
        env = None

    subprocess.run([CODON_BIN, *sys.argv[1:]], env=env)

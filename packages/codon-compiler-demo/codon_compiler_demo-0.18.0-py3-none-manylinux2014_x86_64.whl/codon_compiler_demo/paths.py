from pathlib import Path

CODON_DIR = Path(__file__).resolve().parent / 'binaries/linux-x86_64'
CODON_LIB = str(CODON_DIR / 'lib/codon')
CODON_BIN = str(CODON_DIR / 'bin/codon')

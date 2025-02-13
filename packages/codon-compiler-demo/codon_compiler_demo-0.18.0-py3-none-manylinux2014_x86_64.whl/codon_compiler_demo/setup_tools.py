from pathlib import Path
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from codon_compiler_demo.paths import CODON_BIN, CODON_LIB

class CodonExtension(Extension):
    def __init__(self, name, source):
        self.source = source
        super().__init__(name, sources=[], language='c')

class BuildCodonExt(build_ext):
    def build_extensions(self):
        pass

    def run(self):
        inplace, self.inplace = self.inplace, False
        super().run()
        for ext in self.extensions:
            self.build_codon(ext)
        if inplace:
            self.copy_extensions_to_source()

    def build_codon(self, ext):
        extension_path = Path(self.get_ext_fullpath(ext.name))
        extension_path.parent.absolute().mkdir(parents=True, exist_ok=True)
        build_dir = Path(self.build_temp)
        build_dir.mkdir(parents=True, exist_ok=True)

        optimization = '-debug' if self.debug else '-release'
        ext_name     = ext.name.split('.')[-1]
        self.spawn([CODON_BIN, 'build', optimization, '--relocation-model=pic', '-pyext',
                    '-o', str(extension_path) + ".o", '-module', ext_name, ext.source])

        ext.runtime_library_dirs = [CODON_LIB]
        self.compiler.link_shared_object(
            [str(extension_path) + '.o'],
            str(extension_path),
            libraries=['codonrt'],
            library_dirs=ext.runtime_library_dirs,
            runtime_library_dirs=ext.runtime_library_dirs,
            extra_preargs=['-Wl,-rpath,@loader_path'],
            debug=self.debug,
            build_temp=self.build_temp,
        )
        self.distribution.codon_lib = extension_path

from pathlib import Path
import sysconfig, platform

def find_python_shared_library(not_found_ok=False):
    if platform.system() == 'Linux':
        lib_name = 'libpython{}.{}.so'.format(*platform.python_version_tuple()[:2])
    elif platform.system() == 'Darwin':
        lib_name = 'libpython{}.{}.dylib'.format(*platform.python_version_tuple()[:2])
    else:
        raise NotImplementedError("This script currently supports only Linux and macOS.")

    # Potential directories to check based on common build configurations
    for key in ('LIBDIR', 'LIBPL', 'LIBDEST'):
        path = Path(sysconfig.get_config_var(key)) / lib_name
        if path.exists(): return path

    if not_found_ok: return None

    raise FileNotFoundError(f"Could not find the Python shared library: {lib_name}")



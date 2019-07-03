# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Optix(Package):
    """Nvidia OptiX is a ray tracing API."""
    homepage = "https://developer.nvidia.com/optix"
    version('5.1.1','6e0671d49d08289c5c1ceceb9c505bbf', extension='sh', expand=False)
    url = "file:///gpfs/bbp.cscs.ch/project/proj3/development/deployment/NVIDIA-OptiX-SDK-5.1.1-linux64-25109142.sh"
    phases = [ 'install']

    def install(self, spec, prefix):
        set_executable('./NVIDIA-OptiX-SDK-5.1.1-linux64-25109142.sh')
        install = Executable('./NVIDIA-OptiX-SDK-5.1.1-linux64-25109142.sh')
        install('--skip-license', '--prefix=%s' % prefix)

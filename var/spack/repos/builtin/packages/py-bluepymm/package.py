##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class PyBluepymm(PythonPackage):
    """Blue Brain Model Management Python Library"""

    homepage = "https://github.com/BlueBrain/BluePyMM"
    url = "https://pypi.io/packages/source/b/bluepymm/bluepymm-0.6.35.tar.gz"

    version('0.6.38', sha256='3bba40c3553429b29a1567e5f443a0fae8b477872ea9e400b68d9f19404acc34')

    depends_on('py-setuptools', type='build')
    depends_on('py-bluepyopt', type='run')
    depends_on('py-matplotlib', type='run')
    # The below dependency should disappear once the matplotlib package is fixed
    depends_on('py-backports-functools-lru-cache', type='run', when="^python@:3.3.99")
    depends_on('py-pandas', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-ipyparallel', type='run')
    depends_on('py-lxml', type='run')
    depends_on('py-sh', type='run')
    depends_on('neuron', type='run')

    def setup_environment(self, spack_env, run_env):
        run_env.unset('PMI_RANK')
        run_env.set('NEURON_INIT_MPI', "0")

# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ultraliser(CMakePackage):
    git = "ssh://bbpcode.epfl.ch/viz/Ultraliser"

    version('0.1.0', tag='v0.1.0')

    depends_on('libtiff')
    depends_on('ilmbase')


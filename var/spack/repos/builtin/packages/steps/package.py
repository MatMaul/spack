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
import os.path as osp

from spack import *


class Steps(CMakePackage):
    """STochastic Engine for Pathway Simulation"""

    homepage = "https://groups.oist.jp/cnu/software"
    git      = "https://github.com/CNS-OIST/STEPS.git"

    version("3.3.0", submodules=True)
    version("3.2.0", submodules=True)
    version("develop", branch="master", submodules=True)

    variant("native", default=True, description="Generate non-portable arch-specific code")
    variant("bindings", default="cython",
            values=("cython", "swig"),
            description="Generate bindings using Cython, instead of Swig")
    variant("lapack", default=False, description="Use new BDSystem/Lapack code for E-Field solver")
    variant("petsc", default=False, description="Use PETSc library for parallel E-Field solver")
    variant("mpi", default=True, description="Use MPI for parallel solvers")

    depends_on("blas")
    depends_on("lapack", when="+lapack")
    depends_on("mpi", when="+mpi")
    depends_on("petsc^debug+int64", when="+petsc")
    depends_on("python")
    depends_on("swig", when="bindings=swig")
    depends_on("py-cython", when="bindings=cython")

    def cmake_args(self):
        args = []
        spec = self.spec
        bindings =  spec.variants["bindings"].value

        if "+native" in spec:
            args.append("-DTARGET_NATIVE_ARCH:BOOL=True")
        else:
            args.append("-DTARGET_NATIVE_ARCH:BOOL=False")

        if bindings == "cython":
            args.append("-DPYTHON_BINDINGS_CYTHON:BOOL=True")
        elif bindings == "swig":
            args.append("-DPYTHON_BINDINGS_CYTHON:BOOL=False")
        else:
            raise Exception("Unexpected bindings type: " + bindings)

        if "+lapack" in spec:
            args.append("-DUSE_BDSYSTEM_LAPACK:BOOL=True")
        else:
            args.append("-DUSE_BDSYSTEM_LAPACK:BOOL=False")

        if "+petsc" in spec:
            args.append("-DUSE_PETSC:BOOL=True")
        else:
            args.append("-DUSE_PETSC:BOOL=False")

        if "+mpi" in spec:
            args.append("-DUSE_MPI:BOOL=True")
        else:
            args.append("-DUSE_MPI:BOOL=False")

        args.append('-DBLAS_LIBRARIES=' + spec['blas'].libs.joined(";"))
        return args

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PYTHONPATH', self.prefix)

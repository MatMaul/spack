# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Scorep(AutotoolsPackage):
    """The Score-P measurement infrastructure is a highly scalable and
    easy-to-use tool suite for profiling, event tracing, and online analysis
    of HPC applications.
    """

    homepage = "http://www.vi-hps.org/projects/score-p"
    url      = "http://www.vi-hps.org/cms/upload/packages/scorep/scorep-2.0.2.tar.gz"

    version('4.1',   '7bb6c1eecdd699b4a3207caf202866778ee01f15ff39a9ec198fcd872578fe63')
    version('4.0',   'f04478e0407d67eeb8c49c3c51d91e12')
    version('3.1',   '065bf8eb08398e8146c895718ddb9145')
    version('3.0',   '44da8beaa3f71436a5f6fe51938aab2f')
    version('2.0.2', '8f00e79e1b5b96e511c5ebecd10b2888')
    version('1.4.2', '3b9a042b13bdd5836452354e6567f71e')
    version('1.3',   '9db6f957b7f51fa01377a9537867a55c')

    patch('gcc7.patch', when='@:3')

    variant('mpi', default=True, description="Enable MPI support")
    variant('papi', default=True, description="Enable PAPI")
    variant('pdt', default=False, description="Enable PDT")
    variant('shmem', default=False, description='Enable shmem tracing')
    variant('gui', default=False, description='Depend on CubeGUI')

    # Dependencies for SCORE-P are quite tight. See the homepage for more
    # information. Starting with scorep 4.0 / cube 4.4, Score-P only depends on
    # two components of cube -- cubew and cubelib.

    # SCOREP 4
    depends_on('otf2@2.1:', when='@4:')
    depends_on('opari2@2.0:', when='@4:')
    depends_on('cubew@4.4:', when='@4:')
    depends_on('cubelib@4.4:', when='@4:')
    depends_on('cubegui@4.4:', when='@4: +gui')
    # SCOREP 3
    depends_on('otf2@2:', when='@3:3.99')
    depends_on('opari2@2:', when='@3:3.99')
    depends_on('cube@4.3:', when='@3:3.99')
    # SCOREP 2.0.2
    depends_on('otf2@2.0', when='@2.0.2')
    depends_on('opari2@2.0', when='@2.0.2')
    depends_on('cube@4.3:4.4', when='@2.0.2')
    # SCOREP 1.4.2
    depends_on('otf2@1.5:1.6', when='@1.4.2')
    depends_on('opari2@1.1.4', when='@1.4.2')
    depends_on('cube@4.3:4.4', when='@1.4.2')
    # SCOREP 1.3
    depends_on("otf2@1.4", when='@1.3')
    depends_on("opari2@1.1.4", when='@1.3')
    depends_on("cube@4.2.3", when='@1.3')

    depends_on("mpi", when='+mpi')
    depends_on("papi")
    depends_on("pdt", when="+pdt")

    # Score-P requires a case-sensitive file system, and therefore
    # does not work on macOS
    # https://github.com/spack/spack/issues/1609
    conflicts('platform=darwin')

    def configure_args(self):
        spec = self.spec

        config_args = [
            "--with-otf2=%s" % spec['otf2'].prefix.bin,
            "--with-opari2=%s" % spec['opari2'].prefix.bin,
            "--enable-shared"]

        if spec.satisfies("@4.0:"):
            config_args.extend([
                "--with-cubew=%s" % spec['cubew'].prefix.bin,
                "--with-cubelib=%s" % spec['cubelib'].prefix.bin,
                ])
        else:
            config_args.append("--with-cube=%s" % spec['cube'].prefix.bin)

        cname = spec.compiler.name
        config_args.append('--with-nocross-compiler-suite={0}'.format(cname))

        if "+papi" in spec:
            config_args.append("--with-papi-header=%s" %
                               spec['papi'].prefix.include)
            config_args.append("--with-papi-lib=%s" % spec['papi'].prefix.lib)

        if "+pdt" in spec:
            config_args.append("--with-pdt=%s" % spec['pdt'].prefix.bin)

        config_args += self.with_or_without('shmem')

        if '+mpi' in spec:
            if spec.satisfies('^intel-mpi'):
                config_args.append('--with-mpi=intel3')
            elif spec.satisfies('^mpich') or spec.satisfies('^mvapich2'):
                config_args.append('--with-mpi=mpich3')
            elif spec.satisfies('^openmpi'):
                config_args.append('--with-mpi=openmpi')
            elif spec.satisfies('^hpe-mpi'):
                config_args.append('--with-mpi=sgimpt')
            else:
                raise Exception('Unrecognized MPI library')

        if spec.satisfies('%gcc'):
            config_args.append('--with-nocross-compiler-suite=gcc')
        elif spec.satisfies('%intel'):
            config_args.append('--with-nocross-compiler-suite=intel')
        elif spec.satisfies('%pgi'):
            config_args.append('--with-nocross-compiler-suite=pgi')

        config_args.extend([
            'CFLAGS={0}'.format(self.compiler.pic_flag),
            'CXXFLAGS={0}'.format(self.compiler.pic_flag)
        ])

        if "+mpi" in spec:
            config_args.extend([
                'MPICC={0}'.format(spec['mpi'].mpicc),
                'MPICXX={0}'.format(spec['mpi'].mpicxx),
                'MPIF77={0}'.format(spec['mpi'].mpif77),
                'MPIFC={0}'.format(spec['mpi'].mpifc)
            ])

        return config_args

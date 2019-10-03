# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Brayns(CMakePackage):
    """Visualizer for large-scale and interactive ray-tracing of neurons"""

    homepage = "https://github.com/BlueBrain/Brayns"
    git = "https://github.com/BlueBrain/Brayns.git"
    generator = 'Ninja'

    version('develop', submodules=True)
    version('0.8.0', tag='0.8.0', submodules=True, preferred=True)
    version('1.0.0', tag='1.0.0', submodules=True)
    version('immersive', branch='videostreaming', submodules=True)

    variant('assimp', default=True, description='Build with assimp support')
    variant('ospray', default=True, description='Enable OSPRray engine')
    variant('deflect', default=True, description='Enable Deflect support')
    variant('brion', default=False, description='Build CircuitViewer support')
    variant('net', default=True, description='Enable web interface')
    variant('opendeck', default=False, description='Enable OpenDeck support')
    variant('viewer', default=True, description='Build braynsViewer app')
    variant('optix', default=False, description='Build Optix engine')
    variant('test', default=False, description='Enable extra tests')

    depends_on('cmake@3.1:', type='build')
    depends_on('ispc', type='build')
    depends_on('ninja', type='build')

    depends_on('assimp', when='+assimp')
    depends_on('bbptestdata', type='test', when='+test')
    depends_on('brion', when='+brion')
    depends_on('deflect ~deflect-qt', when='+deflect')
    depends_on('freeimage')
    depends_on('ffmpeg@4.2', when='+net')
    depends_on('glew', when='+viewer')
    depends_on('libarchive')
    depends_on('cgal')
    depends_on('libjpeg-turbo', when='+net')
    depends_on('libuv', when='+net')
    depends_on('opengl', when='+viewer')
    depends_on('ospray', when='+ospray')
    depends_on('rockets', when='+net')
    depends_on('vrpn', when='+opendeck')
    depends_on('optix@5.0.1', when='+optix')
    depends_on('cuda', when='+optix')

    def cmake_args(self):
        args = [
            '-DDISABLE_SUBPROJECTS=ON',
            '-DBRAYNS_ASSIMP_ENABLED={}'.format(
                'ON' if '+assimp' in self.spec else 'OFF'),
            '-DBRAYNS_OSPRAY_ENABLED={}'.format(
                'ON' if '+ospray' in self.spec else 'OFF'),
            '-DBRAYNS_CIRCUITEXPLORER_ENABLED={}'.format(
                'ON' if '+brion' in self.spec else 'OFF'),
            '-DBRAYNS_CIRCUITVIEWER_ENABLED={}'.format(
                'ON' if '+brion' in self.spec else 'OFF'),
            '-DBRAYNS_DTI_ENABLED={}'.format(
                'ON' if '+brion' in self.spec else 'OFF'),
            '-DBRAYNS_NETWORKING_ENABLED={}'.format(
                'ON' if '+net' in self.spec else 'OFF'),
            '-DBRAYNS_DEFLECT_ENABLED={}'.format(
                'ON' if '+deflect' in self.spec else 'OFF')
        ]

        if '+opendeck' in self.spec:
            args.append('-DBRAYNS_OPENDECK_ENABLED=ON')
            args.append('-DBRAYNS_VRPN_ENABLED=ON')
        if '+optix' in self.spec:
            args.append('-DBRAYNS_OPTIX_ENABLED=ON')
            args.append('-DBRAYNS_OPTIX_TESTS_ENABLED=ON')
        return args

    def check(self):
        with working_dir(self.build_directory):
            ninja('tests')

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            if '+optix' in self.spec:
                ninja('braynsOptixEngine')
            ninja()

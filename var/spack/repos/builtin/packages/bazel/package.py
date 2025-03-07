# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from multiprocessing import cpu_count
from spack.util.environment import env_flag
from spack.build_environment import SPACK_NO_PARALLEL_MAKE


class Bazel(Package):
    """Bazel is Google's own build tool"""

    homepage = "https://www.bazel.io"
    url = "https://github.com/bazelbuild/bazel/releases/download/0.11.1/bazel-0.11.1-dist.zip"

    version('0.19.2', '2f2d14a1f879a9ca17abdf9d9e5eee78')
    version('0.17.2', '9805c0593e781295126af6b8be8cc7a9')
    version('0.16.1', 'c333d903c5275286e79316eb19dd742d')
    version('0.15.0', 'fb6b928b62f068697bd66ad6d13aad53')
    version('0.14.1', '841900316b3ec9b996babe1c5b0b92e1')
    version('0.13.0', '64a5124025c1618b550faec64a9b6fa3')
    version('0.12.0', 'b5d67564ceecfe2005a885fe2ffe0da3')
    version('0.11.1', '80daac6b100b7f8e2b17d133150eba44')
    version('0.11.0', 'e6caf93a805b45c33367028e575b91dd')
    version('0.10.1', 'a7e5b9576993b752e31bd2d3259a14c5')
    version('0.10.0', 'c2f15b34255099d25e94fce7283e5cd2')
    version('0.9.0', '7fda74c163108f7c180bbc513bc8123b')
    version('0.4.5', '2b737be42678900470ae9e48c975ac5b2296d9ae23c007bf118350dbe7c0552b')
    version('0.4.4', '5e7c52b89071efc41277e2f0057d258f')
    version('0.3.1', '5c959467484a7fc7dd2e5e4a1e8e866b')
    version('0.3.0', '33a2cb457d28e1bee9282134769b9283')
    version('0.2.3', '393a491d690e43caaba88005efe6da91')
    version('0.2.2b', '75081804f073cbd194da1a07b16cba5f')
    version('0.2.2', '644bc4ea7f429d835e74f255dc1054e6')

    depends_on('java@8:', type=('build', 'link', 'run'))
    depends_on('zip')

    patch('fix_env_handling.patch', when='@:0.4.5')
    patch('fix_env_handling-0.9.0.patch', when='@0.9.0:0.12.0')
    patch('fix_env_handling-0.13.0.patch', when='@0.13.0:0.13.999')
    patch('fix_env_handling-0.17.2.patch', when='@0.14.0:')
    patch('link.patch')
    patch('cc_configure.patch', when='@:0.4.5')
    patch('unix_cc_configure.patch', when='@0.9.0')
    patch('unix_cc_configure-0.10.0.patch', when='@0.10.0:0.14.999')
    patch('unix_cc_configure-0.17.2.patch', when='@0.15.0:')

    def url_for_version(self, version):
        if version >= Version('0.4.1'):
            return 'https://github.com/bazelbuild/bazel/releases/download/{0}/bazel-{0}-dist.zip'.format(version)
        else:
            return 'https://github.com/bazelbuild/bazel/archive/{0}.tar.gz'.format(version)

    def install(self, spec, prefix):
        bash = which('bash')
        bash('-c', './compile.sh')
        mkdir(prefix.bin)
        install('output/bazel', prefix.bin)

    def setup_dependent_package(self, module, dependent_spec):
        class BazelExecutable(Executable):
            """Special callable executable object for bazel so the user can
               specify parallel or not on a per-invocation basis.  Using
               'parallel' as a kwarg will override whatever the package's
               global setting is, so you can either default to true or false
               and override particular calls.

               Note that if the SPACK_NO_PARALLEL_MAKE env var is set it
               overrides everything.
            """

            def __init__(self, name, command, jobs):
                super(BazelExecutable, self).__init__(name)
                self.bazel_command = command
                self.jobs = jobs

            def __call__(self, *args, **kwargs):
                disable = env_flag(SPACK_NO_PARALLEL_MAKE)
                parallel = ((not disable) and kwargs.get('parallel',
                                                         self.jobs > 1))

                jobs = "--jobs=1"
                if parallel:
                    jobs = "--jobs=%d" % self.jobs

                args = (self.bazel_command,) + (jobs,) + args

                return super(BazelExecutable, self).__call__(*args, **kwargs)

        jobs = cpu_count()
        if not dependent_spec.package.parallel:
            jobs = 1
        elif dependent_spec.package.make_jobs:
            jobs = dependent_spec.package.make_jobs
        module.bazel = BazelExecutable('bazel', 'build', jobs)

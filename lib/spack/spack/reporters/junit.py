# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import os.path
import re

import spack.build_environment
import spack.fetch_strategy
import spack.package
from spack.reporter import Reporter

__all__ = ['JUnit']


ANTI_ANSI = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')


class JUnit(Reporter):
    """Generate reports of spec installations for JUnit."""

    def __init__(self, install_command, cdash_upload_url):
        Reporter.__init__(self, install_command, cdash_upload_url)
        self.template_file = os.path.join('reports', 'junit.xml')

    def build_report(self, filename, report_data):
        # Write the report
        with open(filename, 'wb') as fd:
            env = spack.tengine.make_environment()
            template = env.get_template(self.template_file)
            formatted = template.render(report_data)
            # Pre-emptively remove all ANSI escape sequences
            fd.write(ANTI_ANSI.sub('', formatted.encode('utf-8')))

import glob
import logging
import nose
import os
import pkg_resources
import sys
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_raises, assert_rel_error

from vsp_wrapper import VSP

ORIG_DIR = os.getcwd()
VSP_PATH = '/home/setowns1/bin/vsp'


class TestCase(unittest.TestCase):
    """ Test VSP wrapper functionality. """

    directory = os.path.realpath(
        pkg_resources.resource_filename('vsp_wrapper', 'test'))

    def setUp(self):
        """ Called before each test in this class. """
        os.chdir(TestCase.directory)

    def tearDown(self):
        """ Remove output files. """
        for pattern in ('*.3dm', '*.bac', '*.bsf', '*.fel', '*.hrm', '*.log',
                        '*.new', '*.stl',
                        'bodyin.*', 'cfdmesh.*', 'comp_geom.*'):
            for name in glob.glob(pattern):
                os.remove(name)
        os.chdir(ORIG_DIR)

# VSP has problems with -compgeom even with original XML file.
    def test_777(self):
        logging.debug('')
        logging.debug('test_777')

        vsp = set_as_top(VSP('777.xml'))
        vsp.vsp_path = VSP_PATH

        vsp.comp_geom     = False
        vsp.write_xsec    = True
        vsp.write_felisa  = True
        vsp.write_stereo  = True
        vsp.write_rhino   = True
        vsp.write_nascart = False  # Can't write NASCART without comp_geom.

        vsp.run()

        # 'desired' from Linux, 'tolerance' for Mac/Windows.
        assert_rel_error(self, vsp.theoretical_area, 0, 0.0001)
        assert_rel_error(self, vsp.theoretical_volume, 0, 0.0001)
        assert_rel_error(self, vsp.wetted_area, 0, 0.0001)
        assert_rel_error(self, vsp.wetted_volume, 0, 0.0001)

    def test_cessna182(self):
        logging.debug('')
        logging.debug('test_cessna182')

        vsp = set_as_top(VSP('Cessna182.xml'))
        vsp.vsp_path = VSP_PATH

        vsp.comp_geom     = True
        vsp.write_xsec    = True
        vsp.write_felisa  = True
        vsp.write_stereo  = True
        vsp.write_rhino   = True
        vsp.write_nascart = True

        vsp.run()

        # 'desired' from Linux, 'tolerance' for Mac/Windows.
        assert_rel_error(self, vsp.theoretical_area, 849.669075, 0.0001)
        assert_rel_error(self, vsp.theoretical_volume, 303.350163, 0.0001)
        assert_rel_error(self, vsp.wetted_area, 713.083095, 0.0001)
        assert_rel_error(self, vsp.wetted_volume, 287.489547, 0.0001)

    def test_eagle_eye(self):
        logging.debug('')
        logging.debug('test_eagle_eye')

        vsp = set_as_top(VSP('eagle_eye.xml'))
        vsp.vsp_path = VSP_PATH

        vsp.comp_geom     = True
        vsp.write_xsec    = True
        vsp.write_felisa  = True
        vsp.write_stereo  = True
        vsp.write_rhino   = True
        vsp.write_nascart = True

        vsp.run()

        # 'desired' from Linux, 'tolerance' for Mac/Windows.
        assert_rel_error(self, vsp.theoretical_area, 374.888362, 0.0001)
        assert_rel_error(self, vsp.theoretical_volume, 104.646845, 0.0001)
        assert_rel_error(self, vsp.wetted_area, 277.323347, 0.0001)
        assert_rel_error(self, vsp.wetted_volume, 92.116985, 0.0001)

    def test_ge90(self):
        logging.debug('')
        logging.debug('test_ge90')

        vsp = set_as_top(VSP('GE90.xml'))
        vsp.vsp_path = VSP_PATH

        vsp.comp_geom     = True
        vsp.write_xsec    = True
        vsp.write_felisa  = True
        vsp.write_stereo  = True
        vsp.write_rhino   = True
        vsp.write_nascart = True

        vsp.run()

        # 'desired' from Linux, 'tolerance' for Mac/Windows.
        assert_rel_error(self, vsp.theoretical_area, 2043.568902, 0.0001)
        assert_rel_error(self, vsp.theoretical_volume, 1031.974785, 0.0001)
        assert_rel_error(self, vsp.wetted_area, 1894.494077, 0.0001)
        assert_rel_error(self, vsp.wetted_volume, 979.795926, 0.0001)

    def test_schweizer2_32(self):
        logging.debug('')
        logging.debug('test_schweizer2_32777')

        vsp = set_as_top(VSP('Schweizer2_32.xml'))
        vsp.vsp_path = VSP_PATH

        vsp.comp_geom     = True
        vsp.write_xsec    = True
        vsp.write_felisa  = True
        vsp.write_stereo  = True
        vsp.write_rhino   = True
        vsp.write_nascart = True

        vsp.run()

        # 'desired' from Linux, 'tolerance' for Mac/Windows.
        assert_rel_error(self, vsp.theoretical_area, 688.442371, 0.0001)
        assert_rel_error(self, vsp.theoretical_volume, 177.148284, 0.0001)
        assert_rel_error(self, vsp.wetted_area, 590.724803, 0.0001)
        assert_rel_error(self, vsp.wetted_volume, 155.390161, 0.0001)

    def test_hwb(self):
        logging.debug('')
        logging.debug('test_hwb')

        vsp = set_as_top(VSP('hwb.xml'))
        vsp.vsp_path = VSP_PATH

        vsp.generate_cfd_mesh = True
        vsp.geometry.cfd_mesh_base_length = 0.4

        vsp.comp_geom    = True
        vsp.write_xsec   = True
        vsp.write_felisa = True
        vsp.write_stereo = True
        vsp.write_rhino  = True

        vsp.run()

        # 'desired' from Linux, 'tolerance' for Mac/Windows.
        assert_rel_error(self, vsp.theoretical_area, 647.158638, 0.0001)
        assert_rel_error(self, vsp.theoretical_volume, 122.884067, 0.0001)
        assert_rel_error(self, vsp.wetted_area, 608.236512, 0.0001)
        assert_rel_error(self, vsp.wetted_volume, 121.853274, 0.0001)

#FIXME: this should probably work.
# VSP has problems with -compgeom even with original XML file.
    def test_m6_singleside(self):
        logging.debug('')
        logging.debug('test_m6_singleside')

        vsp = VSP(xml_filename='m6_singleside.xml')
        vsp.vsp_path = VSP_PATH

        vsp.comp_geom     = False
        vsp.write_xsec    = True
        vsp.write_felisa  = True
        vsp.write_stereo  = True
        vsp.write_rhino   = True
        vsp.write_nascart = False  # Can't write NASCART without comp_geom.

        vsp.run()

        # 'desired' from Linux, 'tolerance' for Mac/Windows.
        assert_rel_error(self, vsp.theoretical_area, 0, 0.0001)
        assert_rel_error(self, vsp.theoretical_volume, 0, 0.0001)
        assert_rel_error(self, vsp.wetted_area, 0, 0.0001)
        assert_rel_error(self, vsp.wetted_volume, 0, 0.0001)

    def test_collision(self):
        logging.debug('')
        logging.debug('test_collision')

        vsp = set_as_top(VSP('hwb.xml'))

        vsp.generate_cfd_mesh = True
        vsp.write_nascart = True

        msg = ': CFD meshing and NASCART output use the same output filenames'
        assert_raises(self, 'vsp.run()', globals(), locals(), RuntimeError, msg)


if __name__ == '__main__':
    sys.argv.append('--cover-package=vsp_wrapper.')
    sys.argv.append('--cover-erase')
    nose.runmodule()


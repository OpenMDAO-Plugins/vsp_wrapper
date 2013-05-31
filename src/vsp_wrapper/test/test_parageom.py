import logging
import nose
import os
import sys
import shutil
import tempfile
import unittest

from openmdao.main.api import set_as_top
from openmdao.main.component import SimulationRoot
from openmdao.util.testutil import assert_raises, assert_rel_error
from openmdao.lib.components.geomcomp import GeomComponent
from openmdao.util.fileutil import onerror

import vsp_wrapper
from vsp_wrapper import VSPParametricGeometry

VSP_PATH = 'vsp'
TESTDIR = os.path.join(os.path.dirname(os.path.abspath(vsp_wrapper.__file__)), 'test')

class TestCase(unittest.TestCase):
    """ Test VSP wrapper functionality. """

    def setUp(self):
        self.startdir = os.getcwd()
        self.tdir = tempfile.mkdtemp()
        os.chdir(self.tdir)
        SimulationRoot.chroot(self.tdir)

    def tearDown(self):
        try:
            shutil.rmtree(self.tdir, onerror=onerror)
        except:
            pass
        finally:
            os.chdir(self.startdir)
            SimulationRoot.chroot(os.getcwd())

# VSP has problems with -compgeom even with original XML file.
    def test_777(self):
        logging.debug('')
        logging.debug('test_777')

        g = set_as_top(GeomComponent())
        g.add("parametric_geometry", VSPParametricGeometry())
        g.parametric_geometry.model_file = os.path.join(TESTDIR, '777.xml')

        g.vsp_path = VSP_PATH
        g.comp_geom     = False
        g.run()

        # 'desired' from Linux, 'tolerance' for Mac/Windows.
        assert_rel_error(self, g.theoretical_area, 0, 0.0001)
        assert_rel_error(self, g.theoretical_volume, 0, 0.0001)
        assert_rel_error(self, g.wetted_area, 0, 0.0001)
        assert_rel_error(self, g.wetted_volume, 0, 0.0001)

    def test_cessna182(self):
        logging.debug('')
        logging.debug('test_cessna182')

        logging.debug(os.getcwd())

        g = set_as_top(GeomComponent())
        g.add("parametric_geometry", VSPParametricGeometry())
        g.parametric_geometry.model_file = os.path.join(TESTDIR, 'Cessna182.vsp')

        g.vsp_path = VSP_PATH
        g.comp_geom     = True
        g.run()

        # 'desired' from Linux, 'tolerance' for Mac/Windows.
        assert_rel_error(self, g.theoretical_area, 849.669075, 0.0005)
        assert_rel_error(self, g.theoretical_volume, 303.350163, 0.002)
        assert_rel_error(self, g.wetted_area, 713.083095, 0.0005)
        assert_rel_error(self, g.wetted_volume, 287.489547, 0.002)

    def test_eagle_eye(self):
        logging.debug('')
        logging.debug('test_eagle_eye')

        g = set_as_top(GeomComponent())
        g.add("parametric_geometry", VSPParametricGeometry())
        g.parametric_geometry.model_file = os.path.join(TESTDIR, 'eagle_eye.xml')
        g.vsp_path = VSP_PATH
        g.comp_geom     = True
        g.run()

        # 'desired' from Linux, 'tolerance' for Mac/Windows.
        assert_rel_error(self, g.theoretical_area, 374.888362, 0.0007)
        assert_rel_error(self, g.theoretical_volume, 104.646845, 0.002)
        assert_rel_error(self, g.wetted_area, 277.323347, 0.0006)
        assert_rel_error(self, g.wetted_volume, 92.116985, 0.002)

    def test_ge90(self):
        logging.debug('')
        logging.debug('test_ge90')

        g = set_as_top(GeomComponent())
        g.add("parametric_geometry", VSPParametricGeometry())
        g.parametric_geometry.model_file = os.path.join(TESTDIR, 'GE90.xml')        
        g.vsp_path = VSP_PATH
        g.comp_geom     = True
        g.run()

        # 'desired' from Linux, 'tolerance' for Mac/Windows.
        assert_rel_error(self, g.theoretical_area, 2043.568902, 0.001)
        assert_rel_error(self, g.theoretical_volume, 1031.974785, 0.0003)
        assert_rel_error(self, g.wetted_area, 1894.494077, 0.005)
        assert_rel_error(self, g.wetted_volume, 979.795926, 0.002)

    def test_schweizer2_32(self):
        logging.debug('')
        logging.debug('test_schweizer2_32777')

        g = set_as_top(GeomComponent())
        g.add("parametric_geometry", VSPParametricGeometry())
        g.parametric_geometry.model_file = os.path.join(TESTDIR, 'Schweizer2_32.xml')        
        g.vsp_path = VSP_PATH

        g.comp_geom     = True
        g.run()

        # 'desired' from Linux, 'tolerance' for Mac/Windows.
        assert_rel_error(self, g.theoretical_area, 688.442371, 0.0003)
        assert_rel_error(self, g.theoretical_volume, 177.148284, 0.0009)
        assert_rel_error(self, g.wetted_area, 590.724803, 0.0003)
        assert_rel_error(self, g.wetted_volume, 155.390161, 0.0009)

    def test_hwb(self):
        logging.debug('')
        logging.debug('test_hwb')

        g = set_as_top(GeomComponent())
        g.add("parametric_geometry", VSPParametricGeometry())
        g.parametric_geometry.model_file = os.path.join(TESTDIR, 'hwb.xml')        
        g.vsp_path = VSP_PATH

        g.comp_geom    = True

        g.run()

        # 'desired' from Linux, 'tolerance' for Mac/Windows.
        assert_rel_error(self, g.theoretical_area, 647.158638, 0.0001)
        assert_rel_error(self, g.theoretical_volume, 122.884067, 0.0001)
        assert_rel_error(self, g.wetted_area, 608.236512, 0.0001)
        assert_rel_error(self, g.wetted_volume, 121.853274, 0.0001)

#FIXME: this should probably work.
# VSP has problems with -compgeom even with original XML file.
    def test_m6_singleside(self):
        logging.debug('')
        logging.debug('test_m6_singleside')

        g = set_as_top(GeomComponent())
        g.add("parametric_geometry", VSPParametricGeometry())
        g.parametric_geometry.model_file = os.path.join(TESTDIR, 'm6_singleside.xml')        
        g.vsp_path = VSP_PATH
        g.comp_geom     = False
        g.run()

        # 'desired' from Linux, 'tolerance' for Mac/Windows.
        assert_rel_error(self, g.theoretical_area, 0, 0.0001)
        assert_rel_error(self, g.theoretical_volume, 0, 0.0001)
        assert_rel_error(self, g.wetted_area, 0, 0.0001)
        assert_rel_error(self, g.wetted_volume, 0, 0.0001)

    def test_collision(self):
        logging.debug('')
        logging.debug('test_collision')

        g = set_as_top(GeomComponent())
        g.add("parametric_geometry", VSPParametricGeometry())
        g.parametric_geometry.model_file = os.path.join(TESTDIR, 'hwb.xml')        
        g.vsp_path = VSP_PATH

        g.generate_cfd_mesh = True
        g.write_nascart = True

        msg = ': CFD meshing and NASCART output use the same output filenames'
        assert_raises(self, 'g.run()', globals(), locals(), Exception, msg)


if __name__ == '__main__':
    sys.argv.append('--cover-package=vsp_wrapper.')
    sys.argv.append('--cover-erase')
    nose.runmodule()


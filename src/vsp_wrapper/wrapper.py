import csv
import os.path
import xml.etree.cElementTree as ElementTree

from openmdao.main.api import FileMetadata, set_as_top
from openmdao.lib.datatypes.api import Bool, Float, Int, Str
from openmdao.lib.components.external_code import ExternalCode

from vsp_wrapper.geometry import VSPGeometry


class VSP(ExternalCode):
    """
    A file wrapper which exposes VSP XML parameters and executes VSP to
    perform one or more operations.
    """

    vsp_path = Str('vsp', iotype='in',
                   desc='Path to the VSP executable.')

    xml_filename = Str('VspAircraft.xml', iotype='in',
                       desc='Path to the base VSP XML file.')

    comp_geom = Bool(False, iotype='in',
                     desc='Compute areas and volumes.')

    generate_cfd_mesh = Bool(False, iotype='in',
                             desc='Generate CFD mesh in STL and NASCART files.')

    slice = Bool(False, iotype='in', desc='')
    num_slices = Int(iotype='in', desc='')
    mach = Float(iotype='in', desc='')
    cone_sections = Int(iotype='in', desc='')

    write_xsec = Bool(False, iotype='in', desc='Write Herm (Vorview format) file.')
    write_felisa = Bool(False, iotype='in', desc='Write Felisa files.')
    write_stereo = Bool(False, iotype='in', desc='Write Stereolith file.')
    write_rhino = Bool(False, iotype='in', desc='Write Rhino3D file.')
    write_nascart = Bool(False, iotype='in', desc='Write Nascart file.')
    write_tecplot = Bool(False, iotype='in', desc='Write Tecplot file.')
    write_stecplot = Bool(False, iotype='in', desc='Write structured Tecplot file.')

    theoretical_area = Float(iotype='out', desc='Total area of all parts.')
    wetted_area = Float(iotype='out', desc='Total external area.')
    theoretical_volume = Float(iotype='out', desc='Total volume of all parts.')
    wetted_volume = Float(iotype='out', desc='Total internal volume.')

    def __init__(self, xml_filename, *args, **kwargs):
        super(VSP, self).__init__(*args, **kwargs)
        self.xml_filename = xml_filename
        self.add('geometry', VSPGeometry())
        self._etree = None

    def configure(self):
        """ If specified, read XML file. """
        super(VSP, self).configure()
        self.external_files = []

        if self.xml_filename:
            self.read_input(self.xml_filename)
            self.external_files.append(
                 FileMetadata(path=self.xml_filename, input=True,
                              desc='VSP XML file.'))

    def execute(self):
        """ Execute VSP to perform one or more operations. """
        if self.generate_cfd_mesh and self.write_nascart:
            self.raise_exception('CFD meshing and NASCART output use the same'
                                 ' output filenames', RuntimeError)

        # Write XML input file.
        filename = os.path.basename(self.xml_filename)
        if filename.endswith('.xml'):
            base_filename = filename[:-4]
        else:
            base_filename = filename
        filename += '.new'
        self.write_input(filename)

        # Determine command line and output files.
        cmd = [self.vsp_path, '-batch', filename]
        output_files = []

        if self.comp_geom:
            cmd.append('-compgeom')
            output_files.extend(('compgeom.txt', 'comp_geom.csv'))

        if self.generate_cfd_mesh:
            cmd.append('-cfdmesh')
            output_files.extend(('bodyin.dat', 'bodyin.key',
                                 'cfdmesh.bez', 'cfdmesh.stl'))
        if self.slice:
            cmd.extend(['-slice', str(self.num_slices),
                        str(self.mach), str(self.cone_sections)])

        if self.write_xsec:
            cmd.append('-xsec')
            output_files.append('%s.hrm' % base_filename)

        if self.write_felisa:
            cmd.append('-felisa')
            for ext in ('fel', 'bsf', 'bac'):
                output_files.append('%s.%s' % (base_filename, ext))

        if self.write_stereo:
            cmd.append('-stereo')
            output_files.append('%s.stl' % base_filename)

        if self.write_rhino:
            cmd.append('-rhino')
            output_files.append('%s.3dm' % base_filename)

        if self.write_nascart:
            cmd.append('-nascart')
            output_files.extend(('bodyin.dat', 'bodyin.key'))

        if self.write_tecplot:
            cmd.append('-tecplot')

        if self.write_stecplot:
            cmd.append('-stecplot')

        for name in output_files:
            if os.path.exists(name):
                os.remove(name)

        # Run VSP.
        self.command = cmd
        self.stdout = os.path.basename(self.xml_filename)+'.log'
        self.stderr = ExternalCode.STDOUT
        super(VSP, self).execute()

        # Read last line of -compgeom output.
        if self.comp_geom:
            reader = csv.reader(open('comp_geom.csv', 'r'))
            row = []
            for row in reader:
                pass
            if len(row) == 5:
                self.theoretical_area = float(row[1])
                self.wetted_area = float(row[2])
                self.theoretical_volume = float(row[3])
                self.wetted_volume = float(row[4])
            else:
                self.raise_exception('comp_geom.csv invalid', RuntimeError)
        else:
            self.theoretical_area = 0
            self.wetted_area = 0
            self.theoretical_volume = 0
            self.wetted_volume = 0

        # Check CFD meshing if requested.
        if self.generate_cfd_mesh:
            mesh_ok = False
            with open(self.stdout, 'r') as out:
                for line in out:
                    if 'Mesh Complete' in line:
                        mesh_ok = True
                        break
            if not mesh_ok:
                self.raise_exception('Meshing failed', RuntimeError)

    def read_input(self, filename=None):
        """ Read XML file. """
        filename = filename or self.xml_filename
        with self.dir_context:
            self._etree = ElementTree.parse(filename)
            self.geometry.read(self._etree.getroot())

    def write_input(self, filename=None):
        """ Write XML file. """
        root = self.geometry.write(None)
        etree = ElementTree.ElementTree(root)
        filename = filename or self.xml_filename
        with self.dir_context:
            with open(filename, 'w') as out:
                out.write('<?xml version="1.0"?>\n')
                etree.write(out)


from openmdao.lib.datatypes.api import Float, Int, Str

from vsp_wrapper.xml_container import XMLContainer

# Source types.
_POINT_SOURCE = 0
_LINE_SOURCE  = 1
_BOX_SOURCE   = 2


class BaseSource(XMLContainer):
    """ Base class for CFD meshing source objects. """

    XMLTAG = 'CFD_Mesh_Source'

    source_name = Str('Default_Name', iotype='in', xmltag='Name',
                      desc='Name of this source.')
    type = Int(iotype='in', xmltag='Type', desc='Type of meshing source.')
    radius = Float(0.0, iotype='in', xmltag='Rad', desc='Radius of influence.')
    length = Float(0.0, iotype='in', xmltag='Len', desc='Target edge length.')

    def __init__(self):
        super(BaseSource, self).__init__(self.XMLTAG)

    @staticmethod
    def create(element):
        """ Create a source object of the type specified in `element`. """
        typ = int(element.findtext('Type'))
        if typ == _POINT_SOURCE:
            return PointSource()
        elif typ == _LINE_SOURCE:
            return LineSource()
        elif typ == _BOX_SOURCE:
            return BoxSource()
        raise ValueError("Invalid source type '%s'" % typ)


class PointSource(BaseSource):
    """ CFD meshing point source. """

    u = Float(iotype='in', xmltag='U', desc='')
    w = Float(iotype='in', xmltag='W', desc='')


class LineSource(BaseSource):
    """ CFD meshing line source. """

    u1 = Float(iotype='in', xmltag='U1', desc='')
    w1 = Float(iotype='in', xmltag='W1', desc='')
    u2 = Float(iotype='in', xmltag='U2', desc='')
    w2 = Float(iotype='in', xmltag='W2', desc='')


class BoxSource(BaseSource):
    """ CFD meshing box source. """

    u1 = Float(iotype='in', xmltag='U1', desc='')
    w1 = Float(iotype='in', xmltag='W1', desc='')
    u2 = Float(iotype='in', xmltag='U2', desc='')
    w2 = Float(iotype='in', xmltag='W2', desc='')


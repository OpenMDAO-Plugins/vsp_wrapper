from openmdao.lib.datatypes.api import Bool, Enum, Float, Int

from vsp_wrapper.component     import VSPComponent
from vsp_wrapper.xml_container import XMLContainer

# External store types.
_BOMB_TYPE       = 0
_MISSLE_TYPE     = 1
_TANK_TYPE       = 2
_FIXED_TANK_TYPE = 3


class External(VSPComponent):
    """ An external store (bomb, missile, tank). """

    XMLTYPE = 'External'

    def __init__(self):
        super(External, self).__init__()
        self.add('external_parms', ExternalParms())

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(External, self).read(this)

        parms = this.find(ExternalParms.XMLTAG)
        if parms is None:
            self.raise_exception('No %s element!?' % ExternalParms.XMLTAG)
        self.external_parms.read(parms)

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(External, self).write(parent, nesting)
        self.external_parms.write(this, nesting+1)
        return this


class ExternalParms(XMLContainer):
    """ XML parameters specific to an 'external'. """

    XMLTAG = 'External_Parms'

    external_type = Enum(_MISSLE_TYPE, iotype='in', xmltag='External_Type',
                         values=(_BOMB_TYPE, _MISSLE_TYPE, _TANK_TYPE,
                                 _FIXED_TANK_TYPE),
                         aliases=('Bomb', 'Missile', 'Tank', 'Fixed Tank'),
                         desc='Type of external store.')
    length = Float(6.5, low=0.1, high=100., iotype='in', xmltag='Length',
                   desc='Store length.')
    fine_ratio = Float(15.0, low=2., high=50., iotype='in',
                       xmltag='Finess_Ratio', desc='')
    drag = Float(0.01, low=0., high=100., iotype='in', xmltag='Drag',
                 desc='Equivalent flat plate drag of store.')

    pylon = Bool(True, iotype='in', xmltag='Pylon_Flag',
                 desc='If True, include pylon.')
    pylon_height = Float(0.35, low=0.001, high=20., iotype='in',
                         xmltag='Pylon_Height', desc='Height of pylon.')
    pylon_drag = Float(0.01, low=0., high=100., iotype='in', xmltag='Pylon_Drag',
                       desc='Equivalent flat plat drag of pylon.')

    def __init__(self):
        super(ExternalParms, self).__init__(self.XMLTAG)


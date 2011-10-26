from openmdao.lib.datatypes.api import Bool, Float

from vsp_wrapper.component     import VSPComponent
from vsp_wrapper.xml_container import XMLContainer


class Blank(VSPComponent):
    """ A parent for inserted/grouped parts. """

    XMLTYPE = 'Blank'

    def __init__(self):
        super(Blank, self).__init__()
        self.add('blank_parms', BlankParms())

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(Blank, self).read(this)

        parms = this.find(BlankParms.XMLTAG)
        if parms is not None:
            self.blank_parms.read(parms)
        else:  # Must be an older version file.
            self._logger.warning('No %s element' % BlankParms.XMLTAG)

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(Blank, self).write(parent, nesting)
        self.blank_parms.write(this, nesting+1)
        return this


class BlankParms(XMLContainer):
    """ XML parameters specific to a 'blank'. """

    XMLTAG = 'Blank_Parms'

    point_mass_flag = Bool(False, iotype='in', xmltag='PointMassFlag',
                           desc='')
    point_mass = Float(1.0, iotype='in', xmltag='PointMass',
                       desc='')

    def __init__(self):
        super(BlankParms, self).__init__(self.XMLTAG)


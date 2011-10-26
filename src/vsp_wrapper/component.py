from openmdao.lib.datatypes.api import Str

from vsp_wrapper.general       import GeneralParms
from vsp_wrapper.xml_container import XMLContainer


class VSPComponent(XMLContainer):
    """ Base XML parameters for a VSP component/part. """

    XMLTAG = 'Component'

    type = Str(iotype='out', xmltag='Type',
               desc='Type name for this component.')

    def __init__(self):
        super(VSPComponent, self).__init__(self.XMLTAG)
        self.add('general_parms', GeneralParms())

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(VSPComponent, self).read(this)
        parms = this.find('General_Parms')
        if parms is not None:  # No general parameters for 'User' component.
            self.general_parms.read(parms)

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(VSPComponent, self).write(parent, nesting)
        if self.type != 'User':
            self.general_parms.write(this, nesting+1)
        return this


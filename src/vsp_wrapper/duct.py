from openmdao.lib.datatypes.api import Float

from vsp_wrapper.airfoil       import Airfoil
from vsp_wrapper.component     import VSPComponent
from vsp_wrapper.xml_container import XMLContainer


class Duct(VSPComponent):
    """ A duct. """

    XMLTYPE = 'Duct'

    def __init__(self):
        super(Duct, self).__init__()
        self.add('duct_parms', DuctParms())
        self.add('airfoil', Airfoil())

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(Duct, self).read(this)

        parms = this.find(DuctParms.XMLTAG)
        if parms is None:
            self.raise_exception('No %s element!?' % DuctParms.XMLTAG)
        self.duct_parms.read(parms)

        parms = this.find(Airfoil.XMLTAG)
        if parms is None:
            self.raise_exception('No %s element!?' % Airfoil.XMLTAG)
        self.airfoil.read(parms)

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(Duct, self).write(parent, nesting)

        self.duct_parms.write(this, nesting+1)
        self.airfoil.write(this, nesting+1)

        return this


class DuctParms(XMLContainer):
    """ XML parameters specific to a duct. """

    XMLTAG = 'Duct_Parms'

    length = Float(5., low=0.001, high=10000.0, iotype='in',
                   xmltag='Length', desc='')
    chord = Float(5., low=0.001, high=10000., iotype='in',
                  xmltag='Chord', desc='')
    inlet_dia = Float(10., low=0.001, high=1000000., iotype='in',
                      xmltag='Inlet_Dia', desc='')
    inlet_area = Float(10., low=0.001, high=1000000., iotype='in',
                       xmltag='Inlet_Area', desc='')
    outlet_dia = Float(10., low=0.001, high=1000000., iotype='in',
                       xmltag='Outlet_Dia', desc='')
    outlet_area = Float(10., low=0.001, high=1000000., iotype='in',
                        xmltag='Outlet_Area', desc='')
    inlet_outlet = Float(1., low=0.1, high=10., iotype='in',
                         xmltag='Inlet_Outlet', desc='')

    def __init__(self):
        super(DuctParms, self).__init__(self.XMLTAG)


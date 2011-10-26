from openmdao.lib.datatypes.api import Bool, Float, Int

from vsp_wrapper.airfoil       import Airfoil
from vsp_wrapper.component     import VSPComponent
from vsp_wrapper.xml_container import XMLContainer


class Prop(VSPComponent):
    """ A propeller. """

    XMLTYPE = 'Prop'

    def __init__(self):
        super(Prop, self).__init__()
        self.add('prop_parms', PropParms())

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(Prop, self).read(this)

        parms = this.find(PropParms.XMLTAG)
        if parms is None:
            self.raise_exception('No %s element!?' % PropParms.XMLTAG)
        self.prop_parms.read(parms)

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(Prop, self).write(parent, nesting)
        self.prop_parms.write(this, nesting+1)
        return this


class PropParms(XMLContainer):
    """ XML parameters specific to a propeller. """

    XMLTAG = 'Prop_Parms'

    num_blades = Int(4, low=1, iotype='in', xmltag='NumBlades',
                     desc='')
    smooth_flag = Bool(True, iotype='in', xmltag='SmoothFlag',
                       desc='')
    num_u = Int(3, low=1, iotype='in', xmltag='NumU',
                desc='')
    num_w = Int(1, low=1, iotype='in', xmltag='NumW',
                desc='')
    diameter = Float(4., low=0.01, high=1000., iotype='in', xmltag='Diameter',
                     desc='')
    cone_angle = Float(0., low=-45., high=45., units='deg', iotype='in',
                       xmltag='ConeAngle', desc='')
    pitch = Float(0., low=-180., high=180., units='deg', iotype='in',
                  xmltag='Pitch', desc='')

    def __init__(self):
        super(PropParms, self).__init__(self.XMLTAG)
        self._stations = []

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(PropParms, self).read(this)

        stations = this.findall(SectParms.XMLTAG)
        for i, element in enumerate(stations):
            name = 'station_%d' % i
            section = self.add(name, SectParms())
            section.read(element)
            self._stations.append(section)

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(PropParms, self).write(parent, nesting)

        for station in self._stations:
            station.write(this, nesting+2)

        return this


class SectParms(XMLContainer):
    """ XML parameters specific to a propeller blade section. """

    XMLTAG = 'Sect_Parms'

    x_off = Float(low=0., iotype='in', xmltag='X_Off',
                  desc='Location X/R.')
    y_off = Float(low=-1., high=1., iotype='in', xmltag='Y_Off',
                  desc='Offset Y/R.')
    chord = Float(low=0.01, high=2., iotype='in', xmltag='Chord',
                  desc='Chord C/R.')
    twist = Float(iotype='in', xmltag='Twist',
                  desc='')

    def __init__(self):
        super(SectParms, self).__init__(self.XMLTAG)
        self.add('airfoil', Airfoil())

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(SectParms, self).read(this)

        airfoil = this.find(Airfoil.XMLTAG)
        if airfoil is None:
            self.raise_exception('No %s element!?' % Airfoil.XMLTAG)
        self.airfoil.read(airfoil)

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(SectParms, self).write(parent, nesting)
        self.airfoil.write(this, nesting+1)
        return this


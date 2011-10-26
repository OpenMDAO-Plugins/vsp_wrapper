import xml.etree.cElementTree as ElementTree

from openmdao.lib.datatypes.api import Bool, Float, Int

from vsp_wrapper.airfoil       import Airfoil
from vsp_wrapper.component     import VSPComponent
from vsp_wrapper.wing_sect     import WingSect
from vsp_wrapper.xml_container import XMLContainer


class MSWing(VSPComponent):
    """ Multi-Section Wing. """

    XMLTYPE = 'Mswing'

    def __init__(self):
        super(MSWing, self).__init__()
        self.add('wing_parms', MSWingParms())
        self._airfoils = []
        self._sections = []

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(MSWing, self).read(this)

        parms = this.find(MSWingParms.XMLTAG)
        if parms is None:
            self.raise_exception('No %s element!?' % MSWingParms.XMLTAG)
        self.wing_parms.read(parms)

        airfoil_list = this.find('Airfoil_List')
        if airfoil_list is None:
            self.raise_exception('No Airfoil_List!?', RuntimeError)
        airfoils = airfoil_list.findall(Airfoil.XMLTAG)
        for i, element in enumerate(airfoils):
            name = '%s_%d' % (Airfoil.XMLTAG, i)
            airfoil = self.add(name, Airfoil())
            airfoil.read(element)
            self._airfoils.append(airfoil)

        section_list = this.find('Section_List')
        if section_list is None:
            self.raise_exception('No Section_List!?', RuntimeError)
        sections = section_list.findall(WingSect.XMLTAG)
        for i, element in enumerate(sections):
            name = '%s_%d' % (WingSect.XMLTAG, i)
            section = self.add(name, WingSect())
            section.read(element)
            self._sections.append(section)

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(MSWing, self).write(parent, nesting)

        self.wing_parms.write(this, nesting+1)

        airfoil_list = ElementTree.Element('Airfoil_List')
        airfoil_list.text = self.tail(nesting+2)
        airfoil_list.tail = self.tail(nesting+1)
        for airfoil in self._airfoils:
            airfoil.write(airfoil_list, nesting+2)
        this.append(airfoil_list)

        section_list = ElementTree.Element('Section_List')
        section_list.text = self.tail(nesting+2)
        section_list.tail = self.tail(nesting+1)
        for section in self._sections:
            section.write(section_list, nesting+2)
        this.append(section_list)

        return this


class MSWingParms(XMLContainer):
    """ XML parameters specific to a Multi-Section Wing. """

    XMLTAG = 'Mswing_Parms'

    total_span = Float(low=0.1, high=10000., iotype='in', xmltag='Total_Span',
                       desc='')
    total_proj_span = Float(low=0.1, high=10000., iotype='in',
                            xmltag='Total_Proj_Span',
                            desc='')
    avg_chord = Float(low=0.1, high=10000., iotype='in', xmltag='Avg_Chord',
                      desc='Average chord.')
    total_area = Float(low=1., high=1000000., iotype='in', xmltag='Total_Area',
                       desc='')
    sweep_off = Float(iotype='in', xmltag='Sweep_Off',
                      desc='Sweep offset.')
    rounded_tips = Bool(False, iotype='in', xmltag='Round_End_Cap_Flag',
                        desc='')

    deg_per_seg = Int(9, low=1, high=30, units='deg', iotype='in',
                      xmltag='Deg_Per_Seg',
                      desc='Degrees per segment in blend.')
    max_num_segs = Int(iotype='in', xmltag='Max_Num_Seg',
                       desc='Max number of segments in blend.')
    rel_dihedral_flag = Bool(False, iotype='in', xmltag='Rel_Dihedral_Flag',
                             desc='')
    rel_twist_flag = Bool(False, iotype='in', xmltag='Rel_Twist_Flag',
                          desc='')

    def __init__(self):
        super(MSWingParms, self).__init__(self.XMLTAG)


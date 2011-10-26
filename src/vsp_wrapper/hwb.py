import xml.etree.cElementTree as ElementTree

from openmdao.lib.datatypes.api import Float, List

from vsp_wrapper.airfoil       import Airfoil
from vsp_wrapper.component     import VSPComponent
from vsp_wrapper.wing_sect     import WingSect
from vsp_wrapper.xml_container import XMLContainer


class HWB(VSPComponent):
    """ A hybrid wing-body aircraft. """

    XMLTYPE = 'Hwb'

    section_size = List(int, iotype='in',
                        desc='')
    sweep_percent_length = List(float, iotype='in',
                                desc='Sweep percent span of fillet.')
    te_sweep_percent_length = List(float, iotype='in',
                                   desc='TE sweep percent span of fillet.')
    dihedral_percent_length = List(float, iotype='in',
                                   desc='Dihedral percent span of fillet.')
    sweep_deg_per_seg = List(float, units='deg', iotype='in',
                             desc='Sweep degrees per section of fillet.')
    te_sweep_deg_per_seg = List(float, units='deg', iotype='in',
                                desc='TE sweep degrees per section of fillet.')
    dihedral_deg_per_seg = List(float, units='deg', iotype='in',
                                desc='Dihedral degrees per section of fillet.')
    
    def __init__(self):
        super(HWB, self).__init__()
        self.add('hwb_parms', HWBParms())
        self._airfoils = []
        self._sections = []

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(HWB, self).read(this)

        parms = this.find(HWBParms.XMLTAG)
        if parms is None:
            self.raise_exception('No %s element!?' % HWBParms.XMLTAG)
        self.hwb_parms.read(parms)

        airfoil_list = this.find('Airfoil_List')
        if airfoil_list is None:
            self.raise_exception('No Airfoil_List!?', RuntimeError)
        airfoils = airfoil_list.findall(Airfoil.XMLTAG)
        for i, element in enumerate(airfoils):
            name = '%s_%d' % (Airfoil.XMLTAG, i)
            airfoil = self.add(name, Airfoil())
            airfoil.read(element)
            self._airfoils.append(airfoil)

        self.section_size = \
            self._read_list(this, 'Section_Sizes_List', 'Section_Size', int)

        self.sweep_percent_length = \
            self._read_list(this, 'Sweep_Percent_Lengths_List',
                            'Percent_Length')

        self.te_sweep_percent_length = \
            self._read_list(this, 'TESweep_Percent_Lengths_List',
                            'Percent_Length')

        self.dihedral_percent_length = \
            self._read_list(this, 'Dihedral_Percent_Lengths_List',
                            'Percent_Length')

        self.sweep_deg_per_seg = \
            self._read_list(this, 'Sweep_DegPerSeg_List', 'DegPerSeg')

        self.te_sweep_deg_per_seg = \
            self._read_list(this, 'TESweep_DegPerSeg_List', 'DegPerSeg')

        self.dihedral_deg_per_seg = \
            self._read_list(this, 'Dihedral_DegPerSeg_List', 'DegPerSeg')

        section_list = this.find('Section_List')
        if section_list is None:
            self.raise_exception('No Section_List!?', RuntimeError)
        sections = section_list.findall(WingSect.XMLTAG)
        for i, element in enumerate(sections):
            name = '%s_%d' % (WingSect.XMLTAG, i)
            section = self.add(name, WingSect())
            section.read(element)
            self._sections.append(section)

    def _read_list(self, this, list_tag, value_tag, typ=float):
        """ Read `typ` values from `this`, `list_tag`, and `value_tag`. """
        values = []
        list_element = this.find(list_tag)
        if list_element is None:
            self.raise_exception('No %s!?' % list_tag, RuntimeError)
        list_size = list_element.find('List_Size')
        for i in range(int(list_size.text)):
            value = list_element.find('%s%d' % (value_tag, i))
            values.append(typ(value.text))
        return values

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(HWB, self).write(parent, nesting)

        self.hwb_parms.write(this, nesting+1)

        airfoil_list = ElementTree.Element('Airfoil_List')
        airfoil_list.text = self.tail(nesting+2)
        airfoil_list.tail = self.tail(nesting+1)
        for airfoil in self._airfoils:
            airfoil.write(airfoil_list, nesting+2)
        this.append(airfoil_list)

        self._write_list(this, 'Section_Sizes_List', 'Section_Size',
                         self.section_size, nesting)

        self._write_list(this, 'Sweep_Percent_Lengths_List', 'Percent_Length',
                         self.sweep_percent_length, nesting)

        self._write_list(this, 'TESweep_Percent_Lengths_List', 'Percent_Length',
                         self.te_sweep_percent_length, nesting)

        self._write_list(this, 'Dihedral_Percent_Lengths_List', 'Percent_Length',
                         self.dihedral_percent_length, nesting)

        self._write_list(this, 'Sweep_DegPerSeg_List', 'DegPerSeg',
                         self.sweep_deg_per_seg, nesting)

        self._write_list(this, 'TESweep_DegPerSeg_List', 'DegPerSeg',
                         self.te_sweep_deg_per_seg, nesting)

        self._write_list(this, 'Dihedral_DegPerSeg_List', 'DegPerSeg',
                         self.dihedral_deg_per_seg, nesting)

        section_list = ElementTree.Element('Section_List')
        section_list.text = self.tail(nesting+2)
        section_list.tail = self.tail(nesting+1)
        for section in self._sections:
            section.write(section_list, nesting+2)
        this.append(section_list)

        return this

    def _write_list(self, this, list_tag, value_tag, what, nesting):
        """ Write values from `what` to `list_tag` and `value_tag`. """
        list_element = ElementTree.Element(list_tag)
        list_element.text = self.tail(nesting+2)
        list_element.tail = self.tail(nesting+1)
        list_size = ElementTree.Element('List_Size')
        list_size.text = str(len(what))
        list_size.tail = self.tail(nesting+2)
        list_element.append(list_size)
        for i, value in enumerate(what):
            value_element = ElementTree.Element('%s%d' % (value_tag, i))
            value_element.text = str(value)
            value_element.tail = self.tail(nesting+2)
            list_element.append(value_element)
        this.append(list_element)


class HWBParms(XMLContainer):
    """ XML parameters specific to an HWB. """

    XMLTAG = 'Hwb_Parms'

    total_area = Float(low=1., high=1000000., iotype='in', xmltag='Total_Area',
                       desc='')
    total_span = Float(low=0.1, high=10000., iotype='in', xmltag='Total_Span',
                       desc='')
    total_proj_span = Float(low=0.1, high=10000., iotype='in',
                            xmltag='Total_Proj_Span', desc='')
    avg_chord = Float(low=0.1, high=10000., iotype='in', xmltag='Avg_Chord',
                      desc='')
    sweep_off = Float(low=-85., high=85, units='deg', iotype='in',
                      xmltag='Sweep_Off', desc='')

    def __init__(self):
        super(HWBParms, self).__init__(self.XMLTAG)


import xml.etree.cElementTree as ElementTree

from openmdao.lib.datatypes.api import Bool, Float, Str

from vsp_wrapper.component     import VSPComponent
from vsp_wrapper.xml_container import XMLContainer


class CabinLayout(VSPComponent):
    """ Lay-out a cabin. """

    XMLTYPE = 'Cabin_Layout'

    def __init__(self):
        super(CabinLayout, self).__init__()
        self.add('cabin_layout_parms', CabinLayoutParms())

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(CabinLayout, self).read(this)

        parms = this.find(CabinLayoutParms.XMLTAG)
        if parms is None:
            self.raise_exception('No %s element!?' % CabinLayoutParms.XMLTAG)
        self.cabin_layout_parms.read(parms)

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(CabinLayout, self).write(parent, nesting)

        self.cabin_layout_parms.write(this, nesting+1)

        return this


class CabinLayoutParms(XMLContainer):
    """ XML parameters specific to cabin layout. """

    XMLTAG = 'Cabin_Layout_Parms'

    geom_filename = Str(iotype='in', xmltag='Geom_Data_File_Name',
                        desc='')
    mirror_active = Bool(False, iotype='in', xmltag='Mirror_Active',
                         desc='')

    def __init__(self):
        super(CabinLayoutParms, self).__init__(self.XMLTAG)
        self._cross_sections = []

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(CabinLayoutParms, self).read(this)

        section_list = this.find('Cabin_Cross_Sections_List')
        if section_list is None:
            self.raise_exception('No Cabin_Cross_Sections_List!?', RuntimeError)
        sections = section_list.findall(CrossSection.XMLTAG)
        for i, element in enumerate(sections):
            name = '%s_%d' % (CrossSection.XMLTAG, i)
            section = self.add(name, CrossSection())
            section.read(element)
            self._cross_sections.append(section)

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(CabinLayoutParms, self).write(parent, nesting)

        section_list = ElementTree.Element('Cabin_Cross_Sections_List')
        section_list.text = self.tail(nesting+2)
        section_list.tail = self.tail(nesting+1)
        for section in self._cross_sections:
            section.write(section_list, nesting+2)
        this.append(section_list)

        return this


class CrossSection(XMLContainer):
    """ XML parameters specific to a cabin cross-section. """

    XMLTAG = 'Cabin_Cross_Sections'

    xs1_p1x = Float(iotype='in', xmltag='Cabin_Point_XS1_P1X', desc='')
    xs1_p1y = Float(iotype='in', xmltag='Cabin_Point_XS1_P1Y', desc='')
    xs1_p1z = Float(iotype='in', xmltag='Cabin_Point_XS1_P1Z', desc='')
    xs1_p2x = Float(iotype='in', xmltag='Cabin_Point_XS1_P2X', desc='')
    xs1_p2y = Float(iotype='in', xmltag='Cabin_Point_XS1_P2Y', desc='')
    xs1_p2z = Float(iotype='in', xmltag='Cabin_Point_XS1_P2Z', desc='')
    xs1_p3x = Float(iotype='in', xmltag='Cabin_Point_XS1_P3X', desc='')
    xs1_p3y = Float(iotype='in', xmltag='Cabin_Point_XS1_P3Y', desc='')
    xs1_p3z = Float(iotype='in', xmltag='Cabin_Point_XS1_P3Z', desc='')
    xs1_p4x = Float(iotype='in', xmltag='Cabin_Point_XS1_P4X', desc='')
    xs1_p4y = Float(iotype='in', xmltag='Cabin_Point_XS1_P4Y', desc='')
    xs1_p4z = Float(iotype='in', xmltag='Cabin_Point_XS1_P4Z', desc='')
    xs2_p1x = Float(iotype='in', xmltag='Cabin_Point_XS2_P1X', desc='')
    xs2_p1y = Float(iotype='in', xmltag='Cabin_Point_XS2_P1Y', desc='')
    xs2_p1z = Float(iotype='in', xmltag='Cabin_Point_XS2_P1Z', desc='')
    xs2_p2x = Float(iotype='in', xmltag='Cabin_Point_XS2_P2X', desc='')
    xs2_p2y = Float(iotype='in', xmltag='Cabin_Point_XS2_P2Y', desc='')
    xs2_p2z = Float(iotype='in', xmltag='Cabin_Point_XS2_P2Z', desc='')
    xs2_p3x = Float(iotype='in', xmltag='Cabin_Point_XS2_P3X', desc='')
    xs2_p3y = Float(iotype='in', xmltag='Cabin_Point_XS2_P3Y', desc='')
    xs2_p3z = Float(iotype='in', xmltag='Cabin_Point_XS2_P3Z', desc='')
    xs2_p4x = Float(iotype='in', xmltag='Cabin_Point_XS2_P4X', desc='')
    xs2_p4y = Float(iotype='in', xmltag='Cabin_Point_XS2_P4Y', desc='')
    xs2_p4z = Float(iotype='in', xmltag='Cabin_Point_XS2_P4Z', desc='')

    def __init__(self):
        super(CrossSection, self).__init__(self.XMLTAG)


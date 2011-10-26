import xml.etree.cElementTree as ElementTree

from openmdao.lib.datatypes.api import Bool, Enum, Float, Int

from vsp_wrapper.component     import VSPComponent
from vsp_wrapper.xml_container import XMLContainer

# Cross section types.
_POINT     = 0
_CIRCLE    = 1
_ELLIPSE   = 2
_BOX       = 3
_RND_BOX   = 4
_GENERAL   = 5
_FROM_FILE = 6
_EDIT_CRV  = 7

# Point spacing.
_PNT_SPACE_PER_XSEC = 0
_PNT_SPACE_FIXED    = 1
_PNT_SPACE_UNIFORM  = 2


class Fuselage2(VSPComponent):
    """ A second type of fuselage. """

    XMLTYPE = 'Fuselage2'

    def __init__(self):
        super(Fuselage2, self).__init__()
        self.add('fuse_parms', FuseParms())
        self._cross_sections = []

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(Fuselage2, self).read(this)

        parms = this.find(FuseParms.XMLTAG)
        if parms is None:
            self.raise_exception('No %s element!?' % FuseParms.XMLTAG)
        self.fuse_parms.read(parms)

        section_list = this.find('Cross_Section_List')
        if section_list is None:
            self.raise_exception('No Cross_Section_List!?', RuntimeError)
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
        this = super(Fuselage2, self).write(parent, nesting)

        self.fuse_parms.write(this, nesting+1)

        section_list = ElementTree.Element('Cross_Section_List')
        section_list.text = self.tail(nesting+2)
        section_list.tail = self.tail(nesting+1)
        for section in self._cross_sections:
            section.write(section_list, nesting+2)
        this.append(section_list)

        return this


class FuseParms(XMLContainer):
    """ XML parameters specific to a fuselage2. """

    XMLTAG = 'Fuse_Parms'

    fuse_length = Float(30., low=0.001, high=1000., iotype='in',
                        xmltag='Fuse_Length', desc='')
    space_type = Enum(_PNT_SPACE_UNIFORM, iotype='in', xmltag='Space_Type',
                      values=(_PNT_SPACE_PER_XSEC, _PNT_SPACE_FIXED,
                              _PNT_SPACE_UNIFORM),
                      aliases=('Per XSec', 'Fixed', 'Uniform'),
                      desc='')

    def __init__(self):
        super(FuseParms, self).__init__(self.XMLTAG)


class CrossSection(XMLContainer):
    """ XML parameters specific to a fuselage2 cross-section. """

    XMLTAG = 'Cross_Section'

    num_pnts = Int(iotype='in', xmltag='Num_Pnts',
                   desc='')
    spine_location = Float(0., low=0., high=1., iotype='in',
                           xmltag='Spine_Location', desc='')
    z_offset = Float(0., low=-1000., high=1000., iotype='in', xmltag='Z_Offset',
                     desc='')
    top_tan_ang = Float(0., low=-90., high=90., units='deg', iotype='in',
                        xmltag='Top_Tan_Ang', desc='')
    top_tan_str_1 = Float(0.25, low=0., high=1., iotype='in',
                          xmltag='Top_Tan_Str_1', desc='')
    top_tan_str_2 = Float(0.25, low=0., high=1., iotype='in',
                          xmltag='Top_Tan_Str_2', desc='')
    bot_tan_ang = Float(0., low=-90., high=90., units='deg', iotype='in',
                        xmltag='Bot_Tan_Ang', desc='')
    bot_tan_str_1 = Float(0.25, low=0., high=1., iotype='in',
                          xmltag='Bot_Tan_Str_1', desc='')
    bot_tan_str_2 = Float(0.25, low=0., high=1., iotype='in',
                          xmltag='Bot_Tan_Str_2', desc='')
    left_tan_ang = Float(0., low=-90., high=90., units='deg', iotype='in',
                         xmltag='Left_Tan_Ang', desc='')
    left_tan_str_1 = Float(0.25, low=0., high=1., iotype='in',
                           xmltag='Left_Tan_Str_1', desc='')
    left_tan_str_2 = Float(0.25, low=0., high=1., iotype='in',
                           xmltag='Left_Tan_Str_2', desc='')
    right_tan_ang = Float(0., low=-90., high=90., units='deg', iotype='in',
                          xmltag='Right_Tan_Ang', desc='')
    right_tan_str_1 = Float(0.25, low=0., high=1., iotype='in',
                            xmltag='Right_Tan_Str_1', desc='')
    right_tan_str_2 = Float(0.25, low=0., high=1., iotype='in',
                            xmltag='Right_Tan_Str_2', desc='')
    num_sect_interp_1 = Int(5, iotype='in', xmltag='Num_Sect_Interp_1',
                            desc='')
    num_sect_interp_2 = Int(5, iotype='in', xmltag='Num_Sect_Interp_2',
                            desc='')
    top_sym_flag = Bool(False, iotype='in', xmltag='Top_Sym_Flag',
                        desc='')
    side_sym_flag = Bool(True, iotype='in', xmltag='Side_Sym_Flag',
                         desc='')
    type = Enum(_ELLIPSE, iotype='in', xmltag='Type',
                values=(_POINT, _CIRCLE, _ELLIPSE, _BOX, _RND_BOX, _GENERAL,
                        _FROM_FILE, _EDIT_CRV),
                aliases=('Point', 'Ciurcle', 'Ellipse', 'Box', 'Round Box',
                         'General', 'File', 'Edit'),
                desc='')
    height = Float(3., low=0., high=10000., iotype='in', xmltag='Height',
                   desc='')
    width = Float(2.5, low=0., high=10000., iotype='in', xmltag='Width',
                  desc='')
    max_width_location = Float(0., low=-1000., high=1000., iotype='in',
                               xmltag='Max_Width_Location', desc='')
    corner_radius = Float(0.1, low=0.0001, high=1000., iotype='in',
                          xmltag='Corner_Radius', desc='')
    top_tan_angle = Float(90., low=0., high=90., units='deg', iotype='in',
                          xmltag='Top_Tan_Angle', desc='')
    bot_tan_angle = Float(90., low=0., high=90., units='deg', iotype='in',
                          xmltag='Bot_Tan_Angle', desc='')
    top_tan_strength = Float(0.5, low=0.001, high=2., iotype='in',
                             xmltag='Top_Tan_Strength', desc='')
    upper_tan_strength = Float(0.5, low=0.001, high=2., iotype='in',
                               xmltag='Upper_Tan_Strength', desc='')
    lower_tan_strength = Float(0.5, low=0.001, high=2., iotype='in',
                               xmltag='Lower_Tan_Strength', desc='')
    bottom_tan_strength = Float(0.5, low=0.001, high=2., iotype='in',
                                xmltag='Bottom_Tan_Strength', desc='')

    def __init__(self):
        super(CrossSection, self).__init__(self.XMLTAG)


import xml.etree.cElementTree as ElementTree

from openmdao.lib.datatypes.api import Bool, Enum, Float, Int, Str

from vsp_wrapper.component     import VSPComponent
from vsp_wrapper.xml_container import XMLContainer

# Cross section types.
_POINT     = 0
_CIRCLE    = 1
_ELLIPSE   = 2
_RND_BOX   = 3
_GENERAL   = 4
_FROM_FILE = 5
_EDIT_CRV  = 6

# Mold line types.
_OML = 0
_IML = 1

# Space types.
_PNT_SPACE_PER_XSEC = 0
_PNT_SPACE_FIXED    = 1
_PNT_SPACE_UNIFORM  = 2


class Fuselage(VSPComponent):
    """ A fuselage. """

    XMLTYPE = 'Fuselage'

    def __init__(self):
        super(Fuselage, self).__init__()
        self.add('fuse_parms', FuseParms())
        self._cross_sections = []

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(Fuselage, self).read(this)

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
        this = super(Fuselage, self).write(parent, nesting)

        self.fuse_parms.write(this, nesting+1)

        section_list = ElementTree.Element('Cross_Section_List')
        section_list.text = self.tail(nesting+2)
        section_list.tail = self.tail(nesting+1)
        for section in self._cross_sections:
            section.write(section_list, nesting+2)
        this.append(section_list)

        return this


class FuseParms(XMLContainer):
    """ XML parameters specific to a fuselage. """

    XMLTAG = 'Fuse_Parms'

    fuse_length = Float(30., low=0.001, high=1000., iotype='in',
                        xmltag='Fuse_Length', desc='')
    camber = Float(0.0, low=-0.1, high=0.1, iotype='in', xmltag='Camber',
                   desc='')
    camber_loc = Float(0.5, low=0., high=1., iotype='in',
                       xmltag='Camber_Location', desc='')
    aft_offset = Float(0.0, low=-1., high=1., iotype='in', xmltag='Aft_Offset',
                       desc='')
    nose_angle = Float(0.0, low=0., high=90., iotype='in', xmltag='Nose_Angle',
                       desc='')
    nose_strength = Float(0.3, low=0., high=1., iotype='in',
                          xmltag='Nose_Strength', desc='')
    nose_rho = Float(0.5, low=0., high=2., iotype='in', xmltag='Nose_Rho',
                     desc='')
    aft_rho = Float(0.5, low=0., high=2., iotype='in', xmltag='Aft_Rho',
                    desc='')
    iml_on = Bool(False, iotype='in', xmltag='IML_Flag',
                  desc='')
    space_type = Enum(_PNT_SPACE_UNIFORM, iotype='in', xmltag='Space_Type',
                      values=(_PNT_SPACE_PER_XSEC, _PNT_SPACE_FIXED,
                              _PNT_SPACE_UNIFORM),
                      aliases=('Per XSec', 'Fixed', 'Uniform'),
                      desc='')
    nose_super_flag = Bool(True, iotype='in', xmltag='Nose_Super_Flag',
                           desc='')
    aft_super_flag = Bool(True, iotype='in', xmltag='Aft_Super_Flag',
                          desc='')

    def __init__(self):
        super(FuseParms, self).__init__(self.XMLTAG)


class CrossSection(XMLContainer):
    """ XML parameters specific to a fuselage cross-section. """

    XMLTAG = 'Cross_Section'

    num_pnts = Int(33, iotype='in', xmltag='Num_Pnts',
                   desc='')
    spine_location = Float(0., low=0., high=1., iotype='in',
                           xmltag='Spine_Location', desc='')
    z_offset = Float(0., low=-1000., high=1000., iotype='in', xmltag='Z_Offset',
                     desc='')
    top_thick = Float(0.5, low=0., high=1000., iotype='in', xmltag='Top_Thick',
                      desc='')
    bot_thick = Float(0.5, low=0., high=1000., iotype='in', xmltag='Bot_Thick',
                      desc='')
    side_thick = Float(0.5, low=0., high=1000., iotype='in',
                       xmltag='Side_Thick', desc='')
    act_top_thick = Float(0.5, low=0., high=1000., iotype='in',
                          xmltag='Act_Top_Thick', desc='')
    act_bot_thick = Float(0.5, low=0., high=1000., iotype='in',
                          xmltag='Act_Bot_Thick', desc='')
    act_side_thick = Float(0.5, low=0., high=1000., iotype='in',
                           xmltag='Act_Side_Thick', desc='')
    iml_x_offset = Float(0.0, iotype='in', xmltag='IML_X_Offset',
                         desc='')
    iml_z_offset = Float(0.0, low=-1000., high=1000., iotype='in',
                         xmltag='IML_Z_Offset', desc='')
    ml_type = Enum(iotype='in', xmltag='ML_Type',
                   values=(_OML, _IML), aliases=('OML', 'IML'), desc='')
    iml_flag = Bool(False, iotype='in', xmltag='IML_Flag',
                    desc='')
    profile_tan_str_1 = Float(0.25, low=0., high=1., iotype='in',
                              xmltag='Profile_Tan_Str_1', desc='')
    profile_tan_str_2 = Float(0.25, low=0., high=1., iotype='in',
                              xmltag='Profile_Tan_Str_2', desc='')
    profile_tan_ang = Float(0., low=-10., high=10., iotype='in',
                            xmltag='Profile_Tan_Ang', desc='')
    num_sect_interp_1 = Int(iotype='in', xmltag='Num_Sect_Interp_1',
                            desc='')
    num_sect_interp_2 = Int(iotype='in', xmltag='Num_Sect_Interp_2',
                            desc='')

    def __init__(self):
        super(CrossSection, self).__init__(self.XMLTAG)
        self.add('oml_parms', OMLParms())
        self.add('iml_parms', IMLParms())

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(CrossSection, self).read(this)

        parms = this.find(OMLParms.XMLTAG)
        if parms is None:
            self.raise_exception('No %s element!?' % OMLParms.XMLTAG)
        self.oml_parms.read(parms)

        parms = this.find(IMLParms.XMLTAG)
        if parms is None:
            self.raise_exception('No %s element!?' % IMLParms.XMLTAG)
        self.iml_parms.read(parms)

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(CrossSection, self).write(parent, nesting)

        self.oml_parms.write(this, nesting+1)
        self.iml_parms.write(this, nesting+1)

        return this


class MLParms(XMLContainer):
    """ XML parameters specific to a fuselage cross-section mold line. """

    type = Enum(_ELLIPSE, iotype='in', xmltag='Type',
                values=(_POINT, _CIRCLE, _ELLIPSE, _RND_BOX, _GENERAL,
                        _FROM_FILE, _EDIT_CRV),
                aliases=('Point', 'Circle', 'Ellipse', 'Round Box', 'General',
                         'File', 'Edit'),
                desc='Type of cross section.')
    height = Float(3., low=0., high=1000., iotype='in', xmltag='Height',
                   desc='')
    width = Float(2.5, low=0., high=1000., iotype='in', xmltag='Width',
                  desc='')
    max_width_location = Float(0., low=-1000., high=1000., iotype='in',
                               xmltag='Max_Width_Location',
                               desc='')
    corner_radius = Float(0.1, low=0.0001, high=1000., iotype='in',
                          xmltag='Corner_Radius',
                          desc='')
    top_tan_angle = Float(90., low=0., high=90., iotype='in',
                          xmltag='Top_Tan_Angle',
                          desc='')
    bot_tan_angle = Float(90., low=0., high=90., iotype='in',
                          xmltag='Bot_Tan_Angle',
                          desc='')
    top_tan_strength = Float(0.5, low=0.001, high=2., iotype='in',
                             xmltag='Top_Tan_Strength',
                             desc='')
    upper_tan_strength = Float(0.5, low=0.001, high=2., iotype='in',
                               xmltag='Upper_Tan_Strength',
                               desc='')
    lower_tan_strength = Float(0.5, low=0.001, high=2., iotype='in',
                               xmltag='Lower_Tan_Strength',
                               desc='')
    bottom_tan_strength = Float(0.5, low=0.001, high=2., iotype='in',
                                xmltag='Bottom_Tan_Strength',
                                desc='')

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(MLParms, self).read(this)

        if self.type == _FROM_FILE:
            self.add_trait('file_name',
                           Str(iotype='in', xmltag='File_Name',
                           desc=''))
            self.read_element(this, 'file_name')

# TODO: handle array.
            self.add_trait('file_y_pnts',
                           Str(iotype='in', xmltag='File_Y_Pnts',
                           desc=''))
            self.read_element(this, 'file_y_pnts')

# TODO: handle array.
            self.add_trait('file_z_pnts',
                           Str(iotype='in', xmltag='File_Z_Pnts',
                           desc=''))
            self.read_element(this, 'file_z_pnts')


class OMLParms(MLParms):
    """ XML parameters specific to a fuselage cross-section OML. """

    XMLTAG = 'OML_Parms'

    def __init__(self):
        super(OMLParms, self).__init__(self.XMLTAG)


class IMLParms(XMLContainer):
    """ XML parameters specific to a fuselage cross-section OML. """

    XMLTAG = 'IML_Parms'

    def __init__(self):
        super(IMLParms, self).__init__(self.XMLTAG)


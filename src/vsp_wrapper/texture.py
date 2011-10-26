from openmdao.lib.datatypes.api import Bool, Float, Int, Str

from vsp_wrapper.xml_container import XMLContainer


class Texture(XMLContainer):
    """ XML parameters for a texture/image applied to a surface. """

    XMLTAG = 'Applied_Texture'

    texture_name = Str('Default_Name', iotype='in', xmltag='Name',
                       desc='Name of texture.')
    texture_filename = Str('Default_Name', iotype='in', xmltag='Texture_Name',
                           desc='Filename for texture data (.jpg or .tga)')
    all_surf_flag = Bool(False, iotype='in', xmltag='All_Surf_Flag',
                         desc='If True, apply to all surfaces of component.')
    surf_id = Int(0, iotype='in', xmltag='Surf_ID',
                  desc='ID of surface to apply to.')
    u = Float(0.5, iotype='in', xmltag='U',
              desc='Position along U axis.')
    w = Float(0.5, iotype='in', xmltag='W',
              desc='Position along W axis.')
    scale_u = Float(1.0, iotype='in', xmltag='Scale_U',
                    desc='Scaling in U direction.')
    scale_w = Float(1.0, iotype='in', xmltag='Scale_W',
                    desc='Scaling in W direction.')
    wrap_u = Bool(False, iotype='in', xmltag='Wrap_U_Flag',
                  desc='')
    wrap_w = Bool(False, iotype='in', xmltag='Wrap_W_Flag',
                  desc='')
    repeat = Bool(False, iotype='in', xmltag='Repeat_Flag',
                  desc='Repeat texture over surface.')
    bright = Float(1.0, low=0., high=1., iotype='in', xmltag='Bright',
                   desc='Brightness.')
    alpha = Float(1.0, low=0., high=1., iotype='in', xmltag='Alpha',
                  desc='Transparency.')
    flip_u = Bool(False, iotype='in', xmltag='Flip_U_Flag',
                  desc='')
    flip_w = Bool(False, iotype='in', xmltag='Flip_W_Flag',
                  desc='')
    refl_flip_u = Bool(False, iotype='in', xmltag='Refl_Flip_U_Flag',
                       desc='')
    refl_flip_w = Bool(False, iotype='in', xmltag='Refl_Flip_W_Flag',
                       desc='')

    def __init__(self):
        super(Texture, self).__init__(self.XMLTAG)


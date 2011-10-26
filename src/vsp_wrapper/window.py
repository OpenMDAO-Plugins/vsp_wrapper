from openmdao.lib.datatypes.api import Float

from vsp_wrapper.xml_container import XMLContainer


class VirtWindow(XMLContainer):
    """ XML parameters for a virtual window. """

    XMLTAG = 'VirtWindow'

    back_img_scale_w = Float(1.0, iotype='in', xmltag='Back_Img_Scale_W',
                             desc='Backgrund image width scaling.')
    back_img_scale_h = Float(1.0, iotype='in', xmltag='Back_Img_Scale_H',
                             desc='Background image height scaling.')
    back_img_offset_x = Float(0.0, iotype='in', xmltag='Back_Img_Offset_X',
                              desc='Background image X offset.')
    back_img_offset_y = Float(0.0, iotype='in', xmltag='Back_Img_Offset_Y',
                              desc='Background image Y offset.')

    def __init__(self):
        super(VirtWindow, self).__init__(self.XMLTAG)


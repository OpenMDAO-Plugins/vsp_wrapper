import xml.etree.cElementTree as ElementTree

from openmdao.lib.datatypes.api import Bool, Enum, Float, Int, Str

from vsp_wrapper.source        import BaseSource
from vsp_wrapper.texture       import Texture
from vsp_wrapper.xml_container import XMLContainer, XLATE

# Symmetry.
_NO_SYM = 0
_XY_SYM = 1
_XZ_SYM = 2
_YZ_SYM = 3

# Attachment.
_POS_ATTACH_NONE   = 0
_POS_ATTACH_FIXED  = 1
_POS_ATTACH_UV     = 2 
_POS_ATTACH_MATRIX = 3


class GeneralParms(XMLContainer):
    """ General XML parameters for a component. """

    XMLTAG = 'General_Parms'

    part_name = Str('Default_Name', iotype='in', xmltag='Name',
                    desc='Name for this part, may contain spaces.')
    color_r = Float(0.0, low=0., high=255., iotype='in', xmltag='ColorR',
                    desc='Red component of displayed color.')
    color_g = Float(0.0, low=0., high=255., iotype='in', xmltag='ColorG',
                    desc='Green component of displayed color.')
    color_b = Float(255.0, low=0., high=255., iotype='in', xmltag='ColorB',
                    desc='Blue component of displayed color.')
    symmetry = Enum(_NO_SYM, iotype='in', xmltag='Symmetry',
                    values=(_NO_SYM, _XY_SYM, _XZ_SYM, _YZ_SYM),
                    aliases=('None', 'XY', 'XZ', 'YZ'),
                    desc='Symmetry plane.')
    material_id = Int(0, low=0, iotype='in', xmltag='MaterialID',
                      desc='Material identifier, sets display.')
    output_flag = Bool(True, iotype='in', xmltag='OutputFlag',
                       desc='')
    output_name_id = Int(0, iotype='in', xmltag='OutputNameID',
                         desc='')
    display_children_flag = Bool(True, iotype='in',
                                 xmltag='DisplayChildrenFlag',
                                 desc='If True, child parts are listed in the'
                                      ' geometry browser window.')
    num_pnts = Int(21, low=9, high=1001, iotype='in', xmltag='NumPnts',
                   desc='Number of tesselation points.')
    num_x_secs = Int(11, low=4, high=101, iotype='in', xmltag='NumXsecs',
                     desc='Number of tesselation cross-sections.')
    mass_prior = Int(0, iotype='in', xmltag='MassPrior',
                     desc='')
    shell_flag = Bool(False, iotype='in', xmltag='ShellFlag',
                      desc='')

    rel_xform_flag = Bool(False, iotype='in', xmltag='RelXFormFlag',
                          desc='If True, transform in relative frame.')
    tran_x = Float(0.0, iotype='in', xmltag='Tran_X',
                   desc='')
    tran_y = Float(0.0, iotype='in', xmltag='Tran_Y',
                   desc='')
    tran_z = Float(0.0, iotype='in', xmltag='Tran_Z',
                   desc='')
    tran_rel_x = Float(0.0, iotype='in', xmltag='TranRel_X',
                       desc='')
    tran_rel_y = Float(0.0, iotype='in', xmltag='TranRel_Y',
                       desc='')
    tran_rel_z = Float(0.0, iotype='in', xmltag='TranRel_Z',
                       desc='')
    rot_x = Float(0.0, low=-180., high=180., units='deg', iotype='in',
                  xmltag='Rot_X', desc='')
    rot_y = Float(0.0, low=-180., high=180., units='deg', iotype='in',
                  xmltag='Rot_Y', desc='')
    rot_z = Float(0.0, low=-180., high=180., units='deg', iotype='in',
                  xmltag='Rot_Z', desc='')
    rot_rel_x = Float(0.0, low=-180., high=180., units='deg', iotype='in',
                      xmltag='RotRel_X', desc='')
    rot_rel_y = Float(0.0, low=-180., high=180., units='deg', iotype='in',
                      xmltag='RotRel_Y', desc='')
    rot_rel_z = Float(0.0, low=-180., high=180., units='deg', iotype='in',
                      xmltag='RotRel_Z', desc='')
    origin = Float(0.0, low=0., high=1., iotype='in', xmltag='Origin',
                   desc='')

    density = Float(1.0, low=0., high=1000000., iotype='in', xmltag='Density',
                    desc='')
    shell_mass_area = Float(1.0, low=0., high=1000000., iotype='in',
                            xmltag='ShellMassArea',
                            desc='')

    ref_flag = Bool(False, iotype='in', xmltag='RefFlag',
                    desc='')
    ref_area = Float(100.0, iotype='in', xmltag='RefArea',
                     desc='')
    ref_span = Float(10.0, iotype='in', xmltag='RefSpan',
                     desc='')
    ref_cbar = Float(1.0, iotype='in', xmltag='RefCbar',
                     desc='')
    auto_ref_area_flag = Bool(True, iotype='in', xmltag='AutoRefAreaFlag',
                              desc='')
    auto_ref_span_flag = Bool(True, iotype='in', xmltag='AutoRefSpanFlag',
                              desc='')
    auto_ref_cbar_flag = Bool(True, iotype='in', xmltag='AutoRefCbarFlag',
                              desc='')

    aero_center_x = Float(0.0, iotype='in', xmltag='AeroCenter_X',
                          desc='')
    aero_center_y = Float(0.0, iotype='in', xmltag='AeroCenter_Y',
                          desc='')
    aero_center_z = Float(0.0, iotype='in', xmltag='AeroCenter_Z',
                          desc='')
    auto_aero_center_flag = Bool(True, iotype='in', xmltag='AutoAeroCenterFlag',
                                 desc='')

    pos_attach = Enum(iotype='in', xmltag='PosAttachFlag',
                      values=(_POS_ATTACH_NONE, _POS_ATTACH_FIXED,
                              _POS_ATTACH_UV, _POS_ATTACH_MATRIX),
                      aliases=('None', 'Fixed', 'UV', 'Matrix'),
                      desc='Attachment to parent part.')
    u_attach = Float(0.0, low=0., high=1., iotype='in', xmltag='U_Attach',
                     desc='')
    v_attach = Float(0.0, low=0., high=1., iotype='in', xmltag='V_Attach',
                     desc='')

    id_num = Int(0, iotype='out', xmltag='Id_Number',
                 desc='Part identifier (VSP internal use only)')
    id_str = Str('1234567', iotype='in', xmltag='Id_String',
                 desc='Part identifier (VSP internal use only)')
    ptr_id = Int(iotype='out', xmltag='PtrID',
                 desc='Part identifier (VSP internal use only)')
    parent_ptr_id = Int(0, iotype='out', xmltag='Parent_PtrID',
                        desc='Part part identifier (VSP internal use only)')

    def __init__(self):
        super(GeneralParms, self).__init__(self.XMLTAG)
        self._children = []
        self._textures = []
        self._parts    = []
        self._sources  = []
        self._fea_data = []

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(GeneralParms, self).read(this)

        children = this.findall('Children_PtrID')
        for element in children:
            self._children.append(element.text)

        textures = this.findall(Texture.XMLTAG)
        for element in textures:
            name = element.findtext('Name')
            texture = self.add(name.translate(XLATE), Texture())
            texture.read(element)
            self._textures.append(texture)

# TODO: Structure Parts

        sources = this.findall(BaseSource.XMLTAG)
        for element in sources:
            name = element.findtext('Name')
            source = self.add(name.translate(XLATE), BaseSource.create(element))
            source.read(element)
            self._sources.append(source)

# TODO: FEA Structure Data


    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(GeneralParms, self).write(parent, nesting)

        child_tail = self.tail(nesting+1)
        for child in self._children:
            child_id = ElementTree.Element('Children_PtrID')
            child_id.text = child
            child_id.tail = child_tail
            this.append(child_id)

        for texture in self._textures:
            texture.write(this, nesting+1)

# TODO: Structure Parts

        for source in self._sources:
            source.write(this, nesting+1)

# TODO: FEA Structure Data

        return this


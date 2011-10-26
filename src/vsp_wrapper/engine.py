from openmdao.lib.datatypes.api import Bool, Enum, Float, Int

from vsp_wrapper.component     import VSPComponent
from vsp_wrapper.xml_container import XMLContainer

# Inlet types.
_SUB_PITOT     = 1
_SUPER_PITOT   = 2
_TRIANG_2_D    = 3
_INFINITE_2_D  = 4
_FIXED_CONICAL = 5
_TRANS_CONICAL = 6

# Nozzle types.
_CONVER_AXI        = 0
_CONVER_RECT       = 1
_CONVER_DIVER_AXI  = 2
_CONVER_DIVER_RECT = 3


class Engine(VSPComponent):
    """ An engine. """

    XMLTYPE = 'Engine'

    def __init__(self):
        super(Engine, self).__init__()
        self.add('engine_parms', EngineParms())

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(Engine, self).read(this)

        parms = this.find(EngineParms.XMLTAG)
        if parms is None:
            self.raise_exception('No %s element!?' % EngineParms.XMLTAG)
        self.engine_parms.read(parms)

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(Engine, self).write(parent, nesting)
        self.engine_parms.write(this, nesting+1)
        return this


class EngineParms(XMLContainer):
    """ XML parameters specific to an engine. """

    XMLTAG = 'Engine_Parms'

    engine_type = Int(0, iotype='in', xmltag='Engine_Type',
                      desc='')
    radius_tip = Float(1.5, low=0.1, high=100., iotype='in',
                       xmltag='Radius_Tip', desc='')
    hub_tip = Float(0.5, low=0.01, high=0.99, iotype='in', xmltag='Hub_Tip',
                    desc='Hub/Tip ratio.')
    max_tip = Float(1.3, low=1.0001, high=100., iotype='in', xmltag='Max_Tip',
                    desc='Max/Tip ratio.')
    eng_length = Float(4., low=0.1, high=100., iotype='in', xmltag='Eng_Length',
                       desc='')

    inlet_type = Enum(iotype='in', xmltag='Inlet_Type',
                      values=(_SUB_PITOT, _SUPER_PITOT, _TRIANG_2_D,
                              _INFINITE_2_D, _FIXED_CONICAL, _TRANS_CONICAL),
                      aliases=('Sub Pitot', 'Super Pitot', '2D Triangular',
                               '2D INfinite', 'Fixed Conical',
                               'Translating Conical'),
                      desc='')
    inlet_xy_sym_flag = Bool(iotype='in', xmltag='Inlet_XY_Sym_Flag',
                             desc='')

    inlet_duct_on = Bool(False, iotype='in', xmltag='Inlet_Duct_On_Off',
                         desc='')
    inlet_duct_x_offset = Float(3., low=0.01, high=100., iotype='in',
                                xmltag='Inlet_Duct_X_Offset', desc='')
    inlet_duct_y_offset = Float(1., low=0., high=100., iotype='in',
                                xmltag='Inlet_Duct_Y_Offset', desc='')
    inlet_duct_shape_factor = Float(0.5, low=0.01, high=1., iotype='in',
                                    xmltag='Inlet_Duct_Shape_Factor', desc='')

    inlet_half_split = Bool(False, iotype='in', xmltag='Inlet_Half_Split_Flag',
                            desc='')
    cowl_length = Float(2., low=0.001, high=100., iotype='in',
                        xmltag='Cowl_Length', desc='')
    eng_thrt_ratio = Float(1.5, low=0.5, high=10., iotype='in',
                           xmltag='Eng_Thrt_Ratio', desc='')
    hilight_thrt_ratio = Float(1.3, low=1.01, high=10., iotype='in',
                               xmltag='Hilight_Thrt_Ratio', desc='')
    lip_finess_ratio = Float(1.9, low=0.1, high=10., iotype='in',
                             xmltag='Lip_Finess_Ratio', desc='')
    height_width_ratio = Float(1.0, low=0.05, high=20., iotype='in',
                               xmltag='Height_Width_Ratio', desc='')
    upper_surf_shape_factor = Float(-1.3, low=-2., high=2., iotype='in',
                                    xmltag='Upper_Surf_Shape_Factor', desc='')
    lower_surf_shape_factor = Float(0.7, low=-1., high=1., iotype='in',
                                    xmltag='Lower_Surf_Shape_Factor', desc='')
    inlet_x_axis_rot = Float(0., low=-90., high=90., units='deg', iotype='in',
                             xmltag='Inlet_X_Axis_Rot', desc='')
    inlet_scarf_angle = Float(0., low=-60., high=60., units='deg', iotype='in',
                              xmltag='Inlet_Scarf_Angle', desc='')

    inl_noz_color = Int(iotype='in', xmltag='Inl_Noz_Color',
                        desc='')

    divertor_on = Bool(False, iotype='in', xmltag='Divertor_On_Off',
                       desc='')
    divertor_height = Float(0.5, low=0.01, high=100., iotype='in',
                            xmltag='Divertor_Height', desc='')
    divertor_length = Float(1., low=0.01, high=100., iotype='in',
                            xmltag='Divertor_Length', desc='')

    nozzle_type = Enum(iotype='in', xmltag='Nozzle_Type',
                       values=(_CONVER_AXI, _CONVER_RECT,
                               _CONVER_DIVER_AXI, _CONVER_DIVER_RECT),
                       aliases=('Conv Axi', 'Conv Rect',
                                'Conv-Div Axi', 'Conv-Div Rect'),
                       desc='')
    nozzle_duct_on = Bool(False, iotype='in', xmltag='Nozzle_Duct_On_Off',
                          desc='')
    nozzle_duct_x_offset = Float(1., low=0.01, high=100., iotype='in',
                                 xmltag='Nozzle_Duct_X_Offset', desc='')
    nozzle_duct_y_offset = Float(0., low=0., high=100., iotype='in',
                                 xmltag='Nozzle_Duct_Y_Offset', desc='')
    nozzle_duct_shape_factor = Float(0., low=-1., high=1., iotype='in',
                                     xmltag='Nozzle_Duct_Shape_Factor', desc='')
    nozzle_length = Float(2., low=0.01, high=100., iotype='in',
                          xmltag='Nozzle_Length', desc='')
    exit_area_ratio = Float(2., low=0.01, high=100., iotype='in',
                            xmltag='Exit_Area_Ratio', desc='')
    nozzle_height_width_ratio = Float(1., low=0.01, high=100., iotype='in',
                                      xmltag='Nozzle_Height_Width_Ratio',
                                      desc='')
    exit_throat_ratio = Float(1.5, low=0.01, high=100., iotype='in',
                              xmltag='Exit_Throat_Ratio', desc='')
    dive_flap_ratio = Float(1.5, low=0.01, high=100., iotype='in',
                            xmltag='Dive_Flap_Ratio', desc='')

    def __init__(self):
        super(EngineParms, self).__init__(self.XMLTAG)


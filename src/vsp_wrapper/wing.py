from openmdao.lib.datatypes.api import Bool, Float, Int, Str

from vsp_wrapper.airfoil       import Airfoil
from vsp_wrapper.component     import VSPComponent
from vsp_wrapper.xml_container import XMLContainer


class Wing(VSPComponent):
    """ A wing. """

    XMLTYPE = 'Mwing'

    def __init__(self):
        super(Wing, self).__init__()
        self.add('wing_parms', WingParms())
        self.add('root_airfoil', Airfoil('Root_Airfoil'))
        self.add('strake_airfoil', Airfoil('Strake_Airfoil'))
        self.add('aft_airfoil', Airfoil('Aft_Airfoil'))
        self.add('tip_airfoil', Airfoil('Tip_Airfoil'))

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(Wing, self).read(this)

        parms = this.find(WingParms.XMLTAG)
        if parms is None:
            self.raise_exception('No %s element!?' % WingParms.XMLTAG)
        self.wing_parms.read(parms)

        airfoil = this.find('Root_Airfoil')
        if airfoil is None:
            self.raise_exception('No Root_Airfoil element!?')
        self.root_airfoil.read(airfoil)

        airfoil = this.find('Strake_Airfoil')
        if airfoil is None:
            self.raise_exception('No Strake_Airfoil element!?')
        self.strake_airfoil.read(airfoil)

        airfoil = this.find('Aft_Airfoil')
        if airfoil is None:
            self.raise_exception('No Aft_Airfoil element!?')
        self.aft_airfoil.read(airfoil)

        airfoil = this.find('Tip_Airfoil')
        if airfoil is None:
            self.raise_exception('No Tip_Airfoil element!?')
        self.tip_airfoil.read(airfoil)

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(Wing, self).write(parent, nesting)

        self.wing_parms.write(this, nesting+1)
        self.root_airfoil.write(this, nesting+1)
        self.strake_airfoil.write(this, nesting+1)
        self.aft_airfoil.write(this, nesting+1)
        self.tip_airfoil.write(this, nesting+1)

        return this


class WingParms(XMLContainer):
    """ XML parameters specific to a Wing. """

    XMLTAG = 'Mwing_Parms'

    num_pnts = Int(iotype='in', xmltag='Num_Pnts',
                   desc='')
    driver = Int(iotype='in', xmltag='Driver',
                 desc='')
    aspect_ratio = Float(iotype='in', xmltag='Aspect_Ratio',
                         desc='')
    taper_ratio = Float(iotype='in', xmltag='Taper_Ratio',
                        desc='')
    area = Float(iotype='in', xmltag='Area',
                 desc='')
    span = Float(iotype='in', xmltag='Span',
                 desc='')
    tip_chord = Float(iotype='in', xmltag='Tip_Chord',
                      desc='')
    root_chord = Float(iotype='in', xmltag='Root_Chord',
                       desc='')
    sweep = Float(iotype='in', xmltag='Sweep',
                  desc='')
    sweep_loc = Float(iotype='in', xmltag='Sweep_Loc',
                      desc='')
    twist_loc = Float(iotype='in', xmltag='Twist_Loc',
                      desc='')
    in_twist = Float(iotype='in', xmltag='In_Twist',
                     desc='')
    in_dihed = Float(iotype='in', xmltag='In_Dihed',
                     desc='')
    mid_twist = Float(iotype='in', xmltag='Mid_Twist',
                      desc='')
    mid_dihed = Float(iotype='in', xmltag='Mid_Dihed',
                      desc='')
    out_twist = Float(iotype='in', xmltag='Out_Twist',
                      desc='')
    out_dihed = Float(iotype='in', xmltag='Out_Dihed',
                      desc='')
    strake_sweep = Float(iotype='in', xmltag='Strake_Sweep',
                         desc='')
    strake_span_per = Float(iotype='in', xmltag='Strake_Span_Per',
                            desc='')
    aft_ext_sweep = Float(iotype='in', xmltag='Aft_Ext_Sweep',
                          desc='')
    aft_ext_span_per = Float(iotype='in', xmltag='Aft_Ext_Span_Per',
                             desc='')
    all_move_flag = Bool(iotype='in', xmltag='All_Move_Flag',
                         desc='')
    in_flap_type = Int(iotype='in', xmltag='In_Flap_Type',
                       desc='')
    out_flap_type = Int(iotype='in', xmltag='Out_Flap_Type',
                        desc='')
    in_slat_type = Int(iotype='in', xmltag='In_Slat_Type',
                       desc='')
    out_slat_type = Int(iotype='in', xmltag='Out_Slat_Type',
                        desc='')
    in_flap_span_in = Float(iotype='in', xmltag='In_Flap_Span_In',
                            desc='')
    in_flap_span_out = Float(iotype='in', xmltag='In_Flap_Span_Out',
                             desc='')
    in_flap_chord = Float(iotype='in', xmltag='In_Flap_Chord',
                          desc='')
    out_flap_span_in = Float(iotype='in', xmltag='Out_Flap_Span_In',
                             desc='')
    out_flap_span_out = Float(iotype='in', xmltag='Out_Flap_Span_Out',
                              desc='')
    out_flap_chord = Float(iotype='in', xmltag='Out_Flap_Chord',
                           desc='')
    in_slat_span_in = Float(iotype='in', xmltag='In_Slat_Span_In',
                            desc='')
    in_slat_span_out = Float(iotype='in', xmltag='In_Slat_Span_Out',
                             desc='')
    in_slat_chord = Float(iotype='in', xmltag='In_Slat_Chord',
                          desc='')
    out_slat_span_in = Float(iotype='in', xmltag='Out_Slat_Span_In',
                             desc='')
    out_slat_span_out = Float(iotype='in', xmltag='Out_Slat_Span_Out',
                              desc='')
    out_slat_chord = Float(iotype='in', xmltag='Out_Slat_Chord',
                           desc='')
    deflect_on_off = Bool(iotype='in', xmltag='Deflect_On_Off',
                          desc='')
    deflect_name = Str(iotype='in', xmltag='Deflect_Name',
                       desc='')
    deflect_scale = Float(iotype='in', xmltag='Deflect_Scale',
                          desc='')
    deflect_twist_scale = Float(iotype='in', xmltag='Deflect_Twist_Scale',
                                desc='')
    strake_aft_flag = Bool(iotype='in', xmltag='Strake_Aft_Flag',
                           desc='')
# TODO: handle array.
    deflect_pnts = Str(iotype='in', xmltag='Deflect_Pnts',
                       desc='')

    def __init__(self):
        super(WingParms, self).__init__(self.XMLTAG)


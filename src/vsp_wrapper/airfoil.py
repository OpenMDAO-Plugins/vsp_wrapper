from openmdao.lib.datatypes.api import Bool, Enum, Float, Int, Str

from vsp_wrapper.xml_container import XMLContainer

# Airfoil Types
_NACA_4_SERIES = 1
_BICONVEX      = 2
_WEDGE         = 3
_AIRFOIL_FILE  = 4
_NACA_6_SERIES = 5


class Airfoil(XMLContainer):
    """ XML parameters for an airfoil. """

    XMLTAG = 'Airfoil'

    type = Enum(iotype='in', xmltag='Type',
                values=(_NACA_4_SERIES, _BICONVEX, _WEDGE, _AIRFOIL_FILE,
                        _NACA_6_SERIES),
                aliases=('NACA 4-Series', 'Biconvex', 'Wedge', 'Airfoil File',
                         'NACA 6-Series'),
                desc='Type of airfoil.')
    invert_y = Bool(False, iotype='in', xmltag='Inverted_Flag',
                    desc='Invert Y axis.')
    camber = Float(0.0, low=0.0, high=0.1, iotype='in', xmltag='Camber',
                   desc='')
    camber_loc = Float(0.5, low=0.1, high=0.9, iotype='in', xmltag='Camber_Loc',
                       desc='')
    thickness = Float(0.1, low=0.001, high=0.5, iotype='in', xmltag='Thickness',
                      desc='')
    thickness_loc = Float(0.3, iotype='in', xmltag='Thickness_Loc',
                          desc='')
    radius_le = Float(0.01, iotype='in', xmltag='Radius_Le',
                      desc='Radius of leading edge.')
    radius_te = Float(0.0, iotype='in', xmltag='Radius_Te',
                      desc='Radius of trailing edge.')
    six_series = Int(63, iotype='in', xmltag='Six_Series',
                     desc='NACA 6-series identifier.')
    ideal_cl = Float(0.0, iotype='in', xmltag='Ideal_Cl',
                     desc='')
    a = Float(0.0, iotype='in', xmltag='A',
              desc='')

    def __init__(self, xmltag=''):
        tag = xmltag or self.XMLTAG
        super(Airfoil, self).__init__(tag)

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(Airfoil, self).read(this)

        if self.type == _AIRFOIL_FILE:
            self.add_trait('airfoil_name',
                           Str(iotype='in', xmltag='Name',
                               desc=''))
            self.read_element(this, 'airfoil_name')

            self.add_trait('original_af_thickness',
                           Float(iotype='in', xmltag='Original_AF_Thickness',
                                 desc=''))
            self.read_element(this, 'original_af_thickness')

            self.add_trait('radius_le_correction_factor',
                           Float(iotype='in',
                                 xmltag='Radius_LE_Correction_Factor',
                                 desc=''))
            self.read_element(this, 'radius_le_correction_factor')

            self.add_trait('radius_te_correction_factor',
                           Float(iotype='in',
                                 xmltag='Radius_TE_Correction_Factor',
                                 desc=''))
            self.read_element(this, 'radius_te_correction_factor')

# TODO: handle arrays.
            self.add_trait('upper_pnts',
                           Str(iotype='in', xmltag='Upper_Pnts',
                               desc=''))
            self.read_element(this, 'upper_pnts')

            self.add_trait('lower_pnts',
                           Str(iotype='in', xmltag='Lower_Pnts',
                               desc=''))
            self.read_element(this, 'lower_pnts')


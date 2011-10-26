from openmdao.lib.datatypes.api import Bool, Enum, Float, Int

from vsp_wrapper.xml_container import XMLContainer

# Drivers.
_MS_AR_TR_A  = 0
_MS_AR_TR_S  = 1
_MS_AR_TR_TC = 2
_MS_AR_TR_RC = 3
_MS_S_TC_RC  = 4
_MS_A_TC_RC  = 5
_MS_TR_S_A   = 6
_MS_AR_A_RC  = 7


class WingSect(XMLContainer):
    """ XML parameters for one section of a multi-section wing. """

    XMLTAG = 'Section'

    driver = Enum(_MS_AR_TR_S, iotype='in', xmltag='Driver',
                  values=(_MS_AR_TR_A, _MS_AR_TR_S, _MS_AR_TR_TC, _MS_AR_TR_RC,
                          _MS_S_TC_RC, _MS_A_TC_RC, _MS_TR_S_A, _MS_AR_A_RC),
                  aliases=('AR-TR-Area', 'AR-TR-Span', 'AR-TR-TC', 'AR-TR-RC',
                           'Span-TC-RC', 'Area-Tc-RC', 'TR-Span-Area',
                           'AR-Area-RC'),
                  desc='Scheme used for section design.')

    # Driver independents should have ranges, but when used as dependents
    # they don't necessarily stay within the independent range.

    # low=0.05, high=100.
    ar = Float(iotype='in', xmltag='AR', desc='Aspect ratio.')
    # low=0.01, high=5.
    tr = Float(iotype='in', xmltag='TR', desc='Taper ratio.')
    # low=0.001, high=1000000.
    area = Float(iotype='in', xmltag='Area', desc='')
    # low=0.001, high=1000000.
    span = Float(iotype='in', xmltag='Span', desc='')
    # low=0.001, high=10000.
    tc = Float(iotype='in', xmltag='TC', desc='Tip chord.')
    # low=0.001, high=10000.
    rc = Float(iotype='in', xmltag='RC', desc='Root chord.')

    sweep = Float(10.0, low=-85., high=85., units='deg', iotype='in',
                  xmltag='Sweep', desc='')
    sweep_loc = Float(0.0, low=0., high=1., iotype='in', xmltag='SweepLoc',
                      desc='')

    twist = Float(0.0, low=-45., high=45., units='deg', iotype='in',
                  xmltag='Twist', desc='')
    twist_loc = Float(0.0, low=0., high=1., iotype='in', xmltag='TwistLoc',
                      desc='')

    dihedral = Float(0.0, low=-360., high=360., units='deg', iotype='in',
                     xmltag='Dihedral', desc='')
    dihed_crv1 = Float(0.0, low=0., high=1., iotype='in', xmltag='Dihed_Crv1',
                       desc='')
    dihed_crv2 = Float(0.0, low=0., high=1., iotype='in', xmltag='Dihed_Crv2',
                       desc='')
    dihed_crv1_str = Float(0.75, low=0., high=2., iotype='in',
                           xmltag='Dihed_Crv1_Str', desc='')
    dihed_crv2_str = Float(0.75, low=0., high=2., iotype='in',
                           xmltag='Dihed_Crv2_Str', desc='')
    dihedRotFlag = Bool(False, iotype='in', xmltag='DihedRotFlag',
                        desc='')
    smoothBlendFlag = Bool(False, iotype='in', xmltag='SmoothBlendFlag',
                           desc='')
    num_interp_xsecs = Int(1, iotype='in', xmltag='NumInterpXsecs',
                           desc='')

    def __init__(self):
        super(WingSect, self).__init__(self.XMLTAG)


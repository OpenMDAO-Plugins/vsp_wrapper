from openmdao.lib.datatypes.api import Float

from vsp_wrapper.component     import VSPComponent
from vsp_wrapper.xml_container import XMLContainer


class Havoc(VSPComponent):
    """ Input for Hypersonic Aircraft Vehicle Optimization Code. """

    XMLTYPE = 'Havoc'

    def __init__(self):
        super(Havoc, self).__init__()
        self.add('havoc_parms', HavocParms())

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(Havoc, self).read(this)

        parms = this.find(HavocParms.XMLTAG)
        if parms is None:
            self.raise_exception('No %s element!?' % HavocParms.XMLTAG)
        self.havoc_parms.read(parms)

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(Havoc, self).write(parent, nesting)
        self.havoc_parms.write(this, nesting+1)
        return this


class HavocParms(XMLContainer):
    """ XML parameters for HAVAC input. """

    XMLTAG = 'Havoc_Parms'

    length = Float(25., low=1., high=1000., iotype='in', xmltag='Length',
                   desc='Planform length.')
    al = Float(0.25, low=0.01, high=1., iotype='in', xmltag='Al',
               desc='Width left.')
    ar = Float(0.25, low=0.01, high=1., iotype='in', xmltag='Ar',
               desc='Width right.')
    apm = Float(1.7, low=0.01, high=10., iotype='in', xmltag='Apm',
                desc='Planform M exponent')
    apn = Float(2.3, low=0.01, high=10., iotype='in', xmltag='Apn',
                desc='Planform N exponent.')
    lpiovl = Float(0.5, low=0.01, high=0.99, iotype='in', xmltag='Lpiovl',
                   desc='Planform break point.')
    pera = Float(0.5, low=0., high=2., iotype='in', xmltag='Pera',
                 desc='Rear width fraction.')

    mexp1 = Float(2., low=0.01, high=10., iotype='in', xmltag='Mexp1',
                  desc='Xsec M exponent 1.')
    nexp1 = Float(2., low=0.01, high=10., iotype='in', xmltag='Nexp1',
                  desc='Xsec N exponent 1.')
    mexp2 = Float(2., low=0.01, high=10., iotype='in', xmltag='Mexp2',
                  desc='Xsec M exponent 2.')
    nexp2 = Float(2., low=0.01, high=10., iotype='in', xmltag='Nexp2',
                  desc='Xsec N exponent 2.')
    mexp3 = Float(2., low=0.01, high=10., iotype='in', xmltag='Mexp3',
                  desc='Xsec M exponent 3.')
    nexp3 = Float(2., low=0.01, high=10., iotype='in', xmltag='Nexp3',
                  desc='Xsec N exponent 3.')
    mexp4 = Float(2., low=0.01, high=10., iotype='in', xmltag='Mexp4',
                  desc='Xsec M exponent 4.')
    nexp4 = Float(2., low=0.01, high=10., iotype='in', xmltag='Nexp4',
                  desc='Xsec N exponent 4.')

    pln = Float(0.4, low=0.01, high=0.99, iotype='in', xmltag='Pln',
                desc='Nose length fraction.')
    ple = Float(0.2, low=0.01, high=0.99, iotype='in', xmltag='Ple',
                desc='Engine length fraction')
    bu = Float(0.2, low=0.01, high=10., iotype='in', xmltag='Bu',
               desc='Height upper.')
    bl = Float(0.1, low=0.01, high=1., iotype='in', xmltag='Bl',
               desc='Height lower.')
    mu = Float(2., low=0.01, high=10., iotype='in', xmltag='Mu',
               desc='Xsec M upper exponent.')
    nu = Float(2., low=0.01, high=10., iotype='in', xmltag='Nu',
               desc='Xsec N upper exponent.')
    ml = Float(2., low=0.01, high=10., iotype='in', xmltag='Ml',
               desc='Xsec M lower exponent.')
    nl = Float(2., low=0.01, high=10., iotype='in', xmltag='Nl',
               desc='Xsec N lower exponent.')
    gum = Float(1.4, low=0.01, high=10., iotype='in', xmltag='Gum',
                desc='Upper rear shape factor.')
    theta = Float(40.5, low=0., high=80., units='deg', iotype='in',
                  xmltag='Theta', desc='Engine exit angle.')
    ptas = Float(0.4, low=0., high=1., iotype='in', xmltag='Ptas',
                 desc='Exit center height.')
    bue = Float(0.1, low=0., high=1., iotype='in', xmltag='Bue',
                desc='Exit height upper.')
    ble = Float(0.1, low=0., high=1., iotype='in', xmltag='Ble',
                desc='Exit height lower.')

    aum = Float(3., low=0.01, high=10., iotype='in', xmltag='Aum',
                desc='Side M upper exponent.')
    aun = Float(1., low=0.01, high=10., iotype='in', xmltag='Aun',
                desc='Side N upper exponent.')
    alm = Float(1.7, low=0.01, high=10., iotype='in', xmltag='Alm',
                desc='"Side M lower exponent.')
    aln = Float(1.3, low=0.01, high=10., iotype='in', xmltag='Aln',
                desc='Side N lower exponent.')

    def __init__(self):
        super(HavocParms, self).__init__(self.XMLTAG)


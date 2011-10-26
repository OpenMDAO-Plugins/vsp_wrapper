from openmdao.lib.datatypes.api import Float

from vsp_wrapper.component     import VSPComponent
from vsp_wrapper.xml_container import XMLContainer


class User(VSPComponent):
    """ User parameters. """

    XMLTYPE = 'User'

    def __init__(self):
        super(User, self).__init__()
        self.add('user_parms', UserParms())

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        VSPComponent.read(self, this)
        parms = this.find(UserParms.XMLTAG)
        if parms is None:
            self.raise_exception('No %s element!?' % UserParms.XMLTAG,
                                 ValueError)
        self.user_parms.read(parms)

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = VSPComponent.write(self, parent, nesting)
        self.user_parms.write(this, nesting+1)
        return this


class UserParms(XMLContainer):
    """ XML parameters specific to a Wing. """

    XMLTAG = 'User_Parms'

    user_1 = Float(iotype='in', xmltag='User1', desc='')
    user_2 = Float(iotype='in', xmltag='User2', desc='')
    user_3 = Float(iotype='in', xmltag='User3', desc='')
    user_4 = Float(iotype='in', xmltag='User4', desc='')
    user_5 = Float(iotype='in', xmltag='User5', desc='')
    user_6 = Float(iotype='in', xmltag='User6', desc='')
    user_7 = Float(iotype='in', xmltag='User7', desc='')
    user_8 = Float(iotype='in', xmltag='User8', desc='')

    def __init__(self):
        super(UserParms, self).__init__(self.XMLTAG)


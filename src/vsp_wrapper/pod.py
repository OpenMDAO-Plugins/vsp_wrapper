from openmdao.lib.datatypes.api import Float

from vsp_wrapper.component     import VSPComponent
from vsp_wrapper.xml_container import XMLContainer


class Pod(VSPComponent):
    """ A pod. """

    XMLTYPE = 'Pod'

    def __init__(self):
        super(Pod, self).__init__()
        self.add('pod_parms', PodParms())

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(Pod, self).read(this)

        parms = this.find(PodParms.XMLTAG)
        if parms is None:
            self.raise_exception('No %s element!?' % PodParms.XMLTAG)
        self.pod_parms.read(parms)

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(Pod, self).write(parent, nesting)
        self.pod_parms.write(this, nesting+1)
        return this


class PodParms(XMLContainer):
    """ XML parameters specific to a pod. """

    XMLTAG = 'Pod_Parms'

    length = Float(10.0, low=0.1, high=100., iotype='in', xmltag='Length',
                   desc='')
    fine_ratio = Float(15., low=2., high=50., iotype='in', xmltag='Fine_Ratio',
                       desc='')

    def __init__(self):
        super(PodParms, self).__init__(self.XMLTAG)


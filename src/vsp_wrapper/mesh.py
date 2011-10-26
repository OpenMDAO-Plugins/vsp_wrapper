import xml.etree.cElementTree as ElementTree

from openmdao.lib.datatypes.api import Int

from vsp_wrapper.component     import VSPComponent
from vsp_wrapper.xml_container import XMLContainer


class Mesh(VSPComponent):
    """ Meshed geometry. """

    XMLTYPE = 'Mesh'

    def __init__(self):
        super(Mesh, self).__init__()
        self.add('mesh_parms', MeshParms())

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(Mesh, self).read(this)

        parms = this.find(MeshParms.XMLTAG)
        if parms is None:
            self.raise_exception('No %s element!?' % MeshParms.XMLTAG)
        self.mesh_parms.read(parms)

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(Mesh, self).write(parent, nesting)
        self.mesh_parms.write(this, nesting+1)
        return this


class MeshParms(XMLContainer):
    """ XML parameters specific to a Mesh. """

    XMLTAG = 'Mesh_Parms'

    num_tris = Int(0, iotype='in', xmltag='Num_Tris',
                   desc='Number of triangles in mesh.')

    def __init__(self):
        super(MeshParms, self).__init__(self.XMLTAG)
        self._tris = []

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(MeshParms, self).read(this)

        tri_list = this.find('Tri_List')
        if tri_list is None:
            self.raise_exception('No Tri_List!?', RuntimeError)
        tris = tri_list.findall('Tri')
        for element in tris:
            self._tris.append(element.text)

    def write(self, parent, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(MeshParms, self).write(parent, nesting)

        tri_list = ElementTree.Element('Tri_List')
        tri_list.text = self.tail(nesting+2)
        tri_list.tail = self.tail(nesting+1)
        child_tail = self.tail(nesting+2)
        for tri in self._tris:
            child = ElementTree.Element('Tri')
            child.text = tri
            child.tail = child_tail
            tri_list.append(child)
        this.append(tri_list)

        return this


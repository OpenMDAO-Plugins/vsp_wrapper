import xml.etree.cElementTree as ElementTree

from openmdao.lib.datatypes.api import Bool, Float, Int, Str

from vsp_wrapper.blank         import Blank
from vsp_wrapper.cabin         import CabinLayout
from vsp_wrapper.component     import VSPComponent
from vsp_wrapper.duct          import Duct
from vsp_wrapper.engine        import Engine
from vsp_wrapper.external      import External
from vsp_wrapper.fuselage      import Fuselage
from vsp_wrapper.fuselage2     import Fuselage2
from vsp_wrapper.havoc         import Havoc
from vsp_wrapper.hwb           import HWB
from vsp_wrapper.mesh          import Mesh
from vsp_wrapper.ms_wing       import MSWing
from vsp_wrapper.pod           import Pod
from vsp_wrapper.prop          import Prop
from vsp_wrapper.user          import User
from vsp_wrapper.window        import VirtWindow
from vsp_wrapper.wing          import Wing
from vsp_wrapper.xml_container import XMLContainer, XLATE


# Map from component 'Type' element to class.
_REGISTRY = {}

def _register(cls):
    """ Register `cls` with geometry reader. """
    _REGISTRY[cls.XMLTYPE] = cls

_register(Blank)
_register(CabinLayout)
_register(Duct)
_register(Engine)
_register(External)
_register(Fuselage)
_register(Fuselage2)
_register(Havoc)
_register(HWB)
_register(Mesh)
_register(MSWing)
_register(Pod)
_register(Prop)
_register(User)
_register(Wing)


class VSPGeometry(XMLContainer):
    """ XML parameters for a vehicle. """

    XMLTAG = 'Vsp_Geometry'

    version = Int(3, iotype='in', xmltag='Version',
                  desc='')
    geom_name = Str('Aircraft', iotype='in', xmltag='Name',
                    desc='')
    cg_rel_ac_flag = Bool(False, iotype='in', xmltag='CG_Rel_AC_Flag',
                          desc='')
    cg_x = Float(10.0, iotype='in', xmltag='CG_X',
                 desc='')
    cg_y = Float(0.0, iotype='in', xmltag='CG_Y',
                 desc='')
    cg_z = Float(0.0, iotype='in', xmltag='CG_Z',
                 desc='')
    cfd_mesh_base_length = Float(0.5, iotype='in', xmltag='CFD_Mesh_Base_Length',
                                 desc='')

    def __init__(self):
        super(VSPGeometry, self).__init__(self.XMLTAG)
        self._virt_windows = []
        self._components = []

    def read(self, this):
        """ Read parameters from XML tree element `this`. """
        super(VSPGeometry, self).read(this)

        virt_window_list = this.find('VirtWindow_List')
        if virt_window_list:
            virt_windows = virt_window_list.findall(VirtWindow.XMLTAG)
            for i, element in enumerate(virt_windows):
                name = '%s_%d' % (VirtWindow.XMLTAG, i)
                virt_window = self.add(name, VirtWindow())
                virt_window.read(element)
                self._virt_windows.append(virt_window)
        else:  # Must be from an older version of VSP.
            self._logger.warning('No VirtWindow_List')

        # Scan components to create precedence order.
        component_list = this.find('Component_List')
        if component_list is None:
            self.raise_exception('No Component_List!?', RuntimeError)
        components = component_list.findall(VSPComponent.XMLTAG)
        user_element = None
        precedence_list = []
        for element in components:
            typ = element.findtext('Type')
            if typ is None:
                self.throw(RuntimeError, 'No component Type!?')

            if typ == User.XMLTYPE:
                # Not part of precedence list.
                user_element = element
                continue

            parms = element.find('General_Parms')
            if parms is None:
                self.raise_exception('No component General_Parms!?', RuntimeError)
            ptr_id = parms.findtext('PtrID')
            if ptr_id is None:
                self.raise_exception('No component PtrID!?', RuntimeError)

            parent_id = parms.findtext('Parent_PtrID')
            if parent_id is None:
                self.raise_exception('No component Parent_PtrID!?', RuntimeError)

            for i, info in enumerate(precedence_list):
                if info[1] == parent_id:  # This comp is child.
                    precedence_list.insert(i+1, (element, ptr_id, parent_id))
                    break
                elif info[2] == ptr_id:   # This comp is parent.
                    precedence_list.insert(i, (element, ptr_id, parent_id))
            else:
                precedence_list.append((element, ptr_id, parent_id))

        if user_element is not None:
            precedence_list.append((user_element, None, '0'))

        # Add components in precedence order.
        parent_map = {}
        for element, ptr_id, parent_id in precedence_list:
            typ = element.findtext('Type')
            if typ == User.XMLTYPE:
                name = 'User'
            else:
                parms = element.find('General_Parms')
                name = parms.findtext('Name')
                if name is None:
                    self.raise_exception('No component Name!?', RuntimeError)
                name = name.translate(XLATE)

            # Find parent component.
            if parent_id == '0':
                parent = self
            else:
                try:
                    parent = parent_map[parent_id]
                except KeyError:
                    self.raise_exception('Cannot find parent!', RuntimeError)

            # Read component data.
            try:
                comp = self.add(name, _REGISTRY[typ]())
            except KeyError:
                self.throw(RuntimeError, 'Unexpected type %s', typ)

            comp.read(element)
            parent_map[ptr_id] = comp
            self._components.append(comp)

    def write(self, root, nesting=0):
        """
        Write parameters to XML tree under `parent`.
        Returns tree element.
        """
        this = super(VSPGeometry, self).write(root, nesting)

        virt_window_list = ElementTree.Element('VirtWindow_List')
        virt_window_list.text = self.tail(nesting+2)
        virt_window_list.tail = self.tail(nesting+1)
        for virt_window in self._virt_windows:
            virt_window.write(virt_window_list, nesting+2)
        this.append(virt_window_list)

        component_list = ElementTree.Element('Component_List')
        component_list.text = self.tail(nesting+2)
        component_list.tail = self.tail(nesting+1)
        for component in self._components:
            component.write(component_list, nesting+2)
        this.append(component_list)

        label_list = ElementTree.Element('Label_List')
        label_list.text = self.tail(nesting+2)
        label_list.tail = self.tail(nesting+1)
        this.append(label_list)

        parm_link_list = ElementTree.Element('ParmLink_List')
        parm_link_list.text = self.tail(nesting+2)
        parm_link_list.tail = self.tail(nesting+1)
        this.append(parm_link_list)

        return this


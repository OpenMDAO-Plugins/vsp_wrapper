import os
from openmdao.main.interfaces import implements, IParametricGeometry
from openmdao.lib.geometry.stl import STLGeometryObject
from openmdao.lib.components.external_code import ExternalCode
from vsp_wrapper.wrapper import VSP

from pyV3D.stl import STLSender

from traits.trait_base import not_none


class VSPParametricGeometry(object):
    implements(IParametricGeometry)
    
    def __init__(self):
        self._callbacks = []
        self._model_file = None
        self._vsp = None
        self._excludes = set(['xml_filename', 'write_stereo'])
        base = ExternalCode()
        for key, val in base.items(iotype=not_none):
            self._excludes.add(key)

    @property
    def model_file(self):
        return self._model_file

    @model_file.setter
    def model_file(self, fname):
        self.load_model(os.path.expanduser(fname))

    def load_model(self, fpath):
        self._vsp = VSP(fpath)
        self._vsp.write_stereo = True
        self._vsp.cpath_updated()
        self._model_file = fpath
        self.invoke_callbacks()

    def regen_model(self):
        if self._vsp is not None:
            self._vsp.run()
            if self._vsp.return_code != 0:
                raise RuntimeError("VSP had a return code of %d" % self._vsp.return_code)

    def list_parameters(self):
        params = []
        if self._vsp is not None:
            for key, val in self._vsp.items(iotype=not_none, recurse=True):
                if key in self._excludes:
                    continue
                meta = self._vsp.get_metadata(key)
                meta['value'] = val
                del meta['type'] # this is always 'trait' and confuses geomcomp
                params.append((key, meta))
        return params

    def set_parameter(self, name, value):
        self._vsp.set(name, value)

    def get_parameters(self, names):
        if self._vsp is None:
            return []
        get = self._vsp.get
        return [get(n) for n in names]

    def get_static_geometry(self):
        if self._model_file is None:
            return None
        parts = os.path.splitext(self.model_file)
        if self.model_file.lower().endswith('vsp'):
            stl = parts[0]+'.stl'
        else:
            stl = self.model_file+'.new.stl'
        return STLGeometryObject(stl)
    
    def register_param_list_changedCB(self, callback):
        """Register a callback that will be called when self.invoke_callbacks() is called.
        self.invoke_callbacks() should be called from the inheriting class whenever any
        parameters are added, removed, or change their type.
        """
        self._callbacks.append(callback)

    def invoke_callbacks(self):
        """Invokes any callbacks that have been registered via register_param_list_changedCB."""

        for cb in self._callbacks:
            cb()

    def get_attributes(self, io_only=True):
        """Return an attribute dict for use by the openmdao GUI.
        """
        
        return {
            'type': type(self).__name__,
            'Inputs': [
                {
                    'name': 'model_file',
                    'id': 'model_file',
                    'type': type(self._model_file).__name__,
                    'value': self._model_file,
                    'connected': '',
                }
            ]
        }


class VSPSender(STLSender):

    @staticmethod
    def supports(obj):
        if isinstance(obj, (VSPParametricGeometry, STLGeometryObject)):
            return True

    def geom_from_obj(self, obj):
        if isinstance(obj, VSPParametricGeometry):
            obj = obj.get_static_geometry()
        super(VSPSender, self).geom_from_obj(obj)


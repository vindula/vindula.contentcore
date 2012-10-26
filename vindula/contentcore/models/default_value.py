# -*- coding: utf-8 -*-

from storm.locals import *
from storm.locals import Store

from vindula.contentcore.base import BaseStore
        
    
class ModelsDefaultValue(Storm, BaseStore):
    __storm_table__ = 'vin_contentcore_default_value'
    
    id = Int(primary=True)
    value = Unicode()
    lable = Unicode()
    
    def get_DefaultValues(self):
        data = self.store.find(ModelsDefaultValue).order_by(Desc(ModelsDefaultValue.lable))
        if data.count() > 0:
            return data
        else:
            return []
    
    def get_DefaultValue_byId(self, id):
        data = self.store.find(ModelsDefaultValue, ModelsDefaultValue.id==int(id)).one()
        if data:
            return data
        else:
            return None

    def set_DefaultValue(self,**kwargs):
        # adicionando...
        default = ModelsDefaultValue(**kwargs)
        self.store.add(default)
        self.store.flush()

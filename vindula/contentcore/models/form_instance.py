# -*- coding: utf-8 -*-

from storm.locals import *
from storm.locals import Store


from vindula.contentcore.base import BaseStore

from storm.expr import Desc
from datetime import datetime, timedelta

    
class ModelsFormInstance(Storm, BaseStore):
    __storm_table__ = 'vin_contentcore_form_instance'
    __storm_primary__ = "instance_id", "forms_id"
        
    instance_id = Int()
    forms_id = Int() 
    date_creation = DateTime()
    
    def set_FormInstance(self,id):
        D={}
        D['forms_id'] = int(id)
        # adicionando...
        instance = ModelsFormInstance(**D)
        self.store.add(instance)
        self.store.flush()
        return instance.instance_id    
    
    def get_Instance(self,id_form):
        data = self.store.find(ModelsFormInstance, ModelsFormInstance.forms_id==id_form
                               ).order_by(Desc(ModelsFormInstance.date_creation))
        
        if data.count()>0:
            return data
        else:
            return []
    
    def del_Instance(self, form_id, id_instance):
        results = self.store.find(ModelsFormInstance, ModelsFormInstance.forms_id==form_id,
                                                      ModelsFormInstance.instance_id==id_instance).one()
        if results:
            self.store.remove(results)
            self.store.flush()   
    
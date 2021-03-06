# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from storm.expr import Desc
from storm.locals import *
from vindula.contentcore.base import BaseStore


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
    
    def get_Instance(self,id_form,getall=False):
        datahora = datetime.now()-timedelta(days=7)
        data = self.store.find(ModelsFormInstance, ModelsFormInstance.forms_id==id_form,
                              ).order_by(Desc(ModelsFormInstance.date_creation))
        if data.count()>0:
            if getall:
                return data
            
            return data.find(ModelsFormInstance.date_creation >= datahora)
           
        else:
            return []
    
    def del_Instance(self, form_id, id_instance):
        results = self.store.find(ModelsFormInstance, ModelsFormInstance.forms_id==form_id,
                                                      ModelsFormInstance.instance_id==id_instance).one()
        if results:
            self.store.remove(results)
            self.store.flush()   
    
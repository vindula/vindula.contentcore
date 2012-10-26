# -*- coding: utf-8 -*-

from storm.locals import *
from storm.locals import Store


from vindula.contentcore.base import BaseStore




class ModelsParametersForm(Storm, BaseStore):
    __storm_table__ = 'vin_contentcore_parameters'
    
    id = Int(primary=True)
    forms_id = Int()
    fields_id = Int()
    
    parameters = Unicode()
    value_parameters = Unicode()
    
    def get_ParametersForm(self):
        data = self.store.find(ModelsParametersForm)
        if data.count() > 0:
            return data
        else:
            return []
    
    def get_ParametersForm_byId(self, id):
        data = self.store.find(ModelsParametersForm, ModelsParametersForm.id==int(id)).one()
        if data:
            return data
        else:
            return None
        
    def get_ParametersForm_byFormId(self, form_id):
        data = self.store.find(ModelsParametersForm, ModelsParametersForm.forms_id==form_id)
        if data.count() > 0:
            return data
        else:
            return []
        
    def del_ParametersForm(self, form_id):
        results = self.store.find(ModelsParametersForm, ModelsParametersForm.forms_id==form_id)
        if results:
            for result in results:
                self.store.remove(result)
                self.store.flush()   


    def set_ParametersFor(self,**kwargs):
        # adicionando...
        parameter = ModelsParametersForm(**kwargs)
        self.store.add(parameter)
        self.store.flush()
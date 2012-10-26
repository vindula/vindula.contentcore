# -*- coding: utf-8 -*-

from storm.locals import *
from storm.locals import Store


from vindula.contentcore.base import BaseStore


    
class ModelsConfigImport(Storm, BaseStore):
    __storm_table__ = 'vin_contentcore_configImport'

    id = Int(primary=True)
    forms_id = Int()
    fields = Unicode()
    campo_csv = Unicode() 
    date_creation = DateTime()
     

    def set_ConfigImport(self,**kwargs):
        # adicionando...
        confg = ModelsConfigImport(**kwargs)
        self.store.add(confg)
        self.store.flush()

    def update_ConfigImport(self,forms_id,fields,campo_csv):
        result = self.get_Config_byIdForm_and_Field(forms_id, fields)
        if result:
            result.campo_csv = campo_csv
            self.store.commit()
        
        
    
    def get_Config_byIdForm_and_Field(self,id_form,field):
        data = self.store.find(ModelsConfigImport, ModelsConfigImport.fields==field,
                                                 ModelsConfigImport.forms_id==id_form).one()
        if data:
            return data
        else:
            return None
    
    
    def get_Config_byIdForm(self,id_form):
        data = self.store.find(ModelsConfigImport, ModelsConfigImport.forms_id==id_form)
        if data.count() > 0:
            return data
        else:
            return []


    
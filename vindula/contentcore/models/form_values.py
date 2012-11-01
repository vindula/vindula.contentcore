# -*- coding: utf-8 -*-

from storm.locals import *
from storm.locals import Store

from datetime import datetime

from vindula.contentcore.base import BaseStore
from vindula.contentcore.models.log import ModelsLog



class ModelsFormValues(Storm, BaseStore):
    __storm_table__ = 'vin_contentcore_form_values'
    
    id = Int(primary=True)
    value = Unicode()
    value_blob = Pickle()
    date_creation = DateTime()
    
    forms_id = Int()
    instance_id = Int()
    fields = Unicode()
    
    instancia = Reference(instance_id, "ModelsFormInstance.instance_id")
    
    def set_FormValues(self,**kwargs):
        # adicionando...
        values = ModelsFormValues(**kwargs)
        self.store.add(values)
        self.store.flush()


    def update_form_value(self,id_form, id_instance, valor,campo):
        result = self.get_FormValues_byForm_and_Instance_and_Field(id_form,id_instance,campo)
        if result:
            D={}
            D['valor_old'] = result.value or u'Campo em Blob'
            D['instance_id'] = id_instance
            D['forms_id'] =  id_form
            D['fields'] = campo
            
            
            if type(valor) != bool:
                if len(valor) < 65000:
                    D['valor_new'] = self.Convert_utf8(valor.strip())
                    result.value = self.Convert_utf8(valor.strip())
                    result.value_blob = None
            
                else:
                    result.value_blob = valor   
                    result.value = None 
                    D['valor_new'] = u'Campo em Blob'
            
            else:
                D['valor_new'] = self.Convert_utf8(valor)
                result.value = self.Convert_utf8(valor)
                
            if D['valor_new'] != D['valor_old']:
                ModelsLog().set_log(**D)  
            
            result.date_creation = datetime.now()
            self.store.commit()
            
        else:
            self.set_form_value(id_form, id_instance, valor, campo)
                                            

    def set_form_value(self,id_form, id_instance, valor,campo):
        D = {}
        D['forms_id'] = id_form
        D['instance_id'] = id_instance
        D['fields'] = campo
                                            
        if type(valor) != bool:
            if len(valor) < 65000:
                D['value'] = self.Convert_utf8(valor.strip())
                D['value_blob'] = None
                
            else:
                D['value'] = None
                D['value_blob'] = valor
        else:
            D['value'] = self.Convert_utf8(valor)
            
        ModelsFormValues().set_FormValues(**D)
        
        D['valor_new'] = D['value'] or u'Campo em Blob'
        D['valor_old'] = None
        
        D.pop('value')
        D.pop('value_blob')
        
        ModelsLog().set_log(**D)
         

    def get_Values_byID(self,id):
        data = self.store.find(ModelsFormValues, ModelsFormValues.id==int(id)).one()
        if data:
            return data
        else:
            return None

    def get_FormValues_byForm_and_Instance_and_Field(self, id_form, id_instance,field):
        data = self.store.find(ModelsFormValues, ModelsFormValues.forms_id==id_form,
                                                 ModelsFormValues.instance_id==id_instance,
                                                 ModelsFormValues.fields==field).one()
        if data:
            return data
        else:
            return None

    def get_FormValues_byForm_and_Field(self, id_form,field):
        data = self.store.find(ModelsFormValues, ModelsFormValues.forms_id==id_form,
                                                 ModelsFormValues.fields==field)
        if data.count() > 0:
            return data
        else:
            return []
        
    def  get_FormValues_byForm_and_Field_and_Value(self, id_form,field,value):
        data = self.store.find(ModelsFormValues, ModelsFormValues.forms_id==id_form,
                                                 ModelsFormValues.fields==field,
                                                 ModelsFormValues.value==value).one()
        if data:
            return data
        else:
            return None           
    

        
    def get_FormValues_byForm_and_Instance(self, id_form, id_instance):
        data = self.store.find(ModelsFormValues, ModelsFormValues.forms_id==id_form,
                                                 ModelsFormValues.instance_id==id_instance)
        if data.count()>0:
            return data
        else:
            return []
        
    def get_FormValues_byForm(self, id_form):
        data = self.store.find(ModelsFormValues, ModelsFormValues.forms_id==id_form)
        if data.count()>0:
            return data
        else:
            return []
        
        
        

    def Convert_utf8(self,valor):
        try: 
            return unicode(valor,'utf-8')
        except UnicodeDecodeError:
            return valor.decode("utf-8", "ignore")
        except:
            if type(valor) == unicode:
                return valor
            else:
                return u'erro ao converter os caracteres'
        
# -*- coding: utf-8 -*-

from storm.locals import *
from storm.locals import Store
from Products.statusmessages.interfaces import IStatusMessage
from vindula.contentcore import MessageFactory as _

from vindula.myvindula.user import BaseStore
from datetime import date , datetime 

#models
class ModelsForm(Storm, BaseStore):
    __storm_table__ = 'vin_contentcore_forms'
    
    id = Int(primary=True)
    name_form = Unicode()
    description_form = Unicode()
    date_creation = DateTime() 
    
    fields = ReferenceSet(id, "ModelsFormFields.forms_id")
    instancias = ReferenceSet(id, "ModelsFormInstance.forms_id")
    
    def get_Forms(self):
        data = self.store.find(ModelsForm).order_by(Desc(ModelsForm.date_creation))
        if data.count() > 0:
            return data
        else:
            return None
    
    def get_Forns_byId(self, id):
        data = self.store.find(ModelsForm, ModelsForm.id==int(id)).one()
        if data:
            return data
        else:
            return None

    def get_FormValues(self,id_form):
        L=[] 
        inst = ModelsFormInstance().get_Instance(id_form)
        for item in inst: 
            data = self.store.find(ModelsFormValues, ModelsFormValues.forms_id==int(item.forms_id),
                                                     ModelsFormValues.instance_id==int(item.instance_id))
            if data.count()>0:
                L.append(data)
        
        return L
        

    def set_Form(self,**kwargs):
        # adicionando...
        form = ModelsForm(**kwargs)
        self.store.add(form)
        self.store.flush()
        return form.id       
    
    def get_NextForm(self):
        table = 'vin_contentcore_forms'
        data = self.store.execute("SELECT Auto_increment FROM information_schema.tables WHERE table_name='%s'AND table_schema = DATABASE();"%(table))

        if data.rowcount != 0:
            x = data.get_one()
            return int(x[0])
       
    
class ModelsFormFields(Storm, BaseStore):
    __storm_table__ = 'vin_contentcore_fields'
    
    id = Int(primary=True)
    name_field = Unicode() 
    type_fields =  Unicode()
    list_values = Unicode()
    date_creation = DateTime()
    title = Unicode()
    value_default = Unicode()
    description_fields = Unicode()
    ordenacao = Int()
    required = Bool()
    flag_ativo = Bool()
    forms_id = Int()
    
    
    def set_FormFields(self,**kwargs):
        # adicionando...
        fields = ModelsFormFields(**kwargs)
        self.store.add(fields)
        self.store.flush()
        #return form.id       

    def get_Fields_byIdField(self, id):
        data = self.store.find(ModelsFormFields, ModelsFormFields.id==id).one()
        if data:
            return data
        else:
            return None
        
    def get_Fields_byId(self, id_form,id_fields):
        data = self.store.find(ModelsFormFields, ModelsFormFields.id==id_fields,
                                                 ModelsFormFields.forms_id==id_form).one()
        if data:
            return data
        else:
            return None
        
    def get_Fields_ByIdForm(self,id_form):
        data = self.store.find(ModelsFormFields, ModelsFormFields.forms_id==id_form).order_by(ModelsFormFields.ordenacao)
        if data:
            return data
        else:
            return None
    
    
    def check_fields(self,campo,form):
        data = self.store.find(ModelsFormFields, ModelsFormFields.name_field==campo,
                                                 ModelsFormFields.forms_id==form)
        if data.count()>0:
            return False
        else:
            return True
        

    
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
        data = self.store.find(ModelsFormInstance, ModelsFormInstance.forms_id==id_form)
        if data.count()>0:
            return data
        else:
            return []
    
    
class ModelsFormValues(Storm, BaseStore):
    __storm_table__ = 'vin_contentcore_form_values'
    
    id = Int(primary=True)
    value = Unicode()
    value_blob = Pickle()
    date_creation = DateTime()
    
    forms_id = Int()
    instance_id = Int()
    fields = Unicode()
    
    def set_FormValues(self,**kwargs):
        # adicionando...
        values = ModelsFormValues(**kwargs)
        self.store.add(values)
        self.store.flush()

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

        
    def get_FormValues_byForm_and_Instance(self, id_form, id_instance):
        data = self.store.find(ModelsFormValues, ModelsFormValues.forms_id==id_form,
                                                 ModelsFormValues.instance_id==id_instance)
        if data.count()>0:
            return data
        else:
            return None
        
    def get_FormValues_byForm(self, id_form):
        data = self.store.find(ModelsFormValues, ModelsFormValues.forms_id==id_form)
        if data.count()>0:
            return data
        else:
            return None

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
            return None
        
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

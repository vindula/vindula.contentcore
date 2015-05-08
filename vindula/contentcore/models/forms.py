# -*- coding: utf-8 -*-

from storm.locals import *
from storm.locals import Store


from vindula.contentcore.base import BaseStore

from vindula.contentcore.models.form_values import ModelsFormValues
from vindula.contentcore.models.form_instance import ModelsFormInstance

from storm.expr import Desc

class ModelsForm(Storm, BaseStore):
    __storm_table__ = 'vin_contentcore_forms'
    
    id = Int(primary=True)
    name_form = Unicode()
    description_form = Unicode()
    uid_form = Unicode()
    date_creation = DateTime() 
    campo_label = Unicode()
    campo_chave = Unicode()
    
    
    fields = ReferenceSet(id, "ModelsFormFields.forms_id")
    instancias = ReferenceSet(id, "ModelsFormInstance.forms_id")
    
    def get_Forms(self):
        data = self.store.find(ModelsForm).order_by(Desc(ModelsForm.date_creation))
        if data.count() > 0:
            return data
        else:
            return []
    
    def get_Forns_byId(self, id):
        data = self.store.find(ModelsForm, ModelsForm.id==int(id)).one()
        if data:
            return data
        else:
            return None

    def get_FormValues(self,id_form,getall=True):
        L=[] 
        inst = ModelsFormInstance().get_Instance(id_form,getall)
        for item in inst: 
            data = self.store.find(ModelsFormValues, 
                                   ModelsFormValues.forms_id==int(item.forms_id),
                                   ModelsFormValues.instance_id==int(item.instance_id)).order_by(ModelsFormValues.date_creation)
        
            if data.count()>0:
                L.append(data)
        return L
        
    def get_FormValues_filtro(self,id_form):
        data = None
        inst = Select(ModelsFormInstance.instance_id, where=ModelsFormInstance.forms_id==id_form,distinct=True)
        if inst:
            data = self.store.find(ModelsFormValues, ModelsFormValues.forms_id==id_form,
                                                     ModelsFormValues.instance_id.is_in(inst))
            
        
        return data

    def set_Form(self,**kwargs):
        # adicionando...
        form = ModelsForm(**kwargs)
        self.store.add(form)
        self.store.flush()
        return form.id       
    
    def get_NextForm(self):
        data = self.store.find(ModelsForm).max(ModelsForm.id)
        if data:
            return data + 1
        else:
            return 1 
                        
                        
#        table = 'vin_contentcore_forms'
#        data = self.store.execute("SELECT Auto_increment FROM information_schema.tables WHERE table_name='%s'AND table_schema = DATABASE();"%(table))
#
#        if data.rowcount != 0:
#            x = data.get_one()
#            return int(x[0])
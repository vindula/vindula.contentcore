 #-*- coding: utf-8 -*-
from five import grok

from zope.app.container.interfaces import IObjectRemovedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent, IObjectCreatedEvent

from vindula.contentcore.formulario import IFormularioPadrao
from vindula.contentcore.conteudo_basico import IConteudoBasico

from vindula.contentcore.base import BaseFunc
from vindula.myvindula.user import BaseStore
from vindula.contentcore.models import ModelsForm, ModelsFormFields, ModelsFormInstance, ModelsFormValues, ModelsParametersForm


@grok.subscribe(IFormularioPadrao, IObjectRemovedEvent)
def ExcludFormDataBase(context, event):
    basestore = BaseStore()
    id_form = int(context.forms_id)
    
    record_values = ModelsFormValues().get_FormValues_byForm(id_form)
    if record_values:
        for record in record_values:
            basestore.store.remove(record)
            basestore.store.flush()   
    
    record_instances = ModelsFormInstance().get_Instance(id_form)
    if record_instances:
        for record in record_instances:
            basestore.store.remove(record)
            basestore.store.flush()

    record_parameters = ModelsParametersForm().get_ParametersForm_byFormId(id_form)
    if record_parameters:
        for record in record_parameters:
            basestore.store.remove(record)
            basestore.store.flush()
                           
    record_fields = ModelsFormFields().get_Fields_ByIdForm(id_form)
    if record_fields:
        for record in record_fields:
            basestore.store.remove(record)
            basestore.store.flush()                           
    
    record_form = ModelsForm().get_Forns_byId(id_form)
    if record_form:
        basestore.store.remove(record_form)
        basestore.store.flush()
       
@grok.subscribe(IFormularioPadrao, IObjectCreatedEvent)
def CreatFormDataBase(context, event):
    title = context.Title()
    description = context.Description()
    forms_id = context.forms_id
    
    D={}
    try:D['name_form'] = to_utf8(title)
    except:D['name_form'] = title
    
    try:D['description_form'] = to_utf8(description)
    except:D['description_form'] = description
    
    id = ModelsForm().set_Form(**D)
    if forms_id != id:
        context.forms_id = id
    
    if 'original' in event.__dict__.keys():
        org = event.original
        new = event.object
        
        fields_org = ModelsFormFields().get_Fields_ByIdForm(int(org.forms_id))

        campos = ['name_field','type_fields', 'list_values','title','value_default',\
                  'description_fields','ordenacao','required','flag_ativo']

        for item in fields_org:
            D={}
            for i in campos:
                D[i] = item.__getattribute__(i)
            
            D['forms_id'] = int(new.forms_id)

            ModelsFormFields().set_FormFields(**D)
            
        instances_org = ModelsFormInstance().get_Instance(int(org.forms_id))
        
        for instance in instances_org:
            values_instance = ModelsFormValues().get_FormValues_byForm_and_Instance(int(org.forms_id), instance.instance_id)
            
            id_inst = ModelsFormInstance().set_FormInstance(int(new.forms_id))
            
            campos_value = ['value', 'value_blob','fields'] 
            
            for value in values_instance:
                D={}
                for i in campos_value:
                    D[i] = value.__getattribute__(i)
                 
                D['forms_id'] = int(new.forms_id)
                D['instance_id'] = id_inst
                
                ModelsFormValues().set_FormValues(**D)
            

@grok.subscribe(IFormularioPadrao, IObjectModifiedEvent)
def EditFormDataBase(context, event):       
        title = context.Title()
        description = context.Description()
        forms_id = context.forms_id
        
        result = ModelsForm().get_Forns_byId(int(forms_id))
        if result:
            try:result.name_form = to_utf8(title)
            except:result.name_form = title
            
            try:result.description_form = to_utf8(description)
            except:result.description_form = description
            BaseStore().store.flush()
            
            
@grok.subscribe(IConteudoBasico, IObjectRemovedEvent)
def ExcludConteudoDataBase(context, event):
    basestore = BaseStore()
    id_form = int(context.forms_id)
    id_instance = int(context.instance_id)
    
    record_values = ModelsFormValues().get_FormValues_byForm_and_Instance(id_form,id_instance)
    if record_values:
        for record in record_values:
            basestore.store.remove(record)
            basestore.store.flush()   
    
    ModelsFormInstance().del_Instance(id_form,id_instance)    
    
    
              
            
            
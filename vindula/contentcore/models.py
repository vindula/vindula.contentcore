# -*- coding: utf-8 -*-

from storm.locals import *
from storm.locals import Store
from Products.statusmessages.interfaces import IStatusMessage
from vindula.contentcore import MessageFactory as _
from vindula.contentcore.base import BaseFunc
from vindula.contentcore.validation import valida_form

from vindula.myvindula.user import BaseStore


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
    flag_ativo = Bool()
    required = Bool()
    
    forms_id = Int()
    
    
    def set_FormFields(self,**kwargs):
        # adicionando...
        fields = ModelsFormFields(**kwargs)
        self.store.add(fields)
        self.store.flush()
        #return form.id       
        
    def get_Fields_byId(self, id_form,id_fields):
        data = self.store.find(ModelsFormFields, ModelsFormFields.id==id_fields,
                                                 ModelsFormFields.forms_id==id_form).one()
        if data:
            return data
        else:
            return None
        
    def get_Fields_ByIdForm(self,id_form):
        data = self.store.find(ModelsFormFields, ModelsFormFields.forms_id==id_form)
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
        D['instance_id'] = int(id)
        # adicionando...
        instance = ModelsFormInstance(**D)
        self.store.add(instance)
        self.store.flush()
        return instance.forms_id    
    
    def get_Instance(self,id_form):
        data = self.store.find(ModelsFormInstance, ModelsFormInstance.forms_id==id_form)
        if data.count()>0:
            return data
        else:
            return []
    
    
class ModelsFormValues(Storm, BaseStore):
    __storm_table__ = 'vin_contentcore_from_values'
    
    id = Int(primary=True)
    value = Unicode()
    date_creation = DateTime()
    
    forms_id = Int()
    instance_id = Int()
    fields = Unicode()
    
    
    def set_FormValues(self,**kwargs):
        # adicionando...
        values = ModelsFormValues(**kwargs)
        self.store.add(values)
        self.store.flush()
        
    def get_FormValues_byForm_and_Instance(self, id_form, id_instance):
        data = self.store.find(ModelsFormValues, ModelsFormValues.forms_id==id_form,
                                                 ModelsFormValues.instance_id==id_instance)
        if data.count()>0:
            return data
        else:
            return None
    
    
class RegistrationCreateForm(BaseFunc):
    def to_utf8(value):
        return unicode(value, 'utf-8')
      
    campos = {'name_form'        : {'required': True,  'type' : to_utf8, 'label':'Titulo',   'decription':u'Digite o titulo do formulario',    'ordem':0},
              'description_form' : {'required': False, 'type' : to_utf8, 'label':'Descrição','decription':u'Digite a descrição do formulario', 'ordem':1}}

                        
    def registration_processes(self,context):
        success_voltar = context.context.absolute_url() +  '/@@vindula-control-panel'
        access_denied = context.context.absolute_url() + '/login'
                
        form = context.request # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)
        campos = self.campos
        
        # divisao dos dicionarios "errors" e "convertidos"
        form_data = {
            'errors': {},
            'data': {},
            'campos':campos,}
        
        # se clicou no botao "Voltar"
        if 'form.voltar' in form_keys:
            context.request.response.redirect(success_voltar)
          
        # se clicou no botao "Salvar"
        elif 'form.submited' in form_keys:
            # Inicia o processamento do formulario
            # chama a funcao que valida os dados extraidos do formulario (valida_form) 
            errors, data = valida_form(campos, context.request.form)  

            if not errors:
                if 'forms_id' in form_keys:
                    # editando...
                    id = int(self.request.get('forms_id'))
                    result = ModelsForm().get_Forns_byId(id)
                    if result:
                        for campo in campos.keys():
                            value = data.get(campo, None)
                            setattr(result, campo, value)

                else:
                    #adicionando...
                    id = ModelsForm().set_Form(**data)
                    IStatusMessage(context.request).addStatusMessage(_(u"Formulario adcionado com susseço"), "info")
                    url = context.context.absolute_url() +  '/edit-form?forms_id='+ str(id)
                    context.request.response.redirect(url)
                                   
            else:
                form_data['errors'] = errors
                form_data['data'] = data
                return form_data
          
        # se for um formulario de edicao 
        elif 'forms_id' in form_keys:
            id = int(form.get('forms_id','0'))
            data = ModelsForm().get_Forns_byId(id)
            
            if data:
               form_data['data'] = data
               return form_data
            else:
               return form_data
            
        #se for um formulario de adição
        else:
            return form_data

class RegistrationCreateFields(BaseFunc):
    def to_utf8(value):
        return unicode(value, 'utf-8')
       
    campos = {'name_field'            : {'required': True,  'type':'key',     'label':'Nome do Campo',                'decription':u'Digite o nome para o campo',                                       'ordem':0},
              'type_fields'           : {'required': True,  'type':'choice',  'label':'Tipo do Campo',                'decription':u'Selecione o tipo da informação deste campos',                      'ordem':1},
              'list_values'           : {'required': False, 'type':'textarea','label':'Lista de dados para o select', 'decription':u'Digite um item por linha no padrão [ID] | [Valor]',                'ordem':2},
              'title'                 : {'required': True,  'type':to_utf8,   'label':'Titulo',                       'decription':u'Digite o titulo para o campo',                                     'ordem':3},
              'description_fields'    : {'required': False, 'type':'textarea','label':'Descrição',                    'decription':u'Digite a descrição para o campo',                                  'ordem':4},
              'value_default'         : {'required': False, 'type':to_utf8,   'label':'Valor Padrão',                 'decription':u'Digite o comando ou o valor padrão para preenchimento este campo', 'ordem':5},
              'flag_ativo'            : {'required': False, 'type':'bool',    'label':'Campo ativo',                  'decription':u'Marque esta opção se o campo estará atvo para o usuario',          'ordem':6},
              'required'              : {'required': False, 'type':'bool',    'label':'Campo Requerido',              'decription':u'Marque esta opção se o campo for obrigadorio',                     'ordem':7},
              'forms_id'              : {'required': False, 'type':'hidden',  'label':'id form',                      'decription':u'',                                                                 'ordem':8}}
              
                         
    def registration_processes(self,context):
        access_denied = context.context.absolute_url() + '/login'
        form = context.request # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)
        campos = self.campos
        lista_itens = {'type_fields':{'text':'campo de texto',
                                      'textarea':'campo text area',
                                      'bool':'campo booleano',
                                      'choice':'campo de seleção',
                                      'list':'campo de seleção multipla',
                                      'hidden':'campo Oculto'}
                       }

        # divisao dos dicionarios "errors" e "convertidos"
        form_data = {
            'errors': {},
            'data': {},
            'campos':campos,
            'lista_itens':lista_itens}
        
        # se clicou no botao "Voltar"
        if 'form.voltar' in form_keys:
            success_voltar = context.context.absolute_url() +  '/edit-form?forms_id='+form.get('forms_id','0')
            context.request.response.redirect(success_voltar)
          
        # se clicou no botao "Salvar"
        elif 'form.submited' in form_keys:
            # Inicia o processamento do formulario
            # chama a funcao que valida os dados extraidos do formulario (valida_form) 
            
            errors, data = valida_form(campos, context.request.form)  
            
            if not errors:
                
                if 'forms_id'in form_keys and 'id_fields' in form_keys:
                    # editando...
                    id_form = int(form.get('forms_id','0'))
                    id_fields = int(form.get('id_fields','0'))
            
                    result = ModelsFormFields().get_Fields_byId(int(id_form),int(id_fields))
                    if result:
                        for campo in campos.keys():
                            value = data.get(campo, None)
                            setattr(result, campo, value)
                        
                        IStatusMessage(context.request).addStatusMessage(_(u"Formulario editado com com susseço"), "info")
                        url = context.context.absolute_url() +  '/edit-form?forms_id='+ str(id_form)
                        context.request.response.redirect(url)

                else:
                    id_form = form.get('forms_id',0)
                    if ModelsFormFields().check_fields(data['name_field'],int(id_form)): 
                        #adicionando...
                        ModelsFormFields().set_FormFields(**data)
                        IStatusMessage(context.request).addStatusMessage(_(u"Formulario adcionado com susseço"), "info")
                        url = context.context.absolute_url() +  '/edit-form?forms_id='+ str(id_form)
                        context.request.response.redirect(url)
                    
                    else:
                        IStatusMessage(context.request).addStatusMessage(_(u"Ja existem um campo com este nome"), "info")
                        url = context.context.absolute_url() +  '/edit-form?forms_id='+ str(id_form)
                        context.request.response.redirect(url)
                
                                   
            else:
                form_data['errors'] = errors
                form_data['data'] = data
                return form_data
          
        # se for um formulario de edicao 
        elif 'forms_id'in form_keys and 'id_fields' in form_keys:
            id_form = int(form.get('forms_id','0'))
            id_fields = int(form.get('id_fields','0'))
            
            data = ModelsFormFields().get_Fields_byId(int(id_form),int(id_fields))
            
            campos['name_field'] = {'required': True,  'type':'hidden','label':'Nome do Campo', 'decription':u'', 'ordem':0}
            
            if data:
                D = {}
                for campo in campos.keys():
                    D[campo] = getattr(data, campo, '') 
                
                form_data['data'] = D
                return form_data
            else:
               return form_data
            
        #se for um formulario de adição
        else:
            return form_data

class RegistrationLoadForm(BaseFunc):
    def to_utf8(value):
        return unicode(value, 'utf-8')
                        
    def registration_processes(self,context):
        form = context.request # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)
        
        id_form = context.request.get('forms_id','0')
        import pdb;pdb.set_trace()
        success_url = context.context.absolute_url() +  '/view-form?forms_id=' + str(id_form)
        access_denied = context.context.absolute_url() + '/login'

        campos = {}
        lista_itens = {}
        default_value = {}
        n = 0
        fields = ModelsForm().get_Forns_byId(int(id_form)).fields
        for field in fields:
            if field.flag_ativo:
                M={}
                M['required'] = field.required
                M['type'] = field.type_fields
                M['label'] = field.title
                M['decription'] = field.description_fields
                M['ordem'] = n
                n += 1
                campos[field.name_field] = M
            if field.type_fields == 'choice':
                items = field.list_values.splitlines()
                D={}
                for i in items:
                    L = i.split('|')
                    D[L[0].replace(' ','')] = L[1]
                lista_itens[field.name_field] = D
                
            if field.type_fields == 'list':
                items = field.list_values.splitlines()
                D={}
                for i in items:
                    L = i.split('|')
                    D[L[0].replace(' ','')] = L[1]
                lista_itens[field.name_field] = D
            if field.value_default:
                default_value[field.name_field] = field.value_default
                 
        
        # divisao dos dicionarios "errors" e "convertidos"
        form_data = {
            'errors': {},
            'data': {},
            'campos':campos,
            'lista_itens':lista_itens,
            'default_value':default_value}
        
        # se clicou no botao "Voltar"
        if 'form.voltar' in form_keys:
            context.request.response.redirect(success_url)
          
        # se clicou no botao "Salvar"
        elif 'form.submited' in form_keys:
            # Inicia o processamento do formulario
            # chama a funcao que valida os dados extraidos do formulario (valida_form) 
            errors, data = valida_form(campos, context.request.form)  

            if not errors:
                if 'id_instance' in form_keys:
                    # editando...
                    id_form = int(id_form)
                    id_instance = int(form.get('id_instance',0))
                    
                    results = ModelsFormValues().get_FormValues_byForm_and_Instance(id_form,id_instance)
                    if results:
                        for campo in campos.keys():
                           for result in results:
                               if result.vin_contentcore_fields == campo:
                                   valor = data[campo]
                                   if type(valor) == unicode:
                                       result.value = valor.strip()
                                   else:
                                       result.value = unicode(str(valor), 'utf-8')
                                   result.date_creation = datetime.now()
                                   self.store.commit()            
                                
                               else:
                                   if results.find(vin_contentcore_fields=campo).count() == 0:
                                        D={}
                                        D['forms_id'] = id_form
                                        D['instance_id'] = id_instance
                                        D['fields'] = campo
                                        valor = data[campo]
                                        if type(valor) == unicode:
                                            D['value'] = valor.strip()
                                        else:
                                            D['value'] = unicode(str(valor), 'utf-8')
                                        
                                        ModelsFormValues().set_FormValues(**D)

                else:
                    #adicionando...
                    id_instance = ModelsFormInstance().set_FormInstance(id_form)
                    for field in data:
                        D={}
                        D['forms_id'] = int(conf_contentcore.id_form)
                        D['instance_id'] = id_instance
                        D['fields'] = field
                        valor = data[field]
                        if type(valor) == unicode:
                            D['value'] = valor.strip()
                        else:
                            D['value'] = unicode(str(valor), 'utf-8')
                    
                        ModelsFormValues().set_FormValues(**D)
                    
                #Redirect back to the front page with a status message
                #IStatusMessage(context.request).addStatusMessage(_(u"Thank you for your order. We will contact you shortly"), "info")
                context.request.response.redirect(success_url)
                                   
            else:
                form_data['errors'] = errors
                form_data['data'] = data
                return form_data
          
        # se for um formulario de edicao 
        elif 'id_instance' in form_keys:
            id_form = int(id_form)
            id_instance = int(form.get('id_instance',0))
            data_value = ModelsFormValues().get_FormValues_byForm_and_Instance(id_form,id_instance)
            
            if data_value:
                D = {}
                for campo in campos.keys():
                    for data in data_value:
                        if data.vin_contentcore_fields == campo:
                            D[campo] = data.value 
                
                form_data['data'] = D
                return form_data
            else:
                return form_data
        
        else:
            return form_data

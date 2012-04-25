# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.navigation.interfaces import INavigationRoot

from vindula.contentcore.formulario import IFormularioPadrao
from vindula.contentcore.conteudo_basico import IConteudoBasico 
from vindula.contentcore.base import BaseFunc
from vindula.contentcore.models import ModelsForm, ModelsFormFields, ModelsFormValues, ModelsDefaultValue    

from vindula.contentcore.registration import RegistrationCreateForm, RegistrationCreateFields,RegistrationLoadForm, RegistrationExcluirForm ,\
                                             RegistrationAddDefaultValue, RegistrationExcluirDefault, RegistrationParametrosForm, LoadRelatorioForm    

import datetime

#Views Manage Form--------------------------------------------------    
class VindulaManageForm(grok.View, BaseFunc):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('manage-form')
    
    def load_form(self):
        return ModelsForm().get_Forms()
    
    def list_default(self):
        return ModelsDefaultValue().get_DefaultValues()

class VindulaExcluirRegistroForm(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('zope2.View')
    grok.name('excluir-registro-form')
    
    def get_Form_fields(self):
        #form = self.request.form
        id_form = int(self.context.forms_id)
        if id_form:# 'forms_id' in form.keys():
            return ModelsFormFields().get_Fields_ByIdForm(int(id_form))
    
    def update(self):
        return RegistrationExcluirForm().exclud_processes(self)
    
    def list_registro(self):
        form = self.request.form
        if  'id_instance' in form.keys(): #'forms_id' in form.keys() and
            #forms_id = int(form.get('forms_id',''))
            id_form = int(self.context.forms_id)
            id_instance = int(form.get('id_instance',''))
            return ModelsFormValues().get_FormValues_byForm_and_Instance(id_form,id_instance)
        else:
            return None

class VindulaCreateForm(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('cmf.ManagePortal')
    grok.name('add-form')    
    
    def load_form(self):
        return RegistrationCreateForm().registration_processes(self)
    
class VindulaEditForm(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('cmf.ManagePortal')
    grok.name('edit-form')    
    
    def load_form(self):
        return RegistrationCreateForm().registration_processes(self)
    
    def list_form(self,id_form):
        return ModelsForm().get_Forns_byId(int(id_form))
    
    def list_fields(self,id_form):
        return ModelsFormFields().get_Fields_ByIdForm(int(id_form))
    
    
class VindulaAddFieldsForm(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('cmf.ManagePortal')
    grok.name('add-fields-form')    
    
    def load_form(self):
        return RegistrationCreateFields().registration_processes(self)
    
class VindulaEditFieldsForm(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('cmf.ManagePortal')
    grok.name('edit-fields-form')
    
    # This may be overridden in ZCML
    index = ViewPageTemplateFile("content_templates/vindulaaddfieldsform.pt")    
    
    def load_form(self):
        return RegistrationCreateFields().registration_processes(self)
    
    def render(self):
        return self.index()

class VindulaEditParametrosForm(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('cmf.ManagePortal')
    grok.name('edit-parametros')
    
    def load_form(self):
        return RegistrationParametrosForm().registration_processes(self)


class VindulaExportRegisterView(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('zope2.View')
    grok.name('export-form')    

    def render(self):
        pass
    
    def update(self):
        self.request.response.setHeader("Content-Type", "text/csv", 0)
        filename = str(self.context.id)+'-export-register.csv'
        self.request.response.setHeader('Content-Disposition','attachment; filename=%s'%(filename))
        
        id_form = int(self.context.forms_id)
        fields = ModelsFormFields().get_Fields_ByIdForm(int(id_form))
        types = ['list','img','file']
        
        campos_vin = []
        text = ''
        if fields:
            for field in fields:
                if field.flag_ativo:
                    campos_vin.append(field.title)
                    text += field.title + ';'
            text = text[:-1] + '\n'
            
            values = ModelsForm().get_FormValues(id_form)
            if values:
                for item in values:
                    for field in fields:
                        if field.flag_ativo:
                            data = item.find(fields=field.name_field).one()
                            if not field.type_fields in types:
                                valor = str(data.value).replace('\n', '').replace('\r', '').replace(';', '')
                                text += '%s;' % (valor)
           
                    text += '\n'
                 
        self.request.response.write(str(text))
        
class VindulaEditViewForm(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('cmf.ManagePortal')
    grok.name('edit-views')
    
    def get_Form_fields(self,):
        id_form =  int(self.context.forms_id)
        return ModelsFormFields().get_Fields_ByIdForm(id_form)    
    
    def load_form(self):
        return RegistrationViewForm().registration_processes(self)


#--------View Visualização Form----------------------------
class VindulaViewForm(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('zope2.View')
    grok.name('view-form') #Dados
   
    def get_FormValues(self):
        id_form = int(self.context.forms_id)
        return ModelsForm().get_FormValues(id_form)
    
    def get_Form_fields(self):
        id_form = int(self.context.forms_id)
        return ModelsFormFields().get_Fields_ByIdForm(id_form)

    
class VindulaLoadForm(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('zope2.View')
    grok.name('load-form') #View Padrao
    
    def load_form(self):
        return RegistrationLoadForm().registration_processes(self)







#----------View Conteudo Padrao ----------------------
class VindulaViewInstanceForm(grok.View, BaseFunc):
    grok.context(IConteudoBasico)
    grok.require('zope2.View')
    grok.name('view-instance-form')
    
    def get_FormValues(self, id_form,id_instance):
        return ModelsFormValues().get_FormValues_byForm_and_Instance(int(id_form),int(id_instance))
    
    def get_Form_fields(self,id_form):
        return ModelsFormFields().get_Fields_ByIdForm(int(id_form))



#Views de renderização dos objetos do Image e Arquivo ---------------------------------------------------   
class VindulaFormImage(grok.View, BaseFunc):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('form-image')
    
    def render(self):
        pass
    
    def update(self):
        form = self.request.form
        if 'id' in form.keys():
            id = form.get('id','0')
            if id != 'None':
                campo_image = ModelsFormValues().get_Values_byID(int(id))
                valor = campo_image.value
                valor_blob = campo_image.value_blob
                                
                if valor:
                    x = self.decodePickle(valor)
                else:
                    x = self.decodePickle(valor_blob)
                
                self.request.response.setHeader("Content-Type", "image/jpeg", 0)
                
                try:
                    #medoto adicionado na versão 1.1 do vindula
                    self.request.response.write(x['data'])
                except:
                    # medo usutilizado ate a versão antiga do content core
                    self.request.response.write(x)

class VindulaFormFile(grok.View, BaseFunc):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('form-file')
    
    def render(self):
        pass
    
    def update(self):
        form = self.request.form
        if 'id' in form.keys():
            id = form.get('id','0')
            if id != 'None':
                campo_image = ModelsFormValues().get_Values_byID(int(id))
                valor = campo_image.value
                valor_blob = campo_image.value_blob
                if valor:
                    x = self.decodePickle(valor)
                else:
                    x = self.decodePickle(valor_blob)
                
                filename = x['filename']
                self.request.response.setHeader("Content-Type", "type/file", 0)
                self.request.response.setHeader('Content-Disposition','attachment; filename=%s'%(filename))
                self.request.response.write(x['data'])                


#------View Default Value ----------------
class VindulaAddDefaultValue(grok.View, BaseFunc):
    grok.context(Interface)
    grok.require('cmf.ManagePortal')
    grok.name('add-defaut-value')
    
    def load_form(self):
        return RegistrationAddDefaultValue().registration_processes(self) 

class VindulaEditDefaultValue(grok.View, BaseFunc):
    grok.context(Interface)
    grok.require('cmf.ManagePortal')
    grok.name('edit-defaut-value')
    
    # This may be overridden in ZCML
    index = ViewPageTemplateFile("content_templates/vindulaadddefaultvalue.pt")    
    
    def load_form(self):
        return RegistrationAddDefaultValue().registration_processes(self)
    
    def render(self):
        return self.index()

class VindulaExcluirDefaultValue(grok.View, BaseFunc):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('excluir-default-value')
    
    def update(self):
        return RegistrationExcluirDefault().exclud_processes(self)
    
    def list_default(self):
        form = self.request.form
        if 'id' in form.keys():
            id = int(form.get('id','0'))
            return ModelsDefaultValue().get_DefaultValue_byId(id)
        else:
            return None

# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.navigation.interfaces import INavigationRoot

from vindula.contentcore.base import BaseFunc
from vindula.contentcore.models import ModelsForm, ModelsFormFields, ModelsFormValues    
from vindula.contentcore.registration import RegistrationCreateForm, RegistrationCreateFields,RegistrationLoadForm    


#Views registros Form--------------------------------------------------    
class VindulaManageForm(grok.View, BaseFunc):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('manage-form')
    
    def load_form(self):
        return ModelsForm().get_Forms()
    
class VindulaViewForm(grok.View, BaseFunc):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('view-form')
    
    def get_Form(self):
        form = self.request.form
        if 'forms_id' in form.keys():
            return ModelsForm().get_Forns_byId(int(form.get('forms_id','0')))
        else:
            return {}
    
    def get_FormValues(self, id_form):
        return ModelsForm().get_FormValues(int(id_form))
    
    def get_Form_fields(self,id_form):
        return ModelsFormFields().get_Fields_ByIdForm(int(id_form))
    
class VindulaLoadForm(grok.View, BaseFunc):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('load-form')
    
    def load_form(self):
        return RegistrationLoadForm().registration_processes(self)
    
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
                
                self.request.response.setHeader("Content-Type", "type/file", 0)
                self.request.response.write(x)                


#Views Forms ---------------------------------------------------
class VindulaCreateForm(grok.View, BaseFunc):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('add-form')    
    
    def load_form(self):
        return RegistrationCreateForm().registration_processes(self)
    
class VindulaEditForm(grok.View, BaseFunc):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('edit-form')    
    
    def load_form(self):
        return RegistrationCreateForm().registration_processes(self)
    
    def list_form(self,id_form):
        return ModelsForm().get_Forns_byId(int(id_form))
    
    def list_fields(self,id_form):
        return ModelsFormFields().get_Fields_ByIdForm(int(id_form))
    
    
class VindulaAddFieldsForm(grok.View, BaseFunc):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('add-fields-form')    
    
    def load_form(self):
        return RegistrationCreateFields().registration_processes(self)
    
class VindulaEditFieldsForm(grok.View, BaseFunc):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('edit-fields-form')
    
    # This may be overridden in ZCML
    index = ViewPageTemplateFile("content_templates/vindulaaddfieldsform.pt")    
    
    def load_form(self):
        return RegistrationCreateFields().registration_processes(self)
    
    def render(self):
        return self.index()

    
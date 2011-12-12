# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.navigation.interfaces import INavigationRoot

from vindula.contentcore.base import BaseFunc
from vindula.contentcore.models import RegistrationCreateForm, ModelsForm, RegistrationCreateFields,ModelsFormFields, RegistrationLoadForm    



#Views--------------------------------------------------    
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

    
# -*- coding: utf-8 -*-
from five import grok
from zope import schema

from plone.directives import form, dexterity
from vindula.contentcore import MessageFactory as _

from vindula.contentcore.base import BaseFunc
from vindula.contentcore.registration import RegistrationLoadForm    

# Interface and schema
class IConteudoBasico(form.Schema):
    """ Conteudo Basico"""

    form.mode(forms_id='hidden')
    forms_id = schema.TextLine(title=u"Form ID",
                              description=u"campo do formulario",
                              required=True)
    form.mode(instance_id='hidden')
    instance_id = schema.TextLine(title=u"Instance ID",
                              description=u"campo da instancia do formulario",
                              required=True)


#view
class ConteudoPadraoView(grok.View, BaseFunc):
    grok.context(IConteudoBasico)
    grok.require('zope2.View')
    grok.name('view')
    
    
class ConteudoPadraoEdicaoView(grok.View, BaseFunc):
    grok.context(IConteudoBasico)
    grok.require('zope2.View')
    grok.name('edit_form')    
    
    def load_form(self):
        ctx = self.context
        self.request.other['id_instance'] = ctx.instance_id
        return RegistrationLoadForm().registration_processes(self,False)

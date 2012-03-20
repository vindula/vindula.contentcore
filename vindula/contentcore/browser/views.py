# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.navigation.interfaces import INavigationRoot

from vindula.contentcore.base import BaseFunc
from vindula.contentcore.registration import LoadRelatorioForm

from vindula.contentcore.formulario import IFormularioPadrao

# Views    
class VindulaLoadRelatorioView(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('zope2.View')
    grok.name('relatorio-form')
    
    def load_form(self):
        return LoadRelatorioForm().registration_processes(self)


class VindulaAvisosView(grok.View):
    grok.context(IFormularioPadrao)
    grok.require('zope2.View')
    grok.name('myvindula-avisos-view')
    
    def load_list(self):
        ctx = self.context
        dados = ctx.getDadosContent()
        if dados:        
            return dados
        else:
            dados = []
        
        
    
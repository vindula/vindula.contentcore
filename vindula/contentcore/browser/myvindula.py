# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from vindula.contentcore.base import BaseFunc

from vindula.contentcore.browser.views import VindulaMyListPedidoView, VindulaListPedidosView



# Views
class BuscaFormulario(object):

    def list_formularios(self):
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        portal = self.context.portal_url.getPortalObject()
        itens = portal_catalog(**{'portal_type':['vindula.contentcore.formulariobasico'],
                                 'path':{'query':'/'.join(portal.getPhysicalPath()), 'depth': 99}
                                })
        return itens
     
class MinhasSolicitacoesView(VindulaMyListPedidoView,BuscaFormulario):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('minhas-solicitacoes')
    
    # def update(self,form_id=None):
    #     setattr(self, 'form_id', form_id)
    #     super(MinhasSolicitacoesView,self).update()

class GerenciarSolicitacoesView(VindulaListPedidosView,BuscaFormulario):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('gerenciar-solicitacoes')

    # def update(self,form_id=None):
    #     setattr(self, 'form_id', form_id)
    #     super(GerenciarSolicitacoesView,self).update()
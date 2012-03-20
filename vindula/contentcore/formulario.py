# -*- coding: utf-8 -*-
from five import grok
from zope import schema
from vindula.controlpanel.vocabularies import ListExitForm, ListDestinoForm

from Products.CMFCore.permissions import View

from plone.directives import form, dexterity
from vindula.contentcore import MessageFactory as _

from plone.formwidget.contenttree import ObjPathSourceBinder
from z3c.relationfield.schema import RelationChoice
from plone.z3cform.textlines import TextLinesFieldWidget      

from vindula.contentcore.base import BaseFunc
from vindula.contentcore.models import ModelsForm, ModelsFormFields


def to_utf8(value):
    return unicode(value, 'utf-8')

# Interface and schema
class IFormularioPadrao(form.Schema):
    """ Formulario Padrão """

    form.mode(forms_id='hidden')
    forms_id = schema.TextLine(title=u"Form ID",
                              description=u"campo do formulario",
                              required=True)
    
    acao_saida = schema.List(title=_(u"Ação de saída do formulário"),
                            description=_(u"Selecione uma ou mais ações que o formulário deve executar ao salvar"),# <br /> (Use a tecla control para seleciona mais de umvalor)."),
                            value_type=schema.Choice(source=ListExitForm()),
                            required=False)
    
    list_email = schema.Text(title=_(u"Lista de Email"),
                            description=_(u"Digite os email de destinatario dos dados do formulário <br /> (Digite um email por linha)."),
                            required=False)
    
    acao_destino = schema.Choice(title=_(u"Ação de destino do formulário"),
                                 description=_(u"Selecione um destino para o formulário depois de realizar a ação"),
                                 source=ListDestinoForm(),
                                 required=True)
   
    doc_plone = RelationChoice(title=_(u"Enviar o usuário a um documento do plone"),
                               description=_(u"Selecione o objeto no portal para que o usuario seja direcionado após o formulário realizar a ação"),                      
                               source=ObjPathSourceBinder(review_state='published'),
                               required=False,)
    
    url = schema.TextLine(title=_(u"Redireciona o usuário para uma url especifica"),
                              description=_(u"Digite a url que o usuario sera redirecionado após o formulário realizar a ação"),
                              default=u'http://',
                              required=False)
    
    #form.widget(parameto = TextLinesFieldWidget)
    parameto = schema.TextLine(title=_(u"Envia parâmetro a outro formulário ou página"),
                               description=_(u"Digite primeiro a url que o formulário será eviado junto com os parâmetros que serão cadastrado posteriormente"),
                               default=u'http://',
                               required=False)


@form.default_value(field=IFormularioPadrao['forms_id'])
def forms_idDefaultValue(value):
    return ModelsForm().get_NextForm()        


class FormularioPadrao(dexterity.Container):
    """ """
    grok.implements(IFormularioPadrao)

    def getDadosContent(self):
      id_form = int(self.forms_id)
      fields = ModelsFormFields().get_Fields_ByIdForm(id_form)
      values =  ModelsForm().get_FormValues(id_form)
      
      L = []
      for item in values:
          D = {}
          for campo in fields:
              if campo.flag_ativo:
                  data = item.find(fields=campo.name_field).one()
                  if data:
                      if campo.type_fields == u'bool':
                          valor = eval(data.value) 
                      
                      elif data.value:
                          valor = data.value
                      
                      else:
                          valor = data.value_blob
                          
                  else:        
                      valor = ''
                      
                  D[campo.name_field] = valor
          
          L.append(D)        
      
      return L  
    

       
#view
class FormularioPadraoView(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('zope2.View')
    grok.name('view')
    

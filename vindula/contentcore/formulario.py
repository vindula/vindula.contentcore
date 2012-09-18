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

# import fo SimpleVocabulary
from zope.interface import implements
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from plone.app.textfield import RichText

from z3c.form.browser.checkbox import CheckBoxFieldWidget 

def to_utf8(value):
    return unicode(value, 'utf-8')

class ListCamposForm(object):
    """ Create SimpleVocabulary for fields of form """
    implements(IContextSourceBinder)
    def __init__(self):
        self.object = object 
    def __call__(self, context):
        terms = []
        #terms.append(SimpleTerm('', '--NOVALUE--', _(u'option_category', default=u'Padrão')))
        try:
            id_form = int(context.forms_id)
        except:
            id_form = 0
         
        if id_form:
            fields = ModelsFormFields().get_Fields_ByIdForm(id_form)
            
            for campo in fields:
                  if campo.flag_ativo:
                      terms.append(SimpleTerm(campo.name_field, campo.name_field, _(u'option_category', default=campo.title)))
        
        return SimpleVocabulary(terms)    

# Interface and schema
class IFormularioPadrao(form.Schema):
    """ Formulario Padrão """

    form.mode(forms_id='hidden')
    forms_id = schema.TextLine(title=u"Form ID",
                              description=u"campo do formulario",
                              required=True)
    
    text_messenger = RichText(title=_(u"Texto Para o topo do formulário"),
                                     description=_(u"Digite o texto que será mostrado no topo do formulario"),
                                     required=False)
    
    form.widget(acao_saida = CheckBoxFieldWidget)
    acao_saida = schema.Set(title=_(u"Ação de saída do formulário"),
                            description=_(u"Selecione uma ou mais ações que o formulário deve executar ao salvar"),# <br /> (Use a tecla control para seleciona mais de umvalor)."),
                            value_type=schema.Choice(source=ListExitForm()),
                            required=True)
    
    list_email = schema.Text(title=_(u"Lista de Email"),
                            description=_(u"Crie uma lista de e-mails dos destinatários que irão receber os dados do formulário <br /> (Digite um email por linha)."),
                            required=False)
    
    email_padrao = schema.Choice(title=_(u"E-mail padrão"),
                                 description=_(u"elecione um campo para remetente de e-mail, enviado pelo formulário"),
                                 source=ListCamposForm(),
                                 required=False)
    
    acao_destino = schema.Choice(title=_(u"Ação de destino do formulário"),
                                 description=_(u"Selecione um destino para o formulário depois de realizar a ação"),
                                 source=ListDestinoForm(),
                                 required=True)
   
    doc_plone = RelationChoice(title=_(u"Enviar o usuário a um documento do plone"),
                               description=_(u"Selecione o objeto no portal para que o usuário seja direcionado após o formulário realizar a ação"),                      
                               source=ObjPathSourceBinder(review_state='published'),
                               required=False,)
    
    url = schema.TextLine(title=_(u"Redireciona o usuário para uma url especifica"),
                              description=_(u"Digite a url que o usuário será redirecionado após o formulário realizar a ação"),
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
    

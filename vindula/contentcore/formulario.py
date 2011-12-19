# -*- coding: utf-8 -*-
from five import grok
from zope import schema
from vindula.controlpanel.vocabularies import ListExitForm

from plone.directives import form, dexterity
from vindula.contentcore import MessageFactory as _

from plone.formwidget.contenttree import ObjPathSourceBinder
from z3c.relationfield.schema import RelationList, RelationChoice


from vindula.contentcore.models import ModelsForm
from vindula.contentcore.base import BaseFunc
from vindula.myvindula.user import BaseStore

def to_utf8(value):
    return unicode(value, 'utf-8')

# Interface and schema
class IFormularioPadrao(form.Schema):
    """ Formulario Padrão """

    form.mode(forms_id='hidden')
    forms_id = schema.TextLine(title=u"Form ID",
                              description=u"campo do formulario",
                              required=True)
    
    acao_saida = schema.Set(
         title=_(u"Ação de saída do formulário"),
         description=_(u"Selecione uma ou mais ações que o formulário deve executar ao salvar <br /> (Use a tecla control para seleciona mais de umvalor)."),
         value_type=schema.Choice(source=ListExitForm()),
         required=False,
        )
    
    list_email = schema.Text(
        title=_(u"Lista de Email"),
        description=_(u"Digite os email de destinatario dos dados do formulário <br /> (Digite um email por linha)."),
        required=False)
    
    
    
#    acao_destino = schema.Set(
#         title=_(u"Ação de destino do formulário"),
#         description=_(u"Selecione uma ou mais ações que o formulário deve executar ao salvar (Use a tecla control para seleciona mais de umvalor)."),
#         value_type=schema.Choice(source=ListActionForm()),
#         required=False,
#        )                     
    

@form.default_value(field=IFormularioPadrao['forms_id'])
def forms_idDefaultValue(value):
    return ModelsForm().get_NextForm()        
       
       
#view
class FormularioPadraoView(grok.View, BaseFunc ):
    grok.context(IFormularioPadrao)
    grok.require('zope2.View')
    grok.name('view')
    
    def update(self):
        #import pdb;pdb.set_trace()
        title = self.context.Title()
        description = self.context.Description()
        forms_id = self.context.forms_id
        
        result = ModelsForm().get_Forns_byId(int(forms_id))
        if result:
            result.name_form = to_utf8(title)
            result.description_form = to_utf8(description)
            BaseStore().store.flush()
            
        else:
            D={}
            D['name_form'] = to_utf8(title)
            D['description_form'] = to_utf8(description)
            id = ModelsForm().set_Form(**D)
            if forms_id != id:
                self.context.forms_id = id
                

                
                
                
                
            
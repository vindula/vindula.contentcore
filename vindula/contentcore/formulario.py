# -*- coding: utf-8 -*-
from five import grok
from zope import schema
from vindula.controlpanel.vocabularies import ListExitForm, ListDestinoForm

from plone.directives import form, dexterity
from vindula.contentcore import MessageFactory as _

from plone.formwidget.contenttree import ObjPathSourceBinder
from z3c.relationfield.schema import RelationChoice
from plone.z3cform.textlines import TextLinesFieldWidget      

from zope.app.container.interfaces import IObjectRemovedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent, IObjectCreatedEvent

from vindula.contentcore.base import BaseFunc
from vindula.myvindula.user import BaseStore
from vindula.contentcore.models import ModelsForm, ModelsFormFields, ModelsFormInstance, ModelsFormValues, ModelsParametersForm


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
    
    list_email = schema.Text(
        title=_(u"Lista de Email"),
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


@grok.subscribe(IFormularioPadrao, IObjectRemovedEvent)
def ExcludFormDataBase(context, event):
    basestore = BaseStore()
    id_form = int(context.forms_id)
    
    record_values = ModelsFormValues().get_FormValues_byForm(id_form)
    if record_values:
        for record in record_values:
            basestore.store.remove(record)
            basestore.store.flush()   
    
    record_instances = ModelsFormInstance().get_Instance(id_form)
    if record_instances:
        for record in record_instances:
            basestore.store.remove(record)
            basestore.store.flush()

    record_parameters = ModelsParametersForm().get_ParametersForm_byFormId(id_form)
    if record_parameters:
        for record in record_parameters:
            basestore.store.remove(record)
            basestore.store.flush()
                           
    record_fields = ModelsFormFields().get_Fields_ByIdForm(id_form)
    if record_fields:
        for record in record_fields:
            basestore.store.remove(record)
            basestore.store.flush()                           
    
    record_form = ModelsForm().get_Forns_byId(id_form)
    if record_form:
        basestore.store.remove(record_form)
        basestore.store.flush()
       
@grok.subscribe(IFormularioPadrao, IObjectCreatedEvent)
def CreatFormDataBase(context, event):
    title = context.Title()
    description = context.Description()
    forms_id = context.forms_id

    D={}
    try:D['name_form'] = to_utf8(title)
    except:D['name_form'] = title
    
    try:D['description_form'] = to_utf8(description)
    except:D['description_form'] = description
    
    id = ModelsForm().set_Form(**D)
    if forms_id != id:
        context.forms_id = id


@grok.subscribe(IFormularioPadrao, IObjectModifiedEvent)
def EditFormDataBase(context, event):       
        title = context.Title()
        description = context.Description()
        forms_id = context.forms_id
        
        result = ModelsForm().get_Forns_byId(int(forms_id))
        if result:
            try:result.name_form = to_utf8(title)
            except:result.name_form = title
            
            try:result.description_form = to_utf8(description)
            except:result.description_form = description
            BaseStore().store.flush()
       
#view
class FormularioPadraoView(grok.View, BaseFunc ):
    grok.context(IFormularioPadrao)
    grok.require('zope2.View')
    grok.name('view')
    

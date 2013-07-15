 #-*- coding: utf-8 -*-
from five import grok

from zope.app.container.interfaces import IObjectRemovedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent, IObjectCreatedEvent

from vindula.contentcore.formulario import IFormularioPadrao
from vindula.contentcore.conteudo_basico import IConteudoBasico

from vindula.contentcore.validation import to_utf8
from vindula.contentcore.base import BaseFunc, BaseStore

from vindula.contentcore.models.forms import ModelsForm
from vindula.contentcore.models.fields import ModelsFormFields
from vindula.contentcore.models.form_values import ModelsFormValues
from vindula.contentcore.models.form_instance import ModelsFormInstance
from vindula.contentcore.models.parameters import ModelsParametersForm


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

    id_form = ModelsForm().set_Form(**D)
    if forms_id != id_form:
        context.forms_id = id_form


    if context.active_workflow:

        campos_controle = [{'name_field':u'status',
                           'type_fields':u'hidden',
                           'title': u'Status do Pedido',
                           'description_fields':u'Guarda os status do pedido, não editar este campo',
                           'value_default':u'"open"',
                           'ordenacao':0,
                           'required':False,
                           'flag_ativo':True},
                           {'name_field':u'nivel',
                           'type_fields':u'hidden',
                           'title': u'Nivel do Pedido',
                           'description_fields':u'Guarda os nivel do pedido, não editar este campo',
                           'ordenacao':1,
                           'required':False,
                           'flag_ativo':True},
                           {'name_field':u'observacao_responsavel',
                           'type_fields':u'hidden',
                           'title': u'Observação do responsavel',
                           'description_fields':u'Guarda a observação do responsavel os nivel do pedido, não editar este campo',
                           'ordenacao':2,
                           'required':False,
                           'flag_ativo':True},
                           {'name_field':u'username',
                           'type_fields':u'hidden',
                           'title': u'username do usuario logado',
                           'description_fields':u'Guarda o username do usuario logado, não editar este campo',
                           'value_default':u'self.get_username_login()',
                           'ordenacao':3,
                           'required':False,
                           'flag_ativo':True}
                           ]

        for campo in campos_controle:
            campo['forms_id'] = int(id_form)

            ModelsFormFields().set_FormFields(**campo)


    if 'original' in event.__dict__.keys():
        org = event.original
        new = event.object

        fields_org = ModelsFormFields().get_Fields_ByIdForm(int(org.forms_id))

        campos = ['name_field','type_fields', 'list_values','title','value_default',\
                  'description_fields','ordenacao','required','flag_ativo']

        for item in fields_org:
            D={}
            for i in campos:
                D[i] = item.__getattribute__(i)

            D['forms_id'] = int(new.forms_id)

            ModelsFormFields().set_FormFields(**D)

        instances_org = ModelsFormInstance().get_Instance(int(org.forms_id))

        for instance in instances_org:
            values_instance = ModelsFormValues().get_FormValues_byForm_and_Instance(int(org.forms_id), instance.instance_id)

            id_inst = ModelsFormInstance().set_FormInstance(int(new.forms_id))

            campos_value = ['value', 'value_blob','fields']

            for value in values_instance:
                D={}
                for i in campos_value:
                    D[i] = value.__getattribute__(i)

                D['forms_id'] = int(new.forms_id)
                D['instance_id'] = id_inst

                ModelsFormValues().set_FormValues(**D)






@grok.subscribe(IFormularioPadrao, IObjectModifiedEvent)
def EditFormDataBase(context, event):
        title = context.Title()
        description = context.Description()

        campo_chave = context.campo_chave
        campo_label = context.campo_label

        forms_id = int(context.forms_id)

        result = ModelsForm().get_Forns_byId(forms_id)
        if result:
            try:result.name_form = to_utf8(title)
            except:result.name_form = title

            try:result.description_form = to_utf8(description)
            except:result.description_form = description

            try:result.campo_label = to_utf8(campo_label)
            except:result.campo_label = campo_label

            try:result.campo_chave = to_utf8(campo_chave)
            except:result.campo_chave = campo_chave

            BaseStore().store.flush()


        if context.active_workflow:
            result_fields_form = ModelsFormFields().get_Fields_ByIdForm(forms_id)

            campos_controle = [{'name_field':u'status',
                               'type_fields':u'hidden',
                               'title': u'Status do Pedido',
                               'description_fields':u'Guarda os status do pedido, não editar este campo',
                               'value_default':u'"open"',
                               'ordenacao':0,
                               'required':False,
                               'flag_ativo':True},
                               {'name_field':u'nivel',
                               'type_fields':u'hidden',
                               'title': u'Nivel do Pedido',
                               'description_fields':u'Guarda os nivel do pedido, não editar este campo',
                               'ordenacao':1,
                               'required':False,
                               'flag_ativo':True},
                              {'name_field':u'observacao_responsavel',
                               'type_fields':u'hidden',
                               'title': u'Observação do responsavel',
                               'description_fields':u'Guarda a observação do responsavel os nivel do pedido, não editar este campo',
                               'ordenacao':2,
                               'required':False,
                               'flag_ativo':True},
                               {'name_field':u'username',
                               'type_fields':u'hidden',
                               'title': u'username do usuario logado',
                               'description_fields':u'Guarda o username do usuario logado, não editar este campo',
                               'value_default':u'self.get_email_user_login()',
                               'ordenacao':3,
                               'required':False,
                               'flag_ativo':True}
                               ]

            for campo in campos_controle:
                campo['forms_id'] = int(forms_id)
                campo_name = campo.get('name_field')
                result_field = ModelsFormFields().get_Fields_ByField(campo_name, int(forms_id))
                if not result_field:
                    campo['ordenacao'] = (result_fields_form.count()+1)
                    ModelsFormFields().set_FormFields(**campo)


@grok.subscribe(IConteudoBasico, IObjectRemovedEvent)
def ExcludConteudoDataBase(context, event):
    basestore = BaseStore()
    id_form = int(context.forms_id)
    id_instance = int(context.instance_id)

    record_values = ModelsFormValues().get_FormValues_byForm_and_Instance(id_form,id_instance)
    if record_values:
        for record in record_values:
            basestore.store.remove(record)
            basestore.store.flush()

    ModelsFormInstance().del_Instance(id_form,id_instance)

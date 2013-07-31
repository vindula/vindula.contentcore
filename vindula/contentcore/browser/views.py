# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.navigation.interfaces import INavigationRoot

from Products.statusmessages.interfaces import IStatusMessage
from vindula.contentcore import MessageFactory as _

from vindula.contentcore.base import BaseFunc
from vindula.contentcore.registration import LoadRelatorioForm,RegistrationLoadForm
from vindula.contentcore.models.form_values import ModelsFormValues
from vindula.contentcore.models.fields import ModelsFormFields

from vindula.contentcore.formulario import IFormularioPadrao

from vindula.myvindula.tools.utils import UtilMyvindula

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
            return []



class VindulaListPedidosView(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('zope2.View')
    grok.name('list-pedidos')

    def __init__(self, context, request):
        super(VindulaListPedidosView,self).__init__(context=context, request=request)
        
        self.list_status = [{'id':'em_andamento','valor': 'Solicitação em Andamento'},
                            {'id':'cliente',     'valor': 'Aguardando Cliente'},
                            {'id':'aprovado',    'valor': 'Aprovado'},
                            {'id':'reprovado',   'valor': 'Reprovado'},
                            {'id':'enviar_para', 'valor': 'Enviar Para'}
                            ]

        self.form_id = int(self.context.forms_id)

    def rs_to_list(self, rs):
        if rs:
            return [i for i in rs]

        return []

    def update(self):
        #Checagem de permição na view
        if not self.context.is_active_workflow:
            self.request.response.redirect('%s/' % self.context.absolute_url())


        pedidos_nivel2 = []
        self.pedidos = self.rs_to_list(ModelsFormValues().get_FormValues_byForm_and_Field_and_Value(self.form_id,u'status',[u'open', u'em_andamento',u'cliente']))
         
        member =  self.context.restrictedTraverse('@@plone_portal_state').member()
        if member:
            username = member.getUserName()
            if not isinstance(username, unicode):
                username = unicode(username)  
            
            pedidos_nivel2 = ModelsFormValues().get_FormValues_byForm_and_Field_and_Value(self.form_id, u'nivel',username) 

        self.pedidos_nivel2 = self.rs_to_list(pedidos_nivel2)

        self.pedidos_aprovado = self.rs_to_list(ModelsFormValues().get_FormValues_byForm_and_Field_and_Value(self.form_id,u'status',u'aprovado'))
        self.pedidos_reprovado = self.rs_to_list(ModelsFormValues().get_FormValues_byForm_and_Field_and_Value(self.form_id,u'status',u'reprovado'))


    def get_value_field(self, instance_id, name_field):
        if not isinstance(instance_id, int):
            instance_id = int(instance_id)

        if not isinstance(name_field, unicode):
            name_field = unicode(name_field)            

        return ModelsFormValues().get_FormValues_byForm_and_Instance_and_Field(self.form_id,instance_id,name_field)


    def itens(self,instance_id):
        if not isinstance(instance_id, int):
            instance_id = int(instance_id)

        return ModelsFormValues().get_FormValues_byForm_and_Instance(self.form_id,instance_id)

    def get_user(self,instance_id):
        username_field = self.get_value_field(instance_id,'username')
        tool = UtilMyvindula()
        if username_field:
            obj_user = tool.get_prefs_user(username_field.value)
            return obj_user

        return {}

    def get_status(self, valor):
        self.list_status.append({'id':'open','valor': 'Em Aberto'})

        for i in self.list_status:
            if i.get('id') == valor:
                return i.get('valor')
        return valor


class VindulaPedidoView(VindulaListPedidosView):
    grok.context(IFormularioPadrao)
    grok.require('zope2.View')
    grok.name('item-pedidos')

    back_list = [u'status',u'nivel',u'observacao_responsavel',u'username']

    def list_user_nivel(self):
        list_users_nivel2 = self.context.list_users_nivel2 or ''
        list_users_nivel3 = self.context.list_users_nivel3 or ''
        
        list_users_nivel2 = list_users_nivel2.replace('\r','')
        list_users_nivel3 = list_users_nivel3.replace('\r','')

        return list_users_nivel2.split('\n') + list_users_nivel3.split('\n')


    def get_fields(self):
        return ModelsFormFields().get_Fields_ByIdForm(self.form_id)


    def update(self):
        #Checagem de permição na view
        if not self.context.is_active_workflow:
            self.request.response.redirect('%s/' % self.context.absolute_url())        
        
        form = self.request.form
        
        instance_id = form.get('instance_id','0')
        submited = form.get('submited',False)

        if submited:
            fields = self.get_fields()
            if fields:
                models_fields = fields.find(ModelsFormFields.name_field.is_in(self.back_list))

            RegistrationLoadForm().registration_processes(self, models_fields=models_fields)

            IStatusMessage(self.request).addStatusMessage(_(u"Pedido editado com sucesso."), "info")
            self.request.response.redirect('%s/list-pedidos' % self.context.absolute_url())



class VindulaMyPedidoView(VindulaListPedidosView):
    grok.context(IFormularioPadrao)
    grok.require('zope2.View')
    grok.name('my-pedidos')


    def update(self):
        pedidos = []

        member =  self.context.restrictedTraverse('@@plone_portal_state').member()
        if member:
            username = member.getUserName()
            if not isinstance(username, unicode):
                username = unicode(username)  

                pedidos = self.rs_to_list(ModelsFormValues().get_FormValues_byForm_and_Field_and_Value(self.form_id,u'username',username))


        self.meus_pedidos = pedidos









# -*- coding: utf-8 -*-
from five import grok
from storm.locals import Select
from zope.interface import Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFCore.utils import getToolByName

from Products.statusmessages.interfaces import IStatusMessage
from vindula.contentcore import MessageFactory as _

from vindula.contentcore.base import BaseFunc
from vindula.contentcore.registration import LoadRelatorioForm,RegistrationLoadForm
from vindula.contentcore.models.form_values import ModelsFormValues
from vindula.contentcore.models.fields import ModelsFormFields

from vindula.contentcore.formulario import IFormularioPadrao

from vindula.myvindula.tools.utils import UtilMyvindula

import simplejson as json
from random import choice
from datetime import datetime , timedelta
from dateutil.relativedelta import relativedelta

list_colors = ['#00FF40', '#FFE51E', '#0040FF', '#FF4B4B', '#FF00BF',
               '#000000', '#006600', '#00FFFF', '#FF6600', '#CC00FF' ]

# Views
class VindulaLoadRelatorioView(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('zope2.View')
    grok.name('relatorio-form')

    def load_form(self):
        if self.request.form.get('submit_filter'):
            if self.request.form.get('value_filter'):
                value = self.request.form.get('value_filter').decode('utf-8')
                if value.strip():
                    return LoadRelatorioForm().registration_processes(self, filtro={'field': self.context.campo_filtro, 'value': value}) 
        
        return LoadRelatorioForm().registration_processes(self) 

    def get_static(self):
        ctx = self.context
        portal = getToolByName(ctx, 'portal_url').getPortalObject()
        url_portal = portal.absolute_url()
        return url_portal +'/++resource++vindula.contentcore/'
    

    def get_values_filter(self):
        filter = ModelsFormFields().get_Fields_ByField(self.context.campo_filtro, int(self.context.forms_id))
        self.filter = [filter.title, filter.name_field]
        
        if self.filter:
            result = ModelsFormValues().get_FormValues_byForm_and_Field(int(self.context.forms_id),self.filter[1])
            if result.count() > 0:
                L = []
                for i in result:
                    if i.value not in L:
                        L.append(i.value)
            return L
        
class VindulaGraficosView(VindulaLoadRelatorioView):
    grok.context(IFormularioPadrao)
    grok.require('zope2.View')
    grok.name('graficos-form')

    def get_categorias(self, dados):
        L = []
        if dados:
            for item in dados:
                L.append(item.get('name',''))

        return json.dumps(L)

    def get_series(self, dados):
        D = {}
        L = []
        r = lambda: random.randint(0,255)
        if dados:
            for item in dados:
                L.append({'y': item.get('cont','0'),
                          'color': choice(list_colors)
                          }
                        )

        D['name'] = 'Respostas'
        D['data'] = L

        return json.dumps(D)


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
                            
        self.form_id = int(context.forms_id)

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

    def get_Field(self, campo):
        data = ModelsFormFields().get_Fields_ByField(campo,self.form_id)
        return data

    def check_status_superiro(self,enable,pedido):
        if enable:
            field_status = self.get_value_field(pedido.instance_id,'status');

            if field_status:
                if field_status.value == 'aprovado' or\
                   field_status.value == 'reprovado':
                   return False
                
        return True

    def str2datetime(self, str):
        split_date = str.split('/')
        try:
            return datetime(int(split_date[2]),
                            int(split_date[1]),
                            int(split_date[0]))
        except ValueError:
            return datetime.now()

    def get_data_final(self):
        date = datetime.now() + timedelta(days=1)
        return date.strftime('%d/%m/%Y')

    def get_data_inicial(self):
        date = datetime.now() - relativedelta(months=1)
        return date.strftime('%d/%m/%Y') 


    def check_filter_data(self,enable,pedido):
        if enable:
            if self.request.form.get('filter_codigo'):
                codigo = self.request.form.get('codigo')
                if codigo:
                    obj_field = self.get_value_field(pedido.instance_id,u'codigo')
                    if obj_field:
                        if codigo in obj_field.value:
                            return True
                        else:
                            return False
                    else:
                        return False

            if self.request.form.get('filter_data'):
                data_inicial = self.request.form.get('data_inicial',self.get_data_inicial())
                data_final = self.request.form.get('data_final',self.get_data_final())

                if data_inicial and data_final:
                    data_inicial = self.str2datetime(data_inicial)
                    data_final = self.str2datetime(data_final)

                    if pedido.date_creation>=data_inicial and\
                       pedido.date_creation<=data_final:
                        return True
                    else:
                        return False

        return True



class VindulaPedidoView(VindulaListPedidosView):
    grok.context(IFormularioPadrao)
    grok.require('zope2.View')
    grok.name('item-pedidos')

    back_list = [u'status',u'nivel',u'observacao_responsavel',u'username',\
                 u'arquivoauxiliarsolicitacao2', u'email_copia_solicitacao']
    error = ''

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
        # if not self.context.is_active_workflow:
        #     self.request.response.redirect('%s/' % self.context.absolute_url())        
        
        form = self.request.form
        
        submited = form.get('submited',False)

        if submited:
            if form.get('observacao_responsavel',False):
                fields = self.get_fields()
                if fields:
                    models_fields = fields.find(ModelsFormFields.name_field.is_in(self.back_list)).order_by(ModelsFormFields.ordenacao)

                RegistrationLoadForm().registration_processes(self, models_fields=models_fields)

                IStatusMessage(self.request).addStatusMessage(_(u"Pedido editado com sucesso."), "info")
                self.request.response.redirect('%s/list-pedidos' % self.context.absolute_url())
            else:
                self.error = 'Campo de Observação é obrigatorio para o historico da solicitação'


class VindulaMyPedidoView(VindulaPedidoView):
    grok.context(IFormularioPadrao)
    grok.require('zope2.View')
    grok.name('my-pedido')
 
    def update(self):
        self.back_list.append(u'my_observacao')
        #Checagem de permição na view
        # if not self.context.is_active_workflow:
        #     self.request.response.redirect('%s/' % self.context.absolute_url())        
        
        form = self.request.form
        
        submited = form.get('submited',False)

        if submited:
            fields = self.get_fields()
            if fields:
                models_fields = fields.find(ModelsFormFields.name_field.is_in([u'my_observacao']))

            RegistrationLoadForm().registration_processes(self, models_fields=models_fields)

            IStatusMessage(self.request).addStatusMessage(_(u"Pedido editado com sucesso."), "info")
            self.request.response.redirect('%s/my-pedidos' % self.context.absolute_url())


class VindulaMyListPedidoView(VindulaListPedidosView):
    grok.context(IFormularioPadrao)
    grok.require('zope2.View')
    grok.name('my-pedidos')


    def update(self,form_id=None):
        pedidos = []

        if not form_id:
            form_id = self.form_id
        else:
            setattr(self, 'form_id', form_id)

        member =  self.context.restrictedTraverse('@@plone_portal_state').member()
        if member:
            username = member.getUserName()
            if not isinstance(username, unicode):
                username = unicode(username)  

            pedidos = self.rs_to_list(ModelsFormValues().get_FormValues_byForm_and_Field_and_Value(form_id,u'username',username))


        self.meus_pedidos = pedidos

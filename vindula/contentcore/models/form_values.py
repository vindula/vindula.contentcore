# -*- coding: utf-8 -*-

from storm.locals import *
from storm.locals import Store

from datetime import datetime

from vindula.contentcore.base import BaseStore
from vindula.contentcore.models.log import ModelsLog
from vindula.contentcore.models.fields import ModelsFormFields

from zope.app.component.hooks import getSite
def get_username_login():
    user_login = getSite().portal_membership.getAuthenticatedMember()
    return Convert_utf8(user_login.getUserName())

def Convert_utf8(valor):
    try:
        return unicode(valor,'utf-8')
    except UnicodeDecodeError:
        return valor.decode("utf-8", "ignore")
    except:
        if type(valor) == unicode:
            return valor
        else:
            return u'erro ao converter os caracteres'


class ModelsFormValues(Storm, BaseStore):
    __storm_table__ = 'vin_contentcore_form_values'

    id = Int(primary=True)
    value = Unicode()
    value_blob = Pickle()
    date_creation = DateTime()

    forms_id = Int()
    instance_id = Int()
    fields = Unicode()

    instancia = Reference(instance_id, "ModelsFormInstance.instance_id")

    @property
    def get_field(self):
        field = self.fields
        form = self.forms_id
        return ModelsFormFields().get_Fields_ByField(field,form)


    def set_FormValues(self,**kwargs):
        # adicionando...
        values = ModelsFormValues(**kwargs)
        self.store.add(values)
        self.store.flush()


    def update_form_value(self,id_form, id_instance, valor,campo):
        result = self.get_FormValues_byForm_and_Instance_and_Field(id_form,id_instance,campo)
        if result:
            D={}
            D['valor_old'] = result.value or u'Campo em Blob'
            D['instance_id'] = id_instance
            D['forms_id'] =  id_form
            D['fields'] = campo

            # Get UserName Logado
            D['username'] = get_username_login()

            if type(valor) == int:
            
                valor = str(valor)

            if type(valor) != bool:
                if len(valor) < 65000:
                    D['valor_new'] = Convert_utf8(valor.strip())
                    result.value = Convert_utf8(valor.strip())
                    result.value_blob = None

                else:
                    result.value_blob = valor
                    result.value = None
                    D['valor_new'] = u'Campo em Blob'

            else:
                D['valor_new'] = Convert_utf8(valor)
                result.value = Convert_utf8(valor)

            if D['valor_new'] != D['valor_old']:
                ModelsLog().set_log(**D)

            result.date_creation = datetime.now()
            self.store.commit()

        else:
            self.set_form_value(id_form, id_instance, valor, campo)


    def set_form_value(self, id_form, id_instance, valor, campo):

        D = {}
        D['forms_id'] = id_form
        D['instance_id'] = id_instance
        D['fields'] = campo
       
        if type(valor) == int:
            
            valor = str(valor)

        if type(valor) != bool:
            if len(valor) < 65000:
                D['value'] = Convert_utf8(valor.strip())
                D['value_blob'] = None

            else:
                D['value'] = None
                D['value_blob'] = valor
        else:
            D['value'] = Convert_utf8(valor)
            D['value_blob'] = None


        ModelsFormValues().set_FormValues(**D)

        D['valor_new'] = D['value'] or u'Campo em Blob'
        D['valor_old'] = None

        D.pop('value')
        D.pop('value_blob')

        # Get UserName Logado
        D['username'] = get_username_login()

        ModelsLog().set_log(**D)


    def get_Values_byID(self,id):
        data = self.store.find(ModelsFormValues, ModelsFormValues.id==int(id)).one()
        if data:
            return data
        else:
            return None

    def get_FormValues_byForm_and_Instance_and_Field(self, id_form, id_instance,field):
        data = self.store.find(ModelsFormValues, ModelsFormValues.forms_id==id_form,
                                                 ModelsFormValues.instance_id==id_instance,
                                                 ModelsFormValues.fields==field)
        if data.count():
            return data[0]
        else:
            return None

    def get_FormValues_byForm_and_Field(self, id_form,field):
        data = self.store.find(ModelsFormValues, ModelsFormValues.forms_id==id_form,
                                                 ModelsFormValues.fields==field)
        if data.count() > 0:
            return data
        else:
            return []

    def  get_FormValues_byForm_and_Field_and_Value(self, id_form,field,value):
        if isinstance(value, list):
            data = self.store.find(ModelsFormValues, ModelsFormValues.forms_id==id_form,
                                                     ModelsFormValues.fields==field,
                                                     ModelsFormValues.value.is_in(value)) #.one()

        else:
            data = self.store.find(ModelsFormValues, ModelsFormValues.forms_id==id_form,
                                                     ModelsFormValues.fields==field,
                                                     ModelsFormValues.value==value) #.one()
        
        return data



    def get_FormValues_byForm_and_Instance(self, id_form, id_instance):
        data = self.store.find(ModelsFormValues, ModelsFormValues.forms_id==id_form,
                                                 ModelsFormValues.instance_id==id_instance)
        if data.count()>0:
            return data
        else:
            return []

    def get_FormValues_byForm(self, id_form):
        data = self.store.find(ModelsFormValues, ModelsFormValues.forms_id==id_form)
        if data.count()>0:
            return data
        else:
            return []

    #retorna todas as mudanças que teve no valor de um field
    def get_logField(self,):
        data = ModelsFormValues().store.find(ModelsLog, ModelsLog.forms_id==self.forms_id,
                                             ModelsLog.instance_id==self.instance_id,
                                             ModelsLog.fields==self.fields).order_by(ModelsLog.date_creation)
        return data

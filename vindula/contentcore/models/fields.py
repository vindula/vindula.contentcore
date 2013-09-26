# -*- coding: utf-8 -*-

from storm.locals import *
from storm.locals import Store


from vindula.contentcore.base import BaseStore



class ModelsFormFields(Storm, BaseStore):
    __storm_table__ = 'vin_contentcore_fields'

    id = Int(primary=True)
    name_field = Unicode()
    type_fields =  Unicode()
    list_values = Unicode()
    field_ref = Unicode()
    form_ref = Int()
    flag_multi = Bool()
    date_creation = DateTime()
    title = Unicode()
    value_default = Unicode()
    description_fields = Unicode()
    mascara = Unicode()
    ordenacao = Int()
    required = Bool()
    flag_ativo = Bool()
    flag_float_left = Bool()
    forms_id = Int()

    ref_mult = ReferenceSet(name_field, "ModelsFormFields.field_ref")
    ref_form = Reference(form_ref, "ModelsForm.id")

    def set_FormFields(self,**kwargs):
        # adicionando...
        fields = ModelsFormFields(**kwargs)
        self.store.add(fields)
        self.store.flush()
        #return form.id

    def remove_FormFields(self,id_field):
        results = self.get_Fields_byIdField(id_field)

        if results:
            self.store.remove(results)
            self.store.flush()


    def get_Fields_byIdField(self, id):
        data = self.store.find(ModelsFormFields, ModelsFormFields.id==id).one()
        if data:
            return data
        else:
            return None

    def get_fields_byIdForm_and_RefField(self,id_form,ref_field):
        data = self.store.find(ModelsFormFields, ModelsFormFields.field_ref==ref_field,
                                                 ModelsFormFields.forms_id==id_form)
        if data.count() > 0:
            return data
        else:
            return []


    def get_Fields_byId(self, id_form,id_fields):
        data = self.store.find(ModelsFormFields, ModelsFormFields.id==id_fields,
                                                 ModelsFormFields.forms_id==id_form).one()
        if data:
            return data
        else:
            return None

    def get_Fields_ByIdForm(self,id_form):
        data = self.store.find(ModelsFormFields, ModelsFormFields.forms_id==id_form).order_by(ModelsFormFields.ordenacao)
        if data:
            return data
        else:
            return None

    def get_Fields_ByField(self,campo,form):
        data = self.store.find(ModelsFormFields, ModelsFormFields.name_field==campo,
                                                 ModelsFormFields.forms_id==form).one()
        if data:
            return data
        else:
            return None


    def check_fields(self,campo,form):
        data = self.store.find(ModelsFormFields, ModelsFormFields.name_field==campo,
                                                 ModelsFormFields.forms_id==form)
        if data.count()>0:
            return False
        else:
            return True
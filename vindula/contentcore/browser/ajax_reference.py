# -*- coding: utf-8 -*-
from five import grok

from vindula.contentcore.formulario import IFormularioPadrao

from vindula.contentcore.models.fields import ModelsFormFields
from vindula.contentcore.models.form_values import ModelsFormValues

grok.templatedir('views_templates')

class VindulaAjaxReferenceView(grok.View):
    grok.context(IFormularioPadrao)
    grok.require('zope2.View')
    grok.name('ajax-reference')



    def update(self):
        form = self.request.form
        instance = 0

        formulario = form.get('form','0')
        field = form.get('field','')
        self.name_field = field
        value = form.get('value','')

        self.formulario = formulario
        self.campos = ModelsFormFields().get_Fields_ByIdForm(int(formulario))

        campo_busca = ModelsFormValues().store.find(ModelsFormValues, ModelsFormValues.fields==unicode(field),
                                                                      ModelsFormValues.forms_id==int(formulario),
                                                                      ModelsFormValues.value==unicode(value)
                                                    )
        if campo_busca.count():
            instance = campo_busca[0].instance_id

        self.valores = ModelsFormValues().get_FormValues_byForm_and_Instance(int(formulario),instance)


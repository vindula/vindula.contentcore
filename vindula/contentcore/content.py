# -*- coding: utf-8 -*-
from copy import copy
from datetime import datetime, timedelta

import pyExcelerator as xl
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot
from vindula.contentcore.base import BaseFunc
from vindula.contentcore.conteudo_basico import IConteudoBasico
from vindula.contentcore.formulario import IFormularioPadrao
from vindula.contentcore.models.configImport import ModelsConfigImport
from vindula.contentcore.models.default_value import ModelsDefaultValue
from vindula.contentcore.models.fields import ModelsFormFields
from vindula.contentcore.models.form_instance import ModelsFormInstance
from vindula.contentcore.models.form_values import ModelsFormValues
from vindula.contentcore.models.forms import ModelsForm
from vindula.contentcore.registration import RegistrationCreateForm, RegistrationCreateFields,\
    RegistrationLoadForm, RegistrationExcluirForm, RegistrationAddDefaultValue,\
    RegistrationExcluirDefault, RegistrationParametrosForm
from zope.interface import Interface
from zope.security import checkPermission
from storm.expr import Desc


#Views Manage Form--------------------------------------------------
class VindulaManageForm(grok.View, BaseFunc):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('manage-form')

    def load_form(self):
        return ModelsForm().get_Forms()

    def list_default(self):
        return ModelsDefaultValue().get_DefaultValues()

#------View Default Value ----------------
class VindulaAddDefaultValue(grok.View, BaseFunc):
    grok.context(Interface)
    grok.require('cmf.ManagePortal')
    grok.name('add-defaut-value')

    def load_form(self):
        return RegistrationAddDefaultValue().registration_processes(self)

class VindulaEditDefaultValue(grok.View, BaseFunc):
    grok.context(Interface)
    grok.require('cmf.ManagePortal')
    grok.name('edit-defaut-value')

    # This may be overridden in ZCML
    index = ViewPageTemplateFile("content_templates/vindulaadddefaultvalue.pt")

    def load_form(self):
        return RegistrationAddDefaultValue().registration_processes(self)

    def render(self):
        return self.index()

class VindulaExcluirDefaultValue(grok.View, BaseFunc):
    grok.context(Interface)
    grok.require('cmf.ManagePortal')
    grok.name('excluir-default-value')

    def update(self):
        return RegistrationExcluirDefault().exclud_processes(self)

    def list_default(self):
        form = self.request.form
        if 'id' in form.keys():
            id = int(form.get('id','0'))
            return ModelsDefaultValue().get_DefaultValue_byId(id)
        else:
            return None



#Views
class VindulaExcluirRegistroForm(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('cmf.ModifyPortalContent')
    grok.name('excluir-registro-form')

    def get_Form_fields(self):
        #form = self.request.form
        id_form = int(self.context.forms_id)
        if id_form:# 'forms_id' in form.keys():
            return ModelsFormFields().get_Fields_ByIdForm(int(id_form))

    def update(self):
        return RegistrationExcluirForm().exclud_processes(self)

    def list_registro(self):
        form = self.request.form
        if  'id_instance' in form.keys(): #'forms_id' in form.keys() and
            #forms_id = int(form.get('forms_id',''))
            id_form = int(self.context.forms_id)
            id_instance = int(form.get('id_instance',''))
            return ModelsFormValues().get_FormValues_byForm_and_Instance(id_form,id_instance)
        else:
            return None

class VindulaCreateForm(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('cmf.ModifyPortalContent')
    grok.name('add-form')

    def load_form(self):
        return RegistrationCreateForm().registration_processes(self)

class VindulaEditForm(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('cmf.ModifyPortalContent')
    grok.name('edit-form')

    def load_form(self):
        return RegistrationCreateForm().registration_processes(self)

    def list_form(self,id_form):
        return ModelsForm().get_Forns_byId(int(id_form))

    def list_fields(self,id_form):
        return ModelsFormFields().get_Fields_ByIdForm(int(id_form))


class VindulaAddFieldsForm(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('cmf.ModifyPortalContent')
    grok.name('add-fields-form')

    def load_form(self):
        return RegistrationCreateFields().registration_processes(self)

class VindulaEditFieldsForm(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('cmf.ModifyPortalContent')
    grok.name('edit-fields-form')

    # This may be overridden in ZCML
    index = ViewPageTemplateFile("content_templates/vindulaaddfieldsform.pt")

    def load_form(self):
        return RegistrationCreateFields().registration_processes(self)

    def check_exclud_fields(self):
        id_form = int(self.context.forms_id)
        id_fields = int(self.request.form.get('id_fields','0'))

        field = ModelsFormFields().get_Fields_byIdField(id_fields)
        if field:
            check = ModelsFormValues().get_FormValues_byForm_and_Field(id_form,field.name_field)

            if check:
                return False
            else:
                if field.ref_mult.count():
                    return False
                else:
                    return True
        return True

    def render(self):
        return self.index()


class VindulaManageContentForm(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('cmf.ModifyPortalContent')
    grok.name('manage-values-form')


    def update(self):
        id_form = int(self.context.forms_id)
        form = self.request.form
        self.errors = {}
        self.dados = []
        self.configuracao = ModelsConfigImport().get_Config_byIdForm(int(id_form))

        FIELD_BLACKLIST = ['form.config.save','form.importar',]
        configura = form.get('form.config.save',False)
        importacao = form.get('form.importar',False)

        if configura:

            for field in form.keys():
                if not field in FIELD_BLACKLIST:
                    D = {}
                    D['forms_id'] = id_form
                    D['fields'] = self.Convert_utf8(field)
                    D['campo_csv'] = self.Convert_utf8(form.get(field,0))

                    if self.configuracao:
                        ModelsConfigImport().update_ConfigImport(D['forms_id'],D['fields'],D['campo_csv'])

                    else:
                        ModelsConfigImport().set_ConfigImport(**D)

                    if 'form.config.save' in form.keys():
                        form.pop('form.config.save')

        elif importacao:
            if 'arquivo' in form.keys():
                file = form.get('arquivo').read().splitlines()

                for linha in file[1:]:
                    colunas = linha.split(';')
                    dados = {}

                    for campo in self.configuracao:
                        dados[self.Convert_utf8(campo.fields)] = self.Convert_utf8(colunas[int(campo.campo_csv)-1])

                    chave_form = self.context.campo_chave
                    result = ModelsFormValues().get_FormValues_byForm_and_Field_and_Value(id_form,chave_form,dados[chave_form])

                    if result.count():
                        result = result[0]
                        id_instance = result.instance_id
                        for i in dados:
                            ModelsFormValues().update_form_value(id_form,id_instance,dados[i],i)

                    else:
                        id_instance = ModelsFormInstance().set_FormInstance(id_form)
                        for i in dados:
                            valor = dados[i]
                            if valor:
                                ModelsFormValues().set_form_value(id_form,id_instance,valor,i)

                    self.dados.append(dados)



    def load_fields_csv(self):
        form = self.request.form
        colunas_csv = []
        if 'arquivo' in form.keys():

            file = form.get('arquivo').read()
            colunas_csv = file.split('\n')[0].replace('"', '').split(';')

        return colunas_csv


    def load_fields_form(self):
        form = self.request.form
        id_form = self.context.forms_id
        fields_vin = []
        i=0

        fields = ModelsFormFields().get_Fields_ByIdForm(int(id_form))


        camposAux = copy(fields)
        for item in camposAux:
            fields_vin.append(item.ordenacao)

        if fields:

            for field in fields:
                index = field.ordenacao
                D = {}
                D['name'] = field.name_field
                D['label'] = field.title

                pos = fields_vin.index(index)
                fields_vin.pop(pos)
                fields_vin.insert(pos, D)


        return fields_vin



class VindulaEditParametrosForm(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('cmf.ModifyPortalContent')
    grok.name('edit-parametros')

    def load_form(self):
        return RegistrationParametrosForm().registration_processes(self)


#class VindulaExportRegisterView(grok.View, BaseFunc):
#    grok.context(IFormularioPadrao)
#    grok.require('cmf.ListFolderContents')
#    grok.name('export-form')
#
#    def render(self):
#        pass
#    
#    def checkItem(self, item, form):
#        for campo in form.keys():
#            if campo not in ['b_start','date_creation']:
#
#                valor = form.get(campo,'')
#                field = item.find(fields=self.Convert_utf8(campo)).one()
#
#                if not valor :
#                    continue
#                if not field:
#                    return False
#
#                elif type(valor) == list:
#                    existe = False
#                    for val in valor:
#                        if field:
#                            if field.value == self.Convert_utf8(val):
#                                existe = True
#                                break
#
#                    if not existe:
#                        return False
#                elif field:
#                    if not field.value == self.Convert_utf8(valor):
#                        return False
#
#            elif campo == 'date_creation':
#                valor = form.get(campo,'')
#                if valor and item[0].instancia.date_creation.strftime('%d/%m/%Y %H:%M:%S') != valor:
#                    return False
#
#        return True
#
#    def update(self):
#        self.request.response.setHeader("Content-Type", "text/csv; charset=utf-8")
#        self.request.response.setHeader("Content-Transfer-Encoding", "utf-8")
#        self.request.response.setHeader("Transfer-Encoding", "utf-8")
#        self.request.response.setHeader("Content-Encoding", "utf-8")
#        filename = str(self.context.id)+'-export-register.csv'
#        self.request.response.setHeader('Content-Disposition','attachment; filename=%s'%(filename))
#        id_form = int(self.context.forms_id)
#        fields = ModelsFormFields().get_Fields_ByIdForm(int(id_form))
#        types = ['img','file']
#        form = self.request.form
#
#        campos_vin = []
#        text = ''
#
#        values = ModelsForm().get_FormValues(id_form)
#        L = []
#        for item in values:
#            if self.checkItem(item, form):
#                L.append(item)
#        values = L
#
#        if fields:
#            for field in fields:
#                if field.flag_ativo:
#                    titulo = field.title.replace(';', ',')
#                    if isinstance(titulo, str):
#                        titulo = titulo.decode('utf-8')
#                    campos_vin.append(titulo.decode('utf-8'))
#                    text += titulo + ';'
#            text = text[:-1] + '\n'
#            
#            if values:
#                for item in values:
#                    for field in fields:
#                        if field.flag_ativo:
#                            data = item.find(fields=field.name_field).one()
#
#                            if not field.type_fields in types and data:
#                                if field.type_fields == 'list':
#                                    valor = ''
#                                    for i in self.decodePickle(data.value):
#                                        valor += i +','
#
#                                elif field.type_fields == 'date':
#                                    campo_data = self.decodePickle(data.value)
#                                    valor = campo_data.strftime('%d/%m/%Y')
#
#                                else:
#                                    valor = str(data.value).replace('\n', '').replace('\r', '').replace(';', ',')
#
#                            else:
#                                valor = ''
#                                
#                            
#                            text += '%s;' % (valor)
#
#                    text += '\n'
#                    
#        self.request.response.write(str(text))
        
class VindulaExportRegisterView(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('cmf.ListFolderContents')
    grok.name('export-form')

    def render(self):
        pass
    
    def checkItem(self, item, form):
        for campo in form.keys():
            if campo not in ['b_start','date_creation']:

                valor = form.get(campo,'')
                field = item.find(fields=self.Convert_utf8(campo)).one()

                if not valor :
                    continue
                if not field:
                    return False

                elif type(valor) == list:
                    existe = False
                    for val in valor:
                        if field:
                            if field.value == self.Convert_utf8(val):
                                existe = True
                                break

                    if not existe:
                        return False
                elif field:
                    if not field.value == self.Convert_utf8(valor):
                        return False

            elif campo == 'date_creation':
                valor = form.get(campo,'')
                if valor and item[0].instancia.date_creation.strftime('%d/%m/%Y %H:%M:%S') != valor:
                    return False

        return True
    
    def update(self):
        filename = str(self.context.id)+'-export-register.xls'
        id_form = int(self.context.forms_id)
        fields = ModelsFormFields().get_Fields_ByIdForm(int(id_form))
        types = ['img','file']
        form = self.request.form
        campos_vin = []

        values = ModelsForm().get_FormValues(id_form)
        L = []
        for item in values:
            if self.checkItem(item, form):
                L.append(item)

        values = L
        
        if fields:
            fields = fields.find(flag_ativo=True)
            # Create Excel workbook
            wb = xl.Workbook()
            
            # Create Excel sheet and header
            mysheet = wb.add_sheet(self.context.Title() or self.context.id) #Nome do sheet
            
            #write headers
            header_font=xl.Font() #make a font object
            header_font.bold=True
            header_font.underline=True
            #font needs to be style actually
            header_style = xl.XFStyle(); header_style.font = header_font
            
            for field in fields:
                titulo = field.title.replace(';', ',')
                if isinstance(titulo, str):
                    titulo = titulo.decode('utf-8')
                campos_vin.append(titulo.decode('utf-8'))
            
            for col,value in enumerate(campos_vin):
                mysheet.write(0,col,value,header_style)
            
            if values:
                for row_num,row_value in enumerate(values):
                    row_num+=1 #start at row 1

                    for col, field in enumerate(fields):
                        #Campos de histórico
                        if field.name_field in ['observacao_responsavel', 'my_observacao']:
                            data = row_value.find(fields=field.name_field)
                            valor = ''
                            if data and data.count():
                                data = data[0]
                                log_data = data.get_logField()
                                if log_data and log_data.count():
                                    for log in log_data:
                                        valor += str(log.valor_new).replace('\n', '').replace('\r', '').replace(';', ',')
                                        valor += ' \\ '

                        else:
                            data = row_value.find(fields=field.name_field).one()

                            if not field.type_fields in types and data:
                                if field.type_fields == 'list':
                                    valor = ''
                                    for i in self.decodePickle(data.value):
                                        valor += i +','

                                elif field.type_fields == 'date':
                                    campo_data = self.decodePickle(data.value)
                                    valor = campo_data.strftime('%d/%m/%Y')
                                else:
                                    valor = str(data.value).replace('\n', '').replace('\r', '').replace(';', ',')

                            else:
                                valor = ''
                            
                        if isinstance(valor, str):
                            valor = valor.decode('utf-8')
                        
                        mysheet.write(row_num,col,valor)
        
            # Write out Excel file
            wb.save(filename)
        
            self.request.response.setHeader('Content-Type', 'application/x-excel; charset=utf-8')
            self.request.response.setHeader('Content-Disposition','attachment; filename=%s'%(filename))
            
            self.request.response.write(file(filename,"r").read())

class VindulaEditViewForm(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('cmf.AddPortalContent')
    grok.name('edit-views')

    def get_Form_fields(self,):
        id_form =  int(self.context.forms_id)
        return ModelsFormFields().get_Fields_ByIdForm(id_form)

    def load_form(self):
        return RegistrationViewForm().registration_processes(self)


#--------View Visualização Form----------------------------
class VindulaViewForm(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('cmf.ListFolderContents')
    grok.name('view-form') #Dados


    def get_FormValues(self,getall=True):

        #import pdb; pdb.set_trace()
        id_form = int(self.context.forms_id)
        form = self.request.form

        if 'data_inicial' in form.keys():
            data_inicial = self.str2datetime(form.get('data_inicial')) + timedelta(days=0)
        else:
            data_inicial = self.str2datetime(self.get_data_inicial())


        if 'data_final' in form.keys():
            data_final = self.str2datetime(form.get('data_final')) - timedelta(days=-1)
        else:
            data_final = self.str2datetime(self.get_data_final())


        data_instance = ModelsFormInstance().store.find(
            ModelsFormInstance, ModelsFormInstance.forms_id==id_form,
            ModelsFormInstance.date_creation>=data_inicial,
            ModelsFormInstance.date_creation<=data_final,
        ).order_by(Desc(ModelsFormInstance.date_creation))

        ids_instances = [int(i.instance_id) for i in data_instance]

        L_value = []
        data_values = data = ModelsFormValues().store.find(
            ModelsFormValues, 
            ModelsFormValues.forms_id == id_form,
            ModelsFormValues.date_creation >= data_inicial,
            ModelsFormValues.date_creation <= data_final,
            ModelsFormValues.instance_id.is_in(ids_instances))
        for item in data_instance: 
            data = data_values.find(ModelsFormValues.instance_id == int(item.instance_id))
            if data.count() > 0:
                L_value.append(data)
        L = []
        for item in L_value:
            if self.checkItem(item, form):
                L.append(item)
        return L

    def get_FormValues_filtro(self):
        id_form = int(self.context.forms_id)
        return ModelsForm().get_FormValues_filtro(id_form)

    def get_Form_fields(self):
        id_form = int(self.context.forms_id)
        return ModelsFormFields().get_Fields_ByIdForm(id_form)

    def get_Form_instance(self):
        id_form = int(self.context.forms_id)
        return ModelsFormInstance().get_Instance(id_form)

    def find_group_by(self, valores):
        L = []
        for valor in valores:
            V = valor.value
            if V and not V in L:
                L.append(V)

        return L

    def find_group_by_data(self, valores):
        L = []
        for valor in valores:
            V = valor.date_creation.strftime('%d/%m/%Y %H:%M:%S')
            if not V in L:
                L.append(V)

        return L

    def valores_b(self, all_values,campo):
        L = []
        for i in all_values:
            x = i.find(fields=campo.name_field)
            if x.count():
                x = x[0]
                L.append(x)

        return L


    def canRequestPermission(self,permissao):
        return checkPermission(permissao, self.context)

    def checkItem(self, item, form):
        for campo in form.keys():
            if campo not in ['b_start','date_creation','data_final','data_inicial']:

                valor = form.get(campo,'')
                field = item.find(fields=self.Convert_utf8(campo)).one()

                if not valor :
                    continue
                if not field:
                    return False

                elif type(valor) == list:
                    existe = False
                    for val in valor:
                        if field:
                            if field.value == self.Convert_utf8(val):
                                existe = True
                                break

                    if not existe:
                        return False
                elif field:
                    if not field.value == self.Convert_utf8(valor):
                        return False

            elif campo == 'date_creation':
                valor = form.get(campo,'')
                if valor and item[0].instancia.date_creation.strftime('%d/%m/%Y %H:%M:%S') != valor:
                    return False

        return True

    def get_data_final(self):
        date = datetime.now() + timedelta(days=1)
        return date.strftime('%d/%m/%Y')

    def get_data_inicial(self):
        date = datetime.now() - timedelta(days=7)
        return date.strftime('%d/%m/%Y')

    def str2datetime(self, str):
        split_date = str.split('/')
        try:
            return datetime(int(split_date[2]),
                            int(split_date[1]),
                            int(split_date[0]))
        except ValueError:
            return datetime.now()

    def get_data(self, item, campo):
        return item.find(fields=campo.name_field).one()


class VindulaDadosNewWindows(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('cmf.ListFolderContents')
    grok.name('view-dado-newwindows') #View dados em nova janela


class VindulaLoadForm(grok.View, BaseFunc):
    grok.context(IFormularioPadrao)
    grok.require('zope2.View')
    grok.name('load-form') #View Padrao

    def load_form(self):
        return RegistrationLoadForm().registration_processes(self)


#----------View Conteudo Padrao ----------------------
class VindulaViewInstanceForm(grok.View, BaseFunc):
    grok.context(IConteudoBasico)
    grok.require('zope2.View')
    grok.name('view-instance-form')

    def get_FormValues(self, id_form,id_instance):
        return ModelsFormValues().get_FormValues_byForm_and_Instance(int(id_form),int(id_instance))

    def get_Form_fields(self,id_form):
        return ModelsFormFields().get_Fields_ByIdForm(int(id_form))



#Views de renderização dos objetos do Image e Arquivo ---------------------------------------------------
class VindulaFormImage(grok.View, BaseFunc):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('form-image')

    def render(self):
        pass

    def update(self):
        form = self.request.form
        if 'id' in form.keys():
            id = form.get('id','0')
            if id != 'None':
                campo_image = ModelsFormValues().get_Values_byID(int(id))
                valor = campo_image.value
                valor_blob = campo_image.value_blob

                if valor:
                    x = self.decodePickle(valor)
                else:
                    x = self.decodePickle(valor_blob)

                self.request.response.setHeader("Content-Type", "image/jpeg", 0)

                try:
                    #medoto adicionado na versão 1.1 do vindula
                    self.request.response.write(x['data'])
                except:
                    # medo usutilizado ate a versão antiga do content core
                    self.request.response.write(x)

class VindulaFormFile(grok.View, BaseFunc):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('form-file')

    def render(self):
        pass

    def update(self):
        form = self.request.form
        if 'id' in form.keys():
            id = form.get('id','0')
            if id != 'None':
                campo_image = ModelsFormValues().get_Values_byID(int(id))
                valor = campo_image.value
                valor_blob = campo_image.value_blob
                if valor:
                    x = self.decodePickle(valor)
                else:
                    x = self.decodePickle(valor_blob)

                filename = x['filename']
                self.request.response.setHeader("Content-Type", "type/file", 0)
                self.request.response.setHeader('Content-Disposition','attachment; filename=%s'%(filename))
                self.request.response.write(x['data'])

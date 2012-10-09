# -*- coding: utf-8 -*-
from Products.statusmessages.interfaces import IStatusMessage
from vindula.contentcore import MessageFactory as _
from zope.app.component.hooks import getSite
from vindula.contentcore.base import BaseFunc
from datetime import date , datetime 
from vindula.contentcore.validation import valida_form
from vindula.contentcore.models import ModelsForm, ModelsFormFields, ModelsFormValues, ModelsFormInstance, ModelsDefaultValue, ModelsParametersForm


class RegistrationCreateForm(BaseFunc):
    def to_utf8(value):
        return unicode(value, 'utf-8')
      
    campos = {'name_form'          : {'required': True,  'type' : to_utf8,'label':'Titulo',    'decription':u'Digite o título do formulário',    'ordem':0},
              'description_form'   : {'required': False, 'type' : to_utf8,'label':'Descrição', 'decription':u'Digite a descrição do formulário', 'ordem':1}}
                        
    def registration_processes(self,context):
        success_voltar = context.context.absolute_url() #+  '/manage-form'
        form = context.request # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)
        campos = self.campos
        
        # divisao dos dicionarios "errors" e "convertidos"
        form_data = {
            'errors': {},
            'data': {},
            'campos':campos,}
    
        id_form = int(context.context.forms_id) #form.get('forms_id','0'))
        result_form = ModelsFormFields().get_Fields_ByIdForm(id_form)
        
        # se clicou no botao "Voltar"
        if 'form.voltar' in form_keys:
            context.request.response.redirect(success_voltar)

        #se for Ordenação de campos
        elif 'position'in form_keys and 'id_field' in form_keys:
            position = form.get('position','')
            id_field = form.get('id_field','')
            result = result_form.find(id=int(id_field)).one()
            if position == 'up':
                numb = int(result.ordenacao)-1
                result.ordenacao = numb
                
                result_prev = result_form.find(ordenacao=numb,forms_id=id_form).one()
                result_prev.ordenacao = numb+1
                
                self.store.commit()
                
                IStatusMessage(context.request).addStatusMessage(_(u"Campo Movindo para cima"), "info")
                url = context.context.absolute_url() +  '/edit-form' #?forms_id='+ str(id_form)
                context.request.response.redirect(url)
                
            elif position == 'down':
                id_field_next = form.get('id_field_next','')
                
                numb = int(result.ordenacao)+1 
                result.ordenacao = numb
                
                result_next = result_form.find(ordenacao=numb,forms_id=id_form).one()
                result_next.ordenacao = numb-1

                self.store.commit()
                
                IStatusMessage(context.request).addStatusMessage(_(u"Campo Movindo para baixo"), "info")
                url = context.context.absolute_url() +  '/edit-form' #?forms_id='+ str(id_form)
                context.request.response.redirect(url)
            
            else:
                url = context.context.absolute_url() +  '/edit-form' #?forms_id='+ str(id_form)
                context.request.response.redirect(url)
            
        # se for um visualização do formulario 
        else:
            data = ModelsForm().get_Forns_byId(id_form)
            
            if data:
                D = {}
                for campo in campos.keys():
                    D[campo] = getattr(data, campo, '') 
                
                form_data['data'] = D
                return form_data
            else:
               return form_data
            
        #se for um formulario de adição
        #else:
        #    return form_data

class LoadRelatorioForm(BaseFunc):

    def registration_processes(self,ctx):
        id_form = int(ctx.context.forms_id)

        #formulario =  ModelsForm().get_Forns_byId(id_form)
        valores =  ModelsForm().get_FormValues(id_form)
        campos = ModelsFormFields().get_Fields_ByIdForm(id_form)
        L=[]
        for campo in campos:
           D={}
           D['titulo'] = campo.title 
           
           if campo.flag_multi:
               D['flag_multi'] = True
               ref = []
               tipo = campo.type_fields
               
               for item in campo.ref_mult:

                   E = {}
                   instances = ModelsFormValues().get_FormValues_byForm_and_Field(id_form, item.name_field)
                   
                   E['title'] = item.title
                   
                   if tipo == 'bool':
                       regs = ModelsFormInstance().get_Instance(id_form)
                       M=[{'name': 'True', 'cont': instances.count()},
                          {'name': 'False', 'cont': regs.count()-instances.count()}]
                       
                       E['dados'] = M  
                       E['quant'] =  regs.count()
                   elif tipo == 'choice' or tipo == 'radio':
                       M = []
                       opcao = campo.list_values.splitlines()
                       for i in opcao:
                           N = {}
                           j = i.split('|')
                           N['name'] = j[1]
                           N['cont'] = 0 
                           
                           for instance in instances:
                               if instance.value == j[0].strip():
                                    N['cont'] +=1 
                        
                           M.append(N)
                       E['dados'] = M
                   
                   elif tipo == 'list':
                       M = []
                       tmp = []
                       opcoes = []
                       opcao = campo.list_values.splitlines()
                       
                       for i in opcao:
                           i = i.split('|')
                           C ={}
                           C['id'] = i[0].replace(' ','')
                           C['val'] = i[1]
                           opcoes.append(C)
                      
                       for instance in instances:
                           tmp.append(self.decodePickle(instance.value))
                       
                       for i in tmp:
                           N ={}
                           text = ''
                           for x in i:
                               for opcao in opcoes:
                                   if x == str(opcao['id']):
                                       text += opcao['val'] + ', ' 
                           
                           N['name'] = text
                           N['cont'] = tmp.count(i)
                           
                           M.append(N)
                    
                       E['dados'] = M
                       
                   else:
                       M = []
                       for instance in instances:
                           valor = instance.value or instance.value_blob
                           
                           if tipo in ['img','file']:
                               arquivo = self.decodePickle(valor)
                               name = arquivo.get('filename','')
                               
                           N={}
                           if tipo == 'img':
                               N['text'] = '<img width="120px" src="%s/form-image?id=%s">' %(getSite().absolute_url(),instance.id)
                               
                           elif tipo == 'file':
                               N['text'] = '<a href="%s/form-file?id=%s" target="_blank">%s</a><br />' %(getSite().absolute_url(), instance.id,name)
                               
                           else:
                               N['text'] = instance.value
                       
                           M.append(N)
                       
                       E['dados'] = M
                       E['text'] = True
                   
                   ref.append(E)
               
              
               D['dados'] = ref
           
           
           instances = ModelsFormValues().get_FormValues_byForm_and_Field(id_form, campo.name_field)
           if instances:  
               D['quant'] =  instances.count()

               tipo = campo.type_fields
               if tipo == 'referencia':
                   continue
               
               else:
                   if tipo == 'bool':
                       regs = ModelsFormInstance().get_Instance(id_form)
                       M=[{'name': 'True', 'cont': instances.count()},
                          {'name': 'False', 'cont': regs.count()-instances.count()}]
                       
                       D['dados'] = M  
                       D['quant'] =  regs.count()
                   elif tipo == 'choice' or tipo == 'radio':
                       M = []
                       opcao = campo.list_values.splitlines()
                       for i in opcao:
                           N = {}
                           j = i.split('|')
                           N['name'] = j[1]
                           N['cont'] = 0 
                           for instance in instances:
                               if instance.value == j[0].strip():
                                    N['cont'] +=1 
                        
                           M.append(N)
                       D['dados'] = M
                   
                   elif tipo == 'list':
                       M = []
                       tmp = []
                       opcoes = []
                       opcao = campo.list_values.splitlines()
                       
                       for i in opcao:
                           i = i.split('|')
                           C ={}
                           C['id'] = i[0].strip() #.replace(' ','')
                           C['val'] = i[1]
                           opcoes.append(C)
                      
                       for instance in instances:
                           tmp.append(self.decodePickle(instance.value))
                       
                       for i in tmp:
                           N ={}
                           text = ''
                           for x in i:
                               for opcao in opcoes:
                                   if unicode(x, 'utf-8') == opcao['id']:
                                       text += opcao['val'] + ', ' 
                           
                           N['name'] = text
                           N['cont'] = tmp.count(i)
                           
                           M.append(N)
                               
                       D['dados'] = M
                       
                   else:
                       M = []
                       for instance in instances:
                           valor = instance.value or instance.value_blob
                           
                           if tipo in ['img','file']:
                               arquivo = self.decodePickle(valor)
                               name = arquivo.get('filename','')
                               
                           N={}
                           if tipo == 'img':
                               N['text'] = '<img width="120px" src="%s/form-image?id=%s">' %(getSite().absolute_url(),instance.id)
                               
                           elif tipo == 'file':
                               N['text'] = '<a href="%s/form-file?id=%s" target="_blank">%s</a><br />' %(getSite().absolute_url(), instance.id,name)
                               
                           else:
                               N['text'] = instance.value
                       
                           M.append(N)
                       
                       D['dados'] = M
                       D['text'] = True
           else:
               D['quant'] = 0
               D[''] = 'Não possui resultados'
           
           L.append(D) 
        
        return L
    


class RegistrationCreateFields(BaseFunc):
    def to_utf8(value):
        return unicode(value, 'utf-8')
                         
    def registration_processes(self,context):
        form = context.request # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)
        #campos = self.campos
        
        id_form = int(context.context.forms_id)
        context.request.form['forms_id'] = id_form
        #id_form = int(form.get('forms_id','0'))
        
        campos = {'name_field'            : {'required': True,  'type':'key',       'label':'Nome do Campo',                'decription':u'Digite o nome para o campo',                                       'ordem':0},
                  'type_fields'           : {'required': True,  'type':'choice',    'label':'Tipo do Campo',                'decription':u'Selecione o tipo da informação deste campo',                      'ordem':1},
                  'list_values'           : {'required': False, 'type':'textarea',  'label':'Lista de dados para o select', 'decription':u'Digite um item por linha no padrão [ID] | [Valor]',                'ordem':2},
                  'title'                 : {'required': True,  'type':self.to_utf8,'label':'Título',                       'decription':u'Digite o título para o campo',                                     'ordem':3},
                  'description_fields'    : {'required': False, 'type':'textarea',  'label':'Descrição',                    'decription':u'Digite a descrição para o campo',                                  'ordem':4},
                  'value_default'         : {'required': False, 'type':'combo',     'label':'Valor Padrão',                 'decription':u'''Digite o comando ou o valor padrão para preenchimento deste campo,\n
                                                                                                                                             este campo funciona com interpretação python''',                 'ordem':5},
                  
                  'flag_multi'            : {'required': False, 'type':'bool',      'label':'Campo multiplo',               'decription':u'Selecione se este campo suportara outros campos dentro dele',      'ordem':6},                                                                                                               
                  'field_ref'             : {'required': False, 'type':'choice',    'label':'Campo multiplo pai',           'decription':u'Selecione o campo multiplo que este campo pertence',               'ordem':7},
                  
                  'required'              : {'required': False, 'type':'bool',      'label':'Campo Obrigatório',            'decription':u'Marque esta opção se o campo for obrigatório',                     'ordem':8},
                  'ordenacao'             : {'required': False, 'type':'hidden',    'label':'Ordenação',                    'decription':u'',                                                                 'ordem':9},
                  'flag_ativo'            : {'required': False, 'type':'bool',      'label':'Campo ativo',                  'decription':u'Marque esta opção se o campo estará ativo para o usuário',         'ordem':10},
                  'forms_id'              : {'required': False, 'type':'hidden',    'label':'Id form',                      'decription':u'',                                                                 'ordem':11}}    
            
        
        lista_itens = {'type_fields':[['text','Campo de Texto'],['textarea','Campo Texto Multiplas Linhas'],
                                      ['bool','Campo Verdadeiro/Falso'],['choice','Campo de Escolha'],
                                      ['list','Campo de Seleção Multipla'],['hidden','Campo Oculto'],
                                      ['img','Campo de Upload de Imagem'],['file','Campo de Upload de Arquivos'],
                                      ['richtext','Campo de Texto Rico'],['radio','Campo de Opção'],
                                      
                                      ['referencia','Campo com referencia a um campo multiplo']
                                      ]
                       }
        #Valores Default
        dados_defaul =  ModelsDefaultValue().get_DefaultValues()
        L = []
        for i in dados_defaul:
            L.append([i.value,i.lable])
        lista_itens['value_default'] = L
        
        #Campos de referencia
        M =[] 
        dados_ref = ModelsFormFields().get_Fields_ByIdForm(id_form)
        for i in dados_ref:
            if i.flag_multi:
                M.append([i.name_field,i.title])
        
        lista_itens['field_ref'] = M
        
        
        # divisao dos dicionarios "errors" e "convertidos"
        form_data = {
            'errors': {},
            'data': {},
            'campos':campos,
            'lista_itens':lista_itens}
        
        
        result_form = ModelsFormFields().get_Fields_ByIdForm(id_form)
        
        # se clicou no botao "Voltar"
        if 'form.voltar' in form_keys:
            success_voltar = context.context.absolute_url() +  '/edit-form' #?forms_id='+str(id_form)
            context.request.response.redirect(success_voltar)
          
        # se clicou no botao "Salvar"
        elif 'form.submited' in form_keys:
            # Inicia o processamento do formulario
            # chama a funcao que valida os dados extraidos do formulario (valida_form) 
            errors, data = valida_form(context,campos, context.request.form)  
            
            if not errors:
                if 'forms_id'in form_keys and 'id_fields' in form_keys:
                    # editando...
                    id_fields = int(form.get('id_fields','0'))
                    result_fields = ModelsFormFields().get_Fields_byId(id_form,int(id_fields))
                    if result_fields:
                        for campo in campos.keys():
                            value = data.get(campo, None)
                            setattr(result_fields, campo, value)
                        
                        IStatusMessage(context.request).addStatusMessage(_(u"Campo editado com com sucesso"), "info")
                        url = context.context.absolute_url() +  '/edit-form' #?forms_id='+ str(id_form)
                        context.request.response.redirect(url)

                else:
                    if ModelsFormFields().check_fields(data['name_field'],id_form): 
                        #adicionando...
                        ModelsFormFields().set_FormFields(**data)
                        IStatusMessage(context.request).addStatusMessage(_(u"Campo adicionado com sucesso"), "info")
                        url = context.context.absolute_url() +  '/edit-form' #?forms_id='+ str(id_form)
                        context.request.response.redirect(url)
                    
                    else:
                        IStatusMessage(context.request).addStatusMessage(_(u"Já existe um campo com este nome"), "info")
                        url = context.context.absolute_url() +  '/edit-form' #?forms_id='+ str(id_form)
                        context.request.response.redirect(url)
                                   
            else:
                form_data['errors'] = errors
                form_data['data'] = data
                return form_data
          
        # se for um formulario de edicao 
        elif 'id_fields' in form_keys: #'forms_id'in form_keys and :
            id_fields = int(form.get('id_fields','0'))
            data = ModelsFormFields().get_Fields_byId(int(id_form),int(id_fields))
            campos['name_field'] = {'required': True,  'type':'hidden','label':'Nome do Campo', 'decription':u'', 'ordem':0}
            
            if data:
                D = {}
                for campo in campos.keys():
                    D[campo] = getattr(data, campo, '') 
                
                form_data['data'] = D
                return form_data
            else:
               return form_data
            
        #se for um formulario de adição
        else:
            data = {}
            data['ordenacao'] = result_form.count() 
            form_data['data'] = data
            return form_data
        
class RegistrationAddDefaultValue(BaseFunc):
    def to_utf8(value):
        return unicode(value, 'utf-8')
      
    campos = {'value': {'required': True, 'type' : to_utf8,'label':'Médoto ou Valor Padrão', 'decription':u'Digite um método ou valor padrão em formato python','ordem':0},
              'lable': {'required': True, 'type' : to_utf8,'label':'Nome do método',         'decription':u'Digite a descrição do método',                      'ordem':1},}
                        
    def registration_processes(self,context):
        success = context.context.absolute_url() +  '/manage-form'
        form = context.request # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)
        campos = self.campos
        
        # divisao dos dicionarios "errors" e "convertidos"
        form_data = {
            'errors': {},
            'data': {},
            'campos':campos,}

        # se clicou no botao "Voltar"
        if 'form.voltar' in form_keys:
            context.request.response.redirect(success)
          
        # se clicou no botao "Salvar"
        elif 'form.submited' in form_keys:
            # Inicia o processamento do formulario
            # chama a funcao que valida os dados extraidos do formulario (valida_form) 
            errors, data = valida_form(context, campos, context.request.form)  

            if not errors:
                if 'id' in form_keys:
                    # editando...
                    id = int(form.get('id',''))
                    result = ModelsDefaultValue().get_DefaultValue_byId(id)
                    if result:
                        for campo in campos.keys():
                            value = data.get(campo, None)
                            setattr(result, campo, value)
                    
                    IStatusMessage(context.request).addStatusMessage(_(u"Valor editado com sucesso"), "info")
                    context.request.response.redirect(success)

                else:
                    #adicionando...
                    id = ModelsDefaultValue().set_DefaultValue(**data)
                    IStatusMessage(context.request).addStatusMessage(_(u"Valor adicionado com sucesso"), "info")
                    context.request.response.redirect(success)
                                   
            else:
                form_data['errors'] = errors
                form_data['data'] = data
                return form_data

            
        # se for um formulario de edicao 
        elif 'id' in form_keys:
            id = int(form.get('id',''))
            data = ModelsDefaultValue().get_DefaultValue_byId(id)
            
            if data:
                D = {}
                for campo in campos.keys():
                    D[campo] = getattr(data, campo, '') 
                
                form_data['data'] = D
                return form_data
            else:
               return form_data
            
        #se for um formulario de adição
        else:
            return form_data

class RegistrationExcluirDefault(BaseFunc):

    def exclud_processes(self,ctx):        
        form = ctx.request # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)
        id = int(form.get('id','0'))
        success_url = ctx.context.absolute_url() +  '/manage-form'
        
        # se clicou no botao "Voltar"
        if 'form.voltar' in form_keys:
            ctx.request.response.redirect(success_url)
          
        # se clicou no botao "Salvar"
        elif 'form.submited' in form_keys:
            # Inicia o processamento do formulario
            record = ModelsDefaultValue().get_DefaultValue_byId(id)
            if record:
                self.store.remove(record)
                self.store.flush()
            
            IStatusMessage(ctx.request).addStatusMessage(_(u'Valor removido com sucesso.'), 'info')  
            ctx.request.response.redirect(success_url)


class RegistrationParametrosForm(BaseFunc):
    def to_utf8(self, value):
        return unicode(value, 'utf-8')
                            
    def registration_processes(self,context):
        form = context.request # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)
        
        id_form = int(context.context.forms_id)
        success_url = context.context.absolute_url()
        
        # divisao dos dicionarios "errors" e "convertidos"
        form_data = {
            'errors': {},
            'data': {},
            'campos':{},}

        result = ModelsParametersForm().get_ParametersForm_byFormId(id_form)
        fields = ModelsForm().get_Forns_byId(id_form).fields
        form_data['campos'] = fields

        # se clicou no botao "Voltar"
        if 'form.voltar' in form_keys:
            ctx.request.response.redirect(success_url)
          
        # se clicou no botao "Salvar"
        elif 'form.submited' in form_keys:
            ModelsParametersForm().del_ParametersForm(id_form)
            if 'form_fields' in form_keys:
                ModelsParametersForm().del_ParametersForm(id_form)
                valor = form.get('form_fields',[])
                if type(valor) != list:
                    L = []
                    L.append(valor)
                else:
                    L = valor
                    
                for i in L:
                    D={}
                    D['forms_id'] = id_form
                    D['fields_id'] = int(i)
                    ModelsParametersForm().set_ParametersFor(**D)            
            
            if 'parameters' in form_keys and 'value_parameters' in form_keys:
                param = form.get('parameters',[])
                valor = form.get('value_parameters',[])
                
                if type(param) != list:
                    P = []
                    P.append(param)
                else:
                    P = param
                
                if type(valor) != list:
                    L = []
                    L.append(valor)
                else:
                    L = valor
                
                count = 0
                for i in P:
                    D={}
                    D['forms_id'] = id_form
                    D['parameters'] = self.to_utf8(i)
                    D['value_parameters'] = self.to_utf8(L[count])
                
                    ModelsParametersForm().set_ParametersFor(**D)
                    count +=1    
                
            IStatusMessage(context.request).addStatusMessage(_(u'Parametros cadastrados com sucesso.'), 'info')  
            context.request.response.redirect(success_url)
        
        # se for um formulario de edicao 
        elif result:
            data = {}
            fields = []
            parameters = []
            for item in result:
                if item.fields_id:
                    fields.append(item)
                elif item.parameters:
                    parameters.append(item)    
                 
            data['form_fields'] = fields
            data['parameters'] = parameters
            form_data['data'] = data 
            return form_data

        
        #se formulario de listagem dos campos
        else:
            return form_data

        
class RegistrationEditViewForm(BaseFunc):
    def to_utf8(self, value):
        return unicode(value, 'utf-8')
                            
    def registration_processes(self,context):
        form = context.request # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)
        
        # divisao dos dicionarios "errors" e "convertidos"
        form_data = {
            'errors': {},
            'data': {},
            'campos':{},}

        # se clicou no botao "Voltar"
        if 'form.voltar' in form_keys:
            ctx.request.response.redirect(success_url)
          
        # se clicou no botao "Salvar"
        elif 'form.submited' in form_keys:
                
            IStatusMessage(context.request).addStatusMessage(_(u'View cadastrados com sucesso.'), 'info')  
            context.request.response.redirect(success_url)
        
        # se for um formulario de edicao 
        elif result:
            data = {}
            fields = []
            parameters = []
            for item in result:
                if item.fields_id:
                    fields.append(item)
                elif item.parameters:
                    parameters.append(item)    
                 
            data['form_fields'] = fields
            data['parameters'] = parameters
            form_data['data'] = data 
            return form_data

        
        #se formulario de listagem dos campos
        else:
            return form_data        
        

class RegistrationLoadForm(BaseFunc):
    def to_utf8(value):
        return unicode(value, 'utf-8')
                            
    def registration_processes(self,context,isForm=True):
        form = context.request # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)
        
        id_form = int(context.context.forms_id)
        success_url = context.context.absolute_url()
        
        campos = {}
        lista_itens = {}
        default_value = {}
        n = 0
        fields = ModelsForm().get_Forns_byId(int(id_form))
        if fields:
            for field in fields.fields:
                if field.flag_ativo:
                    M={}
                    M['required'] = field.required
                    M['type'] = field.type_fields
                    M['label'] = field.title
                    M['decription'] = field.description_fields
                    M['ordem'] = field.ordenacao
                    M['flag_multi'] = field.flag_multi
                    
                    campos[field.name_field] = M
                else:
                    campos['outro'+str(n)] = {'ordem':field.ordenacao}     
                    n += 1
                    
                if field.type_fields == 'choice' or\
                   field.type_fields == 'list' or\
                   field.type_fields == 'radio':
                    items = field.list_values.splitlines()
                    D=[]
                    for i in items:
                        L = i.split(' | ')
                        #D[L[0].replace(' ','')] = L[1]
                        D.append(L)
                        
                    lista_itens[field.name_field] = D
                    
#                if field.type_fields == 'list':
#                    items = field.list_values.splitlines()
#                    D={}
#                    for i in items:
#                        L = i.split('|')
#                        D[L[0].replace(' ','')] = L[1]
#                    
#                    lista_itens[field.name_field] = D
                
                if field.value_default:
                    default_value[field.name_field] = field.value_default
                 
        # divisao dos dicionarios "errors" e "convertidos"
        form_data = {
            'errors': {},
            'data': {},
            'campos':campos,
            'lista_itens':lista_itens,
            'default_value':default_value}
        
        # se clicou no botao "Voltar"
        if 'form.voltar' in form_keys:
            if 'id_instance' in form_keys and isForm:
                context.request.response.redirect(success_url+'/view-form')
            else:
                context.request.response.redirect(destino_form)
                
        # se clicou no botao "Salvar"
        elif 'form.submited' in form_keys:
            # Inicia o processamento do formulario
            # chama a funcao que valida os dados extraidos do formulario (valida_form)
            errors, data = valida_form(context, campos, context.request.form)
          
            if not errors:
                
                if isForm: 
                    #Rotina para a ação de destino do formulario e ação do formulario
                    acao_destino = context.context.acao_destino
                    acoes = context.context.acao_saida
                else:
                    aq = context.context.aq_parent
                    acao_destino = 'contexto'
                    acoes = aq.acao_saida
                
                if acao_destino == 'doc_plone':
                    if context.context.doc_plone:
                        destino_form = context.context.doc_plone.to_object.absolute_url()
                
                elif acao_destino == 'url': 
                    if context.context.url:
                        url = str(context.context.url)
                        if url.find('http://') != -1:
                            destino_form = str(context.context.url)
                        else:
                            destino_dorm = context.context.absolute_url() + str(context.context.url)
                    
                elif acao_destino == 'parameto':
                    if context.context.parameto:
                        result_parametros = ModelsParametersForm().get_ParametersForm_byFormId(id_form)
                        string = ''
                        if result_parametros:
                            parametros = {}
                            for param in result_parametros:
                                if param.fields_id:
                                    field = ModelsFormFields().get_Fields_byIdField(param.fields_id)
                                    if field:
                                        parametros[field.name_field] = data[field.name_field]
                                
                                elif param.parameters:
                                    parametros[param.parameters] = param.value_parameters
                            
                            for parametro in parametros.keys():
                                string += parametro +'='+ parametros.get(parametro,'') +'&'
                        
                        url = str(context.context.parameto)    
                        if url.find('http://') != -1:
                            destino_form = url + '?'+string
                        else:
                            destino_dorm = context.context.absolute_url() + url + '?'+string
                        
                else:
                    destino_form = success_url
                
                for acao in acoes:
                    if acao == 'savedb':
                        if 'id_instance' in form_keys:
                            # editando...
                            id_instance = int(form.get('id_instance',0))
                            results = ModelsFormValues().get_FormValues_byForm_and_Instance(id_form,id_instance)
                            if results:
                                for campo in campos.keys():
                                    if not 'outro' in campo:
                                       for result in results:
                                           if result.fields == campo:
                                               valor = data[campo]
                                               D={}
                                               if valor:
                                                   if type(valor) != bool:
                                                       if len(valor) < 65000:
                                                           if type(valor) == unicode:
                                                               result.value = valor.strip()
                                                               result.value_blob = None
                                                           else:
                                                               result.value = unicode(str(valor), 'utf-8')
                                                               result.value_blob = None
                                                       else:
                                                           result.value_blob = valor   
                                                           result.value = None 
                                                   else:
                                                       D['value'] = unicode(str(valor), 'utf-8')
                                                   
                                                   result.date_creation = datetime.now()
                                                   self.store.commit()
                                               
                                               elif campos[campo]['type'] == u'bool':
                                                    result.value = unicode(str(valor), 'utf-8')
                                                        
                                                    result.date_creation = datetime.now()
                                                    self.store.commit()             
                                        
                                       else:
                                           if results.find(fields=campo).count() == 0 and not 'outro' in campo:
                                                valor = data[campo]
                                                if valor:
                                                    D={}
                                                    D['forms_id'] = id_form
                                                    D['instance_id'] = id_instance
                                                    D['fields'] = campo
                                                    
                                                    if type(valor) != bool:
                                                        if len(valor) < 65000:
                                                            if type(valor) == unicode:
                                                                D['value'] = valor.strip()
                                                                D['value_blob'] = None
                                                            else:
                                                                D['value'] = unicode(str(valor), 'utf-8')
                                                                D['value_blob'] = None
                                                        else:
                                                            D['value'] = None
                                                            D['value_blob'] = valor
                                                    else:
                                                        D['value'] = unicode(str(valor), 'utf-8')
                                                        
                                                    ModelsFormValues().set_FormValues(**D)
                                                
                                                elif campos[campo]['type'] == u'bool':
                                                    D={}
                                                    D['forms_id'] = id_form
                                                    D['instance_id'] = id_instance
                                                    D['fields'] = campo

                                                    D['value'] = unicode(str(valor), 'utf-8')
                                                    D['value_blob'] = None
                                                        
                                                    ModelsFormValues().set_FormValues(**D)
        
                        else:
                            #adicionando...
                            id_instance = ModelsFormInstance().set_FormInstance(id_form)
                            for field in data:
                                valor = data[field]
                                if valor:
                                    D={}
                                    D['forms_id'] = int(id_form)
                                    D['instance_id'] = id_instance
                                    D['fields'] = field
                                    
                                    if type(valor) != bool:
                                        if len(valor) < 65000:
                                            if type(valor) == unicode:
                                                D['value'] = valor.strip()
                                            else:
                                                D['value'] = unicode(str(valor), 'utf-8')
                                        else:
                                            D['value_blob'] = valor
                                    
                                    else:
                                        D['value'] = unicode(str(valor), 'utf-8')
                                    
                                    ModelsFormValues().set_FormValues(**D)
                            
                            if 'content_type' in acoes:
                                count = 0
                                name_file = name_file_org = 'conteudo-'+context.context.id
                                title_file = title_file_org = 'Conteúdo - '+ context.context.Title()
                                while name_file in context.context.objectIds():
                                    name_file = name_file_org + '-' + str(count)
                                    title_file = title_file_org + ' - ' + str(count)
                                    count +=1
                                
                                objects = {'type_name':'vindula.contentcore.conteudobasico',
                                           'id': name_file,
                                           'title':name_file,
                                           
                                           'forms_id':id_form,
                                           'instance_id':id_instance}

                                context.context.invokeFactory(**objects)  
                
                    elif acao == 'email':
                        emails = context.context.list_email
                        if emails:
                            emails = emails.splitlines()
                        else:
                            emails = []
                        assunto = 'E-mail enviado do Formulário - %s'%(context.context.Title())
                        
                        msg = []
                        arquivos = []
                        i=0
                        while i < len(campos.keys()):
                            msg.append(i)
                            i+=1
                       
                        for campo in campos:
                            index = campos[campo].get('ordem',0)
                            x = ''
                            if campos[campo].get('type','') == 'file' or \
                                campos[campo].get('type','') == 'img':
                                    
                                decode = self.decodePickle(data.get(campo))
                                arquivos.append(decode)
                                                                
                            else:
                                x = "%s: %s" % (campos[campo].get('label',''),data.get(campo,''))
                            
                            msg.pop(index)
                            msg.insert(index, x)  
                        
                        if context.context.email_padrao:
                            to_email = data.get(context.context.email_padrao)
                        else:
                            to_email = None
                        
                        # Pega o conteudo impresso na tela e define como mensagem
                        msg = '\n<br>'.join(msg)
                        
                        envio = False
                        for email in emails:
                            envio = self.envia_email(context,msg, assunto, email,arquivos,to_email)
                        
                        if envio:
                            IStatusMessage(context.request).addStatusMessage(_(u"E-mail foi enviado com sucesso."), "info")
                        else:
                            IStatusMessage(context.request).addStatusMessage(_(u"Não foi possivel enviar o e-mail contate o administrados do portal."), "error")
                    
                    elif acao == 'content_type':
                        if not 'savedb' in acoes:
                            if 'id_instance' in form_keys:
                                # editando...
                                id_instance = int(form.get('id_instance',0))
                                results = ModelsFormValues().get_FormValues_byForm_and_Instance(id_form,id_instance)
                                if results:
                                    for campo in campos.keys():
                                        if not 'outro' in campo:
                                           for result in results:
                                               if result.fields == campo:
                                                   valor = data[campo]
                                                   D={}
                                                   if valor:
                                                       if type(valor) != bool:
                                                           if len(valor) < 65000:
                                                               if type(valor) == unicode:
                                                                   result.value = valor.strip()
                                                                   result.value_blob = None
                                                               else:
                                                                   result.value = unicode(str(valor), 'utf-8')
                                                                   result.value_blob = None
                                                           else:
                                                               result.value_blob = valor   
                                                               result.value = None 
                                                       else:
                                                           D['value'] = unicode(str(valor), 'utf-8')
                                                       
                                                       result.date_creation = datetime.now()
                                                       self.store.commit()
                                                   
                                                   elif campos[campo]['type'] == u'bool':
                                                        result.value = unicode(str(valor), 'utf-8')
                                                            
                                                        result.date_creation = datetime.now()
                                                        self.store.commit()             
                                            
                                           else:
                                               if results.find(fields=campo).count() == 0 and not 'outro' in campo:
                                                    valor = data[campo]
                                                    if valor:
                                                        D={}
                                                        D['forms_id'] = id_form
                                                        D['instance_id'] = id_instance
                                                        D['fields'] = campo
                                                        
                                                        if type(valor) != bool:
                                                            if len(valor) < 65000:
                                                                if type(valor) == unicode:
                                                                    D['value'] = valor.strip()
                                                                    D['value_blob'] = None
                                                                else:
                                                                    D['value'] = unicode(str(valor), 'utf-8')
                                                                    D['value_blob'] = None
                                                            else:
                                                                D['value'] = None
                                                                D['value_blob'] = valor
                                                        else:
                                                            D['value'] = unicode(str(valor), 'utf-8')
                                                            
                                                        ModelsFormValues().set_FormValues(**D)
                                                    
                                                    elif campos[campo]['type'] == u'bool':
                                                        D={}
                                                        D['forms_id'] = id_form
                                                        D['instance_id'] = id_instance
                                                        D['fields'] = campo
    
                                                        D['value'] = unicode(str(valor), 'utf-8')
                                                        D['value_blob'] = None
                                                            
                                                        ModelsFormValues().set_FormValues(**D)

                            else:
                                #adicionando...
                                id_instance = ModelsFormInstance().set_FormInstance(id_form)
                                for field in data:
                                    valor = data[field]
                                    if valor:
                                        D={}
                                        D['forms_id'] = int(id_form)
                                        D['instance_id'] = id_instance
                                        D['fields'] = field
    
                                        if type(valor) != bool:                                                  
                                            if len(valor) < 65000:
                                                if type(valor) == unicode:
                                                    D['value'] = valor.strip()
                                                else:
                                                    D['value'] = unicode(str(valor), 'utf-8')
                                            else:
                                                D['value_blob'] = valor
                                        else:
                                            D['value'] = unicode(str(valor), 'utf-8')
                                    
                                        ModelsFormValues().set_FormValues(**D)
                                
                                count = 0
                                name_file = name_file_org = 'conteudo-'+context.context.id
                                title_file = title_file_org = 'Conteúdo - '+ context.context.Title()
                                while name_file in context.context.objectIds():
                                    name_file = name_file_org + '-' + str(count)
                                    title_file = name_file_org + ' - ' + str(count)
                                    count +=1
                                
                                objects = {'type_name':'vindula.contentcore.conteudobasico',
                                           'id': name_file,
                                           'title':name_file,
                                           
                                           'forms_id':id_form,
                                           'instance_id':id_instance}
    
                                context.context.invokeFactory(**objects)  
                            
                #Redirect back to the front page with a status message
                mensagem = context.context.mensagem
                if mensagem:
                    IStatusMessage(context.request).addStatusMessage(_(mensagem), "info")
                
                context.request.response.redirect(destino_form)
                        
                if not acoes:
                    # Menssagem de Erro na ação - volta para a view do formulario
                    IStatusMessage(context.request).addStatusMessage(_(u"Ação Indisponível, contate o administrados do portal."), "error")
                    context.request.response.redirect(success_url)
             
            else:
                form_data['errors'] = errors
                form_data['data'] = data
                return form_data           
          
        # se for um formulario de edicao 
        elif 'id_instance' in form_keys:
            id_instance = int(form.get('id_instance','0'))
            data_value = ModelsFormValues().get_FormValues_byForm_and_Instance(int(id_form),id_instance)
            
            if data_value:
                D = {}
                for campo in campos.keys():
                    for data in data_value:
                        if data.fields == campo:
                            D[campo] = data.value 
                
                form_data['data'] = D
                return form_data
            else:
                return form_data
        
        else:
            return form_data
        
        
class RegistrationExcluirForm(BaseFunc):

    def exclud_processes(self,ctx):        
        form = ctx.request # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)
        
        id_form = int(ctx.context.forms_id)
        id_instance = int(form.get('id_instance',''))
        success_url = ctx.context.absolute_url() +  '/view-form' #?forms_id=' + str(id_form)
        
        # se clicou no botao "Voltar"
        if 'form.voltar' in form_keys:
            ctx.request.response.redirect(success_url)
          
        # se clicou no botao "Salvar"
        elif 'form.submited' in form_keys:
            # Inicia o processamento do formulario
            records = ModelsFormValues().get_FormValues_byForm_and_Instance(int(id_form),id_instance)
            for record in records:
                self.store.remove(record)
                self.store.flush()
            
            ModelsFormInstance().del_Instance(id_form,id_instance)    
            
            IStatusMessage(ctx.request).addStatusMessage(_(u"Registro removido com sucesso."), "info")  
            ctx.request.response.redirect(success_url)



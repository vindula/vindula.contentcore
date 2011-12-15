# coding: utf-8
from vindula.myvindula.user import BaseStore
from vindula.contentcore.models import ModelsFormValues
import pickle
import datetime


class BaseFunc(BaseStore):
    #default class for standard functions

    # define se aparece ou nao as mensagens e marcacoes de erros  
    def field_class(self, errors, field_name):
        if errors is not None:
            if errors.get(field_name, None) is not None:
                return 'field error'                   
            else:
                 return 'field'
        else:
              return 'field'

    def TypesFields(self,type):
        D = {'text':'campo de texto','textarea':'campo text area','bool':'campo booleano',
             'choice':'campo de seleção', 'list':'campo de seleção multipla','hidden':'campo Oculto',
             'img':'Campo de Upload de Imagem','file':'Campo de Upload de Arquivos'}
        if type:
            return D.get(type)
        else:
            return None

          
    def checaEstado(self,config, campo):
        if config:
            try:
                return config.__getattribute__(campo)
            except:
                return True
        else:
            return True
    
    def getValue(self,campo,request,data,default_value):
        if campo in request.keys():
            if request.get(campo, None):
                return request.get(campo,'')
            else:
                return ''
        elif campo in data.keys():
            return data.get(campo,'')
            
        else:
            default = eval(default_value.get(campo,'None'))
            if default: 
                return default
            else:
                return '' 
    
    def getValueList(self,campo,request,data,default_value):
        if campo in request.keys():
            if request.get(campo, None):
                return request.get(campo,[])
            else:
                return []
        elif data:
            L = data.get(campo)
            return self.decodePickle(L)
        else:
            default = eval(default_value.get(campo,'None'))
            if type(default) == list:
                return default
            else:
                return []    
            
    def getPhoto(self,campo,request,data):
        if campo in request.keys():
            if request.get(campo, None):
                return ''
            else:
                id_form = int(request.get('forms_id','0'))
                id_instance = int(request.get('id_instance','0'))
                field = campo
                result = ModelsFormValues().get_FormValues_byForm_and_Instance_and_Field(id_form,id_instance,field)
                if result:
                    return '../form-image?id=%s' % result.id
            
        elif campo in data.keys():
            id_form = int(request.get('forms_id','0'))
            id_instance = int(request.get('id_instance','0'))
            field = campo
            result = ModelsFormValues().get_FormValues_byForm_and_Instance_and_Field(id_form,id_instance,field)
            if result:
                return '../form-image?id=%s' % result.id

            else:
                return ''
        else:
            return ''  
    
    def getFile(self,campo,request,data):
        if campo in request.keys():
            if request.get(campo, None):
                return ''
            else:
                id_form = int(request.get('forms_id','0'))
                id_instance = int(request.get('id_instance','0'))
                field = campo
                result = ModelsFormValues().get_FormValues_byForm_and_Instance_and_Field(id_form,id_instance,field)
                if result:
                    return '../form-file?id=%s' % result.id
            
        elif campo in data.keys():
            id_form = int(request.get('forms_id','0'))
            id_instance = int(request.get('id_instance','0'))
            field = campo
            result = ModelsFormValues().get_FormValues_byForm_and_Instance_and_Field(id_form,id_instance,field)
            if result:
                return '../form-file?id=%s' % result.id

            else:
                return ''
        else:
            return ''     
        
    def getParametersFromURL(self, ctx):
        traverse = ctx.context.REQUEST.get('traverse_subpath')
        vars = {}
        if traverse != None:
            size = len(traverse)
            counter = 0
            for i in range(size/2):
                position = i+counter
                vars.update({traverse[position]:traverse[position+1]})
                counter+=1
        return vars
                
        
    def checked(self,campo,request,data,default_value):
        if campo in request.keys():
            if request.get(campo, '') == True or\
                request.get(campo,'') == 'True':
                return "checked"
            else:
                return ""
        elif campo in data.keys():
            if data.get(campo,'') == True or\
                data.get(campo,'') == 'True':
                return "checked"
            else:
                return ""
        else:
            if eval(default_value.get(campo,'None')):
                return "checked"
            else:
                return ""    
        
    # retorna dado convertido para o campos de data 
    def converte_data(self, data, data_atual=False):
        if data is not None and data != '':
            if type(data) == date:
                return data.strftime('%d/%m/%Y')
            else:
                return data
        else:
            if data_atual == True:
                data = date.today()
                dia = data.day
                mes = data.month
                ano = data.year
        
                if dia < 10:
                    dia = '0' + str(dia)
                else:
                    dia = str(dia)
                    
                if mes < 10:
                    mes = '0' + str(mes)
                else:
                    mes = str(mes)
                    
                datastr = dia + '/' + mes + '/' + str(ano)
        
                return datastr  
            else:
                return data

    def decodePickle(self,valor):
        if valor:
            return pickle.loads(str(valor))
        else:
            return ''


    def geraHTMLContent(self,id,tipo,valor):
        if tipo == 'list':
            return self.decodePickle(valor)
        
        elif tipo == 'img':
            if id:
                return '<img width="100px" src="../form-image?id=%s">' % id
            else:
                return ''
        
        elif tipo == 'file':
            if id:
                return '<a href="../form-file?id=%s" target="_blank">Download do Arquivo</a><br />'% id
            else:
                return ''
        
        else:
            return valor


    def geraCampos(self,form_data):
        if type(form_data) == dict:
            errors = form_data.get('errors',None)
            data = form_data.get('data',None)
            campos = form_data.get('campos',None)
            value_choice = form_data.get('lista_itens',{})
            default_value = form_data.get('default_value',{})

            html=[]
            i=0
            while i < len(campos.keys()):
                html.append(i)
                i+=1
            
            for campo in campos.keys():
                type_campo = campos[campo]['type']
                index = campos[campo].get('ordem',0)
                tmp = ""
                tmp += "<!-- Campo %s -->"%(campo)
                tmp += "<div class='%s' id='%s'>"%(self.field_class(errors, campo),campo)
                
                if type_campo != 'hidden':
                    tmp += "   <label for='%s'>%s</label>"%(campo,campos[campo]['label'])
                    if campos[campo]['required'] == True and type_campo != 'hidden':
                        tmp += "   <span class='fieldRequired' title='Obrigatório'>(Obrigatório)</span>"
    
                    tmp += "   <div class='formHelp'>%s.</div>"%(campos[campo]['decription'])   
                    tmp += "   <div >%s</div>"%(errors.get(campo,''))
                
                if type_campo == 'hidden':
                    tmp += "<input id='%s' type='hidden' value='%s' name='%s' size='25'/>"%(campo,self.getValue(campo,self.request,data,default_value),campo)
                
                elif type_campo == 'img':
                    if errors:
                        if data:
                            tmp += "<img src='%s' style='width:100px;height:100px;' /><br />"%(self.getPhoto(campo,self.request,data))
                    else: 
                        if self.getPhoto(campo,self.request,data):
                            tmp += "<img src='%s' style='width:100px;height:100px;' /><br />"%(self.getPhoto(campo,self.request,data))
                    tmp += "<input id='%s' type='file' value='%s' name='%s' size='25' />"%(campo,self.getPhoto(campo,self.request,data),campo)
                
                elif type_campo == 'file':
                    if errors:
                        if data:
                            tmp += "<a href='%s' target='_blank'>Download do Arquivo</a><br />"%(self.getFile(campo,self.request,data))
                    else:
                        if self.getFile(campo,self.request,data):
                            tmp += "<a href='%s' target='_blank'>Download do Arquivo</a><br />"%(self.getFile(campo,self.request,data))
                    tmp += "<input id='%s' type='file' value='%s' name='%s' size='25' />"%(campo,self.getFile(campo,self.request,data),campo)
                
                elif type_campo == 'date':
                    tmp += """<input id='%s' type='text' maxlength='10' onKeyDown='Mascara(this,Data);' onKeyPress='Mascara(this,Data);' onKeyUp='Mascara(this,Data);'
                                     value='%s' name='%s' size='25'/>"""%(campo,self.converte_data(self.getValue(campo,self.request,data,default_value),True),campo)
    
                elif type_campo == 'textarea':
                    tmp += "<textarea id='%s' name='%s' style='width: 100; height: 81px;'>%s</textarea>"%(campo, campo, self.getValue(campo,self.request,data,default_value)) 
                
                elif type_campo == 'bool':
                    tmp += "<input id='%s' type='checkbox' value='%s' name='%s' size='25' %s/>"%(campo,'True',campo,self.checked(campo,self.request,data,default_value))
                
                elif type_campo == 'list':
                    tmp += "<div class='boxSelecao' name='%s'>"%(campo)
                    for item in value_choice[campo]:
                        lable =  value_choice[campo][item]
                        if item in self.getValueList(campo,self.request,data,default_value):
                            tmp += "<input value='%s' type='checkbox' checked name='%s'/><label>%s</label><br/>"%(item,campo,lable)
                        else:
                            tmp += "<input value='%s' type='checkbox' name='%s'/><label>%s</label><br/>"%(item,campo,lable)
                    tmp += "</div>" 
                
                elif type_campo == 'choice':
                    tmp += "<select name='%s'>"%(campo)
                    tmp += "<option value="">-- Selecione --</option>"
                    for item in value_choice[campo]:
                        if item == self.getValue(campo,self.request,data,default_value):
                            tmp +="<option value='%s' selected>%s</option>"%(item, value_choice[campo][item])
                        else:
                            tmp +="<option value='%s'>%s</option>"%(item, value_choice[campo][item])
                                    
                    tmp += "</select>"
                    
                else:
                    tmp += "<input id='%s' type='text' value='%s' name='%s' size='25'/>"%(campo,self.getValue(campo,self.request,data,default_value),campo)

                tmp += "</div>"
                
                html.pop(index)
                html.insert(index, tmp)    
            
            return html

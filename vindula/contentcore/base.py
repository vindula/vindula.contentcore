# -*- coding: utf-8 -*-
from vindula.myvindula.user import BaseStore
from vindula.contentcore.models import ModelsFormValues
import pickle
import datetime

#from Products.TinyMCE.utility import TinyMCE, form_adapter
from zope.component import getUtility
from Products.TinyMCE.interfaces.utility import ITinyMCE

# Import para envio de E-mail
#from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.MIMEImage import MIMEImage
from email import Encoders

#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc
from zope.component import getUtility
from storm.zope.interfaces import IZStorm
from storm.locals import Store
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.statusmessages.interfaces import IStatusMessage
from datetime import date , datetime 

class BaseStore(object):
   
    def __init__(self, *args, **kwargs):
        self.store = getUtility(IZStorm).get('myvindula')
        
        #Lazy initialization of the object
        for attribute, value in kwargs.items():
            if not hasattr(self, attribute):
                raise TypeError('unexpected argument %s' % attribute)
            else:
                setattr(self, attribute, value)        
  
        # divide o dicionario 'convertidos'
        for key in kwargs:
            setattr(self,key,kwargs[key])
        # adiciona a data atual
        self.date_creation = datetime.now()    


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
        D = {'text':'Campo de Texto','textarea':'Campo Texto Multiplas Linhas',
             'bool':'Campo Verdadeiro/Falso','choice':'Campo de Escolha',
             'list':'Campo de Seleção Multipla','hidden':'Campo Oculto',
             'img':'Campo de Upload de Imagem','file':'Campo de Upload de Arquivos',
             'richtext':'Campo de Texto Rico'} 
        
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
        #import pdb;pdb.set_trace() 
        if campo in request.keys():
            if request.get(campo, None):
                return request.get(campo,'')
            else:
                return ''
        elif campo in data.keys():
            if data.get(campo,None) != None:
                return data.get(campo,'')
            else:
                return ''

        else:
            try:
                default = eval(default_value.get(campo,'None'))
                if default: 
                    return default
                else:
                    return '' 
            except:
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

    def envia_email(self,ctx, msg, assunto, mail_para, arquivos,to_email=None):
        """
        Parte do codigo retirado de:
            - http://dev.plone.org/collective/browser/ATContentTypes/branches/release-1_0-branch/lib/imagetransform.py?rev=10162
            - http://www.thescripts.com/forum/thread22918.html
            - http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/473810
        """

        portal = getSite()

        # Cria a mensagem raiz, configurando os campos necessarios para envio da mensagem.
        mensagem = MIMEMultipart('related')
        mensagem['Subject'] = assunto

        #Pega os remetentes do email pelas configurações do zope @@mail-controlpanel
        if to_email:
            mensagem['From'] = '%s <%s>' % (to_email,to_email)
        else:
            mensagem['From'] = '%s <%s>' % (portal.getProperty('email_from_name'),
                                            portal.getProperty('email_from_address'))
        
        mensagem['To'] = mail_para
        mensagem.preamble = 'This is a multi-part message in MIME format.'
        mensagem.attach(MIMEText(msg, 'html', 'utf-8'))
        
        # Atacha os arquivos
        for f in arquivos:
            if type(f) == dict:
                parte = MIMEBase('application', 'octet-stream')
                parte.set_payload(f.get('data',f))
                Encoders.encode_base64(parte)
                parte.add_header('Content-Disposition', 'attachment; filename="%s"' % f.get('filename','image.jpeg'))
                
                mensagem.attach(parte)
        
        mail_de = mensagem['From']

        #Pegando SmtpHost Padrão do Plone
        smtp_host   = ctx.context.MailHost.smtp_host
        smtp_port   = ctx.context.MailHost.smtp_port
        smtp_userid = ctx.context.MailHost.smtp_uid
        smtp_pass   = ctx.context.MailHost.smtp_pwd
        server_all  = '%s:%s'%(smtp_host,smtp_port)

        smtp = smtplib.SMTP()
        try:
            smtp.connect(server_all)
            #Caso o Usuario e Senha estejam preenchdos faz o login
            if smtp_userid and smtp_pass:
                try:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login(smtp_userid, smtp_pass)
                except:
                    smtp.login(smtp_userid, smtp_pass)
                    
            smtp.sendmail(mail_de, mail_para, mensagem.as_string())
            smtp.quit()
        except:
            return False

        return True

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
                index = campos[campo].get('ordem',0)
                tmp = ""
                if not 'outro' in campo:
                    type_campo = campos[campo]['type']
                    if type_campo == 'richtext':
                        classe = 'richTextWidget'
                    else:
                        classe = ''
                    
                    tmp += "<!-- Campo %s -->"%(campo)
                    tmp += "<div class='%s' id='%s'>"%(self.field_class(errors, campo)+' '+classe,'field-'+campo)
                    
                    if type_campo != 'hidden':
                        tmp += "   <label for='%s'>%s</label>"%(campo,campos[campo]['label'])
                        if campos[campo]['required'] == True and type_campo != 'hidden':
                            tmp += "   <span class='fieldRequired' title='Obrigatório'>(Obrigatório)</span>"
        
                        tmp += "   <div class='formHelp'>%s</div>"%(campos[campo]['decription'])   
                        tmp += "   <div >%s</div>"%(errors.get(campo,''))
                    
                    if type_campo == 'hidden':
                        tmp += "<input id='%s' type='hidden' value='%s' name='%s' size='25'/>"%(campo,self.getValue(campo,self.request,data,default_value),campo)
                    
                    elif type_campo == 'img':
                        if errors:
                            if self.getPhoto(campo,self.request,data):
                                tmp += "<img src='%s' style='width:100px;height:100px;' /><br />"%(self.getPhoto(campo,self.request,data))
                        else: 
                            if self.getPhoto(campo,self.request,data):
                                tmp += "<img src='%s' style='width:100px;height:100px;' /><br />"%(self.getPhoto(campo,self.request,data))
                        tmp += "<input id='%s' type='file' value='%s' name='%s' size='25' />"%(campo,self.getPhoto(campo,self.request,data),campo)
                    
                    elif type_campo == 'file':
                        if errors:
                            if self.getFile(campo,self.request,data):
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
                    
                    elif type_campo == 'combo':
                        select = False
                        tmp += "<select name='%s'>"%(campo)
                        tmp += "<option value="">-- Selecione --</option>"
                        for item in value_choice[campo]:
                            if item == self.getValue(campo,self.request,data,default_value):
                                select = True
                                tmp +="<option value='%s' selected>%s</option>"%(item, value_choice[campo][item])
                            else:
                                tmp +="<option value='%s'>%s</option>"%(item, value_choice[campo][item])
                        tmp += "</select>"
                        if select:
                            tmp += "<input id='%s' type='text' value='%s' name='%s' size='25'/>"%(campo,'', campo)
                        else:
                            tmp += "<input id='%s' type='text' value='%s' name='%s' size='25'/>"%(campo, self.getValue(campo, self.request,data, default_value), campo)
                    
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
                    
                    elif type_campo == 'richtext':
                        utility = getUtility(ITinyMCE)
                        conf = utility.getConfiguration(context=self.context,
                                                        field=campo,
                                                        request=self.request)
                        
                        tmp += "<div class='fieldTextFormat'><label>Formato do Texto</label>"
                        tmp += "<select name='%s_text_format' id='%s_text_format'><option value='text/html' selected='selected'>HTML</option>"%(campo,campo)
                        tmp += "<option value='text/x-web-textile'>Textile</option><option value='text/x-plone-outputfilters-html'>Plone Output Filters HTML</option></select></div>"
                        tmp += "<textarea id='%s' class='mce_editable' name='%s' rows='25' cols='40' title='%s' >%s</textarea>"%(campo,campo, conf, self.getValue(campo, self.request,data, default_value))
                   
                    else:
                        tmp += "<input id='%s' type='text' value='%s' name='%s' size='25'/>"%(campo, self.getValue(campo, self.request,data, default_value), campo)
    
                    tmp += "</div>"
                
                else:
                    tmp += ''
                
                
                    
                html.pop(index)
                html.insert(index, tmp)    
                
            
            return html
        
        
        
        
        

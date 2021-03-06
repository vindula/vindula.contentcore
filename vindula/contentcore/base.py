# -*- coding: utf-8 -*-
import pickle
import smtplib
import sys
from datetime import date, datetime
from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from Products.CMFCore.utils import getToolByName
from storm.locals import *
from storm.zope.interfaces import IZStorm
from vindula.myvindula.tools.utils import UtilMyvindula
from zope.app.component.hooks import getSite
from zope.component import getUtility

from vindula.contentcore.layoutemail import LayoutEmail
from vindula.myvindula.models.funcdetails import FuncDetails

try:
    # python 2.7
    from collections import OrderedDict
except ImportError:
    # python 2.6
    from vindula.contentcore.ordered_dict import OrderedDict


class BaseStore(object):

    def __init__(self, *args, **kwargs):
        #self.store = getUtility(IZStorm).get('contentcore')
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


from vindula.contentcore.models.form_values import ModelsFormValues
from vindula.contentcore.models.fields import ModelsFormFields

class BaseFunc(BaseStore):

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
             'richtext':'Campo de Texto Rico','radio':'Campo de Opção',
             'foreign_key':'Campo de referencia','date':'Campo de Data',
        }

        if type:
            return D.get(type)
        else:
            return None

    def Convert_utf8(self,valor):
        try:
            return unicode(valor,'utf-8')
        except UnicodeDecodeError:
            return valor.decode("utf-8", "ignore")
        except:
            if type(valor) == unicode:
                return valor
            if type(valor) == bool:
                return unicode(str(valor))
            else:
                return u'erro ao converter os caracteres'


    def checaEstado(self,config, campo):
        if config:
            try:
                return config.__getattribute__(campo)
            except:
                return True
        else:
            return True

    def getBuscaContents(self,context, type):
        query = {}
        pc = getToolByName(context, 'portal_catalog')

        query['portal_type'] = type
        #query['review_state'] = ['published', 'internally_published', 'external']
        query['path'] = {'query':'/'.join(context.getPhysicalPath())}
        query['sort_on'] = 'sortable_title'
        query['sort_order'] = 'ascending'

        itens = pc(**query)
        return itens

    #Retorna o username do usuario logado, usado para valor padrão do formulario
    def get_username_login(self):
        user_login = getSite().portal_membership.getAuthenticatedMember()
        return user_login.getUserName()


    #Retorna o email do usuario logado, usado para valor padrão do formulario
    def get_email_user_login(self):
        tool = UtilMyvindula()
        obj_user = tool.get_prefs_user(self.get_username_login())

        return obj_user.get('email','none')


    #Retorna um numero sequencial para o registro do formulario
    def get_codigo_registro(self):
        form_id = self.context.forms_id
        from vindula.contentcore.models.form_instance import ModelsFormInstance
        number_itens = ModelsFormInstance().get_Instance(int(form_id),True)
        if number_itens:
            number_itens = number_itens.count()
            if number_itens:
                return number_itens + 1
        return 1


    def getValue(self,campo,request,data,default_value):
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
            except :
                e = sys.exc_info()[0]
                print 'Error: %s - %s' %(e, default_value.get(campo,'None'))
                return ''
            
    def getDataFieldByUser(self, field):
        tool = UtilMyvindula()
        username = self.get_username_login().decode('utf-8')
        
        return tool.get_prefs_user(username).get(field,'')

    def getDataFieldByUser(self, field):
        username = self.context.portal_membership.getAuthenticatedMember().getId()
        username = username.decode('utf-8')
        
        user_instance = FuncDetails(username)
        
        return user_instance.get(field, '')

    def getValuePickle(self,campo,request,data,default_value):
        if campo in request.keys():
            if request.get(campo, None):
                return request.get(campo,'')
            else:
                return ''
        elif campo in data.keys():
            if data.get(campo,None) != None:
                value = data.get(campo,'') 
                return self.decodePickle(value)
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
                if hasattr(self, 'context'):
                    default_form_id = self.context.forms_id
                else:
                    default_form_id = 0
                id_form = int(request.get('forms_id',default_form_id))
                id_instance = int(request.get('id_instance','0'))
                field = campo
                result = ModelsFormValues().get_FormValues_byForm_and_Instance_and_Field(id_form,id_instance,field)
                if result:
                    return '../form-file?id=%s' % result.id

        elif campo in data.keys():
            if hasattr(self, 'context'):
                default_form_id = self.context.forms_id
            else:
                default_form_id = 0
            id_form = int(request.get('forms_id',default_form_id))
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
            try:
                return pickle.loads(str(valor))
            except (IndexError, KeyError):
                return [valor]
        else:
            return ''


    def geraHTMLContent(self,id,tipo,valor,full_text=False):
        if tipo == 'list':
            txt = ''
            for i in self.decodePickle(valor):
                txt += i +', '

            return txt

        elif tipo == 'img':

            if id:
                return '<img width="100px" src="../form-image?id=%s">' % id
            else:
                return ''

        elif tipo == 'file':
            if id:
                arquivo = self.decodePickle(valor)
                if arquivo != '':
                    name = arquivo.get('filename','')
                    return '<a href="../form-file?id=%s" target="_blank">%s</a><br />'%(id,name)
                else:
                    return ''
            else:
                return ''

        elif tipo == 'date':
            data = self.decodePickle(valor)
            try:
                return data.strftime('%d/%m/%Y')

            except:
                return ''


        elif tipo == 'choice':
            if id:
                valor_campo = ModelsFormValues().get_Values_byID(id)
                id_form = int(self.context.forms_id)

                if valor_campo:
                    campo = ModelsFormFields().get_Fields_ByField(valor_campo.fields,id_form)
    
                    items = campo.list_values.splitlines()
                    D=[]
                    for i in items:
                        L = i.split(' | ')
    
                        if len(L) >= 2:
                            if L[0] == valor:
                                return L[1]

            return valor

        elif tipo == 'foreign_key':
            if id:
                valor_campo = ModelsFormValues().get_Values_byID(id)
                id_form = int(self.context.forms_id)







                if valor_campo:
                    campo = ModelsFormFields().get_Fields_ByField(valor_campo.fields,id_form)

                    if campo:
                        form_ref = campo.ref_form

                        form_ref_id = form_ref.id
                        label = form_ref.campo_label
                        key = form_ref.campo_chave

                        if full_text:
                            instance = 0
                            txt = ''

                            v_campos = form_ref.fields 
                            campo_busca = ModelsFormValues().store.find(ModelsFormValues, ModelsFormValues.fields==key,
                                                                                          ModelsFormValues.forms_id==form_ref_id,
                                                                                          ModelsFormValues.value==valor
                                                                        )
                            if campo_busca.count():
                                instance = campo_busca[0].instance_id

                                valores = ModelsFormValues().get_FormValues_byForm_and_Instance(form_ref_id,instance)

                                txt = '<br/>'
                                for v_campo in v_campos:
                                    v_valor = valores.find(fields=v_campo.name_field).one()
                                    txt += '<b> %s : </b><span> %s </span><br/>' %(v_campo.title,v_valor.value)

                            return txt

                        else:
                            dados = ModelsFormValues().get_FormValues_byForm_and_Field(form_ref_id,key)
                            for item in dados:
                                if item.value == valor:
                                    dados_label = ModelsFormValues().get_FormValues_byForm_and_Instance_and_Field(form_ref_id, item.instance_id, label)

                                    return dados_label.value

        return valor

    def convertSelect(self,valor, tipo, id):
        if tipo == 'list':
            txt = ''
            for i in self.decodePickle(valor):
                if txt:
                    txt += ', ' + i
                else:
                    txt += i

            return txt
        elif tipo == 'choice':
            campo = ModelsFormFields().get_Fields_byIdField(id)
            if campo:
                items = campo.list_values.splitlines()
                D=[]
                for i in items:
                    L = i.split(' | ')

                    if len(L) >= 2:
                        if L[0] == valor:
                            return L[1]

            return valor
        elif tipo == 'date':
            data = self.decodePickle(valor)
            try:
                return data.strftime('%d/%m/%Y')
            except:
                return ''

        elif tipo == 'foreign_key':
            campo = ModelsFormFields().get_Fields_byIdField(id)

            if campo:
                form_ref = campo.ref_form

                form_ref_id = form_ref.id
                label = form_ref.campo_label
                key = form_ref.campo_chave

                dados = ModelsFormValues().get_FormValues_byForm_and_Field(form_ref_id,key)
                for item in dados:
                    if item.value == valor:
                        dados_label = ModelsFormValues().get_FormValues_byForm_and_Instance_and_Field(form_ref_id, item.instance_id, label)

                        return dados_label.value

        return valor


    def envia_email(self,ctx, msg, assunto, mail_para, arquivos=[],to_email=None):
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


        if hasattr(ctx, 'context'):
            email_layout_obj = LayoutEmail(msg=msg, ctx=ctx.context)
        else:
            email_layout_obj = LayoutEmail(msg=msg, ctx=ctx)

        mensagem.attach(MIMEText(email_layout_obj.layout(), 'html', 'utf-8'))
        
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
        smtp_host   = portal.MailHost.smtp_host
        smtp_port   = portal.MailHost.smtp_port
        smtp_userid = portal.MailHost.smtp_uid
        smtp_pass   = portal.MailHost.smtp_pwd
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
            # i=0
            # while i < len(campos.keys()):
            #     html.append(i)
            #     i+=1
            #Ordenando os campos pela chave 'ordem'
            campos = OrderedDict((sorted(campos.items(), key=lambda campo: campo[1]['ordem'])))

            for campo in campos.keys():
                # index = campos[campo].get('ordem',0)
                tmp = ""
                valor = ''
                obj_campo = campos[campo].get('obj','')
                if not 'outros_hidden' in campo:
                    type_campo = campos[campo].get('type', '')

                    if type_campo == 'richtext':
                        classe = 'richTextWidget'
                    elif type_campo == 'referencia':
                        tmp += ''
#                       html.pop(index)
#                       html.insert(index, tmp)
#                       html.append(tmp)
                        continue
                    else:
                        classe = ''

                    mascara_campo = campos[campo].get('mascara', None)
                    if mascara_campo:
                        mascara="onKeyDown='Mascara(this,{0});' onKeyPress='Mascara(this,{0});' onKeyUp='Mascara(this,{0});'".format(mascara_campo)
                    else:
                        mascara = ''

                    #Classe para campo oculto
                    if type_campo == 'hidden':                        
                        classe += ' hidden_field'

                    #Campo Com Float Left
                    if campos[campo].get('flag_float_left', False):
                        classe += ' left'

                    tmp += "<!-- Campo %s -->"%(campo)
                    tmp += "<div class='%s' id='%s'>"%(self.field_class(errors, campo)+' '+classe,'field-'+campo)

                    if type_campo != 'hidden' and type_campo !='bool':
                        tmp += "   <label for='%s'>%s</label>"%(campo,campos[campo].get('label', ''))
                        tmp += "   <div class='formHelp'>%s</div>"%(campos[campo].get('decription', ''))
                   
                    if campos[campo].get('required', '') == True and type_campo != 'hidden':
                        tmp += "   <span class='fieldRequired' title='Obrigatório'>&nbsp;&nbsp;</span>"
                        tmp += "   <div >%s</div>"%(errors.get(campo,''))

                    if type_campo == 'hidden':
                        valor += "<input id='%s' type='hidden' value='%s' name='%s' size='25'/>"%(campo,self.getValue(campo,self.request,data,default_value),campo)

                    elif type_campo == 'img':
                        if errors:
                            if self.getPhoto(campo,self.request,data):
                                valor += "<img src='%s' style='width:100px;height:100px;' /><br />"%(self.getPhoto(campo,self.request,data))
                        else:
                            if self.getPhoto(campo,self.request,data):
                                valor += "<img src='%s' style='width:100px;height:100px;' /><br />"%(self.getPhoto(campo,self.request,data))
                        valor += "<input id='%s' type='file' value='%s' name='%s' size='25' />"%(campo,self.getPhoto(campo,self.request,data),campo)

                    elif type_campo == 'file':
                        if errors:
                            if self.getFile(campo,self.request,data):
                                valor += "<a href='%s' target='_blank'>Download do Arquivo</a><br />"%(self.getFile(campo,self.request,data))
                        else:
                            if self.getFile(campo,self.request,data):
                                valor += "<a href='%s' target='_blank'>Download do Arquivo</a><br />"%(self.getFile(campo,self.request,data))
                        valor += "<input id='%s' type='file' value='%s' name='%s' size='25' />"%(campo,self.getFile(campo,self.request,data),campo)

                    elif type_campo == 'date':
                        valor += """<input id='%s' type='text' maxlength='10' class="dateField"
                                         value='%s' name='%s' size='25'/>"""%(campo,self.converte_data(self.getValuePickle(campo,self.request,data,default_value),True),campo)

                    elif type_campo == 'textarea':
                        valor += "<textarea id='%s' name='%s' style='width: 100; height: 81px;'>%s</textarea>"%(campo, campo, self.getValue(campo,self.request,data,default_value))

                    elif type_campo == 'bool':
                        valor += "<input id='%s' type='checkbox' value='%s' name='%s' size='25' %s/>"%(campo,'True',campo,self.checked(campo,self.request,data,default_value))

                    elif type_campo == 'combo':
                        select = False
                        valor += "<select name='%s'>"%(campo)
                        valor += "<option value="">-- Selecione --</option>"
                        for item in value_choice[campo]:
                            if item[0] == self.getValue(campo,self.request,data,default_value):
                                select = True
                                valor +="<option value='%s' selected>%s</option>"%(item[0], item[-1])
                            else:
                                valor +="<option value='%s'>%s</option>"%(item[0], item[-1])
                        valor += "</select>"
                        if select:
                            valor += "<input id='%s' type='text' value='%s' name='%s' size='25'/>"%(campo,'', campo)
                        else:
                            valor += "<input id='%s' type='text' value='%s' name='%s' size='25'/>"%(campo, self.getValue(campo, self.request,data, default_value), campo)

                    elif type_campo == 'list':
                        valor += "<div class='boxSelecao' name='%s'>"%(campo)
                        for item in value_choice[campo]:
                            lable =  item[0]
                            if item[0] in self.getValueList(campo,self.request,data,default_value):
                                valor += "<input value='%s' type='checkbox' checked name='%s'/><span>%s</span><br/>"%(item[0],campo,lable)
                            else:
                                valor += "<input value='%s' type='checkbox' name='%s'/><span>%s</span><br/>"%(item[0],campo,lable)
                        valor += "</div>"

                    elif type_campo == 'choice':
                        valor += "<select name='%s'>"%(campo)
                        valor += "<option value="">-- Selecione --</option>"
                        for item in value_choice[campo]:
                            if item[0] == self.getValue(campo,self.request,data,default_value):
                                valor +="<option value='%s' selected>%s</option>"%(item[0], item[-1])
                            else:
                                valor +="<option value='%s'>%s</option>"%(item[0], item[-1])

                        valor += "</select>"

                    elif type_campo == 'radio':
                        valor += "<div id='%s' >"%(campo)
                        for item in value_choice[campo]:
                            if item[0] == self.getValue(campo,self.request,data,default_value):
                                valor += "<input type='radio' name='%s' value='%s' checked >%s" %(campo, item[0], item[-1])
                            else:
                                valor += "<input type='radio' name='%s' value='%s' >%s" %(campo, item[0], item[-1])

                            valor += '<br />'
                        valor += "</div>"

                    elif type_campo == 'foreign_key':
                        refform = obj_campo.ref_form
                        
                        valor += "<select name='%s' class='select-filter' data-ref_from='%s' data-id_field='%s' >"%(campo,refform.id,refform.campo_chave)
                        valor += "<option value="">-- Selecione --</option>"
                        for item in value_choice[campo]:
                            if item[0] == self.getValue(campo,self.request,data,default_value):
                                valor +="<option value='%s' selected>%s</option>"%(item[0], item[-1])
                            else:
                                valor +="<option value='%s'>%s</option>"%(item[0], item[-1])

                        valor += "</select>"
                        valor += '<div id="ajax_content_%s"> </div>' %(campo)
                        

                    elif type_campo == 'richtext':
                        url = self.context.absolute_url()

                        valor += "<div class='fieldTextFormat'><label>Formato do Texto</label>"
                        valor += "<select name='%s_text_format' id='%s_text_format'><option value='text/html' selected='selected'>HTML</option>"%(campo,campo)
                        valor += "<option value='text/x-web-textile'>Textile</option><option value='text/x-plone-outputfilters-html'>Plone Output Filters HTML</option></select></div>"
                        valor += "<input class='cke_config_ur' type='hidden' value='%s/ckeditor_plone_config.js' name='cke_config_url'>"%(url)
                        valor += "<input class='cke_iswidget' type='hidden' value='True' name='cke_iswidget'>"
                        valor += "<div class='widget_settings'><input class='cke_baseHref' type='hidden' name='cke_baseHref' value='%s' >"%(url)
                        valor += "<input class='cke_height' type='hidden' value='100px' name='cke_height'></div>"
                        valor += "<textarea id='%s' class='ckeditor_plone' name='%s' rows='25' cols='40' >%s</textarea>"%(campo,campo, self.getValue(campo, self.request,data, default_value))

#                        utility = getUtility(ITinyMCE)
#                        conf = utility.getConfiguration(context=self.context,
#                                                        field=campo,
#                                                        request=self.request)
#
#                        valor += "<div class='fieldTextFormat'><label>Formato do Texto</label>"
#                        valor += "<select name='%s_text_format' id='%s_text_format'><option value='text/html' selected='selected'>HTML</option>"%(campo,campo)
#                        valor += "<option value='text/x-web-textile'>Textile</option><option value='text/x-plone-outputfilters-html'>Plone Output Filters HTML</option></select></div>"
#                        valor += "<textarea id='%s' class='mce_editable' name='%s' rows='25' cols='40' title='%s' >%s</textarea>"%(campo,campo, conf, self.getValue(campo, self.request,data, default_value))

                    elif type_campo != 'referencia':
                        valor += "<input id='%s' type='text' value='%s' name='%s' size='25' %s />"%(campo, self.getValue(campo, self.request,data, default_value), campo, mascara)

                    if campos[campo].get('flag_multi'):
                        table = ''
                        table +='<table id="listing-table" class="listing"><th style="width: 50%"></th>'

                        if type_campo in ['list','radio']:
                            for item in value_choice[campo]:
                                table += '<th class="posted">%s</th>'%( item[-1])

                        else:
                            table += '<th>%s</th>'%('Responda')

                        id_form = int(self.context.forms_id)
                        ref = ModelsFormFields().get_fields_byIdForm_and_RefField(id_form,campo)
                        for i in ref:

                            mascara_campo = i.mascara or ''
                            if mascara_campo:
                                mascara="onKeyDown='Mascara(this,{0});' onKeyPress='Mascara(this,{0});' onKeyUp='Mascara(this,{0});'".format(mascara_campo)
                            else:
                                mascara = ''

                            table += '<tr><td>%s</td>'%(i.title)

                            valor = ''
                            if type_campo == 'list':
                                for item in value_choice[campo]:
                                    valor = ''
                                    lable =  item[-1]
                                    if item[0] in self.getValueList(i.name_field,self.request,data,default_value):
                                        valor += "<input value='%s' type='checkbox' checked name='%s'/>"%(item[0],i.name_field)
                                    else:
                                        valor += "<input value='%s' type='checkbox' name='%s'/>"%(item[0],i.name_field)
                                    table += '<td>%s</td>'%(valor)

                            elif type_campo == 'radio':
                                for item in value_choice[campo]:
                                    valor = ''
                                    if item[0] == self.getValue(i.name_field,self.request,data,default_value):
                                        valor += "<input type='radio' name='%s' value='%s' checked >" %(i.name_field, item[0])
                                    else:
                                        valor += "<input type='radio' name='%s' value='%s' >" %(i.name_field, item[0])

                                    table += '<td>%s</td>'%(valor)


                            elif type_campo == 'img':
                                if errors:
                                    if self.getPhoto(i.name_field,self.request,data):
                                        valor += "<img src='%s' style='width:100px;height:100px;' /><br />"%(self.getPhoto(campo,self.request,data))
                                else:
                                    if self.getPhoto(i.name_field,self.request,data):
                                        valor += "<img src='%s' style='width:100px;height:100px;' /><br />"%(self.getPhoto(i.name_field,self.request,data))
                                valor += "<input id='%s' type='file' value='%s' name='%s' size='25' />"%(i.name_field,self.getPhoto(i.name_field,self.request,data),i.name_field)

                                table += '<td>%s</td>'%(valor)

                            elif type_campo == 'file':
                                if errors:
                                    if self.getFile(i.name_field,self.request,data):
                                        valor += "<a href='%s' target='_blank'>Download do Arquivo</a><br />"%(self.getFile(i.name_field,self.request,data))
                                else:
                                    if self.getFile(i.name_field,self.request,data):
                                        valor += "<a href='%s' target='_blank'>Download do Arquivo</a><br />"%(self.getFile(i.name_field,self.request,data))
                                valor += "<input id='%s' type='file' value='%s' name='%s' size='25' />"%(campo,self.getFile(i.name_field,self.request,data),campo)

                                table += '<td>%s</td>'%(valor)

                            elif type_campo == 'date':
                                valor += """<input id='%s' type='text' maxlength='10' onKeyDown='Mascara(this,Data);' onKeyPress='Mascara(this,Data);' onKeyUp='Mascara(this,Data);'
                                                 value='%s' name='%s' size='25'/>"""%(i.name_field,self.converte_data(self.getValuePickle(i.name_field,self.request,data,default_value),True),i.name_field)

                                table += '<td>%s</td>'%(valor)

                            elif type_campo == 'textarea':
                                valor += "<textarea id='%s' name='%s' style='width: 100; height: 81px;'>%s</textarea>"%(i.name_field, i.name_field, self.getValue(i.name_field,self.request,data,default_value))

                                table += '<td>%s</td>'%(valor)

                            elif type_campo == 'bool':
                                valor += "<input id='%s' type='checkbox' value='%s' name='%s' size='25' %s/>"%(i.name_field,'True',i.name_field,self.checked(i.name_field,self.request,data,default_value))
                                tmp += "   <label class='label-input' for='%s'>%s</label>"%(campo,campos[campo].get('label', ''))
                                tmp += "   <div class='formHelp'>%s</div>"%(campos[campo].get('decription', ''))

                                table += '<td>%s</td>'%(valor)

                            elif type_campo == 'choice':
                                valor += "<select name='%s'>"%(i.name_field)
                                valor += "<option value="">-- Selecione --</option>"
                                for item in value_choice[campo]:
                                    if item[0] == self.getValue(i.name_field,self.request,data,default_value):
                                        valor +="<option value='%s' selected>%s</option>"%(item[0], item[-1])
                                    else:
                                        valor +="<option value='%s'>%s</option>"%(item[0], item[-1])

                                valor += "</select>"

                                table += '<td>%s</td>'%(valor)

                            elif type_campo != 'referencia':
                                valor += "<input id='%s' type='text' value='%s' name='%s' size='25' %s />"%(i.name_field, self.getValue(i.name_field, self.request,data, default_value), i.name_field,mascara)

                                table += '<td>%s</td>'%(valor)

                            table += '</tr>'

                        table += '</table>'
                        tmp += table + "</div>"
                    else:
                        tmp += valor + "</div>"

                    if type_campo != 'hidden' and type_campo =='bool':
                        tmp += "   <label class='label-input' for='%s'>%s</label>"%(campo,campos[campo].get('label', ''))
                        tmp += "   <div class='formHelp'>%s</div>"%(campos[campo].get('decription', ''))
                        tmp += "   <div >%s</div>"%(errors.get(campo,''))

                else:
                    tmp += ''

                # html.pop(index)
                # html.insert(index, tmp)
                html.append(tmp)

            return html

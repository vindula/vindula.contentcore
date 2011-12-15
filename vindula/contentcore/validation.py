# coding: utf-8

from datetime import date
from datetime import datetime
import re
from decimal import Decimal
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility
#from plone.scale import scale
#from plone.namedfile.scaling import ImageScaling
import pickle

def to_utf8(value):
    return unicode(value, 'utf-8')

         

def valida_form(ctx, configuracao, form):
    # metodo que valida um sequencia de campos e retorna um dicionario
    # com os valores, erros e mensagem de erro
    
    errors = {} # dicionario que vai retornar os erros para o formulario
    convertidos = {} # dicionario que vai retornar os dados convertidos para unicode
    
    # var 'campo' - usado para verificar se campo e obrigatorio
    # var 'valor' - usado para converter dos dados inseridos no fomulario
    for campo in configuracao.keys():
        valor = form.get(campo)   #configuracao[campo]['campo_form'], '')
        # logica para verificacao de obrigatoriedade de campo
        
        if configuracao.get(campo).get('required', None) is not None:
            if configuracao[campo]['required'] == True: # configuracao: campo e obrigatorio
                if valor == '' or valor.isspace(): # se o campo estiver vazio
                    errors[campo] = u'Este campo é obrigatório' # indica o campo vazio

        if configuracao[campo]['type'] == date:
            if valor != '':   
                try:       
                    data = tuple(valor) # pega a string no formato '00/00/0000' e transforma em tupla dividindo os elementos
                    
                    # separa o ano, mes e dia da tupla
                    ano = int(data[6]+data[7]+data[8]+data[9])                              
                    mes = int(data[3]+data[4]) 
                    dia = int(data[0]+data[1])
                    
                    if ano < 1900:
                        errors[campo] = u'Data inválida.'
                    else:
                        convertidos[campo] = date(ano, mes, dia)
                except:
                    errors[campo] = u'Data inválida.'
        
        #logica para converter campos tipo Boolen
        elif configuracao[campo]['type'] == 'bool':
            if valor:
                convertidos[campo] = True
            else:
                convertidos[campo] = False            
        
        #logica para converter campos tipo Boolen
        elif configuracao[campo]['type'] == bool:
            if valor:
                convertidos[campo] = True
            else:
                convertidos[campo] = False        
        
        elif configuracao[campo]['type'] == int:
            convertidos[campo] = int(valor)
            
        elif configuracao[campo]['type'] == 'choice':
            if type(valor) == unicode:
                convertidos[campo] = valor.strip()
            else:
                convertidos[campo] = to_utf8((valor.strip()))    
            
        elif configuracao[campo]['type'] == 'hidden':
            try:
                convertidos[campo] = int(valor)
            except:
                convertidos[campo] = to_utf8((valor.strip()))
                
        elif configuracao[campo]['type'] == 'text':
            if type(valor) == unicode:
                convertidos[campo] = valor.strip()
            else:
                convertidos[campo] = to_utf8((valor.strip()))

        elif configuracao[campo]['type'] == 'list':
            valor_convert = ''
            if type(valor) == list:
                valor_convert = pickle.dumps(valor)
                convertidos[campo] = to_utf8(valor_convert)
            else:
                L = []
                L.append(valor)
                valor_convert = pickle.dumps(L)
                convertidos[campo] = to_utf8(valor_convert)
                
        elif configuracao[campo]['type'] == 'img':
            data = valor.read()
            if len(data) != 0 : 
                valor_convert = pickle.dumps(data)
                convertidos[campo] = to_utf8(valor_convert)
            else:
                 convertidos[campo] = ''

        #logica para converter campos tipo File           
        elif configuracao[campo]['type'] == 'file':
            data = valor.read()
            if len(data) != 0 : 
                valor_convert = pickle.dumps(data)
                convertidos[campo] = to_utf8(valor_convert)
            else:
                 convertidos[campo] = ''           
        
        elif configuracao[campo]['type'] == 'textarea':
            if type(valor) == unicode:
                convertidos[campo] = valor.strip()
            else:
                convertidos[campo] = to_utf8((valor.strip()))
                
        elif configuracao[campo]['type'] == 'key':
            normalizer = getUtility(IIDNormalizer)
            convertidos[campo] = to_utf8(normalizer.normalize(unicode(valor, 'utf-8')))
            
        elif configuracao[campo]['type'] == 'email':
            if(re.match('(.+)@(.+)\.(.+)',valor,re.IGNORECASE)):
                if type(valor) == unicode:
                    convertidos[campo] = valor.strip()
                else:
                    convertidos[campo] = to_utf8((valor.strip()))
            else:
                errors[campo] = u'E mail inválido, digite um email valido'
            
                    
        # logica para conversao de dados para unicode de acordo com a configuracao      
        elif valor != '' and valor != '--NOVALUE--' and valor != '-- Selecione --': # se o campo nao estiver vazio, vai tentar converter
            if campo != 'skills_expertise' and campo != 'languages':
                try:
                    if type(valor) == unicode:
                        convertidos[campo] = valor.strip()
                    else:
                        convertidos[campo] = to_utf8(valor.strip()) # conversao do campo
                    # "(valor)" == "(def __call__(self, *args, **kwargs):", callable
                except:
                    # Falhou ao converter para o tipo requerido
                    errors[campo] = u'Erro ao converter o conteúdo do campo para um formato válido'
                    #errors[campo] = u'Não foi possível converter o campo %s para %s.' % (campo, configuracao[campo]['type'])

    return errors, convertidos #retorna campos validados   
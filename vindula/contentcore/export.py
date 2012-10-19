# coding: utf-8
from five import grok
from zope.interface import Interface


from StringIO import StringIO
#from test.regrtest import printlist

import datetime
import ho.pisa as pisa
import pyExcelerator as xl  

class ExportacaoView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('export_view')
    
    def render(self):
        pass
    
    def html_to_pdf(self, html, pdfname='',inPlone=False):
        """Usa PISA para gera um pdf"""
        #if not pdfname:
        #    pdfname = str(random.random()).split('.')[1]
        
        portal = self.context.portal_url.getPortalObject()
        
        #pdfname += datetime.datetime.now().__str__()
        pdfname = pdfname.replace(':','-')
        pdfname = pdfname.replace(' ','_')
        
        filename = '/tmp/'+pdfname+'.pdf' 

        try:
             pdf = self.pdf_file(html, filename)
             pdf_file = file(filename,"r").read()

             if pdf and not inPlone:
                self.request.response.setHeader('Content-Type', 'application/pdf')
                self.request.response.setHeader('Content-Disposition','attachment; filename=%s.pdf'%(pdfname))
                self.request.response.write(pdf_file)       
            
             elif inPlone:
                count = 0
                nome_arquivo = pdfname +'.pdf' 
                
                while nome_arquivo in portal.objectIds():
                    nome_arquivo = pdfname + '-' + str(count) +'.pdf' 
                    count +=1
                
                
                objeto = {'type_name':'File',
                          'id': nome_arquivo,
                          'title': nome_arquivo,
                          'file': pdf_file}
       
                obj_pdf = portal.invokeFactory(**objeto)
                obj_pdf = portal[obj_pdf]
                
                return obj_pdf.absolute_url()
                
        except Exception, erro:
            return 'erro | Não possível gerar o arquivo, Detalhes %s'%(erro)
        
        return 'ok | Arquivo gerado com sucesso.'

    
    def pdf_file(self, html, filename):
        """Cria um arquivo temporario no filesystem"""
    
        fopen = file(filename,"wb")
        pdf = pisa.CreatePDF(StringIO(html), fopen, encoding='utf-8')
        fopen.close()
        if not pdf.err:                             
            #pisa.startViewer(filename)
            return True
        else:
            return False      

    def html_to_excel(self, dados, excelname=''):
        tablename = excelname
        excelname += datetime.datetime.now().__str__()
        excelname = excelname.replace(':','-')
        excelname = excelname.replace(' ','_')
        
        filename = '/tmp/'+excelname+'.xls' 
        try:
             excell = self.excel_file(dados,filename)

             if excell:
                self.request.response.setHeader('Content-Type', 'application/x-excel')
                self.request.response.setHeader('Content-Disposition','attachment; filename=%s.xls'%(excelname))
                self.request.response.write(file(filename,"r").read())       
        except Exception, erro:
            return 'erro | Não possível gerar o arquivo, Detalhes %s'%(erro)
        
        return 'ok | Arquivo gerado com sucesso.'
    

    
    def excel_file(self, dados,filename):
        try:
            #Open new workbook
            mydoc=xl.Workbook()
            
            for item in dados:
                #Add a worksheet
                
                mysheet=mydoc.add_sheet(item.get('title'))
                #write headers
                header_font=xl.Font() #make a font object
                header_font.bold=True
                header_font.underline=True
                #font needs to be style actually
                header_style = xl.XFStyle(); header_style.font = header_font
                
                headers = item.get('head')
                values = item.get('values')
                
                for col,value in enumerate(headers):
                    mysheet.write(0,col,value,header_style)
            
                #write values and highlight those that match my criteria
                highlighted_row_font=xl.Font() #no real highlighting available?
                highlighted_row_font.bold=True
                highlighted_row_font.colour_index=2 #2 is red,
                highlighted_row_style = xl.XFStyle(); highlighted_row_style.font = highlighted_row_font
                for row_num,row_values in enumerate(values):
                    row_num+=1 #start at row 1
                    if row_values[1]=='Manatee':
                        for col,value in enumerate(row_values):
                            #make Manatee's (sp) red
                            mysheet.write(row_num,col,value,highlighted_row_style)
                    else:
                        for col,value in enumerate(row_values):
                            #normal row
                            mysheet.write(row_num,col,value)
            
            #save file
            mydoc.save(filename)
                
            return True
            
        except:
            return False
             
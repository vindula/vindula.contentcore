# -*- coding: utf-8 -*-

class LayoutEmail(object):
	"""docstring for LayoutEmail"""

	def __init__(self, msg, ctx):
		super(LayoutEmail, self).__init__()
		themeconfig = ctx.restrictedTraverse('personal-layout.css')

		config = themeconfig.getConfiguration()[0]

		self.conteudo = msg 
		self.form_title = ctx.title

		self.url_logo_topo = config.get('logo_portal')
		self.url_logo_radape = config.get('logo_footer')
		self.url_banner = config.get('banner_topo')


	def layout (self):

		texto = u"""
					<html>
						<body>
							<div>
								<div>
									<h4>
										Novo cadastro no fomulário %s:
									</h4>
								</div>
								<div style="padding: 20px 10px 40px 10px; 
		                           			color: rgba(34, 34, 34, 0.76);
		                            		font-family: tahoma,'lucida grande',verdana,helvetica,arial,sans-serif;">
			                    	<div id="conteudo">	%s </div>
								</div>
							</div>
						</body>
					<html/>
				""" %(self.form_title,
					  self.conteudo,)
		
		return texto 


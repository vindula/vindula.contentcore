$j = jQuery.noConflict();

function addHTMLParameters(){
	
	var html=''
	html+='<tr>'
	html+='	<td>'
	html+='		<input id="parameters" type="text" value="" name="parameters" size="25"/>'
	html+='	</td>'	
	html+='	<td>'
	html+='		<input id="value_parameters" type="text" value="" name="value_parameters" size="25"/>'
	html+='	</td>'
	html+='	<td>'
	html+='		<a style="cursor:pointer;" onClick="$j(this).parent().parent().remove();">'
	html+='			<img alt="Adicionar Parâmetros" title="Adicionar Parâmetros" src="/++resource++vindula.contentcore/icone-False.png" />'
	html+='		</a>'
	html+='	</td>'
	html+='</tr>'

	$j("#addParameters").append(html);
	
};


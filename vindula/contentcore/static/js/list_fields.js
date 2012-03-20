$j = jQuery.noConflict();

$j(document).ready(function(){
	/* Aba de edição do conteudo*/
	$j('#contentview-form').addClass('selected');
	$j('#contentview-view').removeClass('selected');
	
	/* Exibição do campo de list value*/
	$j('div#field-list_values').hide();
	$j("select[name='type_fields']").change(function(){
		val = this.value;
		if (val =='list' || val == 'choice'){
			$j('div#field-list_values').show();
		}else{
			$j('div#field-list_values').hide();
		};  
	});
	
	
	
	
});
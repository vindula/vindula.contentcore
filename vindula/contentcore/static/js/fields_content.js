$j = jQuery.noConflict();

function checkValue(val){
	
	if (val == 'doc_plone') {
		$j('#formfield-form-widgets-doc_plone').show();
		$j('#formfield-form-widgets-url').hide();
		$j('#formfield-form-widgets-parameto').hide();
		
	}
	else 
		if (val == 'url') {
			$j('#formfield-form-widgets-doc_plone').hide();
			$j('#formfield-form-widgets-url').show();
			$j('#formfield-form-widgets-parameto').hide();
			
		}
		else 
			if (val == 'parameto') {
				$j('#formfield-form-widgets-doc_plone').hide();
				$j('#formfield-form-widgets-url').hide();
				$j('#formfield-form-widgets-parameto').show();
				
			}
			else {
				$j('#formfield-form-widgets-doc_plone').hide();
				$j('#formfield-form-widgets-url').hide();
				$j('#formfield-form-widgets-parameto').hide();
			};
	};


$j(document).ready(function(){

	var val = $j('#form-widgets-acao_destino').val();
	checkValue(val);
	$j('#form-widgets-acao_destino').change(function(evt){
		var val = $j('#form-widgets-acao_destino').val();
		checkValue(val);
	});	
		
		
	

});
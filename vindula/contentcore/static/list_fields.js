$j = jQuery.noConflict();

$j(document).ready(function(){
	$j('div#list_values').hide();
	$j("select[name='type_fields']").change(function(){
		val = this.value;
		if (val =='list' || val == 'choice'){
			$j('div#list_values').show();
		}else{
			$j('div#list_values').hide();
		};  
	});
});
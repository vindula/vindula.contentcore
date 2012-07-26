$j = jQuery.noConflict();

function hideShowListValues () {
    var val = $j("select[name='type_fields']").val();
    if (val =='list' || val == 'choice'){
        $j('div#field-list_values').show();
    }else{
        $j('div#field-list_values').hide();
    };
}

$j(document).ready(function(){
	/* Aba de edição do conteudo*/
	$j('#contentview-form').addClass('selected');
	$j('#contentview-view').removeClass('selected');
	
	/* Exibição do campo de list value*/
	hideShowListValues();
	//$j('div#field-list_values').hide();
	$j("select[name='type_fields']").change(function(){
	   hideShowListValues();  
	});
	
});
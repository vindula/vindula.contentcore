$j = jQuery.noConflict();

function hideShowListValues () {
    var val = $j("select[name='type_fields']").val();
    if (val =='list' || val == 'choice' || val == 'radio'){
        $j('div#field-list_values').show();
    }else{
        $j('div#field-list_values').hide();
    };
}

function hideShowFieldRef () {
    var val = $j("select[name='type_fields']").val();
    if (val =='referencia'){
        $j('div#field-field_ref').show();
        $j('div#field-flag_multi').hide();
    }else{
        $j('div#field-field_ref').hide();
        $j('div#field-flag_multi').show();
    };
}

function hideShowFormRef () {
    var val = $j("select[name='type_fields']").val();
    if (val =='foreign_key'){
        $j('div#field-form_ref').show();
    }else{
        $j('div#field-form_ref').hide();
    };
}

$j(document).ready(function(){
	/* Aba de edição do conteudo*/
	$j('#contentview-form').addClass('selected');
	$j('#contentview-view').removeClass('selected');
	
	/* Exibição do campo de list value*/
	hideShowListValues();
	hideShowFieldRef();
	hideShowFormRef();
	//$j('div#field-list_values').hide();
	$j("select[name='type_fields']").change(function(){
	   hideShowListValues();
	   hideShowFieldRef();
	   hideShowFormRef();  
	});
	
});
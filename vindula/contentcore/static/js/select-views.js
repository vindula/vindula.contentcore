$j = jQuery.noConflict();

$j(document).ready(function(){
	
	$j('select#opcao-view').change(function(){
		/*
		var url = $j('#context_url').val() + "/ajax_views";

		$j('#content-edicao').addClass('display-none');
		$j('#spinner').removeClass('display-none');
		
		$j.get(url,{view:ctx.val()}, function(data){
				$j('#content-edicao').append(data);
				
				$j('#content-edicao').removeClass('display-none');
				$j('#spinner').addClass('display-none');
				
		});*/
		var ctx = $j(this).val();
		
		if (ctx == 'avisos'){		
			$j('#content-avisos').removeClass('display-none');
		}
	});
});
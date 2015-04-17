 $j = jQuery.noConflict();
 
function ajaxBusca(){
    var base_url = $j('base').attr('href');
    var url = base_url + "view-form";
    var parametros = {};
    var string_params = ''
    
    $j('#load-save').show();
    $j('#content-tabela').hide();
    $j('#content-macro').hide();
    
    $j('select.select-filter').each(function(){
        var pai = this.id;
        var L = [];
        var string_L = ''
        $j(this).find('option:selected').each(function(){
            if (this.value){
                L.push(this.value);
                string_L += this.value
            };
        });
        parametros[pai] = L;
        
        if (string_L.length > 0) {
            if(string_params.length > 0 ) {
                string_params += '&'+pai+'='+L;
            }else {
                string_params += '?'+pai+'='+string_L;
            }
        }
    });
    
    parametros['data_inicial'] =  $j('#data_inicial').val();
    parametros['data_final'] = $j('#data_final').val();


    $j('#link-export').attr('href', base_url+'export-form'+string_params)
        
    $j.ajax({traditional: true,
        type: "get",url: url,dataType: "text",
        data: parametros,
        success: function(data){
            $j('#content-tabela').html($j(data).find('#content-tabela').html());
            $j('#content-macro').html($j(data).find('#content-macro').html());
            
            setFilter();
            setPopup();
            
            $j('#load-save').hide();
            $j('#content-tabela').show();
            $j('#content-macro').show();        
        }
    });
};
 
function setFilter(){
    $j(".select-filter").multiselect({
        selectedList:5,
        minWidth:150,
        height:100,
        
        checkAll: function(){
            ajaxBusca();
        },
        uncheckAll: function(){
            ajaxBusca();
        }
    }).multiselectfilter({
        width:120
    },'refresh');

    $j('select.select-filter').change(function(){
       ajaxBusca(); 
    });
    
};

function setPopup(){
    var common_content_filter = '#content=*:not(div.configlet),dl.portalMessage.error,dl.portalMessage.info';
    var common_jqt_config = {fixed:false,speed:'fast',mask:{color:'#000',opacity: 0.4,loadSpeed:0,closeSpeed:0}};

   $j('a.excluir-data').prepOverlay({
        subtype: 'ajax',
        formselector: 'form[name=excluir-data]',
        closeselector: '[name=form.voltar]',
        noform: 'reload',
        filter: common_content_filter,
        config: common_jqt_config,
        width:'50%'
    
    });
    
};
 
$j(document).ready(function(){
    setFilter();
    setPopup();

    $j('#filter_data').click(function(){
        ajaxBusca();
    });
 });
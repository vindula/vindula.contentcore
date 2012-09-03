 $j = jQuery.noConflict();
 
function ajaxBusca(){
    var url = $j('base').attr('href') + "view-form";
    var parametros = {};
    
    $j('#load-save').show();
    $j('#content-tabela').hide();
    $j('#content-macro').hide();
    
    $j('select.select-filter').each(function(){
        var pai = this.id;
        var L = [];
        $j(this).find('option:selected').each(function(){
            L.push(this.value);
        });
        parametros[pai] = L;
        
    });
        
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
        noform: 'close',
        filter: common_content_filter,
        config: common_jqt_config,
        width:'50%'
    
    });
    
};
 
$j(document).ready(function(){
    setFilter();
    setPopup();
 });
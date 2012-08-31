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
                $j('#load-save').hide();
                $j('#content-tabela').show();
                $j('#content-macro').show();        
            }
    });
};
 
$j(document).ready(function(){
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
    });

    $j('select.select-filter').change(function(){
       ajaxBusca(); 
    });
       
 });
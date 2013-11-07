$j = jQuery.noConflict();

$j(document).ready(function(){
    
    $j('.accordion').click(function(){
        $hide_ele = $j('[data-id="'+this.id+ '"]');
        $hide_ele.toggle(500);
        
        var $arrow = $j(this).find('.arrow');
        $arrow.toggleClass('close');
        $arrow.toggleClass('open');
        
        return false;
    });
    
});
$(document).ready(function() {
    var DRINK_NAME = 'drink_name';
    var DRINK_PRICE = 'drink_price';

    var $removers;
    var $ctx       = $(this);
    var $menu      = $('ul.menu-item-list');
    var $template  = $ctx.find('li.menu-item').last();
    var $addOne    = $('a.add-one');    
    var $itemCounter = $('input[name=item_counter]');    
    
    repopulate_removers();
    $removers.on('click', function(evt) {
        evt.preventDefault();
        
        var postUrl = $(this).attr('href');
        var item = $(this).attr('data');
        var that = $(this);
        var successCallback = function() {that.parent().effect('explode', 'fast');}
        
        ajaxCall("POST", postUrl, {'item_id' : item}, successCallback, function() {});        
    });
    
    $addOne.click(function(evt) {
        var numItems = parseInt($itemCounter.val());        
        
        $itemCounter.val(numItems+1);   //we have to uniquely name each input element which is why we're doing this hackish thing
        var $clone = $template.clone();
        $clone.find('.item-name').attr("name", DRINK_NAME+numItems);
        $clone.find('.item-price').attr("name", DRINK_PRICE+numItems);        
        
        repopulate_removers();
        $menu.append($clone);          
    });
    
    function repopulate_removers() {
        $removers = $ctx.find('a.remove-one');
    }
})

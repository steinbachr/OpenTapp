/* copied whole-sale from https://gist.github.com/rca/1696408 */
$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
         }
     }
});

$(document).ready(function() {
    $("select").selectBoxIt({showEffect: "fadeIn", showEffectSpeed: 200, hideEffect: "explode", hideEffectSpeed: 500});
    $('.time-select').each(function() {        
        createTimepicker($(this));
    });
    
    var maxWidth = $('.accordion .accordion-group.first').css('width');
    $('.accordion-body').on('hide', function() {
        $(this).parent().css('width','600px');
        $(this).parent().find('.accordion-heading a span i.up').first().css('display', 'none');
        $(this).parent().find('.accordion-heading a span i.down').first().css('display', 'inline-block');
    });
    $('.accordion-body').on('show', function() {
        $(this).parent().css('width', maxWidth);
        $(this).parent().find('.accordion-heading a span i.up').first().css('display', 'inline-block');
        $(this).parent().find('.accordion-heading a span i.down').first().css('display', 'none');
    });

    /***MODALS***/
    $('.modal').each(function() {
        if($(this).hasClass('hide')) {
            $(this).modal({keyboard : true, show : false});    
        } else {
            $(this).modal();    
        }        
    });
    /***END MODALS***/
});
/**A function to check if the input matches currency format**/
function isCurrency(item) {
    var patternToMatch = /\d+(\.\d\d)?/;
    return patternToMatch.exec(item);
}

/**A helper function for making jquery ajax calls**/
function ajaxCall(type, url, data, successCallback, errorCallback) {
    $.ajax({
        type: type,
        url: url,
        data: data,
        success: successCallback,
        error: errorCallback
    });
};

/**A function to check if checkboxes are "on" or "off" and return the more colloquial "yes" or "no"**/
function checkboxConverter($checkbox) {
    if($checkbox.is(':checked')) {
        return "yes";
    } else {
        return "no"
    }   
}

/**A function to create a timepicker on a given $el**/
function createTimepicker($el) {
    $el.wrap('<div class="input-append bootstrap-timepicker timepicker-div">');
    $el.after('<span class="add-on"><i class="icon-time"></i></span>');
    $el.timepicker();
}




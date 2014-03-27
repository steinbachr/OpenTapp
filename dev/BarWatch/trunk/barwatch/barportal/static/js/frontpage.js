$(document).ready(function() {
    var $ctx = $('#signup_popup');

    /**BAR SIGNUP FORM**/        
    
    //setup
    $('input.bar-location').typeahead();
    autocomplete = new google.maps.places.Autocomplete($('input.bar-location').get(0));
    //put an asterisk next to required fields
    $('.step input').each(function() {
        if ($(this).attr('required')) {
            $(this).parent().prev().find('.required-asterisk').css('display', 'inline');
        }
    })

    function moveStep(direction) {
        var pattern = /step(\d)/;
        var current_step;
        var next_step;
        var first_step = $ctx.find('.step').first();
        var last_step = $ctx.find('.step').last();

        $ctx.find('.step.current').each(function() {            
            current_step = parseInt(pattern.exec($(this).attr('class'))[1]);
            next_step = 'step'+(current_step + direction);
            $(this).removeClass('current');
        })

        $('.'+next_step).addClass('current');

        //if its the last step, show the submit button and hide the next button
        if (last_step.hasClass(next_step)) {
            $ctx.find('input[type="submit"]').css('display', 'inline-block');
            $('.next').css('display', 'none');
        } else {
            $ctx.find('input[type="submit"]').css('display', 'none');
            $('.next').css('display', 'inline-block');
        }
        //if the next step is the first step, dont show previous button
        if (first_step.hasClass(next_step)) {
            $('.prev').css('display', 'none');
        } else {
            $('.prev').css('display', 'inline-block');
        }
    }

    //binding
    $('.next').bind('click', function(evt) {
        //form validation stuff        
        $("#signup_popup form").validate({
            rules : {
                email : {
                    required : true,
                    email : true
                },
                phone : {
                    required : true,
                    phoneUS : true
                }
                
            }
        });  
        
        if($("#signup_popup form").valid()) {
            moveStep(1);
        }
    });
    $('.prev').bind('click', function(evt) {
        moveStep(-1);
    });
});

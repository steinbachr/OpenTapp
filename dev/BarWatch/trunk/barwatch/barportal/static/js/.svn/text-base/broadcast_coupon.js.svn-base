$(document).ready(function() {
    var DEAL_TYPES = {"Single_Deal" : 0, "Group_Deal" : 1};     //this is NOT the right way to do this. TODO: refactor
    var GROUP_FIELDS = ".group-coupon";
    var SINGLE_FIELDS = ".single-coupon";
    var EXTRA_TIER = '.discount-group.extra';
    var GROUP_RANGE_SPAN = ".group-range-display";    

    var $ADD_TIER = $('.add-tier');
    var $DEAL_TYPE_SELECT = $('.deal-type-select');
    var $BROADCAST_BUTTON = $('.broadcast-button');    

    var $ctx = $(document);
    $('.date-select').datepicker();
    
    var toggleFields = function(field, showFields) {
        //we have to do some extra work if the field to toggle is a group or single deal field because have to subtract fields in that case
        $ctx.find(field).each(function() {
            if (showFields) {
                $(this).css('display', 'block');
            } else {
                $(this).css('display', 'none');
            }
        });
    };
    
    var showGroupRange = function(slider, ui, low, high) {
        //because this is used in oncreate of the slider now, ui.values is undefined in that case so we just use the given low and high values
        if (ui && ui.values) {
            var low = ui.values[0];
            var high = ui.values[1];
        }
    
        var $sliderMinRangeInput = $(slider).parent().find('input.min-range');
        var $sliderMaxRangeInput = $(slider).parent().find('input.max-range');
    
        var $low = $(slider).prev(GROUP_RANGE_SPAN).find('span.low-number');
        var $high = $(slider).prev(GROUP_RANGE_SPAN).find('span.high-number');
    
        $low.html(low);
        $high.html(high);
    
        $sliderMinRangeInput.val(low);
        $sliderMaxRangeInput.val(high);
    }
    
    //groups vertical sliders    
    $(".discount-tiers .discount-group .group-range").first().slider({
        orientation: "vertical",
        range: true,
        values: [0, 5],
        max: 15,
        min: 0,
        step: 1,
        slide: function(event, ui) {
            showGroupRange(event.target, ui);
        },
        create: function(event, ui) {
            showGroupRange(event.target, ui, 0, 5);
        }
    });
    
    //when the broadcast button is clicked, we need to copy relevant data into the confirmation modal
    $BROADCAST_BUTTON.bind('click', function(evt) {
        var $BROADCAST_CONFIRM_MODAL = $('#broadcast_confirm');
        var GROUP_DESCRIPTION_DIV = 'div.group-description';
        
        var template =  $('#all_coupons').html();        
        var view = {
            startDate : $('input[name="coupon_valid_from_date"]').val(),
            endDate : $('input[name="coupon_valid_to_date"]').val(),
            startTime : function() {
                if($('input[name="valid_all_day"]').is(':checked')) {
                    return "12:00AM";
                } else {
                    return $('input[name="coupon_valid_from_time"]').val();
                }
            }, 
            endTime : function() {
                if($('input[name="valid_all_day"]').is(':checked')) {
                    return "11:59PM";
                } else {
                    return $('input[name="coupon_valid_to_time"]').val();
                }                    
            }, 
            limit : checkboxConverter($('input[name="one_per_customer"]'))
        };
        var output = Mustache.render(template, view);        
        
        // depending on whether the deal is a group or single deal, prepare the appropriate template        
        if ($DEAL_TYPE_SELECT.val() == DEAL_TYPES.Group_Deal) {
            template = $('#group_coupon').html();
            view = {
                tierOne : {
                    min : $(GROUP_RANGE_SPAN+".tier-one").find('span.low-number').html(),
                    max : $(GROUP_RANGE_SPAN+".tier-one").find('span.high-number').html(),
                    description : $(GROUP_DESCRIPTION_DIV+".tier-one").find('input').val()
                },
                tierTwo : {
                    min : $(GROUP_RANGE_SPAN+".tier-two").find('span.low-number').html(),
                    max : $(GROUP_RANGE_SPAN+".tier-two").find('span.high-number').html(),
                    description : $(GROUP_DESCRIPTION_DIV+".tier-two").find('input').val()
                }
            }                 
        } else {
            template = $('#single_coupon').html();
            view = {description : $(SINGLE_FIELDS).find('.coupon-description input').val()};            
        }
        
        output = Mustache.render(template, view) + output;        
               
        $BROADCAST_CONFIRM_MODAL.find('.coupon-confirm ul').html(output);  
    });
    
    //setting the initial values
    toggleFields(GROUP_FIELDS, $DEAL_TYPE_SELECT.val() == DEAL_TYPES.Group_Deal);
    $(EXTRA_TIER).find('input').val('');    //set the extra tiers values to None initially
    
    $DEAL_TYPE_SELECT.bind('change', function(evt) {
        var showGroupFields = ($(evt.target).val() == DEAL_TYPES.Group_Deal);
    
        toggleFields(GROUP_FIELDS, showGroupFields);
        toggleFields(SINGLE_FIELDS, !showGroupFields);
    });
    $ADD_TIER.bind('click', function(evt) {
        var showExtraTier = $(EXTRA_TIER).css('display') != 'block';
        toggleFields(EXTRA_TIER, showExtraTier);
    
        if (showExtraTier) {
            $(this).html('<button class="btn btn-normal">remove tier</button>');
            $(EXTRA_TIER+' .group-range').slider({
                orientation: "vertical",
                range: true,
                values: [5, 10],
                max: 15,
                min: 0,
                step: 1,
                slide: function(event, ui) {
                    showGroupRange(event.target, ui);
                },
                create: function(event, ui) {
                    showGroupRange(event.target, ui, 5, 10);
                }
            });
        } else {
            $(this).html('<button class="btn btn-normal">add tier</button>');
            $(EXTRA_TIER+' .group-range').slider('destroy');
            $(EXTRA_TIER).find('input').val('');    //set the extra tiers values to None when we remove the extra tier
        }
    });
});

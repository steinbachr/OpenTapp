$(document).ready(function() {        
    $('.launch-coupon-details').click(function() {
        var url = $(this).attr('href');
        $.ajax(url, {
            success : function(data) {populateModal(data);}
        });

    
        function populateModal(data) {                        
            var template =  $('#coupon_details_template').html();
            var view = {
                broadcastDate : data.issued_at,
                fromDate : data.from_date,
                toDate : data.to_date,
                fromTime : data.from_time,                
                toTime : data.to_time,
                redemptions : data.num_redeemed
            };            
            
            var output = Mustache.render(template, view);
            $('#coupon_details').find('div.data').html(output);
            $('h3.coupon-details-header').html(data.coupon_description);
        }        
    });
});

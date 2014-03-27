 /**
 * Created with IntelliJ IDEA.
 * User: Bobby
 * Date: 8/14/12
 * Time: 12:19 AM
 * To change this template use File | Settings | File Templates.
 */

$(document).ready(function() {              
    /*********QUEUED COUPONS********/
    $('table.queued-coupons').tablecloth({theme:"default", bordered:true})
    $(".queued-coupons td.coupon-cancel a").click(function(evt) {
        evt.preventDefault();
        
        var postUrl = $(this).attr('href');
        var coupon = $(this).attr('class');        
        var that = $(this)
        
        var successCallback = function() { that.parent().parent().effect("explode", "slow"); };
        var errorCallback = function() { $.jGrowl("Can't remove active coupons"); };

        ajaxCall("POST", postUrl, {'coupon_id' : coupon}, successCallback, errorCallback);
    });
    
    
});

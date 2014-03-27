from django import template

register = template.Library()

@register.simple_tag
def single_coupon_details(coup):
    '''a template tag for building the html to create a link to a coupon details modal'''
    return '<a href="/api/singlecoupons/%s" class="launch-coupon-details" data-toggle="modal" data-target="#coupon_details">%s</a>' % \
           (coup.id, coup.coupon_description)

@register.simple_tag
def group_coupon_details(coup):
    '''a template tag for building the html to create a link to a coupon details modal'''
    return '<a href="/api/groupcoupons/%s" class="launch-coupon-details" data-toggle="modal" data-target="#coupon_details">%s</a>' %\
           (coup.id, coup.coupon_description)

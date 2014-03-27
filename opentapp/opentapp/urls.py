from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
#comment out in production
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
from django.contrib import admin
from barportal import enums as e
from barportal import views
from rest_framework import routers


admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'bars', views.BarViewSet)
router.register(r'singlecoupons', views.SingleCouponViewSet)
router.register(r'groupcoupons', views.GroupCouponViewSet)
router.register(r'users', views.MobileUserViewSet)

##HOME PATTERNS###
urlpatterns = patterns('barportal.views',
    url(r'^$', 'home'),        
    url(r'^admin/', include(admin.site.urls)),
)

##API PATTERNS##
urlpatterns += patterns('',
    url(r'^api/', include(router.urls)),    
    url(r'^api/singlecoupons/(?P<coupon>\d+)/redeem/$', 'barportal.views.redeem_coupon', {'type': e.DealTypes.SINGLE}),
    url(r'^api/groupcoupons/(?P<coupon>\d+)/invite/$', 'barportal.views.invite_group'),
    url(r'^api/groupcoupons/(?P<coupon>\d+)/redeem/$', 'barportal.views.redeem_coupon', {'type': e.DealTypes.GROUP}),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

##BAR PATTERNS##
urlpatterns += patterns('barportal.views',
    url(r'^user/(?P<user>\d+)/signed-in/$', 'logged_in'),    
    url(r'^user/(?P<user>\d+)/signed-in/broadcast/$', 'broadcast_coupon'),
    url(r'^user/(?P<user>\d+)/signed-in/edit-profile/$', 'edit_profile'),    
    url(r'^user/(?P<user>\d+)/signed-in/remove-menu-item/$', 'remove_menu_item'),
    url(r'^user/signed-in/logout/$', 'logout_user'),
)

##INTERNAL SERVICE PATTERNS##
urlpatterns += patterns('barportal.internal_services',
    url(r'^internal-service/autocomplete/$', 'autocompleter')    
)

#comment out in prod
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


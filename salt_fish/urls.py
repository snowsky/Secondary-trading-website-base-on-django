from django.conf.urls import url, include
from django.contrib import admin
from user import views
from good.views import test
urlpatterns = [

    url(r'^web_chat/(?P<good_id>\d+)/$', views.web_chat),

    url(r'^test/$', test),
    # 增加全文搜索

    url(r'^search/', include('haystack.urls')),

    url(r'^admin/', admin.site.urls),

    url(r'^$', views.IndexView.as_view()),
    url(r'^index/$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    # url(r'^good/', include('good.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^order/', include('order.urls')),
    url(r'^order-list/', views.OrderList.as_view(), name='order_list'),
    url(r'^contact_me/', views.ContactMe.as_view(), name='contact_me'),
    url(r'^register/', views.RegisterView.as_view(), name='register'),

    # 注册时获取验证码
    url(r'^getcode/', views.GetCode.as_view(), name='getcode'),



    url(r'^.*/$', views.error404, name='error')
]

from django.conf.urls import url, include
from django.contrib import admin
from user import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.IndexView.as_view()),
    url(r'^index/$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^good/', include('good.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^order-list/', views.OrderList.as_view(), name='order_list'),
    url(r'^contact_me/', views.ContactMe.as_view(), name='contact_me'),
    url(r'^register/', views.RegisterView.as_view(), name='register'),
    url(r'^getcode/', views.GetCode.as_view(), name='getcode'),

    url(r'^.*/$', views.error404, name='error')
]

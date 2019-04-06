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

    url(r'^.*/$', views.error404, name='error')
]

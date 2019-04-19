from django.conf.urls import url
from order import views

urlpatterns = [
    url(r'^pay/(?P<order_id>\d+)/$', views.page1),
    url(r'^page2/', views.page2),
]
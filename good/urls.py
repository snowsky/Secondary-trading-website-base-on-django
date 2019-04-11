from django.conf.urls import url
from good import views

urlpatterns = [
    url(r'^release/$', views.GoodRelease.as_view(), name='good_release'),
    url(r'^edit/(?P<good_id>\d*)$', views.GoodEdit.as_view(), name='good_edit'),
    url(r'^(?P<good_id>\d+)/$', views.GoodDetail.as_view(), name='good_detail'),
]
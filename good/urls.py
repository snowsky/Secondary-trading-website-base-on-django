from django.conf.urls import url
from good import views

urlpatterns = [
    url(r'^', views.GoodDetail.as_view(), name='good_detail')
]
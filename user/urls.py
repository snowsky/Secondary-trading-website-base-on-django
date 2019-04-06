from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^', views.UserInfo.as_view(), name='user_info')
]
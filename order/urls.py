from django.conf.urls import url
from order import views

urlpatterns = [
    url(r'^page1/', views.page1),
    url(r'^page2/', views.page2),
]
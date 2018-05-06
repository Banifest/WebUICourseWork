from django.conf.urls import url
from webui import views

urlpatterns = [
    url(r'^reg|reg.html$', views.RegView.as_view(), name='RegView'),
    url(r'^main|main.html$', views.MainView.as_view(), name='MainView'),
    url(r'^auth|auth.html$', views.AuthView.as_view(), name='AuthView'),
    url(r'^logout|logout.html$', views.LogOutView.as_view(), name='LogOutView'),
    url(r'^index|index.html$', views.IndexView.as_view(), name='index'),
]
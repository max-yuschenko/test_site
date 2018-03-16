from django.urls import path, include
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
# from django.contrib import admin
urlpatterns = [
    # path('', ),
    path(r'', views.home, name='home'),
    path(r'signup/', views.signup, name='signup'),
    url(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path(r'login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    # url(r'activate/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    # views.activate, name='activate'),
]
from cuentas import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url

app_name = 'cuentas'

urlpatterns = [
    url(r'^registro/$', views.register, name='registro'),
    url(r'^activar/(?P<key>.+)$', views.activation, name='activar'),
    url(r'^nuevo_link/(?P<user_id>\d+)/$',views.new_activation_link,name= 'nuevo_link'),
    url(r'^login/$', auth_views.login, {'template_name': 'cuentas/login.html'},name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'cuentas/logout.html','next_page':'cuentas:login'},name='logout'),
]

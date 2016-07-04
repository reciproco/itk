from interacciones import views
from django.conf.urls import url

app_name = 'interacciones'

urlpatterns = [
    url(r'^prueba/$', views.prueba, name='prueba'),
]

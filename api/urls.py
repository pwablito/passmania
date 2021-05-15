from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('register', views.register, name='register'),
    path('get_password', views.get_password, name='get_password'),
    path('add_password', views.add_password, name='add_password'),
    path('get_two_factor_code', views.get_two_factor_code, name='get_two_factor_code'),
    path('set_two_factor_codes', views.set_two_factor_codes, name='set_two_factor_codes'),
]

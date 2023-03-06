from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('test_code', test_code, name='test_code'),
    path('get_status', get_status, name='get_status'),
]
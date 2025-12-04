from django.urls import path

from .views import *

urlpatterns = [
    path('auth/login',EtablissementViewSet.as_view({'get': 'list'}),name='etablissement-list'),    
]
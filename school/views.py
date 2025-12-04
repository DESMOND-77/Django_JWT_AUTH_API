# apps/etablissement/views.py
from rest_framework import viewsets, permissions
from .models import Etablissement
from .serializers import EtablissementSerializer

class EtablissementViewSet(viewsets.ModelViewSet):
    queryset = Etablissement.objects.all()
    serializer_class = EtablissementSerializer
    permission_classes = [permissions.IsAdminUser]  # uniquement admin pour CRUD établissements

# apps/etablissement/serializers.py
from rest_framework import serializers
from .models import Etablissement

class EtablissementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etablissement
        fields = ['id','nom','code_etablissement','adresse','date_creation','statut']
        read_only_fields = ['id']

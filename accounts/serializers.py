# apps/accounts/serializers.py
from django.contrib.auth import authenticate
from rest_framework import serializers

# from school.serializers import EtablissementSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    # etablissement = EtablissementSerializer(read_only=True)

    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id','email', 'phone_number', 'first_name', 'last_name', 'username', 'profile_picture',
                  'profile_picture_url',  'created_at',  ]
        read_only_fields = ['id', 'created_at', 'updated_at','profile_picture_url']

    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            return self.context['request'].build_absolute_uri(obj.profile_picture.url)
        return None


class RegisterSerializer(serializers.ModelSerializer):
    mot_de_passe = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [ 'prenom', 'nom', 'email', 'role', 'mot_de_passe']

    def create(self, validated_data):
        mot_de_passe = validated_data.pop('mot_de_passe')
        etab = validated_data.pop('etablissement_id')
        user = User.objects.create_user(etablissement=etab, mot_de_passe=mot_de_passe, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    code_etablissement = serializers.CharField()
    matricule = serializers.CharField()
    mot_de_passe = serializers.CharField(write_only=True)

    def validate(self, attrs):
        code_etablissement = attrs.get('code_etablissement')
        matricule = attrs.get('matricule')
        mot_de_passe = attrs.get('mot_de_passe')

        user = authenticate(
            request=self.context.get('request'),
            code_etablissement=code_etablissement,
            matricule=matricule,
            password=mot_de_passe
        )

        if not user:
            raise serializers.ValidationError("Identifiants incorrects ou utilisateur introuvable.")
        if not user.is_active:
            raise serializers.ValidationError("Ce compte est désactivé.")

        attrs['user'] = user
        return attrs

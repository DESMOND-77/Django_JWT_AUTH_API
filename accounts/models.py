from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from school.models import Etablissement


class UserManager(BaseUserManager):
    def create_superuser(self, email,  password, **extra_fields):
        """
        Crée un superuser.
        """
        if not password:
            raise ValueError("mot de passe non definit pour le superUser")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email,  password, **extra_fields)

    def create_user(self, email, password, **extra_fields):
        """
        Crée un utilisateur normal.
        """
        if not password:
            raise ValueError("mot de passe non definit pour le User")
        if not email:
            raise ValueError("email non definit pour le User")
        
        # if not matricule or not school_id:
        #     raise ValueError("Le matricule et le code établissement sont obligatoires.")

        # Convertir l'ID reçu (string) en instance Etablissement
        # try:
        #     school_obj = Etablissement.objects.get(pk=school_id)
        # except Etablissement.DoesNotExist:
        #     raise ValueError(f"L'établissement '{school_id}' n'existe pas.")

        # extra_fields["school"] = school_obj

        # username et email doivent être passés via extra_fields
        # if "username" not in extra_fields:
        #     raise ValueError("Le champ 'username' est obligatoire.")
        # if "email" not in extra_fields:
        #     raise ValueError("Le champ 'email' est obligatoire.")
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ("etudiant", "Étudiant"),
        ("enseignant", "Enseignant"),
        ("parent", "Parent"),
        ("administrateur", "Administrateur"),
    ]

    id = models.BigAutoField(primary_key=True)
    # school = models.ForeignKey(settings.SCHOOL_MODEL, on_delete=models.CASCADE)
    matricule = models.CharField(unique=True, max_length=50)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=191, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    full_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", null=True, blank=True
    )
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLES)

    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # class Meta:
    # unique_together = ("school", "matricule")

    def __str__(self):
        return f"{self.username} ({self.matricule} - {self.school.id})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def get_short_name(self):
        return self.first_name or self.username

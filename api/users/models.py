from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from users.utils import generate_otp_code
import uuid


class PostlyUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be set.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_verified", False)
        

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_verified", False)
        

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
        edit the user table to have its pk equal to uuid
    """
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        unique=True, 
        editable=False
        )
    
    username = None
    email = models.EmailField(
        _("email address"),
        unique=True,
    )
    token_version = models.UUIDField(default=uuid.uuid4, unique=True)

    """
        add the fields for adding the otp verification feature during sign up
    """
    is_verified = models.BooleanField(default=False)
    otp_code = models.CharField(default=generate_otp_code)
    otp_version = models.UUIDField(default=uuid.uuid4, unique=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    """
        edit the field is_active default=False, user account is activated after email verification.
    """
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )


    objects = PostlyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

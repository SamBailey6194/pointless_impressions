from django.contrib.auth.models import (
    BaseUserManager,
    PermissionsMixin,
    AbstractBaseUser
    )
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(
            self,
            email,
            username,
            phone,
            password=None,
            **extra_fields
            ):
        if not email:
            raise ValueError("Email must be set")
        if not username:
            raise ValueError("Username must be set")
        if not password:
            raise ValueError("Password must be set")
        if not phone:
            raise ValueError("Phone number must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            phone=phone,
            **extra_fields
            )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
            self,
            email,
            username,
            phone,
            password=None,
            **extra_fields
            ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(
            email,
            username,
            phone,
            password,
            **extra_fields
            )

    def create_staff(
            self,
            email,
            username,
            phone,
            password=None,
            **extra_fields
            ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff must have is_staff=True.')
        if extra_fields.get('is_superuser') is not False:
            raise ValueError('Staff must have is_superuser=False.')

        return self.create_user(
            email,
            username,
            phone,
            password,
            **extra_fields
            )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(blank=False, null=False, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']

    def __str__(self):
        return self.username

    @property
    def is_dashboard_admin(self):
        """
        Check if the user is one of the dashboard staff groups.
        This is separate from the Django is_staff flag.
        """
        if not self.is_authenticated:
            return False

        allowed_groups = ['Employee', 'Manager', 'Owner']

        return self.groups.filter(name__in=allowed_groups).exists()

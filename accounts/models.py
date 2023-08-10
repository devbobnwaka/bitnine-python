import uuid
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

class UserManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **other_fields):
        user = self.create_user(
            email = self.normalize_email(email),
            password=password,
            **other_fields
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    email = models.EmailField(max_length=255, unique=True)
    has_accepted_terms = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff =  models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'
    

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(uuid.uuid4())
            qs = User.objects.filter(slug=self.slug).exclude(id=self.id)
            if qs.exists():
                self.slug = uuid.uuid4()
        super().save(*args, **kwargs)
        if self.slug is None:
            self.slug = uuid.uuid4()
            qs = User.objects.filter(slug=self.slug).exclude(id=self.id)
            if qs.exists():
                self.slug = uuid.uuid4()
            self.save()



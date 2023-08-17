from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_('The phone number must be set'))
        phone_number = self.normalize_email(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_TYPES = (
        ('women', 'женщина'),
        ('men', 'мужчина'),
    )

    email = models.EmailField('Email', null=True, blank=True)
    phone_number = models.CharField('Телефон', max_length=12, unique=True)
    auth_code = models.CharField(max_length=4, blank=True)
    invite_code = models.CharField(max_length=6, blank=True)
    has_used_invite = models.BooleanField(default=False)
    name = models.CharField('Имя', max_length=255, blank=True, default='')
    avatar = models.ImageField('Фото', upload_to='', blank=True, null=True)
    gender = models.CharField('Пол', choices=GENDER_TYPES, max_length=10, null=True, blank=True)
    is_active = models.BooleanField('Активный', default=True)
    is_superuser = models.BooleanField('Суперпользователь', default=False)
    is_staff = models.BooleanField('Администратор', default=False)
    date_joined = models.DateTimeField('Дата регистрации', default=timezone.now)
    last_login = models.DateTimeField('Последний визит', auto_now_add=True, blank=True, null=True)
    company_name = models.CharField('Название компании', max_length=100, null=True, blank=True)
    full_address = models.CharField('Адрес', max_length=100, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('name',)
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.phone_number

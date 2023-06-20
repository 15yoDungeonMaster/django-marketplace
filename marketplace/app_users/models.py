from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from marketplace.settings import MEDIA_URL


# Create your models here.

class MyUserManager(BaseUserManager):
    # Создаём метод для создания пользователя
    def _create_user(self, username, name, password, **extra_fields):
        # Проверяем есть ли логин
        if not name:
            raise ValueError('Вы не ввели Имя')
        if not username:
            # Выводим сообщение в консоль
            raise ValueError("Вы не ввели Логин")
        # Делаем пользователя
        user = self.model(
            name=name,
            username=username,
            **extra_fields,
        )
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем всё остальное
        user.save(using=self._db)
        # Возвращаем пользователя
        return user

    # Делаем метод для создание обычного пользователя
    def create_user(self, username, name, password):
        # Возвращаем нового созданного пользователя
        return self._create_user(username, name, password)

    # Делаем метод для создание админа сайта
    def create_superuser(self, username, name, password):
        # Возвращаем нового созданного админа
        return self._create_user(username, name, password, is_staff=True, is_superuser=True)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    username = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']
    objects = MyUserManager()

    def __str__(self):
        return self.username


def profile_image_directory_path(instance, filename: str) -> str:
    return f'profiles/profile_{instance.id}/images/{filename}'


class Profile(models.Model):
    fullName = models.CharField(max_length=200, verbose_name='full name')
    email = models.EmailField(verbose_name='email', blank=True)
    phone = PhoneNumberField(region='RU', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)

    avatar = models.ImageField(upload_to=profile_image_directory_path, null=False, blank=True, verbose_name='avatar')

    def __str__(self):
        return self.user.name

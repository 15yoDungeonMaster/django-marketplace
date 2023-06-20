from rest_framework import serializers

from marketplace.settings import MEDIA_URL
# Подключаем модель user
from .models import User, Profile


# class ImageSerializer(serializers.Serializer):
#     src = serializers.ImageField()
#     alt = serializers.CharField(max_length=50)
#
#     # def to_representation(self, instance):
#     #     representation = super().to_representation(instance)
#     #     print(representation)
#     #     if instance.src.url == '':
#     #         representation['src'] = ''
#     #     else:
#     #         representation['src'] = instance.src.url
#     #     representation['alt'] = instance.alt
#
#     #
#     # def to_internal_value(self, data):
#     #     ...


class UserRegistrSerializer(serializers.ModelSerializer):
    # Настройка полей
    class Meta:
        # Поля модели которые будем использовать
        model = User
        # Назначаем поля которые будем использовать
        fields = ['name', 'username', 'password']

    # Метод для сохранения нового пользователя
    def save(self, *args, **kwargs):
        # Создаём объект класса User
        user = User(
            name=self.validated_data['name'],  # Назначаем name
            username=self.validated_data['username'],  # Назначаем Логин
        )
        # Проверяем на валидность пароль
        password = self.validated_data['password']
        user.set_password(password)
        # Сохраняем пользователя
        user.save()
        # Возвращаем нового пользователя
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        required_fields = ['username', 'password']


class ProfileAvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(method_name='get_avatar')

    class Meta:
        model = Profile
        fields = ('avatar',)

    def validate(self, data):
        print(data)
        if 'avatar' not in data:
            raise serializers.ValidationError("bad file")
        return data

    def get_avatar(self, obj):
        print(obj)
        if obj.avatar:
            return {
                'src': obj.avatar.url,
                'alt': 'profile image'
            }

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('fullName', 'email', 'phone')

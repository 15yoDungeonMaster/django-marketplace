import json

from django.contrib.auth import logout, login
from django.contrib.auth.handlers.modwsgi import check_password
from rest_framework.exceptions import ValidationError
# Подключаем компонент для создания данных
from rest_framework.generics import CreateAPIView
# Подключаем компонент для прав доступа
from rest_framework.permissions import AllowAny, IsAuthenticated
# Подключаем компонент для ответа
from rest_framework.response import Response
from rest_framework.views import APIView

# Подключаем компонент Token
# from rest_framework import Token
# Подключаем модель User
from .models import User, Profile
# Подключаем UserRegistrSerializer
from .serializers import UserRegistrSerializer, UserLoginSerializer, ProfileSerializer, ProfileAvatarSerializer


class SignUpUserView(CreateAPIView):
    permission_classes = [AllowAny]
    # Добавляем в queryset
    queryset = User.objects.all()
    # Добавляем serializer UserRegistrSerializer
    serializer_class = UserRegistrSerializer
    # Добавляем права доступа
    permission_classes = [AllowAny]

    # Создаём метод для создания нового пользователя
    def post(self, request, *args, **kwargs):
        request_data = json.loads(*request.data.dict().keys())

        # Добавляем UserRegistrSerializer
        serializer = UserRegistrSerializer(data=request_data)
        # Создаём список data
        # Проверка данных на валидность
        if serializer.is_valid():
            user = serializer.save()

            # Возвращаем что всё в порядке
            profile = Profile(user=user, fullName=user.name)
            profile.save()
            login(request, user=user)
            return Response('successful operation')
        else:  # Иначе
            # Присваиваем data ошибку
            data = serializer.errors
            # Возвращаем ошибку
            return Response(data)


class SignOutUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response('successful operation')


class SignInUserView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        data = {}
        request_data = json.loads(*request.data.dict().keys())
        username = request_data['username']
        print(username)
        password = request_data['password']
        data['username'] = username
        data['password'] = password
        try:

            account = User.objects.get(username=username)
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})
        if account:
            if check_password(account.password, username, password):
                login(request, account)
                return Response('successful operation')
            return Response('Invalid credentials', status=400)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        profile_object = Profile.objects.get(user=self.request.user)
        return profile_object

    def get(self, request):
        profile = self.get_object()
        profile_data = ProfileSerializer(profile).data
        avatar_data = ProfileAvatarSerializer(profile).data
        return Response((profile_data | avatar_data))

    def post(self, request, *args, **kwargs):
        profile = self.get_object()

        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            profile.fullName = serializer.validated_data['fullName']
            profile.email = serializer.validated_data['email']
            profile.phone = serializer.validated_data['phone']
            profile.save()

            return Response(serializer.data)


class ProfileAvatarAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        request_data = request.data.dict()

        user.profile.avatar = request_data['avatar']
        user.profile.save()

        return Response('successful operation')


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        print(request.data)

        if not user.check_password(request.data['currentPassword']):
            raise ValueError('reset password failed')
        else:
            user.set_password(request.data['newPassword'])
            user.save()
        return Response('successful operation')

from django.urls import path

from .views import SignUpUserView, SignOutUserView, SignInUserView, ProfileView, ProfileAvatarAPIView, \
    ChangePasswordAPIView

urlpatterns = [
    path('sign-up', SignUpUserView.as_view(), name='sign-up'),
    path('sign-in', SignInUserView.as_view(), name='sign-in'),
    path('sign-out', SignOutUserView.as_view(), name='sign-out'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('profile/avatar', ProfileAvatarAPIView.as_view(), name='profile-avatar'),
    path('profile/password', ChangePasswordAPIView.as_view(), name='change-password'),

]

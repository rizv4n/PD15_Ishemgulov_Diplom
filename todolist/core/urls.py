from django.urls import path
from core.views import UserCreateView, UserLoginView, UserRetrieveUpdateView, UpdatePasswordView

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserRetrieveUpdateView.as_view(), name='retrieve'),
    path('update_password/', UpdatePasswordView.as_view(), name='update_password')
]

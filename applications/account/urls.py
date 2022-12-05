from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)
from applications.account.views import *

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('logout/', LogoutApiView.as_view()),
    path('activate/<uuid:activation_code>/', AcitvationApiView.as_view()),
    path('change_password/', ChangePasswordApiView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
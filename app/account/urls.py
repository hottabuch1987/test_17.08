from django.urls import path
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('api/auth/send_code/', SendAuthCode.as_view()),
    path('api/auth/check_code/', CheckAuthCode.as_view()),
    path('api/auth/profile/<str:phone_number>/', UserProfile.as_view()),

]

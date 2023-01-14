from django.contrib import admin
from django.urls import path
from .views import UserRegistration, UserSiginin, UserSignout, GetPackagePlan, AddPhoneNumber, AddpaymentForPackage

urlpatterns = [
    path('signup/',UserRegistration.as_view()),
    path('signin/',UserSiginin.as_view()),
    path('signout/',UserSignout.as_view()),
    path('plan/<str:pk>/', GetPackagePlan.as_view()),
    path('phone/<str:pk>/<int:ph>', AddPhoneNumber.as_view()),
    path('payment/<str:pk>/', AddpaymentForPackage.as_view())
]
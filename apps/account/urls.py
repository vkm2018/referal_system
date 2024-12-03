from django.urls import path, include

from apps.account.views import RegisterAPIView, CodeView, ProfileView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('send_code/', CodeView.as_view(), name='send_code'),
    path('register/', RegisterAPIView.as_view(), name='verify_code'),
    path('profile/<str:number_phone>/', ProfileView.as_view(), name='profile'),


]

from django.urls import path, include


from . import views

urlpatterns = [
    path('getEnergyData/', views.getEnergyData, name='getEnergyData'),
    path('getEnergyDataDay/', views.getEnergyDataDay, name='getEnergyDataDay'),
    path('getEnergyDataMonth/', views.getEnergyDataMonth, name='getEnergyDataMonth'),
    path('loginUser/', views.loginUser, name='loginUser'),
]
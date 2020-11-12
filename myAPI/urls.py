from django.urls import path, include


from . import views

urlpatterns = [
    path('getEnergyData/', views.getEnergyData, name='getEnergyData'),
    path('getEnergyDataDay/', views.getEnergyDataDay, name='getEnergyDataDay'),
    path('getEnergyDataMonth/', views.getEnergyDataMonth, name='getEnergyDataMonth'),
    path('loginUser/', views.loginUser, name='loginUser'),
    path('loginUser2/', views.loginUser2, name='loginUser2'),
    path('logout/', views.logout_view, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('user_info/', views.user_info, name='user_info'),
    path('update_package/', views.update_package, name='update_package'),
    path('getCarbonReduce/', views.getCarbonReduce, name='getCarbonReduce'),
    path('getUsage/', views.getUsage, name='getUsage'),
    path('getRemainPackage/', views.getRemainPackage, name='getRemainPackage'),


]

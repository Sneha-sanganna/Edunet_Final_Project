from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('vote/', views.vote, name='vote'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('results/', views.results, name='results'),


    path('login/', views.login_view, name='login'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    
    path('reset-password/', views.reset_password, name='reset_password'),
    # urls.py
    path('logout/', views.logout_view, name='logout'),
    path('final-results/<str:location>/', views.final_results, name='final_results'),
    path('download-receipt/', views.download_receipt, name='download_receipt'),
]
    
    



   
   


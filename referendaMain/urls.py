from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.dashboard, name='dashboard'),
    path('account/', views.accountUpdate, name='account'),
    path('create/', views.createReferendumPage, name='create'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('vote/<uuid:id>/', views.votePage, name='vote'),
    path('results/<uuid:id>/', views.resultsPage, name='results'),
    
]
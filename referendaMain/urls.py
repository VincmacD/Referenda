from django.urls import path
from . import views
from .views import loginPage

urlpatterns = [

    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage.as_view(), name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.dashboard, name='dashboard'),
    path('account/', views.accountUpdate, name='account'),
    path('create/', views.createReferendumPage, name='create'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('vote/<uuid:id>/', views.votePage, name='vote'),
    path('results/<uuid:id>/', views.resultsPage, name='results'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('password_reset/', views.resetPassword, name="password_reset"),
    path('set_password/', views.resetPasswordConfirm, name="set_password"),
    path('reset/<uidb64>/<token>', views.resetPasswordConfirm, name='password_reset_confirm'),
    
    
]
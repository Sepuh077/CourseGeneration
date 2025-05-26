from django.urls import path

from .views import register, sign_in, sign_out, password_reset_api, reset_password_page, forget_password_page, password_reset_api_confirm


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', sign_in, name='login'),
    path('logout/', sign_out, name='logout'),
    path('reset/', reset_password_page, name='reset_password'),
    path('forget/', forget_password_page, name='forget_password'),
    path('api/password-reset/', password_reset_api, name='api_password_reset'),
    path('api/password-reset-confirm/', password_reset_api_confirm, name='api_password_reset'),
]

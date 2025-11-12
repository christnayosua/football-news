from django.urls import path

# Import fungsi login dan register
from authentication.views import login, logout, register

app_name = 'authentication'

urlpatterns = [
    # login
    path('login/', login, name='login'),
    # logout
    path('register/', register, name='register'),
    # Logout
    path('logout/', logout, name='logout')
]
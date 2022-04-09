from unicodedata import name
from django.urls import path
from .views import *
urlpatterns = [
    path('' , home , name="home"),
    path('game' , game , name="game"),
    path('login' , login_main , name="login"),
    path('signup' , signup , name="signup"),
    path('success' , success , name="success"),
    path('signup/login' , login_main , name="login"),
    path('verify/<auth_token>' , verify , name="verify"),
    path('error' , error , name="error"),
    path('token_send' , token_send , name="token_send"),
    path('game' , game , name = "game"),
]
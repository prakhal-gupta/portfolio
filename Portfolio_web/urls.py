from django.urls import path
from Portfolio_web.views import *

app_name = 'Portfolio_web'
urlpatterns = [
    path('Message/',User_message),
 	path('registration/',Admin_registration),
	path('login/',Admin_login),
	path('Dash/',Admin_dash),
    path('Response/key',Response_key),
    path('Response/',Response_Update),
	path('logout/',Logout),
]
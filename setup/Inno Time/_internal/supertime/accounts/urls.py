from django.urls import path
from . import views

app_name = "accounts"
#path('nom_voulu',views.nom_def,name='nom_html')
urlpatterns = [
    path('login_admin/',views.login_admin, name= 'login_a'),
    #path('login/',views.login_user, name= 'login_e'),
    path('logout/',views.logout_user, name= 'logout'),
    path('register/',views.register_user, name= 'register'),
]
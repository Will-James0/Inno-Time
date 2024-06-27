from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'profil'

urlpatterns=[
    path('',views.first_time_user,name='register'),
    path('index/',views.index, name='index'),
    path('dashboad/',views.dashboard,name='dashboad'),
    path('add/poste/', views.add_poste , name='save_poste'),
    path('add/personnel/', views.add_personnel, name='save_employe'),
    # path('details/', views.detail_register, name='details_user'),
    path('personnel/list/', views.personnel_list , name='liste_employe'),
    # path('Ajout horaire/', views.part3, name='part3'),
    path('attendance/',views.attendance,name='attendance'),
    path('dowloands/log/lecteur?<int:lecteur_id>/',views.get_log_data,name='get_log_data'),
    path('dowloands/user/lecteur?<int:lecteur_id>/',views.add_users,name='add_users'),
    path('user/list/',views.user_list,name="liste_user"),
    path('logs/data/',views.raw_data,name='logs'),
    path('get_somme_for_poste/', views.get_somme_for_poste, name='get_somme_for_poste'),
    path('get_start/', views.get_start, name='get_start'),
    path('get_end/', views.get_end, name='get_end'),
    path('get_time_work/', views.get_time_work, name='get_time_work'),
    path('get_tolerance_time/', views.get_tolerance_time, name = 'get_tolerance_time'),
    path('dowloands/attendance/', views.get_attendance_data, name = 'add_horaire'),
    path('historique/',views.historique,name='historique'),
    path('add/lecteur/',views.add_drive, name='add_drive'),
    path('help/',views.help,name='help'),
    path('edit/poste/<int:poste_id>/', views.edit_poste, name='modife_poste'),
    path('edit/personnel/personnel?<int:personnel_id>/',views.edit_personnel,name='modife_employe'),
    path('edit/attendances/attendance?<int:Horaire_id>/',views.edit_attendance,name='modife_attendance'),
    path('profil/employe?<int:Personnel_id>/',views.personnel_profil,name='profil_employe'),
    path('delete-employe/employé?<int:Personnel_id>/',views.delete_personnel,name='delete_personnel'),
    path('delete-poste/poste?<int:Poste_id>/',views.delete_poste,name='delete_poste'),
    path('ternimal/list/', views.terminal_list, name = 'liste_drive'),
    path('profil/user/',views.user_profil, name = 'profil_user'),
    path('poste/', views.poste_list, name='liste_poste'),
    path('Fiche/<int:Personnel_id>/', views.personnel_salary, name='salary'),
    path('delete-lecteur/id=<int:lecteur_id>/',views.delete_drive,name='delete_drive'),
    path('edit/lecteur/id=<int:lecteur_id>/',views.edit_drive,name='modife_drive'),
    path('delete-employe/',views.delete_employees,name='delete_employees'),
    path('dowloands/log-alls/',views.get_all_log_data,name='get_all_log_data'),
      
]
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'profil'

urlpatterns=[
    path('',views.index,name='index'),
    path('liste/',views.liste_e,name='liste_e'),
    path('Acceuil/',views.acceuil,name='acceuil'),
    path('Ajout poste/', views.part1, name='part1'),
    path('Ajout personnel/', views.part2, name='part2'),
    # path('Ajout horaire/', views.part3, name='part3'),
    path('attendance/',views.attendance,name='attendance'),
    #-------------------------------------------#
    path('add_att/',views.add_attendance,name='add_attendance'),
    path('add_user/',views.add_user,name='add_user'),
    path('liste_u/',views.liste_u,name="liste"),
    path('data/',views.data,name='data'),
    path('data_zk/',views.data_brute,name='a_valide'),
    path('get_save/',views.filter_and_save_attendance ,name='filter_and_save_attendance'),
    
    path('data_get/',views.save_attendance ,name='attendance_saved.html'),
    #-------------------------------------------#
    path('historique/',views.historique,name='historique'),
    path('machine/',views.machine, name='machine'),
    path('help/',views.help,name='help'),
    # path('modifie_infor_poste/<int:Poste_id>/',views.edit_Poste,name='partm1'),
    path('partm1/<int:poste_id>/', views.partm1, name='partm1'),
    path('modifie_infor_personnel/<int:personnel_id>/',views.part2m,name='partm2'),
    path('modifie_infor_horaire/<int:Horaire_id>/',views.edit_Horaire,name='partm3'),
    path('profile_employé/id=<int:Personnel_id>/',views.profil_e,name='profil_e'),
    path('delete employé/id=<int:Personnel_id>/',views.del_user,name='delt_user'),
    path('delete poste/id=<int:Poste_id>/',views.del_poste,name='delt_poste'),
    path('liste_t', views.liste_t, name = 'liste_t'),
    path('profil_u/',views.profil_u, name = 'profil_user'),
    path('poste/', views.post, name='poste'),
  
    path('Fiche/<int:Personnel_id>/', views.personnel_salary, name='salaire'),
  path('delete_lecteur/id=<int:lecteur_id>/',views.del_lecteur,name='del_lecteur'),
    
    path('edit_lecteur/id=<int:lecteur_id>/',views.edit_lecteur,name='edit_lecteur'),
    #path('data/id=<int:lecteur_id>/', views.data, name='data'),
    path('poste/', views.post, name='poste'),
    path('delete_employees',views.delete_employees,name='delete_employees')
  

    # path('ajout_profil/',views.add_Profil,name='add_Profil'),
]
from django.urls import path
from . import views

app_name = 'profil'

urlpatterns=[
    path('',views.index,name='index'),
    path('liste',views.liste_e,name='liste_e'),
    path('Acceuil/',views.acceuil,name='acceuil'),
    path('Ajout poste/', views.part1, name='part1'),
    path('Ajout personnel/', views.part2, name='part2'),
    path('Ajout horaire/', views.part3, name='part3'),
    path('attendance/',views.attendance,name='attendance'),
    path('historique/',views.historique,name='historique'),
     path('help/',views.help,name='help'),
    path('modifie_infor_poste/<int:Poste_id>/',views.edit_Poste,name='partm1'),
    path('modifie_infor_personnel/<int:Personnel_id>/',views.edit_Personnel,name='partm2'),
    path('modifie_infor_horaire/<int:Horaire_id>/',views.edit_Horaire,name='partm3'),
     path('profile_employé/id=<int:Personnel_id>/',views.profil_e,name='profil_e'),
    path('delete employé/id=<int:Personnel_id>/',views.del_user,name='delt_user'),
    path('delete poste/id=<int:Poste_id>/',views.del_poste,name='delt_poste'),
    path('s/<int:Personnel_id>/', views.personnel_salary, name='salaire'),
    path('Fiche/<int:personnel_id>/',views.fiche,name='salaire'),
    path('poste/', views.post, name='poste'),
    path('delete_employees',views.delete_employees,name='delete_employees')
    # path('ajout_profil/',views.add_Profil,name='add_Profil'),
]
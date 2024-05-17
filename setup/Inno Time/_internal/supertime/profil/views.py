from django.shortcuts import render, get_list_or_404,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Horaire,Poste, Salaire,Zklecteur,Personnel,Attendance
from .forms import Part1Form, Part2Form,Part3Form,ZKTecoForm
from django.contrib.auth.models import User
from datetime import datetime, timedelta, timezone,date,time
from django.core.paginator import Paginator
from django.db.models import Count, Q
import subprocess
from zk import ZK, const
import threading
from threading import Thread
import os
import sys
import asyncio
from django.utils import timezone
import calendar
from django.db.models import Min, Max
from dateutil.relativedelta import relativedelta



CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)




   
# # @login_required(login_url="/account/login_admin/")
# @login_required(login_url="/account/login_admin/")
# def liste_t(request):
#     lecteurs = Zklecteur.objects.all()
#     status_list = []
#     messages = []

#     for lecteur in lecteurs:
#         zk = ZK(lecteur.ip_adresse, lecteur.n_port, timeout=1)
#         conn = None
#         status = False

#         try:
#             conn = zk.connect()
#             status = conn.is_connect
#             status_list.append(status)
#         except Exception as e:
#             messages.append("Erreur de connexion avec le lecteur {}: {}".format(lecteur.id, e))
#         finally:
#             if conn is not None and conn.is_connect:
#                 conn.disconnect()

#     return render(request, 'profil/liste_t.html', {'zklect': lecteurs, 'status_list': status_list, 'messages': messages})


@login_required(login_url="/account/login_admin/")
def liste_t(request):
    lecteurs = Zklecteur.objects.all()
    status_list = []
    messages = []

    def check_status(lecteur):
        zk = ZK(lecteur.ip_adresse, lecteur.n_port, timeout=1)
        conn = None
        status = False

        try:
            conn = zk.connect()
            status = conn.is_connect
            status_list.append(status)
        except Exception as e:
            messages.append("Erreur de connexion avec le lecteur {}: {}".format(lecteur.id, e))
        finally:
            if conn is not None and conn.is_connect:
                conn.disconnect()

    def check_all_statuses():
        threads = []
        for lecteur in lecteurs:
            thread = threading.Thread(target=check_status, args=(lecteur,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    check_all_statuses()

    return render(request, 'profil/liste_t.html', {'zklect': lecteurs, 'status_list': status_list, 'messages': messages})


#-------------------------------------------------------------------------------------------------------------#
@login_required(login_url="/account/login_admin/")
def add_users(request, lecteur_id):
    statut=None
    lecteurs = Zklecteur.objects.get(pk=lecteur_id)
    conn = None
    zk = ZK(lecteurs.ip_adresse, port=lecteurs.n_port, timeout=2)
    try:
        conn = zk.connect()
        print('Disabling device ...')
        conn.disable_device()
        print('--- Get User ---')
        users = conn.get_users()
        
        for user in users:
            zkteco_username = user.name
            zkteco_user_id = user.user_id
            pw = user.password
            print(zkteco_user_id, zkteco_username, pw)
            
            try:
                django_user = User.objects.get(username=zkteco_user_id)
                # Si l'utilisateur existe, mettez à jour ses informations
                django_user.zkteco_user_id = zkteco_user_id
                django_user.save()
                pass
            except User.DoesNotExist:
                # Si l'utilisateur n'existe pas, créez un nouvel utilisateur Django
                django_user = User.objects.create_user(username=zkteco_user_id,password=pw)
                django_user.zkteco_user_id = zkteco_user_id
                django_user.save()
                if user.privilege == const.USER_ADMIN:  # Assurez-vous que votre appareil ZKTeco fournit cette information
                    django_user.is_superuser = True
                    django_user.save()
               
    
            
            # Vérifier le statut de l'utilisateur dans le lecteur
            
                
        print('Enabling device ...')
        conn.enable_device()
            
    except Exception as e:
        print("Process terminate : {}".format(e))
    finally:
        if conn is not None and conn.is_connect:
            conn.disconnect()
            
    return render(request, "profil/valide.html", {'statut':statut})

# def add_users(request, lecteur_id):
    # statut = None
    # lecteurs = Zklecteur.objects.get(pk=lecteur_id)
    # conn = None
    # zk = ZK(lecteurs.ip_adresse, port=lecteurs.n_port, timeout=2)
    # try:
    #     conn = zk.connect()
    #     print('Disabling device ...')
    #     conn.disable_device()
    #     print('--- Get Users ---')
    #     users = conn.get_all_users()
        
    #     for user in users:
    #         zkteco_username = user.name
    #         zkteco_user_id = user.uid
    #         pw = user.password
    #         print(zkteco_user_id, zkteco_username, pw)
            
    #         try:
    #             django_user = User.objects.get(username=zkteco_username)
    #             # Si l'utilisateur existe, mettez à jour ses informations
    #             django_user.zkteco_user_id = zkteco_user_id
    #             django_user.save()
    #         except User.DoesNotExist:
    #             # Si l'utilisateur n'existe pas, créez un nouvel utilisateur Django
    #             django_user = User.objects.create_user(username=zkteco_username, password=pw)
    #             django_user.zkteco_user_id = zkteco_user_id
    #             django_user.save()
    #             # Enregistrer l'utilisateur en tant que superutilisateur si nécessaire
    #             if user.privilege == const.USER_ADMIN:  # Assurez-vous que votre appareil ZKTeco fournit cette information
    #                 django_user.is_superuser = True
    #                 django_user.save()
                
    #         # Vérifier le statut de l'utilisateur dans la base de données Django
    #         if User.objects.filter(username=zkteco_username).exists():
    #             if conn.get_user(uid=zkteco_user_id):
    #                 statut = "Actif"
    #             else:
    #                 statut = "Inactif"
            
    #     print('Enabling device ...')
    #     conn.enable_device()
            
    # except Exception as e:
    #     print("Process terminate : {}".format(e))
    # finally:
    #     if conn is not None and conn.is_connect:
    #         conn.disconnect()
            
    # return render(request, "profil/valide.html", {'statut': statut})

@login_required(login_url="/account/login_admin/")
def valide(request):
    statut = request.GET.get('statut', None)
    return render(request, "profil/valide.html", {'statut':statut})


@login_required(login_url="/account/login_admin/")
def data(request):
    attendance=Attendance.objects.all()
    if request.method == "GET":
        
        date_search=request.GET.get('rechercher')
        personnel_search=request.GET.get('rechercher')
        if personnel_search is not None or date_search:
            
            attendance_list = Attendance.objects.filter(date__startswith=date_search,personnel_a=personnel_search)
    


    paginator = Paginator(attendance_list, 10)  # Paginer la liste avec 10 employés par page
    
    page_number = request.GET.get('page')  # Récupérer le numéro de page depuis les paramètres GET
    page_obj = paginator.get_page(page_number)  # Obtenir l'objet Page pour la page demandée
    context = {'page_obj': page_obj,
               
               
               }
    return render(request,'profil/data.html',context)

@login_required(login_url="/account/login_admin/")
def data_brute(request):
    attendance_list=Attendance.objects.order_by('-date','-heure_punch')
    if request.method == "GET":
        
        # date_search=request.GET.get('date_search')
        personnel_search=request.GET.get('user_search')
        if personnel_search is not None: 
            
            attendance_list = Attendance.objects.filter(personnel_a=personnel_search)
          
    paginator = Paginator(attendance_list, 10)  # Paginer la liste avec 10 employés par page
    
    page_number = request.GET.get('page')  # Récupérer le numéro de page depuis les paramètres GET
    page_obj = paginator.get_page(page_number)  # Obtenir l'objet Page pour la page demandée
    context = {'page_obj': page_obj,
               
               
               }
    return render(request,'profil/a_valide.html',context)



@login_required(login_url="/account/login_admin/")
def liste_u(request):
    users=User.objects.all()
    return render(request,'profil/liste.html',{"users":users})



@login_required(login_url="/account/login_admin/")
def get_attendance_data(request, lecteur_id):
    lecteurs = Zklecteur.objects.get(pk=lecteur_id)
    zk = ZK(lecteurs.ip_adresse, lecteurs.n_port, timeout=2)
    try:
        conn = zk.connect()
        print('Disabling device ...')
        conn.disable_device()
        print('--- Get User ---')
        attendance = conn.get_attendance()
        print(type(attendance))
        print(attendance)

        for user in attendance:
            id_a = user.uid
            check_heure = user.timestamp
            status_a = user.status
            user_id = user.user_id
            punch_a = user.punch
            try:
                try:
                    # Tentative de récupération de l'objet Attendance avec l'identifiant spécifié
                    django_user = Attendance.objects.get(id_att=id_a)
                    pass
                except Attendance.DoesNotExist:
                    
                        # Tentative de récupération de l'objet Personnel associé à l'identifiant
                    user_id_zk =User.objects.get(username=user_id)
                    pk_user=user_id_zk.pk
                    user_c = Personnel.objects.get(user=pk_user)
                # Si le Personnel existe, crée une nouvelle instance du modèle Attendance
                    django_user = Attendance.objects.create(id_att=id_a, personnel_a=user_c, date=check_heure.date(), status=status_a, punch=punch_a, heure_punch=check_heure)
                    django_user.save()
                    print("1411")
            except:
                pass
            
    
        print('Enabling device ...')
        conn.enable_device()
    except Exception as e:
        print("Processus interrompu :", e)
    finally:
        if conn is not None and conn.is_connect:
            conn.disconnect()




    message = "Données téléchargées avec succès"
    return redirect('profil:liste_t')


#----------------------------------------------------------------------------------------------------#
# def data(request,):
#             CWD = os.path.dirname(os.path.realpath(__file__))
            
            
#             zk = ZK('192.168.1.206' ,timeout=5)
#             conn =None
#             # print(lecteurs.ip_adresse,'',lecteurs.n_port)
#             try:
#                 conn = zk.connect()
#                 print ('Disabling device ...')
#                 conn.disable_device()
#                 print ('--- Get User ---')
#                 users = conn.get_attendance()
                
#                 st=conn.is_connect
#                 print(st)

#                 conn.enable_device()
            
#                 return render(request, 'profil/data.html',{'users':users,'st':st})

#             except Exception as e:
#                 print ("Process terminate : {}".format(e))
#             finally:
#                 if conn != None and conn.is_connect:
#                     conn.disconnect()
#             return render(request, 'profil/data.html',)






@login_required(login_url="/account/login_admin/")  
def del_lecteur(request,lecteur_id):
    lecteur = Zklecteur.objects.get(pk=lecteur_id)
    lecteur.delete()
    return redirect("profil:liste_t")



@login_required(login_url="/account/login_admin/")
def edit_lecteur(request,lecteur_id):
    lecteur = Zklecteur.objects.get(pk=lecteur_id)
    if request.method == 'POST':
        form = ZKTecoForm(request.POST,instance=lecteur)
        if form.is_valid():
            form.save()
            return redirect("profil:liste_t")
    else:
        form = ZKTecoForm(instance=lecteur)
    
    return render(request,"profil/machine.html",{"form": form})





@login_required(login_url="/account/login_admin/")
def acceuil(request):
    # maintenant=datetime.now()
    maintenant=datetime.now()

    annee = maintenant.year
    mois = mois = maintenant.month

    # Nombre de jours à récupérer
    nb_jours = calendar.monthrange(annee, mois)[1]
    nombre_jours = nb_jours

    # Liste pour stocker les dates
    dates_du_jour = []

    # Récupération des dates du jour
    # aujourd_hui = datetime.now().date()
    aujourd_hui = date(annee, mois, 1)
    for i in range(nombre_jours):
        date_day = aujourd_hui + timedelta(days=i)
        dates_du_jour.append(date_day)

    # Affichage des dates
    # for date in dates_du_jour:
    #      print(date)

    date_j = date.today()
    attendance_dates = Horaire.objects.values_list('date_d', flat=True).distinct()
    # Séparer les dates et les nombres d'employés en deux listes distinctes
    dates_list = []
    counts_list = []
    # i=30
    # day_nbr = date.today().strftime("%d")
    # while i == 30:
    for entry in  dates_du_jour:
            dates_list.append(str(entry.strftime("%d-%m-%Y")))
            present = Horaire.objects.filter(arrival_time__startswith=entry).count()
            counts_list.append(int(present))

    # i +=1
    total_employees = Personnel.objects.count()
    
    # Compter le nombre d'employés présents à la date donnée
    employees_present = Horaire.objects.filter(arrival_time__startswith=date_j).count()
    # Calculer le nombre d'employés absents
    employees_absent = total_employees - employees_present

    context={
         'total_employees':total_employees,
         'p':employees_present,
         'a':employees_absent,
        #  'dates': dates_du_jour , 
        'dates':dates_list,
        #  'nbre_present': present_p,
        'nbrepresent':counts_list,
      
         }



    return render(request,"profil/acceuil.html",context)
    # return render(request, 'profil/liste_t.html')


def index(request):
   
    return render(request,"profil/index.html")


def first_time_user(request):
    # Vérifier si un utilisateur existe déjà dans la base de données
    existing_users = User.objects.all()
    
    if existing_users:
        # Si des utilisateurs existent, rediriger vers une autre vue ou effectuer toute autre action
        return render(request,"profil/index.html")
    else:
        if request.method == 'POST':
            # Récupérer les données du formulaire
            username = request.POST['username']
            password = request.POST['password']
            
            # Créer un nouvel utilisateur
            User.objects.create_user(username=username, password=password)
            
            # Rediriger vers une autre vue ou effectuer toute autre action
            return render(request,"profil/index.html")
    
    # Afficher le formulaire d'inscription pour le premier utilisateur
    return render(request, 'accounts/register.html')

# Poste
@login_required(login_url="/account/login_admin/")
def part1(request):
   if request.method == 'POST':
       as_poste = request.POST.get('as_poste')
       poste = request.POST.get('poste')
       salary = request.POST.get('salary')
       debut = request.POST.get('debut')
       tolerance_time = request.POST.get('tolerance_time')
       fin = request.POST.get('fin')
       time_work = request.POST.get('time_work')

       poste = Poste(as_poste = as_poste, nom_poste = poste, somme = salary, heure_debut = debut,  tolerance_time = tolerance_time,heure_fin = fin, time_work = time_work)
       poste.save()
       return redirect('profil:poste')
   return render(request, 'profil/part1.html')

@login_required(login_url="/account/login_admin/")
def part2(request):
        if request.method == 'POST':
                nom = request.POST.get('nom')
                email = request.POST.get('email')
                prenom = request.POST.get('prenom')
                gender = request.POST.get('gender')
                heure_fixe = request.POST.get('heure_fixe')
                salary = request.POST.get('salary')
                poste_id = request.POST.get('poste')
                user_id = request.POST.get('user_id')
                time_a = request.POST.get('time_a')
                tolerance_time = request.POST.get('tolerance_time')
                time_s = request.POST.get('time_s')
                photo = request.FILES.get('photo')
                # Récupérer le poste sélectionné à partir de son ID
                if poste_id or user_id:
                    try:
                        poste = Poste.objects.get(pk=poste_id)
                        users = User.objects.get(pk=user_id)
                    except Poste.DoesNotExist or User.DoesNotExist:
                        # Gérer l'erreur si le poste n'existe pas
                        return redirect('error')

                personnel = Personnel(name=nom,email=email,prenom=prenom, gender=gender,
                                      heure_fixe=heure_fixe,salary=salary, time_a = time_a, tolerance_time = tolerance_time, time_s = time_s,poste=poste,user=users, photo = photo)
                personnel.save()
                return redirect('profil:liste_e')
        else:
            users_not_linked = User.objects.exclude(personnel__isnull=False)

        return render(request, 'profil/part2.html', {"postes":Poste.objects.all(),"users":users_not_linked} )

def partm1(request, poste_id):
    try:
        poste = Poste.objects.get(pk=poste_id)  # Get the position to modify
    except Poste.DoesNotExist:
        # Handle the case where the position is not found
        return redirect('profil:liste_postes')  # Redirect to list view on error

    if request.method == 'POST':
        as_poste = request.POST['as_poste']
        nom_poste = request.POST['poste']
        salary = request.POST['salary']  # Assuming this is the intended field name
        debut = request.POST['debut']
        tolerance_time = request.POST['tolerance_time']
        fin = request.POST['fin']
        time_work = request.POST['time_work']

        poste.as_poste = as_poste
        poste.nom_poste = nom_poste
        poste.somme = salary
        poste.heure_debut = debut
        poste.tolerance_time = tolerance_time
        poste.heure_fin = fin
        poste.time_work = time_work
        poste.save()

        return redirect('profil:poste')  # Redirect to list view on successful update

    context = {'poste': poste}
    return render(request, 'profil/partm1.html', context)

@login_required(login_url="/account/login_admin/")
def part2m(request, personnel_id):
    try:
        personnel = Personnel.objects.get(id=personnel_id)
    except Personnel.DoesNotExist:
        return redirect('profil:liste_e')
    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        prenom = request.POST.get('prenom')
        gender = request.POST.get('gender')
        heure_fixe = request.POST.get('heure_fixe')
        salary = request.POST.get('salary')
        poste_id = request.POST.get('poste')
        time_a = request.POST.get('time_a')
        tolerance_time = request.POST.get('tolerance_time')
        time_s = request.POST.get('time_s')
        user_id = request.POST.get('user_id')
        photo = request.FILES.get('photo')  # Utiliser request.FILES pour récupérer le fichier téléchargé

        if poste_id:
            try:
                poste = Poste.objects.get(pk=poste_id)
            except Poste.DoesNotExist:
                return redirect('error')
        
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return redirect('error')

        # Mettre à jour les données du personnel
        personnel.name = nom
        personnel.email = email
        personnel.prenom = prenom
        personnel.gender = gender
        personnel.heure_fixe = heure_fixe
        if salary:
            personnel.salary = salary
        personnel.poste = poste
        personnel.time_a = time_a
        personnel.tolerance_time = tolerance_time
        personnel.time_s = time_s
        personnel.user = user
        if photo:  # Vérifier si une nouvelle photo a été téléchargée
            personnel.photo = photo  # Mettre à jour la photo uniquement si un fichier a été téléchargé
        personnel.save()

        return redirect('profil:liste_e')
    
    # Filtrer les utilisateurs pour exclure ceux qui sont déjà liés à l'employé
    users = User.objects.filter(Q(personnel__isnull=True) | Q(personnel=personnel))

    context = {
        'personnel': personnel,
        'postes': Poste.objects.all(),
        'users': users
    }
    return render(request, 'profil/part2m.html', context)



@login_required(login_url="/account/login_admin/")
def liste_e(request):
    employee_list = Personnel.objects.all()
    if request.method == "GET":
        
        name=request.GET.get('rechercher')
        if name is not None:
            #employee_list = Personnel.objects.filter(name__icontains=name)
            employee_list = Personnel.objects.filter(name__startswith=name)
    


    paginator = Paginator(employee_list, 10)  # Paginer la liste avec 10 employés par page
    
    page_number = request.GET.get('page')  # Récupérer le numéro de page depuis les paramètres GET
    page_obj = paginator.get_page(page_number)  # Obtenir l'objet Page pour la page demandée
    context = {'page_obj': page_obj,
               
               
               }
    return render(request,"profil/liste_e.html",context)



@login_required(login_url="/account/login_admin/")
def attendance(request):
    # date_filter=datetime.date()

    # attendance=Horaire.objects.filter(date_d__startswith=date_filter)
    attendance=Horaire.objects.all()
    context={
           'horaires':Horaire.objects.order_by('-date_d','-arrival_time'),
           }
    return render(request,"profil/attendance.html",context)
    

@login_required(login_url="/account/login_admin/")
def historique(request):
    context={
           'horaires':Horaire.objects.order_by('-date_d','-arrival_time'),
           }
    return render(request,"profil/historique.html",context)

@login_required(login_url="/account/login_admin/")
def profil_e(request,Personnel_id): 
    context = {"Personnels": get_list_or_404(Personnel,pk=Personnel_id),
               
            }
    return render(request, "profil/profil_e.html", context)
  




#-----#
# def labels_date(date_planing):
#     horaires = Horaire.objects.filter(date_d=date_planing)
#     lab_date=[]
#     for horaire in horaires:
#         lab_date.append(horaire)

#     return lab_date



@login_required(login_url="/account/login_admin/")
def help(request):
   
    
    return render(request,"Profil/help.html")

@login_required(login_url="/account/login_admin/")
def del_user(request,Personnel_id):
    Personne = Personnel.objects.get(pk=Personnel_id)
    Personne.delete()
    return redirect("profil:liste_e")

@login_required(login_url="/account/login_admin/")
def del_poste(request,Poste_id):
    poste = Poste.objects.get(pk=Poste_id)
    poste.delete()
    return redirect("profil:poste")



@login_required(login_url="/account/login_admin/")
def delete_employees(request):
    if request.method == 'POST':
        selected_employees = request.POST.getlist('selected_employees')
        # Code pour supprimer les employés sélectionnés
        # selected_employees contient une liste des ID des employés sélectionnés
        Personnel.objects.filter(id__in=selected_employees).delete()
        
    
    return redirect('profil:liste_e')



# 
@login_required(login_url="/account/login_admin/")
def del_poste(request,Poste_id):
    poste = Poste.objects.get(pk=Poste_id)
    poste.delete()
    return redirect("profil:poste")

def profil_u(request):
    return render(request, 'profil/profil_u.html')


@login_required(login_url="/account/login_admin/")
def edit_Poste(request,Poste_id):
    poste = Poste.objects.get(pk=Poste_id)
    if request.method == 'POST':
        form = Part1Form(request.POST,instance=poste)
        if form.is_valid():
            form.save()
            return redirect("profil:poste")
    else:
        form = Part1Form(instance=poste)
    
    return render(request,"profil/partm1.html",{"form": form})
   

@login_required(login_url="/account/login_admin/")
def edit_Personnel(request,Personnel_id):
    Personnels = Personnel.objects.get(pk=Personnel_id)
    if request.method == 'POST':
        form = Part2Form(request.POST,instance=Personnels)
        if form.is_valid():
            form.save()
            return redirect("profil:liste_e")
    else:
        form = Part2Form(instance=Personnels)
    
    return render(request,"profil/part2.html",{"form": form})
   



@login_required(login_url="/account/login_admin/")
def edit_Horaire(request,Horaire_id):
    Personnels = Personnel.objects.get(pk=Horaire_id)
    if request.method == 'POST':
        form = Part3Form(request.POST,instance=Personnels)
        if form.is_valid():
            form.save()
            return redirect("profil:attendance")
    else:
        form = Part3Form(instance=Personnels)
   
    return render(request,"profil/part3.html",{"form": form})
    



# def calculate_daily_work_hours(personnel,date_month):
#     # Récupérer toutes les présences de l'employé pour la journée spécifiée
#     horaires = Horaire.objects.filter(personnel=personnel,date_d__date=date_month)
#     total_work_hours = timedelta()
#     for horaire in horaires:
#         # total_work_hours += horaire.calculate_duration()
#         duration_timedelta = timedelta(hours=horaire.calculate_duration().hour, minutes=horaire.calculate_duration().minute, seconds=horaire.calculate_duration().second)
#         total_work_hours += duration_timedelta

#     return total_work_hours

# def calculate_daily_work_hours(personnel,date_month):
#     # Récupérer toutes les présences de l'employé pour la journée spécifiée
#     horaires = Horaire.objects.filter(personnel=personnel,date_d__date=date_month)
 
#     total_work_hours = timedelta()  # Initialiser la durée totale à zéro
    
#     for horaire in horaires:
#         total_work_hours += horaire.calculate_duration()
#     for horaire in horaires:
#         duration_timedelta = timedelta(hours=horaire.calculate_duration().hour, minutes=horaire.calculate_duration().minute, seconds=horaire.calculate_duration().second)
#         total_work_hours += duration_timedelta

#     return total_work_hours

def calculate_daily_work_hours(personnel, date_month):
    # Récupérer toutes les présences de l'employé pour la journée spécifiée
    horaires = Horaire.objects.filter(personnel=personnel, date_d__date=date_month)
 
    total_work_hours = timedelta()  # Initialiser la durée totale à zéro
    
    for horaire in horaires:
        if isinstance(horaire, datetime):  # Vérifier si horaire est un objet datetime
            duration_timedelta = timedelta(hours=horaire.calculate_duration().hour, minutes=horaire.calculate_duration().minute, seconds=horaire.calculate_duration().second)
            total_work_hours += duration_timedelta
        elif isinstance(horaire, time):  # Vérifier si horaire est un objet time
            total_work_hours += horaire.calculate_duration()

    return total_work_hours


def calculate_daily_salary(personnel,date_month):
    total_work_hours = calculate_daily_work_hours(personnel,date_month)
    daily_salary = (total_work_hours.total_seconds() / 3600 *  personnel.salary)/personnel.heure_fixe #n

    return daily_salary

@login_required(login_url="/account/login_admin/")
def personnel_salary(request, Personnel_id):
     # Obtenez la date du mois actuel
    current_date = datetime.now().date()
    # Déterminez le premier jour du mois actuel
    first_day_of_month = current_date.replace(day=1)
    # Déterminez le dernier jour du mois actuel
    last_day_of_month = (first_day_of_month + relativedelta(months=1) - relativedelta(days=1))

    personnel = Personnel.objects.get(id=Personnel_id)
    horaires=Horaire.objects.values_list('date_d',flat=True).distinct()
    try:
        for horaire in horaires:
            daily_work_hours = calculate_daily_work_hours(personnel,horaire)
            daily_salary = calculate_daily_salary(personnel,horaire)
            daily_salary+=daily_salary
        salaire_month = Salaire(date_month=horaire,personnel=personnel,montant=daily_salary)
        salaire_month.save()
    except:
        daily_work_hours=0
        daily_salary=0

    context = {
        'personnel': personnel,
        'daily_work_hours': daily_work_hours,
        'daily_salary': daily_salary,
        'first_month':first_day_of_month ,
        'last_month':last_day_of_month 

    }

    return render(request, 'profil/salaire.html', context)
    

# @login_required(login_url="/account/login_admin/")
# def personnel_salary(request, Personnel_id):
#     personnel = Personnel.objects.get(id=Personnel_id)
    
#     # Obtenez la date du mois actuel
#     current_date = datetime.now().date()
#     # Déterminez le premier jour du mois actuel
#     first_day_of_month = current_date.replace(day=1)
#     # Déterminez le dernier jour du mois actuel
#     last_day_of_month = (first_day_of_month + relativedelta(months=1) - relativedelta(days=1))

#     # Obtenez les horaires du personnel pour le mois actuel
#     horaires = Horaire.objects.filter(personnel=personnel, date_d__range=[first_day_of_month, last_day_of_month])
#     try:
#         total_salary = 0
#         for horaire in horaires:
#             daily_work_hours = calculate_daily_work_hours(personnel, horaire.date_d)
#             daily_salary = calculate_daily_salary(personnel, horaire.date_d)
#             total_salary += daily_salary

#         # Enregistrez le salaire mensuel dans la base de données
#         salaire_month = Salaire(date_month=current_date, personnel=personnel, montant=total_salary)
#         salaire_month.save()
#     except:
#         total_salary=0
#         daily_salary=0
#         daily_work_hours=0


#     context = {
#         'personnel': personnel,
#         'daily_salary': total_salary,
#         'daily_work_hours': daily_work_hours,
#         'first_month':first_day_of_month ,
#         'last_month':last_day_of_month 

#     }

#     return render(request, 'profil/salaire.html', context)


@login_required(login_url="/account/login_admin/")
def fiche(request,personnel_id):
    personnel = Personnel.objects.get(id=personnel_id)
  
    daily_work_hours = calculate_daily_work_hours(personnel)
    daily_salary = calculate_daily_salary(personnel)

    context = {
        'personnel': personnel,
        'daily_work_hours': daily_work_hours,
        'daily_salary': daily_salary,
    }

    return render(request, 'profil/salary.html', context)




@login_required(login_url="/account/login_admin/")
def fiche(request,personnel_id):
    personnel = Personnel.objects.get(id=personnel_id)
  
    daily_work_hours = calculate_daily_work_hours(personnel)
    daily_salary = calculate_daily_salary(personnel)

    context = {
        'personnel': personnel,
        'daily_work_hours': daily_work_hours,
        'daily_salary': daily_salary,
    }
    return render(request, 'profil/salaire.html', context)
 


@login_required(login_url="/account/login_admin/")
def post(request):
    context={'postes':Poste.objects.all(),}
    return render(request, "profil/post.html",context)
   



 # ajoute un lecteur   
@login_required(login_url="/account/login_admin/")
def machine(request):
    if request.method == 'POST':
       form = ZKTecoForm(request.POST)
       if form.is_valid():
           form.save()
           return redirect("profil:liste_t")
    else:
       form = ZKTecoForm()
    
    return render(request, "profil/machine.html", {'form': form})

# @login_required(login_url="/account/login_admin/")    
# def horaire(request):
#     # Récupérer tous les enregistrements de la table Attendance
#     attendances = Attendance.objects.all()

#     for attendance in attendances:
#         # Récupérer la date et le personnel de l'entrée d'assistance
#         date = attendance.date.date()  # Récupérer uniquement la date sans l'heure
#         personnel = attendance.personnel_a
#         punch = attendance.punch

#         # Récupérer tous les enregistrements pour ce personnel et cette date
#         attendance_records = Attendance.objects.filter(personnel_a=personnel, date__date=date)

#         # Si des enregistrements existent pour ce jour et ce personnel
#         if attendance_records.exists():
#             # Trier les enregistrements par heure_punch
#             sorted_records = attendance_records.order_by('heure_punch')

#             # Associer le premier heure_punch à arrival_time et le dernier à departure_time
#             first_punch = sorted_records.first()
#             last_punch = sorted_records.last()

#             # Créer ou mettre à jour l'enregistrement dans la table Horaire
#             horaire, created = Horaire.objects.get_or_create(date_d=date, personnel=personnel)

#             # Mettre à jour les champs arrival_time et departure_time
#             horaire.arrival_time = first_punch.heure_punch
#             horaire.departure_time = last_punch.heure_punch
#             horaire.save()
#     return render(request, "profil/attendance.html", {'horaires' : Horaire.objects.all()})



@login_required(login_url="/account/login_admin/")    
def horaire(request):
    # Récupérer tous les enregistrements de la table Attendance
    attendances = Attendance.objects.all()

    for attendance in attendances:
        # Récupérer la date et le personnel de l'entrée d'assistance
        date = attendance.date.date()  # Récupérer uniquement la date sans l'heure
        personnel = attendance.personnel_a
        punch = attendance.punch

        # Récupérer tous les enregistrements pour ce personnel et cette date
        attendance_records = Attendance.objects.filter(personnel_a=personnel, date__date=date)

        # Si des enregistrements existent pour ce jour et ce personnel
        if attendance_records.exists():
            # Trier les enregistrements par heure_punch
            sorted_records = attendance_records.order_by('heure_punch')

            # Associer le premier heure_punch à arrival_time et le dernier à departure_time
            first_punch = sorted_records.first()
            last_punch = sorted_records.last()

            # Si les heures de premier et dernier punch sont égales, 
            # définir last_punch.heure_punch à None et last_punch.status à None
            if first_punch.heure_punch == last_punch.heure_punch:
                last_punch.heure_punch = None
                last_punch.status = None

            # Récupérer ou créer tous les objets Horaire correspondant à ces critères
            horaires = Horaire.objects.filter(date_d=date, personnel=personnel)

            if horaires.exists():
                # Il existe déjà un ou plusieurs objets Horaire pour cette date et ce personnel
                for horaire in horaires:
                    # Mettre à jour les champs arrival_time et departure_time
                    horaire.arrival_time = first_punch.heure_punch
                    horaire.departure_time = last_punch.heure_punch

                    # Mettre à jour les champs status et statute
                    if first_punch.status == "1":
                        horaire.status = "fingerprint"
                    elif first_punch.status == "3":
                        horaire.status = "pass word"
                    elif first_punch.status == "4":
                        horaire.status = "card"
                    
                    if last_punch.status == "1":
                        horaire.statute = "fingerprint"
                    elif last_punch.status == "3":
                        horaire.statute = "pass word"
                    elif last_punch.status == "4":
                        horaire.statute = "card"
                    
                    horaire.save()
            else:
                # Aucun objet Horaire trouvé, créer un nouvel objet Horaire
                horaire = Horaire.objects.create(
                    date_d=date,
                    arrival_time=first_punch.heure_punch,
                    departure_time=last_punch.heure_punch,
                    personnel=personnel
                )

                # Mettre à jour les champs status et statute
                if first_punch.status == "1":
                    horaire.status = "fingerprint"
                elif first_punch.status == "3":
                    horaire.status = "pass word"
                elif first_punch.status == "4":
                    horaire.status = "card"
                
                if last_punch.status == "1":
                    horaire.statute = "fingerprint"
                elif last_punch.status == "3":
                    horaire.statute = "pass word"
                elif last_punch.status == "4":
                    horaire.statute = "card"
                
                horaire.save()

    # Renvoyer tous les horaires pour affichage
    return redirect("profil:attendance")






# from datetime import datetime

# @login_required(login_url="/account/login_admin/")    
# def horaire(request):
#     # Récupérer tous les enregistrements de la table Attendance
#     attendances = Attendance.objects.all()

#     for attendance in attendances:
#         # Extraire la date et l'heure du check-in
#         check_in_date = attendance.heure_punch.strftime('%Y-%m-%d')  # Extraire la date sous forme de chaîne de caractères
#         check_in_time = attendance.heure_punch.strftime('%H:%M:%S')  # Extraire l'heure du check-in sous forme de chaîne de caractères
#         print(check_in_date,'***', check_in_time)
#         # Extraire la date et l'heure du check-out
#         last_check_out = Attendance.objects.filter(personnel_a=attendance.personnel_a, date__date=attendance.heure_punch.date()).order_by('-heure_punch').first()
#         if last_check_out:
#             check_out_date = last_check_out.date.strftime('%Y-%m-%d')  # Extraire la date sous forme de chaîne de caractères
#             check_out_time = last_check_out.heure_punch.strftime('%H:%M:%S')# Extraire l'heure du check-out sous forme de chaîne de caractères
#             print(check_out_date,'iiiiiiii', check_out_time)
#         else:
#             check_out_date = None
#             check_out_time = None

#         # Si un enregistrement de check-out existe pour ce jour et ce personnel
#         if last_check_out:
#             # Comparer les heures de check-in et de check-out pour déterminer lequel est le plus récent
#             if datetime.strptime(check_in_time, '%H:%M:%S') > datetime.strptime(check_out_time, '%H:%M:%S'):
#                 # Si l'heure de check-in est postérieure à l'heure de check-out, inverser les valeurs
#                 check_in_date, check_out_date = check_out_date, check_in_date
#                 check_in_time, check_out_time = check_out_time, check_in_time

#             # Créer ou mettre à jour l'enregistrement dans la table Horaire
#             horaire, created = Horaire.objects.get_or_create(date_d=check_in_date, personnel=attendance.personnel_a)

#             # Mettre à jour les champs arrival_time et departure_time
#             horaire.arrival_time = attendance.date
#             horaire.departure_time = last_check_out.date
#             horaire.save()

#     return render(request, "profil/attendance.html", {'horaires': Horaire.objects.all()})










@login_required(login_url="/account/login_admin/")
def get_somme_for_poste(request):
    if request.method == 'GET' and 'poste_id' in request.GET:
        poste_id = request.GET.get('poste_id')
        try:
            poste = Poste.objects.get(pk=poste_id)
            return JsonResponse({'somme': poste.somme})
        except Poste.DoesNotExist:
            return JsonResponse({'error': 'Le poste spécifié n\'existe pas'}, status=404)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@login_required(login_url="/account/login_admin/")
def get_start(request):
  if request.method == 'GET' and 'poste_id' in request.GET:
    poste_id = request.GET.get('poste_id')
    try:
      poste = Poste.objects.get(pk=poste_id)
      return JsonResponse({'start': poste.heure_debut})
    except Poste.DoesNotExist:
      return JsonResponse({'error': 'Le poste spécifié n\'existe pas'}, status=404)
  else:
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


@login_required(login_url="/account/login_admin/")    
def get_end(request):
    if request.method == 'GET' and 'poste_id' in request.GET:
        poste_id = request.GET.get('poste_id')
        try:
            poste = Poste.objects.get(pk=poste_id)
            return JsonResponse({'end': poste.heure_fin})
        except Poste.DoesNotExist:
            return JsonResponse({'error': 'Le poste spécifié n\'existe pas'}, status=404)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@login_required(login_url="/account/login_admin/")    
def get_time_work(request):
    if request.method == 'GET' and 'poste_id' in request.GET:
        poste_id = request.GET.get('poste_id')
        try:
            poste = Poste.objects.get(pk=poste_id)
            return JsonResponse({'time_work': poste.time_work})
        except Poste.DoesNotExist:
            return JsonResponse({'error': 'Le poste spécifié n\'existe pas'}, status=404)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@login_required(login_url="/account/login_admin/")    
def get_tolerance_time(request):
    if request.method == 'GET' and 'poste_id' in request.GET:
        poste_id = request.GET.get('poste_id')
        try:
            poste = Poste.objects.get(pk=poste_id)
            return JsonResponse({'tolerance_time': poste.tolerance_time})
        except Poste.DoesNotExist:
            return JsonResponse({'error': 'Le poste spécifié n\'existe pas'}, status=404)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

# @login_required(login_url="/account/login_admin/")
# def save_attendance(request):
  
#     return render(request, "profil/attendance_saved.html")
   
   



# def filter_and_save_attendance(request):
#     users = Personnel.objects.all()
#     # user_c= Personnel.objects.get(pk=user_id)
#     # print(users)

#     for user in users:
#         # Récupération des enregistrements de présence de l'utilisateur
#         user_logs =Attendance.objects.filter(personnel_a=user.pk)
        
#         # print(user.pk)

#         # Filtrage des enregistrements par jour
#         attendance_data = {}
#         for log in user_logs:
#             date_key = log.heure_punch.date()
#             print( 4*"-",date_key)

#             if date_key not in attendance_data:
#                 attendance_data[date_key] = {'check_in': None, 'check_out': None}

#             if log.punch == '0':
#                 if attendance_data[date_key]['check_in'] is None or log.heure_punch < attendance_data[date_key]['check_in']:
#                     attendance_data[date_key]['check_in'] = log.heure_punch
#             elif log.punch == '1':
#                 if attendance_data[date_key]['check_out'] is None or log.heure_punch > attendance_data[date_key]['check_out']:
#                     attendance_data[date_key]['check_out'] = log.heure_punch

#         # Enregistrement des enregistrements de présence filtrés dans la table Attendance
#         for date_key, attendance in attendance_data.items():
#             if attendance['check_in'] and attendance['check_out']:
#                 # Vérification si un enregistrement de présence existe déjà pour cette journée
#                 existing_attendance = Horaire.objects.filter(date_d=date_key, personnel=user.pk).first()

#                 if not existing_attendance:
#                     # Enregistrement de la présence dans la table Attendance
#                     user_c= Personnel.objects.get(pk=user.pk)
#                     attendance_entry = Horaire(date_d=date_key, personnel=user_c, arrival_time=attendance['check_in'], departure_time=attendance['check_out'])
#                     attendance_entry.save()
#                     print(10*"x")
#                 else:
#                     pass
#             print(attendance_data)
#     return redirect('profil:attendance_saved.html')








#fin#




























# def retrieve_users_data(zk):
#     # attendances = zk.get_attendance()
#     # users_data = []

#     # for attendance in attendances:
#     #     user_data = {
#     #         'id': attendance.user_id,
            
#     #         'date_arrival': attendance.timestamp.strftime("%d-%m-%Y"),
#     #         'time_arrival': attendance.timestamp.strftime("%H:%M:%S"),
#     #         # 'date_departure': attendance.timestamp_out.strftime("%d-%m-%Y"),
#     #         # 'time_departure': attendance.timestamp_out.strftime("%H:%M:%S"),
#     #         # 'duration': attendance.duration
#     #     }
#     #     users_data.append(user_data)

#     # return users_data


# @login_required(login_url="/account/login_admin/")
# def data(request):
#             CWD = os.path.dirname(os.path.realpath(__file__))
#             ROOT_DIR = os.path.dirname(CWD)
#             sys.path.append(ROOT_DIR)
#             conn = None
#             zk = ZK('192.168.1.206', port=4370)
#             try:
#                 conn = zk.connect()
#                 print ('Disabling device ...')
#                 conn.disable_device()
#                 print ('--- Get User ---')
#                 users = conn.get_users()
#                 conn.enable_device()
#             except Exception as e:
#                 print ("Process terminate : {}".format(e))
#             finally:
#                 if conn:
#                     conn.disconnect()
#             return render(request, 'profil/data.html',{'users':users})



# Personnel
# @login_required(login_url="/account/login_admin/")
# def part2(request):
#    if request.method == 'POST':
#        form = Part2Form(request.POST)
#        if form.is_valid():
#            form.save()
#         #    request.session['field2'] = form.cleaned_data['field2']
#         #    request.session['field3'] = form.cleaned_data['field3']
#            # Enregistrez les données dans la base de données ou effectuez toute autre action requise
#            return redirect('profil:liste_e')
#    else:
#        form = Part2Form()
#    return render(request, 'profil/part2.html', {'form': form})



# Horaire
# @login_required(login_url="/account/login_admin/")
# def part3(request):
#    if request.method == 'POST':
#        date_d = request.POST.get('date_d')
#        arrive = request.POST.get('arrive')
#        depart = request.POST.get('depart')
#        person = request.POST.get('person')

#        perso = Personnel.objects.get(id=person)
        
#                 # Gérer l'erreur si le poste n'existe pa
       
#        horaire = Horaire(date_d = date_d, arrival_time = arrive, departure_time = depart, personnel = perso)
#        horaire.save()
#        return redirect('profil:attendance')
       
#    return render(request, 'profil/part3.html', {'personne':Personnel.objects.all()})








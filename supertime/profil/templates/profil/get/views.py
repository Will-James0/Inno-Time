from django.shortcuts import render, get_list_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Horaire,Poste,Zklecteur,Personnel,Attendance
from .forms import Part1Form, Part2Form,Part3Form,ZKTecoForm
from django.contrib.auth.models import User
from datetime import datetime, timedelta, timezone,date
from django.core.paginator import Paginator
from django.db.models import Count
import subprocess
from zk import ZK, const
import os
import sys
from django.utils import timezone
import calendar


CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)


@login_required(login_url="/account/login_admin/")
def liste_t(request):
    zk = ZK('192.168.1.206' ,timeout=5)
    conn = None
    status = False
    try:
        conn = zk.connect()
        status=conn.is_connect
        return render(request, 'profil/liste_t.html',{'zklect':Zklecteur.objects.all() ,'st':status})
    
    except Exception as e:
        msm = " {} ".format(e)
        return render(request, 'profil/liste_t.html',{'zklect':Zklecteur.objects.all() ,'st':status,'message':msm})
    finally:
        if conn != None and conn.is_connect:
            conn.disconnect()


#-------------------------------------------------------------------------------------------------------------#
@login_required(login_url="/account/login_admin/")
def add_user(request):
    
    conn = None
    zk = ZK('192.168.1.206', port=4370,timeout=5)
    try:
        conn = zk.connect()
        print ('Disabling device ...')
        conn.disable_device()
        print ('--- Get User ---')
        users = conn.get_users()
       
        for user in users:
            zkteco_username = user.name
            zkteco_user_id = user.uid
            pw=user.password
            email_zk= f"{user.name}@gmail.com"
            # Vérifiez si l'utilisateur ZKTeco existe déjà dans la base de données Django
            try:
                django_user = User.objects.get(username=zkteco_username)
                # Si l'utilisateur existe, mettez à jour ses informations
                django_user.zkteco_user_id = zkteco_user_id
                django_user.save()
            except User.DoesNotExist:
                # Si l'utilisateur n'existe pas, créez un nouvel utilisateur Django
                django_user = User.objects.create_user(username=zkteco_username,password=pw,email=email_zk)
                django_user.zkteco_user_id = zkteco_user_id
                django_user.save()
                print('///////////////////////////')
                return render(request,"profil/valide.html")
            #conn.test_voice()
            print ('Enabling device ...')
            conn.enable_device()
            # return redirect("appzk:liste")
    except Exception as e:
        print ("Process terminate : {}".format(e))
    finally:
        if conn != None and conn.is_connect:
            conn.disconnect()
            
    return redirect("profil:valide")

@login_required(login_url="/account/login_admin/")
def data(request):
    today=datetime.today()
    # attendance=Horaire.objects.filter(date_d__startswith=today)
    attendance=Attendance.objects.all()

    return render(request,'profil/data.html',{"attendance":attendance})

@login_required(login_url="/account/login_admin/")
def data_brute(request):
    today=datetime.today()
    # attendance=Horaire.objects.filter(date_d__startswith=today)
    attendance=Attendance.objects.all()

    return render(request,'profil/a_valide.html',{"attendance":attendance})



@login_required(login_url="/account/login_admin/")
def liste_u(request):
    users=User.objects.all()
    return render(request,'profil/liste.html',{"users":users})


@login_required(login_url="/account/login_admin/")
# def add_attendance(request):
#     # lecteurs = Zklecteur.objects.get(pk=lecteur_id)
#     # zk = ZK(lecteurs.ip_adresse, lecteurs.n_port)
#     conn = None
#     zk = ZK('192.168.1.206',timeout=5)
#     try:
#         conn = zk.connect()
#         print ('Disabling device ...')
#         conn.disable_device()
#         print ('--- Get User ---')
#         attendance = conn.get_attendance()
#         print(type(attendance))
#         print(attendance)
#         for user in attendance:
                      
#             id_a=user.uid
#             maintenant = datetime.now()
#             # Afficher la date et l'heure du jour avec les secondes
#             # maintenant.strftime("%Y-%m-%d %H:%M:%S")
#             date_a =user.timestamp
#             if user.status == 1:
#                 status = 'enpreinte digital'
#             elif user.status ==3:
#                 status = 'pass word'
#             elif user.status == 4:
#                 status='card'
#             status_a=status
#             user_id =user.user_id
#             user_c= Personnel.objects.get(pk=user_id)
#             try:
#                 horaire_instance=Horaire.objects.filter(personnel=user_c).first()
               
#             except Horaire.DoesNotExist:
                
#                 # if user_c:
#                 # django_user = Attendance.objects.create(id_att=id_a,user=user_c,date=date_a,status=status_a,punch=punch_a,heure_entree = c)
#                 #     # django_user.pk=id_a
#                 date_s=datetime.now()
#                 if user.punch == 0:
#                     horaire_instance=Horaire(personnel=user_c)
#                     check_in = user.timestamp
#                     horaire_instance.arrival_time  = check_in
#                     horaire_instance.id_att=id_a
#                     horaire_instance.date_d=date_s
#                     horaire_instance.status=status_a
#                     # horaire_instance.save()
#                     # horaire_instance.punch=punch
#                 elif user.punch == 1:
#                     check_out = user.timestamp
#                     horaire_instance.departure_time=check_out
#                     horaire_instance.save()
#                 elif user.punch == 4:
#                     pass
#                 elif user.punch == 5:
#                     pass
#                 elif user.punch == 255:
#                     pass
#                 print('///////////////////////////')
#                 horaire_instance.save()
                    
#                 #conn.test_voice()
#             print ('Enabling device ...')
#             conn.enable_device()
#     except Exception as e:
#         print ("Process terminate : {}".format(e))
#     finally:
#         if conn != None and conn.is_connect:
#             conn.disconnect()
           
#     return render(request,"profil/a_valide.html")
def add_attendance(request):
    # lecteurs = Zklecteur.objects.get(pk=lecteur_id)
    # zk = ZK(lecteurs.ip_adresse, lecteurs.n_port)
    conn = None
    zk = ZK('192.168.1.206')
    try:
        conn = zk.connect()
        print ('Disabling device ...')
        conn.disable_device()
        print ('--- Get User ---')
        attendance = conn.get_attendance()
        print(type(attendance))
        print(attendance)
        for user in attendance:
                      
            id_a=user.uid
            # Afficher la date et l'heure du jour avec les seconde
            date_a =user.timestamp
            if user.status == 1:
                status = 'enpreinte digital'
            elif user.status ==3:
                status = 'pass word'
            elif user.status == 4:
                status='card'
            status_a=status
            user_id =user.user_id
            # user_c= Personnel.objects.get(pk=user_id)
            try:
                django_user=Horaire.objects.get(id_att=id_a)
                pass
            except Horaire.DoesNotExist:


                user_c= Personnel.objects.get(pk=user_id)
                # if user_c:
                # django_user = Attendance.objects.create(id_att=id_a,user=user_c,date=date_a,status=status_a,punch=punch_a,heure_entree = c)
                #     # django_user.pk=id_a
                if user.punch == 0:
                   
                    punch = 'check in'
                    check_in = user.timestamp
                    date_s=datetime.now()
                   
                    django_user = Attendance.objects.create(personnel_a=user_c,date=date_s,heure_punch=check_in,punch=punch,status=status_a)
                    django_user.save()
                    print('1111111111111111111111111111111')
                elif user.punch == 1:
                    date_s=datetime.now()
                    check_out = user.timestamp
                    # Horaire.objects.filter(personnel=user_c,arrival_time  = check_in).update(check_out=check_out)
                    django_user = Attendance.objects.create(personnel_a=user_c,date=date_s,heure_punch=check_out,punch=punch,status=status_a)
                    django_user.save()
                    print('222222222222222222222222222222222')
                elif user.punch == 4:
                   
                    print(10*'4')
                    
                elif user.punch == 5:
                    # punch = 'overtime out'
                    # check_in = user.timestamp
                    # date_s=datetime.now()
                   
                    # django_user = Attendance.objects.create(personnel_a=user_c,date=date_s,heure_punch=check_in,punch=punch,status=status_a)
                    # django_user.save()
                    print(10*'5')
                
                elif user.punch == 255:
                    # punch = 'pause'
                    # check_in = user.timestamp
                    # date_s=datetime.now()
                   
                    # django_user = Attendance.objects.create(personnel_a=user_c,date=date_s,heure_punch=check_in,punch=punch,status=status_a)
                    # django_user.save()
                    print(10*'255')
                print('///////////////////////////')
                
                #conn.test_voice()
            print ('Enabling device ...')
            conn.enable_device()
            # r
    except Exception as e:
        print ("Process terminate : {}".format(e))
    finally:
        if conn != None and conn.is_connect:
            conn.disconnect()
           
    return redirect("profil:a_valide")
 





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
#                 today=datetime.today()
#                 return render(request, 'profil/data.html',{'users':Horaire.objects.filter(date_d__with=today),'st':st})

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





@login_required(login_url="/account/login_admin")
def acceuil(request):
    maintenant=datetime.now()

    annee = maintenant.year
    mois = mois = maintenant.month

    # Nombre de jours à récupérer
    nb_jours = calendar.monthrange(annee, mois)[1]
    nombre_jours = nb_jours

    # Liste pour stocker les dates
    dates_du_jour = []

    # Récupération des dates du jour
    aujourd_hui = datetime.now().date()
    for i in range(nombre_jours):
        date = aujourd_hui + timedelta(days=i)
        dates_du_jour.append(date)

    # Affichage des dates
    for date in dates_du_jour:
         print(date)

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
            present = Horaire.objects.filter(date_d__startswith=entry).count()
            counts_list.append(int(present))

    # i +=1
    total_employees = Personnel.objects.count()
    
    # Compter le nombre d'employés présents à la date donnée
    employees_present = Horaire.objects.filter(date_d=date_j).count()
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

# Poste
@login_required(login_url="/account/login_admin")
def part1(request):
   if request.method == 'POST':
       as_poste = request.POST.get('as_poste')
       poste = request.POST.get('poste')
       salary = request.POST.get('salary')
       debut = request.POST.get('debut')
       fin = request.POST.get('fin')

       poste = Poste(as_poste = as_poste, nom_poste = poste, somme = salary, heure_debut = debut, heure_fin = fin)
       poste.save()
       return redirect('profil:poste')
   return render(request, 'profil/part1.html')

@login_required(login_url="/account/login_admin")
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
                # Récupérer le poste sélectionné à partir de son ID
                if poste_id or user_id:
                    try:
                        poste = Poste.objects.get(pk=poste_id)
                        users = User.objects.get(pk=user_id)
                    except Poste.DoesNotExist or User.DoesNotExist:
                        # Gérer l'erreur si le poste n'existe pas
                        return redirect('error')

                personnel = Personnel(name=nom,email=email,prenom=prenom, gender=gender,
                                      heure_fixe=heure_fixe,salary=salary,poste=poste,user=users)
                personnel.save()
                return redirect('profil:liste_e')

        return render(request, 'profil/part2.html', {"postes":Poste.objects.all(),"users":User.objects.all()} )

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
        fin = request.POST['fin']

        poste.as_poste = as_poste
        poste.nom_poste = nom_poste
        poste.somme = salary
        poste.heure_debut = debut
        poste.heure_fin = fin
        poste.save()

        return redirect('profil:poste')  # Redirect to list view on successful update

    context = {'poste': poste}
    return render(request, 'profil/partm1.html', context)

@login_required
def part2m(request, personnel_id):
    try:
        personnel = Personnel.objects.get(id=personnel_id)
    except Personnel.DoesNotExist:
        return redirect('profil:liste_e')
    
    if request.method == 'POST':
        nom = request.POST['nom']
        email = request.POST['email']
        prenom = request.POST['prenom']
        gender = request.POST['gender']
        heure_fixe = request.POST['heure_fixe']
        salary = request.POST['salary']
        poste_id = request.POST['poste']
        if poste_id:
            try:
                poste = Poste.objects.get(pk=poste_id)
            except Poste.DoesNotExist:
                        # Gérer l'erreur si le poste n'existe pas
                return redirect('error')
            
        personnel.name = nom
        personnel.email = email
        personnel.prenom = prenom
        personnel.gender = gender
        personnel.heure_fixe = heure_fixe
        personnel.salary = salary
        personnel.poste = poste
        personnel.save()

        return redirect('profil:liste_e')
    postes = Poste.objects.all()
    context = {'personnel' : personnel,
               'postes':postes}
    return render(request, 'profil/part2m.html', context)


@login_required(login_url="/account/login_admin")
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



@login_required(login_url="/account/login_admin")
def attendance(request):
    context={'postes':Poste.objects.all(),
           'horaires':Horaire.objects.all(),
           'personnels':Personnel.objects.all(),
           #'attendances':Attendance.objects.all(),
      
           }
    return render(request,"profil/attendance.html",context)
    

@login_required(login_url="/account/login_admin")
def historique(request):
    return render(request,"profil/historique.html")

@login_required(login_url="/account/login_admin")
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



@login_required(login_url="/account/login_admin")
def help(request):
   
    
    return render(request,"Profil/help.html")

@login_required(login_url="/account/login_admin")
def del_user(request,Personnel_id):
    Personne = Personnel.objects.get(pk=Personnel_id)
    Personne.delete()
    return redirect("profil:liste_e")

@login_required(login_url="/account/login_admin")
def del_poste(request,Poste_id):
    poste = Poste.objects.get(pk=Poste_id)
    poste.delete()
    return redirect("profil:poste")




def delete_employees(request):
    if request.method == 'POST':
        selected_employees = request.POST.getlist('selected_employees')
        # Code pour supprimer les employés sélectionnés
        # selected_employees contient une liste des ID des employés sélectionnés
        Personnel.objects.filter(id__in=selected_employees).delete()
        
    
    return redirect('profil:liste_e')



# 
@login_required(login_url="/account/login_admin")
def del_poste(request,Poste_id):
    poste = Poste.objects.get(pk=Poste_id)
    poste.delete()
    return redirect("profil:poste")

def profil_u(request):
    return render(request, 'profil/profil_u.html')


@login_required(login_url="/account/login_admin")
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
   

@login_required(login_url="/account/login_admin")
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
   



@login_required(login_url="/account/login_admin")
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
    



def calculate_daily_work_hours(personnel):
    # Récupérer toutes les présences de l'employé pour la journée spécifiée
    horaires = Horaire.objects.filter(personnel=personnel)
    total_work_hours = timedelta()
    for horaire in horaires:
        total_work_hours += horaire.calculate_duration()

    return total_work_hours

def calculate_daily_salary(personnel):
    total_work_hours = calculate_daily_work_hours(personnel)
    daily_salary = total_work_hours.total_seconds() / 3600 * (personnel.poste.somme+personnel.salary)
    daily_salary = (total_work_hours.total_seconds() / 3600 * (personnel.poste.somme + personnel.salary))/personnel.heure_fixe #n

    return daily_salary

@login_required(login_url="/account/login_admin")
def personnel_salary(request, Personnel_id):
    personnel = Personnel.objects.get(id=Personnel_id)
    daily_work_hours = calculate_daily_work_hours(personnel)
    daily_salary = calculate_daily_salary(personnel)

    context = {
        'personnel': personnel,
        'daily_work_hours': daily_work_hours,
        'daily_salary': daily_salary,
    }

    return render(request, 'profil/salaire.html', context)
    

@login_required(login_url="/account/login_admin")
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




@login_required(login_url="/account/login_admin")
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
 


@login_required(login_url="/account/login_admin")
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
    

@login_required(login_url="/account/login_admin")
def save_attendance(request):
  
    return render(request, "profil/attendance_saved.html")
   
   



def filter_and_save_attendance(request):
    users = Personnel.objects.all()
    # user_c= Personnel.objects.get(pk=user_id)
    # print(users)

    for user in users:
        # Récupération des enregistrements de présence de l'utilisateur
        user_logs =Attendance.objects.filter(personnel_a=user.pk)
        
        # print(user.pk)

        # Filtrage des enregistrements par jour
        attendance_data = {}
        for log in user_logs:
            date_key = log.heure_punch.date()
            print( 4*"-",date_key)

            if date_key not in attendance_data:
                attendance_data[date_key] = {'check_in': None, 'check_out': None}

            if log.punch == '0':
                if attendance_data[date_key]['check_in'] is None or log.heure_punch < attendance_data[date_key]['check_in']:
                    attendance_data[date_key]['check_in'] = log.heure_punch
            elif log.punch == '1':
                if attendance_data[date_key]['check_out'] is None or log.heure_punch > attendance_data[date_key]['check_out']:
                    attendance_data[date_key]['check_out'] = log.heure_punch

        # Enregistrement des enregistrements de présence filtrés dans la table Attendance
        for date_key, attendance in attendance_data.items():
            if attendance['check_in'] and attendance['check_out']:
                # Vérification si un enregistrement de présence existe déjà pour cette journée
                existing_attendance = Horaire.objects.filter(date_d=date_key, personnel=user.pk).first()

                if not existing_attendance:
                    # Enregistrement de la présence dans la table Attendance
                    user_c= Personnel.objects.get(pk=user.pk)
                    attendance_entry = Horaire(date_d=date_key, personnel=user_c, arrival_time=attendance['check_in'], departure_time=attendance['check_out'])
                    attendance_entry.save()
                    print(10*"x")
                else:
                    pass
            print(attendance_data)
    return redirect('profil:attendance_saved.html')





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


# @login_required(login_url="/account/login_admin")
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
# @login_required(login_url="/account/login_admin")
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
# @login_required(login_url="/account/login_admin")
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








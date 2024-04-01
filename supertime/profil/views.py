from django.shortcuts import render, get_list_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Personnel,Horaire,Poste,Attendance
from .forms import Part1Form, Part2Form,Part3Form
from datetime import datetime, timedelta



def index(request):
   
    return render(request,"profil/index.html")

# Poste

def part1(request):
   if request.method == 'POST':
       form = Part1Form(request.POST)
       if form.is_valid():
           form.save()
     
           return redirect('profil:part2')
   else:
       form = Part1Form()
   return render(request, 'profil/part1.html', {'form': form})

# Personnel

def part2(request):
   if request.method == 'POST':
       form = Part2Form(request.POST)
       if form.is_valid():
           form.save()
        #    request.session['field2'] = form.cleaned_data['field2']
        #    request.session['field3'] = form.cleaned_data['field3']
           # Enregistrez les données dans la base de données ou effectuez toute autre action requise
           return redirect('profil:part3')
   else:
       form = Part2Form()
   return render(request, 'profil/part2.html', {'form': form})

# Horaire

def part3(request):
   if request.method == 'POST':
       form = Part3Form(request.POST)
       if form.is_valid():
           form.save()
           #request.session['field1'] = form.cleaned_data['field1']
           return redirect("profil:liste_e")
   else:
       form = Part3Form()
   return render(request, 'profil/part3.html', {'form': form})




def liste_e(request):
    context={'postes':Poste.objects.all(),
           
           'personnels':Personnel.objects.all(),
      
           }
    return render(request,"profil/liste_e.html",context)



def acceuil(request):
    
    return render(request,"profil/acceuil.html")


def attendance(request):
    context={'postes':Poste.objects.all(),
           'horaires':Horaire.objects.all(),
           'personnels':Personnel.objects.all(),
           'attendances':Attendance.objects.all(),
      
           }
    return render(request,"profil/attendance.html",context)


def historique(request):
    return render(request,"profil/historique.html")

def profil_e(request,Personnel_id): 
    context = {"Personnels": get_list_or_404(Personnel,pk=Personnel_id),
               
            }
    return render(request, "profil/profil_e.html", context)


def help(request):
    return render(request,"Profil/help.html")


def del_user(request,Personnel_id):
    Personne = Personnel.objects.get(pk=Personnel_id)
    Personne.delete()
    return redirect("profil:liste_e")




def edit_Personnel(request,Personnel_id):
    Personnels = Personnel.objects.get(pk=Personnel_id)
    # if request.method == 'POST':
    #     form = ProfilForm(request.POST,instance=Personnels)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("profil:liste_e")
    # else:
    #     form = ProfilForm(instance=Personnels)
    form={}
    return render(request,"profil/part1.html",{"form": form})



# 
# def add_Profil(request):
   
#     if request.method == 'POST':
#         form = ProfilForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("profil:liste_e")
#     else:
#         form = ProfilForm()
#     context = {"form": form}
#     return render(request,"profil/form.html",context)


# 


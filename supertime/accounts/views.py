from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User 
#from .models import Profile, Poste

#{{ user.personne.get_self.nom }}

# Create your views here.
def login_admin(request):
    if request.method =='POST':
        username_u = request.POST["username"]
        password_u = request.POST["password"]

        user = authenticate(request, username = username_u, password= password_u)

        if user is not None:
            login(request, user)
            return redirect("profil:dashboad")
        else:
            messages.info(request, "Identifiant ou le mot de passe incorrect")
    form = AuthenticationForm()
    return render(request,"accounts/login_a.html", {"form":form})
   

# def login_user(request,Personnel_id):
#     Personnels = Personnel.objects.get(pk=Personnel_id)

#     if request.method =='POST':
#         id_u = request.POST["id"]
#         email_u = request.POST["email"]

#         user = authenticate(request, id = id_u, password= email_u)

#         if user is not None:
#             login(request, user)
#             return redirect("profil:acceuil")
#         else:
#             messages.info(request, "Identifiant ou le mot de passe incorrect")
#     form = ProfilForm()
#     return render(request,"accounts/login_e.html", {"form":form})



def logout_user(request):
    logout(request)
    return redirect("profil:index")


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("accounts:details_user")
    else:
        form = UserCreationForm()
        
    return render(request, "accounts/register.html",{"form":form})
    

# #details
# def register(request):
#     if request.method == 'POST':
#         # Récupérer les données du formulaire HTML
#         user_id = request.POST.get('user_id')
#         email = request.POST.get('email')
#         nom = request.POST.get('nom')
#         prenom = request.POST.get('prenom')
#         genre = request.POST.get('genre')
#         poste_id = request.POST.get('poste')
#         photo = request.FILES.get('photo')  # Récupérer le fichier image (optionnel)

#     #     users = User.objects.get(pk=user_id)
#     #     poste_d = Poste.objects.get(pk=poste_id)
#     #     profile = Profile(user=users, nom=nom,prenom=prenom,email=email, genre=genre,poste=poste_d, photo = photo)
#     #     profile.save()
#     #     return redirect('profil:acceuil')
#     #     # return render(request, 'accounts/details_user.html', {'message':"bon"})

#     # postes = Poste.objects.all()
    
#     # context = {'postes': postes,
#     #            'users': User.objects.all()
#     #            }
#     # return render(request, 'accounts/details_user.html', context)
#     return render(request, 'accounts/details_user.html')

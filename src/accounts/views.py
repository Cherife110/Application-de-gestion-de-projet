from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from .forms import ProjectForm, RegisterForm, LoginForm, SubjectForm
from .models import CustomUser, PreviousProject, Project, Subject 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required # importez le décorateur
from django.views.generic import UpdateView, DeleteView


# Create your views here.
def index(request):
    return render(request, "index.html")
def home_admin(request):
    users = CustomUser.objects.all()
    projects = Project.objects.all()
    context = {'users': users, 'projects': projects }

    return render(request, "home_admin.html",context)
def home_teacher(request):
    projects = Project.objects.all()
    context = {'projects': projects }
    return render(request, "home_teacher.html",context)

def home_student(request):
    projects = Project.objects.all()
    context = {'projects': projects }
    return render(request, "home_student.html",context)
class ProjectUpdateView(UpdateView):
    model = Project # utilise le modèle Project
    template_name = 'project_form.html' # utilise le même template que pour la création
    fields = '__all__' # utilise tous les champs du modèle
    success_url = '/home_teacher'

class ProjectDeleteView(DeleteView):
    model = Project # utilise le modèle Project
    template_name = 'project_confirm_delete.html' # utilise le template project_confirm_delete.html
    success_url = '/home_teacher' # redirige vers la page d'accueil après la suppression

class UserUpdateView(UpdateView):
    model = CustomUser # utilise le modèle Project
    template_name = 'user_form.html' # utilise le même template que pour la création
    fields = '__all__' # utilise tous les champs du modèle
    success_url = '/home_admin'

class UserDeleteView(DeleteView):
    model = CustomUser # utilise le modèle Project
    template_name = 'user_confirm_delete.html' # utilise le template project_confirm_delete.html
    success_url = '/home_admin' # redirige vers la page d'accueil après la suppression

class SubjectUpdateView(UpdateView):
    model = Subject # utilise le modèle Project
    template_name = 'subject_form.html' # utilise le même template que pour la création
    fields = '__all__' # utilise tous les champs du modèle
    success_url = '/home_admin'

class SubjectDeleteView(DeleteView):
    model = Subject # utilise le modèle Project
    template_name = 'subject_confirm_delete.html' # utilise le template project_confirm_delete.html
    success_url = '/home_teacher' # redirige vers la page d'accueil après la suppression

def register(request):
    # if this is a POST request we need to process the form data
    template = 'register.html'
   
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if CustomUser.objects.filter(id_number=form.cleaned_data['id_number']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'ID number already exists.'
                })
            else:
                # Create the user:
                user = CustomUser.objects.create_user(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    birth_date=form.cleaned_data['birth_date'],
                    id_number=form.cleaned_data['id_number'],
                    password=form.cleaned_data['password'],
                    role=form.cleaned_data['role'],
                )

               
                # redirect to accounts page:
                return redirect('home_admin')

   # No post data availabe, let's just show the page.
    else:
        form = RegisterForm()

    return render(request, template, {'form': form})

def Customlogin(request):
    template = 'login.html'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            id_number = form.cleaned_data['id_number']
            password = form.cleaned_data['password']
            user = authenticate(request, username=id_number, password=password)
            if user is not None:
                login(request, user)
                if user.role == CustomUser.STUDENT:
                    return HttpResponseRedirect('home_sudent')
                elif user.role == CustomUser.TEACHER:
                    return HttpResponseRedirect('home_teacher')
                elif user.role == CustomUser.ADMIN:
                    return HttpResponseRedirect('home_admin')
            else:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Authentification invalide. ID ou mot de passe incorrecte'
                })
    else:
        form = LoginForm()
    return render(request, template, {'form': form})
def logout_view(request):
    logout(request) # appelez la fonction logout
    return redirect('/') # redirigez vers la page d'accueil


# Vue pour afficher la liste des projets archivés
def archived_project_list(request):
    # Récupérer les objets PreviousProject dont le champ archived est True
    archived_projects = PreviousProject.objects.filter(archived=True)
    # Rendre le gabarit avec le contexte contenant les projets archivés
    return render(request, 'archived_project_list.html', {'archived_projects': archived_projects})

def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save() # enregistre un nouveau projet dans la base de données
            return redirect('home_teacher') # redirige vers la page d'accueil
    else:
        print("erreur")
        form = ProjectForm()
    return render(request, 'add_project.html', {'form': form})
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_admin')

    else:
        form = SubjectForm()
    return render(request, 'add_subject.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from contact.forms import ClientForm,ClientLoginForm
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required

def Home(request):
    return render(request,'contact/index.html')

def SignUpIn(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    if request.method == 'POST':
        loginForm = ClientLoginForm(request.POST)
        if loginForm.is_valid():
            name = loginForm.cleaned_data['name']
            password = loginForm.cleaned_data['password']
            user = authenticate(request, username=name, password=password)
            if user:
                login(request, user)    
                return redirect("/dashboard")

        cadastrarForm = ClientForm(request.POST)
        if cadastrarForm.is_valid():
            name = cadastrarForm.cleaned_data['name']
            email = cadastrarForm.cleaned_data['email']
            password = cadastrarForm.cleaned_data['password']
            #Verificar se tem alguem já com esse nome
            if not User.objects.filter(username=name, email=email).exists():
                user = User.objects.create_user(username=name, email=email, password=password)
                if cadastrarForm['admin']:
                    group, created = Group.objects.get_or_create(name='Administradores')
                    group.user_set.add(user)
                login(request, user) 
                return redirect("dashboard")
            else:
                raise PermissionError("Nome já cadastrado")
    else:
        loginForm = ClientLoginForm()
        cadastrarForm = ClientForm()

    return render(request,'contact/login.html',{'login':loginForm, 'cadastrar':cadastrarForm})

@login_required(login_url="login/")
def Dashboard(request):
    if request.method == 'POST':
        pass

    user = request.user
    context = {
        'user': user.username,
        'email': user.email,
        'alluser': User.objects.all(),
    }
    return render(request, 'contact/dashboard.html', context=context)

@login_required(login_url="login/")
def UserLogout(request):
    logout(request)
    return redirect('login/')


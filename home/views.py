from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "welcome.html")

# SUCCESS PAGE
def success(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    context = {
        'cur_user': User.objects.get(id = request.session['user_id']),
        'users' : User.objects.all(),
    }
    return render(request, 'success.html', context)

# REGISTRATION
def create(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        request.session.clear()
        request.session['first_name'] = request.POST['first_name']
        request.session['last_name'] = request.POST['last_name']
        request.session['email'] = request.POST['email']
        errors = User.objects.validator(request.POST)
        if len(errors)>0:
            for value in errors.values():
                messages.error(request, value)
            return redirect('/register')
        new_user = User.objects.register(request.POST)
        request.session.clear()
        request.session['user_id'] = new_user.id
        return redirect('/success')

# to login
def login(request):
    if request.method == "GET":
        if 'first_name' in request.session:
            request.session.clear()
        return render(request, "login.html")
    else: #to check login
        result = User.objects.authenticate(request.POST['email'],request.POST['password'])
        if result == False:
            messages.error(request, "Email or passwort do not match.")
        else:
            user = User.objects.get(email = request.POST['email'])
            request.session['user_id'] = user.id
            return redirect('/success')
        return redirect('/login')


# to logout
def logout(request):
    request.session.clear()
    return redirect("/login")

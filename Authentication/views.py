from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date
from authenticationModule import signIn,signOut,signUp,reset_password,google_signin,google_signout

# Create your views here.
#Index Page Call function
def home(request):
    return render(request,'Authentication/index.html')
#Login Page Calling function
def signin(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        passwd = request.POST['passwd']
        response = signIn(email,passwd)
        if response['success']:
            return render(request,'MainPage/main.html',{'responce-msg':response['response_msg'],'username':response['user'],'uid':response['uid']})
        else:
         messages.error(request,response['response_msg'])
         return redirect('home')

    return render(request,'Authentication/index.html')
#signup calling
def signup(request):
    
    if request.method == "POST":
        username = request.POST['username']
        email =request.POST['email']
        passwd = request.POST['passwd']
        cpasswd = request.POST['cpasswd']
        response = signUp(username,email,passwd,cpasswd)
        if response['success']:
            messages.success(request,response['response_msg'])
            return redirect('home')
        else:
            messages.error(request,response['response_msg'])
            return redirect('signup')
    return render(request,'Authentication/registrationPage.html')


def signout(request):
    messages.success(request,'Logged out Successfully !')
    return redirect('home') 

def resetPassword(request):
    if request.method == "POST":
        email =request.POST['email']
        response = reset_password(email)
        if response['success']:
            messages.success(request,response['response_msg'])
            return redirect('home')
        else:
             messages.error(request,response['response_msg'])
             return redirect('resetPassword')
    return render(request,'Authentication/resetPage.html')

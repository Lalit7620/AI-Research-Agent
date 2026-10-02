from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.views import View


class LoginView(View):
    def get(self,request):
        return render(request,"accounts/login.html")
    
    def post(self,request):
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        user=authenticate(
            request,
            username=username,
            password=password,
        )
        
        if user is not None:
            login(request,user)
            return redirect("research")
        
        return render(
            request,
            "accounts/login.html",
            {
                "error":"Invalid username or password."
            }
        )
        
class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("login")
    
class RegisterView(View):
    def get(self,request):
        return render(request,"accounts/register.html")
    
    def post(self,request):
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        
        if User.objects.filter(username=username).exists():
            return render(request,"accounts/register.html",{"error":"Username already exists."})
        
        user=User.objects.create_user(username=username,email=email,password=password)
        
        login(request,user)
        return redirect("dashboard")
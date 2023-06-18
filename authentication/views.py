from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout

# Create your views here.
class LoginView(View):

    def get(self, request: HttpRequest):
        return render(request, 'authentication/login.html')
    
    def post(self, request: HttpRequest):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is None:
            return redirect('/auth/login')

        login(request, user)

        return redirect('/dashboard')

class LogoutView(View, LoginRequiredMixin):
    def get(self, request: HttpRequest):
        logout(request)

        return redirect('/auth/login')